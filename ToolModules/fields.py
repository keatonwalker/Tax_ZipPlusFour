'''
Created on Apr 29, 2014

@author: kwalker
'''
class Fields (object):
    
    def __init__(self):
        self._fieldList = []
    
    def getFields(self):
        return self._fieldList
    
    def getI(self, field):
        fieldI = self._fieldList.index(field)
        return fieldI
    
class Input(Fields):

    def __init__(self):
        self.lowHouseNum = "LowAdd1"#"Addr_PrimaryLowNo"
        self.highHouseNum = "HighAdd1"#"AddrPrimaryHighNo"
        self.preDirection = "PreDir"#"StreetPreDrctnAbbrev"
        self.streetName = "Name"#"StreetName"
        self.streetSuffix = "Type"#"StreetSuffixAbbrev"
        self.postDirection = "SufDir"#"StreetPostDrctnAbbrev"
        self.zipCode = "Zip51"#"ZipCode"
        self.zip4SegLow = "LowSeg"#"LowZipSegmentrNo"
        self.zip4SegHigh = "HighSeg"#"HighZipSegmentNo"
        self.zip4SectorLow = "LowSec"#"LowZipSectorNo"
        self.zip4SectorHigh = "HighSec"#"HighZipSectorNo"
        self.objectId = "OID"#"OID@"
        
        self._fieldList = [self.lowHouseNum, self.highHouseNum, self.preDirection,
                     self.streetName, self.streetSuffix, self.postDirection,
                     self.zipCode, self.zip4SegLow, self.zip4SegHigh, 
                     self.zip4SectorLow, self.zip4SectorHigh, self.objectId]


class Output(Fields):
    
    def __init__(self):
        self.zipPlus4 = "Zip4"
        self.type = "Type"
        self.match = "Match"
        self.originRowID = "OrigId"
        self.inputAddress = "InAddr"
        self.inputZone = "InZone"
        self.matchAddress = "MatchAddr"
        self.matchZone = "MatchZone"
        self.geocoder = "Geocoder"
        self.score = "Score"
        self.xCoord = "X"
        self.yCoord = "Y"
        self.nonMatchMsg = "nomatchmsg"
        #Line specific fields
        
    
        self._fieldList = (self.zipPlus4, self.type, self.match, 
                     self.originRowID, self.inputAddress, self.inputZone, 
                     self.matchAddress, self.matchZone, self.geocoder, 
                     self.score, self.xCoord, self.yCoord, self.nonMatchMsg)
    
    def getLineFields(self):
        lineFields = []
        for i in range(3):
            fieldNum = ""
            if i != 0:
                fieldNum = str(i)        
            
            for f in self._fieldList[:-1]:#Slice to remove nonMatchMsg
                lineFields.append(f + fieldNum)
        
        return lineFields
        
    def addFieldsToFeature(self, feature):
        import arcpy
        addFieldParams = [[self.zipPlus4, "TEXT", 9],
                        [self.type, "TEXT", 10],
                        [self.match, "TEXT", 15],
                        [self.originRowID, "LONG"],
                        [self.inputAddress, "TEXT", 75],
                        [self.inputZone, "TEXT", 50],
                        [self.matchAddress, "TEXT", 75],
                        [self.matchZone, "TEXT", 50],
                        [self.geocoder, "TEXT", 50],
                        [self.score, "DOUBLE"],
                        [self.xCoord, "DOUBLE"],
                        [self.yCoord, "DOUBLE"],
                        [self.nonMatchMsg, "TEXT", 100]]
        
        for params in addFieldParams:
            textFieldLength = ""
            if len(params) > 2:
                textFieldLength = params[2]
                
            arcpy.AddField_management(in_table = feature, field_name = params[0], 
                                      field_type = params[1], field_length = textFieldLength)
            
    def addFieldsToLineFeature(self, feature):
        import arcpy
        addFieldParams = [[self.zipPlus4, "TEXT", 9],
                        [self.type, "TEXT", 10],
                        [self.match, "TEXT", 15],
                        [self.originRowID, "LONG"],
                        [self.inputAddress, "TEXT", 75],
                        [self.inputZone, "TEXT", 50],
                        [self.matchAddress, "TEXT", 75],
                        [self.matchZone, "TEXT", 50],
                        [self.geocoder, "TEXT", 50],
                        [self.score, "DOUBLE"],
                        [self.xCoord, "DOUBLE"],
                        [self.yCoord, "DOUBLE"]]
        
        for i in range(3):
            fieldNum = ""
            if i != 0:
                fieldNum = str(i)

            for params in addFieldParams:
                textFieldLength = ""
                if len(params) > 2:
                    textFieldLength = params[2]
                    
                arcpy.AddField_management(in_table = feature, field_name = params[0] + fieldNum, 
                                          field_type = params[1], field_length = textFieldLength)
