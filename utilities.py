import os

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
    with open(configFilePath, "r", -1, "utf-8") as configFile:
        for line in configFile:
            if not line.startswith("#") and len(line.strip()) > 0:
                terms = line.strip().split("=")
                try:
                    properties[terms[0].strip()] = terms[1].strip()
                except Exception as e:
                    raise Exception("File not well formed, line = " + str(numLine))
            numLine += 1
    return properties

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
