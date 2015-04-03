'''
Created on Aug 18, 2014

@author: kwalker
'''

import arcpy, fields, ZipPlusFourTool
from operator import attrgetter
#from ZipPlusFourTool import Address



class AddressTableParser (object):
    
    def __init__(self, addressTable):
        self._addressTable = addressTable
    
        
    def _getHouseNumbers(self, addressLowNum, addressHighNum):
        """Creates house numbers from range between provided fields.
        May return a list of: 
            - [low]
            - [low, high]
            - [low, high, mid]"""
        
        #remove all non digit chars and strip leading zeros
        lownum = ''.join(i for i in addressLowNum if i.isdigit())
        lownum = str(int(lownum)).strip()
        highnum = ''.join(i for i in addressHighNum if i.isdigit())
        highnum = str(int(highnum)).strip()
    
        houseNumList = [str(int(lownum) + 2)]# + 2 Moves low number two away from the corner
    
        numdiff = int(highnum) - int(lownum)
    
        if numdiff > 0 and numdiff > 4:
            houseNumList.append(str(int(highnum) - 2))# - 2 Moves high number two away from the corner
        
        elif numdiff > 0:
            houseNumList.append(highnum)
    
        if numdiff > 40:
            
            #TODO Add some logic to handle the 0 - 99 ranges
            if numdiff % 4 == 0:
                midnum = str(int(lownum) + (numdiff/2))
                houseNumList.append(midnum)
            elif numdiff % 2 == 0:
                midnum = str(int(lownum) + (numdiff/2) + 1)
                houseNumList.append(midnum)
        
        return houseNumList    


    def _buildStreetName(self, preDir, streetName, stType, sufDir):
        """Build the street name from parts that exist in many fields in input table"""
        streetAddress = ""
    
        if not (preDir == None):
            if len(preDir.strip()) > 0:
                streetAddress = preDir + " "
    
        streetAddress +=  streetName.strip()
    
        if not (stType == None):
            if len(stType.strip()) > 0:
                streetAddress = streetAddress + " " + stType

        if not (sufDir == None):
            if len(sufDir.strip()) > 0:
                streetAddress = streetAddress + " " + sufDir
    
        #remove unnecessary characters
        for c in range(34,48):
            streetAddress = streetAddress.replace(chr(c)," ")
        streetAddress = streetAddress.replace("_"," ")
        
        return streetAddress
    
    def _getZipPlusForNumbers(self, segmentLow, segmentHigh, sectorLow, sectorHigh):
        "Uses the segment and sector numbers to build a list of zip plus four numbers"
        zipPlusFours = []
        segLow = int(segmentLow)
        segHigh = int(segmentHigh)
        secLow = int(sectorLow)
        secHigh =  int(sectorHigh)
        segmentRange = segHigh - segLow
        sectorRange = secHigh - secLow
        
        for i in range(segmentRange + 1):
            seg = "{0:02d}".format(segLow + i)
            for j in range(sectorRange + 1):
                plus4 = "{0}{1:02d}".format(seg, (secLow + j))
                zipPlusFours.append(plus4)
                plus4 = ""
        
        return zipPlusFours

    
    def getAddressListAndGrps(self):
        addrList = []
        addrGrps = []
        inFields = fields.Input()
        fieldList = inFields.getFields()       
        whereClause = "RecType = 'S' or RecType = 'H' and not( HighAdd1 is null or Name is null)"#"RecordTypeCode = 'S' or RecordTypeCode = 'H' and not( AddrPrimaryHighNo is null or StreetName is null)"
        with arcpy.da.SearchCursor(self._addressTable, fieldList, whereClause) as cursor:
            for row in cursor:
                if not row[inFields.getI(inFields.lowHouseNum)].isnumeric() or not row[inFields.getI(inFields.highHouseNum)].isnumeric():
                    continue#Skip a malformed record.
                
                streetName = self._buildStreetName(row[inFields.getI(inFields.preDirection)], row[inFields.getI(inFields.streetName)],
                                                   row[inFields.getI(inFields.streetSuffix)], row[inFields.getI(inFields.postDirection)]) #row[2], row[3], row[4], row[5])
                
                zone = str(row[inFields.getI(inFields.zipCode)])
                if zone[:1] == "8":
                    zone = zone.strip()[:5]

                tempPlusFourList = []
                zipPlusFourNumbers = self._getZipPlusForNumbers(row[inFields.getI(inFields.zip4SegLow)], row[inFields.getI(inFields.zip4SegHigh)],
                                                                row[inFields.getI(inFields.zip4SectorLow)], row[inFields.getI(inFields.zip4SectorHigh)]) #row[7], row[8], row[9], row[10])
                for plus4Num in zipPlusFourNumbers:
                    plus4Area = ZipPlusFourTool.AddressGroup(plus4Num)
                    tempPlusFourList.append(plus4Area)

                houseNumList = self._getHouseNumbers(row[inFields.getI(inFields.lowHouseNum)], row[inFields.getI(inFields.highHouseNum)])#row[0], row[1])
                #Check how many house numbers  _getHouseNumbers returned
                #If one address returned it is the low address
                lowAddr = ZipPlusFourTool.Address(streetName, houseNumList[0], zone, 0, row[inFields.getI(inFields.objectId)])#row[11])
                addrList.append(lowAddr)
                for plus4Area in tempPlusFourList:
                    plus4Area.addAddress(lowAddr)
 
                if len(houseNumList) > 1:
                    highAddr = ZipPlusFourTool.Address(streetName, houseNumList[1], zone, 2, row[inFields.getI(inFields.objectId)])
                    addrList.append(highAddr)
                    for plus4Area in tempPlusFourList:
                        plus4Area.addAddress(highAddr)                    
                        
                if len(houseNumList) > 2:
                    midAddr = ZipPlusFourTool.Address(streetName, houseNumList[2], zone, 1, row[inFields.getI(inFields.objectId)])
                    addrList.append(midAddr)
                    for plus4Area in tempPlusFourList:
                        plus4Area.addAddress(midAddr)                    
                
                addrGrps.extend(tempPlusFourList)
                
        return [addrList, addrGrps]
    
    def getAddressGroups(self):
        
        return self._addressGroups
        
    
        
        