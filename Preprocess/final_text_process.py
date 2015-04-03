import time

start = time.time()
newText = r"C:\KW_Working\Geocoder_Tools\Zip_plus4\TaxProject\FinalOutput\ustcmtsa20150401_NoHeaders.txt"
textFile = r"C:\KW_Working\Geocoder_Tools\Zip_plus4\TaxProject\FinalOutput\ustcmtsa20150401_all.txt"
with open(newText, 'wb') as outFile:
    with open(textFile, 'rb') as inFile:
        for line in inFile:
    #         line = inFile.readline()
            parts = line.split(",")
            outString = parts[len(parts) -1:]
            outFile.write(outString[0])
        
print "{}".format(time.time() - start)