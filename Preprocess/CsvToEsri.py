import arcpy, os
from arcpy.arc import Create
from interpreterInfo import join


def createGdbTables():
    files = ['829', '833', '840', '841', '842', '843', '844', '845', '846', '847']
    for file in files:
        inputFilesStr = r"C:\KW_Working\Geocoder_Tools\Zip_plus4\TaxProject\USPSInput\ConvertedCsvs\old"
        inputFilesStr = os.path.join(inputFilesStr, file + "Old.csv")
        outputFolder = r"C:\KW_Working\Geocoder_Tools\Zip_plus4\TaxProject\USPSInput\ConvertedCsvs\old\ZipTables_Old.gdb"
        outputFileName = "old_" + file #"825Test.csv"
        
        arcpy.TableToTable_conversion(inputFilesStr, outputFolder, outputFileName)
        
def createNameField(oldOrNew):
    files = ['833', '840', '841', '842', '843', '844', '845', '846', '847']
    for file in files:
        inputFile = r"C:\KW_Working\Geocoder_Tools\Zip_plus4\TaxProject\USPSInput\ConvertedCsvs"
        inputFile = os.path.join(inputFile, oldOrNew, "ZipTables_{}.gdb".format(oldOrNew), oldOrNew + "_" + file)
        print inputFile
#         outputFolder = r"C:\KW_Working\Geocoder_Tools\Zip_plus4\TaxProject\USPSInput\ConvertedCsvs\old\ZipTables_Old.gdb"
#         outputFileName = "old_" + file #"825Test.csv"
        
        arcpy.AddField_management(in_table = inputFile, field_name = "joinedName", 
                          field_type = "TEXT", field_length = 200)
        arcpy.CalculateField_management (in_table = inputFile, field = "joinedName",
                                         expression = """"{}{}{}{}{}{}".format( str(!PreDir!).strip(), str(!Name!).strip(), str(!Type!).strip(), str(!SufDir!).strip(), str( !LowAdd!), str(!HighAdd!))""""",
                                         expression_type = "PYTHON_9.3")
                                         
                                         
def joinOnCombinedName():
    files = ['833', '840', '841', '842', '843', '844', '845', '846', '847']
    for file in files:
        inputFile = r"C:\KW_Working\Geocoder_Tools\Zip_plus4\TaxProject\USPSInput\ConvertedCsvs"
        inputFile = os.path.join(inputFile, "new", "ZipTables_{}.gdb".format("new"), "new" + "_" + file)
        oldFile = r"C:\KW_Working\Geocoder_Tools\Zip_plus4\TaxProject\USPSInput\ConvertedCsvs"
        oldFile = os.path.join(oldFile, "old", "ZipTables_{}.gdb".format("old"), "old" + "_" + file)
        print inputFile
        arcpy.JoinField_management(inputFile, "joinedName", oldFile, "joinedName", "joinedName")
        
def extractNewRecords():
    files = ['829', '833', '840', '841', '842', '843', '844', '845', '846', '847']
    for file in files:
        inputFile = r"C:\KW_Working\Geocoder_Tools\Zip_plus4\TaxProject\USPSInput\ConvertedCsvs"
        inputFile = os.path.join(inputFile, "new", "ZipTables_{}.gdb".format("new"), "new" + "_" + file)
        print inputFile
        outputFile = os.path.join("C:\KW_Working\Geocoder_Tools\Zip_plus4\TaxProject\USPSInput\ConvertedCsvs\ZipFour_NewRecords.gdb", 
                                  "newRec_{}".format(file))
        whereClause = "joinedName_1 IS NULL"
        outTableView = "tableView" + file
        arcpy.MakeTableView_management(inputFile, outTableView, whereClause)
        result = arcpy.GetCount_management(outTableView)
        count = int(result.getOutput(0))
        print count
        arcpy.CopyRows_management(outTableView, outputFile)
        
def addOrignalFieldsToResults():
    gdb = r"C:\KW_Working\Geocoder_Tools\Zip_plus4\TaxProject\NewAddresses_Results\Results_20150222223115.gdb"
    results = ["AddressesNotGeocoded", "Zip4Line", "Zip4NoMatch", "Zip4Point"]
    resultJoinField = "OrigId"
    originalTable = "GdbZipTable"
    originalFields = ['Zip9', 'Zip5', 'RecType', 'PreDir', 'Name', 'Type', 'SufDir', 'LowAdd', 'HighAdd', 'EvenOdd', 'PrefKey', 'CoNbr']
    originalJoinField = "OBJECTID" 
    for r in results:
        print r
        arcpy.JoinField_management(os.path.join(gdb, r), resultJoinField,
                                   os.path.join(gdb, originalTable), originalJoinField,
                                   originalFields)
def correctTypeFieldInResults():
    gdb = r"C:\KW_Working\Geocoder_Tools\Zip_plus4\TaxProject\NewAddresses_Results\Results_20150222223115.gdb"
    results = ["AddressesNotGeocoded", "Zip4Line", "Zip4NoMatch", "Zip4Point"]
    for r in results:
        print r
        arcpy.DeleteField_management(os.path.join(gdb, r), "Type")
        arcpy.AlterField_management(os.path.join(gdb, r), "Type_1", "Type")

def addPlus4Fields():
    inputFile = r"C:\GIS\Work\Geocoding\TaxProject\ConvertedCsvs\ZipFour_NewRecords.gdb"
    inputFile = os.path.join(inputFile, "newRec_All")
    fields = [('LowSegment', 4), ('HighSegment', 4), ('LowSector', 4), ('HighSector', 4),
                   ('LowAddress', 20), ('HighAddress', 20), ('Zip', 10)]
    
#     for field in fields:
#         arcpy.AddField_management(in_table = inputFile, field_name = field[0], 
#                           field_type = "TEXT", field_length = field[1])
        
    updateFields = ['Zip9', 'Zip5', 'LowAdd', 'HighAdd']
    updateFields.extend([f[0] for f in fields])
    with arcpy.da.UpdateCursor(inputFile, updateFields) as cursor:
        for row in cursor:
            zip9 = str(row[0] or "")
            zip5 = str(row[1] or "")
            lowAddStr = str(row[2] or "")
            highAddStr = str(row[3] or "")
            
            segment = zip9[5:-2]
            sector = zip9[7:]
            row[4] = segment
            row[5] = segment
            row[6] = sector
            row[7] = sector
            row[8] = lowAddStr
            row[9] = highAddStr
            row[10] = zip5
            cursor.updateRow(row)
     

# createNameField("old")
#joinOnCombinedName()
#extractNewRecords()
#addOrignalFieldsToResults()
correctTypeFieldInResults()