import sys, arcgisscripting
gp= arcgisscripting.create()

#TEST VALUES (for use outside ArcGIS environment
inputFilesStr = "C:\\GIS\\Zip9DB\\USPSInput\\ut.txt"
outputFolder = "C:\\GIS\\Zip9DB\\ScratchFiles"
outputFileName = "USPSCityState.csv"

outputFile = outputFolder + "\\" + outputFileName
gp.AddMessage("Output Location:" + outputFile)

output = open(outputFile, 'a')
outList = ['cskey,cszip,csname,cszipclass,csprefkey,csprefname,csuniquezc,csconbr,csconame,csfaccode\n'] 
recordCount = 0  
fileList = inputFilesStr.split(';')

for currFile in fileList:
    gp.AddMessage("Processing: " + currFile)

    currDoc = open(currFile, 'r')
    inFileStr = currDoc.read()

    sMax = len(inFileStr)
    gp.AddMessage("sMax = " +str(sMax))
    sIterations = (sMax / 129) -1
    gp.AddMessage("sIterations = " + str(sIterations))
    print "Iterations = " + str(sIterations)
    currIteration = 1
    
    while currIteration <= sIterations:
        outstr = ""
        print "Now Serving: " + str(currIteration)
        currStr = inFileStr[(currIteration * 129):((currIteration + 1) * 129)]
        if (currStr[0:1] == "D"):
            print currStr[6:12]
            outStr =  currStr[6:12].strip()
            outStr =  outStr + "," + currStr[1:6].strip()
            outStr =  outStr + "," + currStr[13:41].strip()
            outStr =  outStr + "," + currStr[12:13].strip()
            outStr =  outStr + "," + currStr[56:62].strip()
            outStr =  outStr + "," + currStr[62:90].strip()
            outStr =  outStr + "," + currStr[92:93].strip()
            outStr =  outStr + "," + currStr[101:104].strip()
            outStr =  outStr + "," + currStr[104:129].strip()
            outStr =  outStr + "," + currStr[54:55].strip()+ "\n"
            outList.insert((currIteration + 1),outStr)
            recordCount = recordCount + 1
            
        currIteration = currIteration + 1

    output.writelines(outList)
    outList = []
    currDoc.close()
        
    gp.AddMessage('COMPLETED FILE: ' + currFile+ '\n' + str(sMax) + ' Characters processed.\n' \
    + str(recordCount) + ' Records written to ' + outputFile+ '\n' \
    + str(129 * (currIteration -1)) + ' characters utilized.\n\n')
    
output.close()
gp.RefreshCatalog(outputFolder)
gp.AddMessage('COMPLETED PROCESS.\n' + str(recordCount) + ' TOTAL Records Added.')