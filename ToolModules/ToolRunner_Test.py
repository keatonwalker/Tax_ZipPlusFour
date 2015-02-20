'''
Created on Mar 21, 2014

@author: kwalker
'''
import ZipPlusFourTool, arcpy, AddressTableParser, time


apiKey = "AGRC-D7C80921565994"#"AGRC-CB612714234155"
inputTable = r"C:\GIS\Work\Geocoding\TaxProject\testData\test845.dbf"#r"C:\KW_Working\Geocoder_Tools\Zip_plus4\2012_11.mdb\ZIP4_845_Table_Tester"
outputDirectory = r"C:\Users\kwalker\Documents\GitHub\Tax_ZipPlusFour\ToolModules\data\testoutput\taxproject"#"C:\Users\kwalker\Documents\GitHub\ZipPlusFour\ToolModules\data"

    
version = "1.1.0"
arcpy.AddMessage("Version " + version)
startTime = time.time()
addrParser = AddressTableParser.AddressTableParser(inputTable)
addrTableAndGroups = addrParser.getAddressListAndGrps()
testTool = ZipPlusFourTool.ZipPlusFourTool(apiKey, inputTable, outputDirectory)
testTool.start(addrTableAndGroups[0], addrTableAndGroups[1])
print "{} seconds".format(time.time() - startTime)