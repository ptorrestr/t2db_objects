import os
import re

# Return a numeric representation of boolean values. 0 if booleanValue is false,
# 1 if bool_is true
def boolean2int(booleanValue):
    if (booleanValue):
        return 1
    else:
        return 0

# Read configuration file. The file has the following structure:
#
#propertyName1 = someValue1
#propertyName2 = someValue2
##some coment [# is the comment character]
#...
#
# Each property is listed in one line. The name of the property is at
# the left side of the equal symbol. The value of the property is at
# the right side of the equal symbol. 
def readConfigFile(configFilePath):
    #TODO Comment could be in any place
    properties = {}
    numLine = 1
    keymatch = re.compile('^[A-Za-z0-9_]+[ \t]*=[ \t]*')
    keymatch2 = re.compile('^[A-Za-z0-9_]+')
    with open(configFilePath, "r", -1, "utf-8") as configFile:
        for line in configFile:
            try:
                sublines = line.split("#")
                subline = sublines[0]
                if len(subline.strip()) > 0:
                    gkey = keymatch.match(subline).group()
                    value = subline.split(gkey)
                    key = keymatch2.match(gkey).group()
                    properties[key] = value[1]

            except Exception as e:
                raise Exception("File not well formed, line = " + str(numLine) + ", str = " + str(e))
            numLine += 1
    return properties

""" Read a file line by line, adding each line to a list """
def readListFile(listFilePath):
    #TODO Comment could be in any place
    lines = []
    with open(listFilePath, "r", -1, "utf-8") as listFile:
        for line in listFile:
            if not line.startswith("#") and len(line.strip()) > 0:
                lines.append(line)
    return lines

# Write the content in the file pointed by filePath
def writeFile(filePath, content, encoding = "utf-8"):
    with open(filePath, "w", -1, encoding) as newFile:
        newFile.write(content)

# Remove file pointed by filePath
def removeFile(filePath):
    try:
        os.remove(filePath)
    except Exception as e:
        raise Exception("Could not remove " + filePath + ": " + str(e))
