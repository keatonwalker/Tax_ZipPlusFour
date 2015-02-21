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
     

# createNameField("old")
#joinOnCombinedName()
extractNewRecords()
