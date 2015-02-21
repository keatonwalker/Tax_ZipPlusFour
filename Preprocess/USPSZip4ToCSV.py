import sys, arcgisscripting, os
gp= arcgisscripting.create()
#inputFilesStr = sys.argv[1]
#outputFolder = sys.argv[2]
#outputFileName = sys.argv[3]

#TEST VALUES (for use outside ArcGIS environment
files = ['829.txt', '833.txt', '840.txt', '841.txt', '842.txt', '843.txt', '844.txt', '845.txt', '846.txt', '847.txt']
for file in files:
    inputFilesStr = r"C:\KW_Working\Geocoder_Tools\Zip_plus4\TaxProject\USPSInput\old"
    inputFilesStr = os.path.join(inputFilesStr, file)
    outputFolder = r"C:\KW_Working\Geocoder_Tools\Zip_plus4\TaxProject\USPSInput\ConvertedCsvs\old"
    outputFileName = file[:-4] + "Old" + ".csv"#"825Test.csv"
    
    outputFile = outputFolder + "\\" + outputFileName
    gp.AddMessage("Output Location:" + outputFile)
    print "Output Location:" + outputFile
    
    output = open(outputFile, 'a')
    outList = ['Zip9,Zip5,RecType,PreDir,Name,Type,SufDir,LowAdd,HighAdd,EvenOdd,PrefKey,CoNbr\n'] 
    outList.insert((1),'0,0,X,X,X,X,X,0,0,X,X,X\n')
    recordCount = 0  
    
    fileList = inputFilesStr.split(';')
    for currFile in fileList:
        gp.AddMessage("Processing: " + currFile)
    
        currDoc = open(currFile, 'r')
        inFileStr = currDoc.read()
    
        sMax = len(inFileStr)
        gp.AddMessage("sMax = " +str(sMax))
        sIterations = (sMax / 182) -1
        gp.AddMessage("sIterations = " + str(sIterations))
        print "sIterations = " + str(sIterations)
        currIteration = 1
        while currIteration <= sIterations:
            outstr = ""
            print currIteration
            currStr = inFileStr[(currIteration * 182):((currIteration + 1) * 182)]
            low67 =  currStr[140:142].strip()
            low89 =  currStr[142:144].strip()
            high67 = currStr[144:146].strip()
            high89 = currStr[146:148].strip()
            low69 = low67 + low89
            high69 = high67 + high89
            #gp.AddMessage(low69 + " " + high69)
            if (low69).isdigit():
                loopLow = int(low69)
                loopHigh = loopLow
                if (high69).isdigit():
                    loopHigh = int(high69)
                    if loopHigh < loopLow:
                        loopHigh = loopLow
                
                currPlusFour = loopLow
                #gp.AddMessage(str(loopLow) + " " + str(loopHigh))
                #print loopHigh
        
                while currPlusFour <= loopHigh:
                    currPlusFourStr = str(currPlusFour)
                    if len(currPlusFourStr) == 1:
                        currPlusFourStr = "000" + currPlusFourStr
                    elif len(currPlusFourStr) == 2:
                        currPlusFourStr = "00"+ currPlusFourStr
                    elif len(currPlusFourStr) == 3:
                        currPlusFourStr = "0"+ currPlusFourStr    
                    outStr = ""
                    outStr =  currStr[1:6].strip() + currPlusFourStr
                    outStr =  outStr + "," + currStr[1:6].strip()
                    outStr =  outStr + "," + currStr[17:18].strip()
                    outStr =  outStr + "," + currStr[22:24].strip()
                    outStr =  outStr + ",\"" + currStr[24:52].strip()+"\""
                    outStr =  outStr + "," + currStr[52:56].strip()
                    outStr =  outStr + "," + currStr[56:58].strip()
                    outStr =  outStr + "," + currStr[58:68].strip()
                    outStr =  outStr + "," + currStr[68:78].strip()
                    outStr =  outStr + "," + currStr[78:79].strip()
                    outStr =  outStr + "," + currStr[176:182].strip()
                    outStr =  outStr + "," + currStr[159:162].strip()+ "\n"
                    outList.insert((currIteration + 2),outStr)
                    recordCount = recordCount + 1
                    currPlusFour = currPlusFour + 1
                    #currPlusFour = 9999
            currIteration = currIteration + 1
            #gp.AddMessage(outstr)
    
        output.writelines(outList)
        outList = []
        currDoc.close()
        
        
        gp.AddMessage('COMPLETED FILE: ' + currFile+ '\n' + str(sMax) + ' Characters processed.\n' \
        + str(recordCount) + ' Records written to ' + outputFile+ '\n' \
        + str(182 * (currIteration -1)) + ' characters utilized.\n\n')
        
    output.close()
    gp.RefreshCatalog(outputFolder)
    gp.AddMessage('COMPLETED PROCESS.\n' + str(recordCount) + ' TOTAL Records Added.')
