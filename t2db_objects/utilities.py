import os
import re
import ast

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
                    properties[key] = value[1].strip()

            except Exception as e:
                raise Exception("File not well formed, line = " + str(numLine) + ", str = " + str(e))
            numLine += 1
    return properties

# The same method for python2
def readConfigFile2(configFilePath):
  properties = {}
  numLine = 1
  keymatch = re.compile('^[A-Za-z0-9_]+[ \t]*=[ \t]*')
  keymatch2 = re.compile('^[A-Za-z0-9_]+')
  with open(configFilePath, "r", -1) as configFile:
    for line in configFile:
      try:
        sublines = line.split("#")
        subline = sublines[0]
        if len(subline.strip()) > 0:
          gkey = keymatch.match(subline).group()
          value = subline.split(gkey)
          key = keymatch2.match(gkey).group()
          value[1] = value[1].strip()
          if value[1] == "\\t":
            value[1] = "\t"
          elif value[1] == "\\n":
            value[1] = "\n"
          properties[key] = value[1]

      except Exception as e:
        raise Exception("File not well formed, line = " + str(numLine) + ", str = " + str(e))
      numLine += 1
  return properties

def formatHash(myHash, myFields):
  """
  Ensure that the configuration values (myHash) are in the correct format (myFields).
  """
  newHash = {}
  for field in myFields:
    if not "name" in field:
      raise Exception ("'" + field + "' is not valid tuple: Name missing")
    if not "kind" in field:
      raise Exception ("'" + field + "' is not valid tuple: Kind missing")
    if not "type" in field:
      raise Exception ("'" + field + "' is not valid tuple: Type missing")
    name_ = field["name"]
    kind_ = field["kind"]
    type_ = field["type"]
    if kind_ == "mandatory" and not name_ in myHash:
      raise Exception ("'Object does not have '" + name_ + "'")
    elif name_ in myHash:
      newHash[name_] = check_value(type_, myHash[name_])
    elif kind_ == 'non-mandatory' and 'default' in field:
      newHash[name_] = check_value(type_, field['default'])
  return newHash  

def check_value(type_, value):
  if type_ == dict or type_ == list or type_ == tuple:
    return ast.literal_eval(value)
  else:
    return type_(value)

""" Read a file line by line, adding each line to a list """
def readListFile(listFilePath):
  #TODO Comment could be in any place
  if not os.path.isfile(listFilePath):
    raise Exception("File : " + path + " was not found")
  lines = []
  with open(listFilePath, "r") as listFile:
    for line in listFile:
      if not line.startswith("#") and len(line.strip()) > 0:
        lines.append(line.strip())
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

# Read environment variable
def read_env_variable(env_variable_name):
  if env_variable_name in os.environ:
    return os.environ[ env_variable_name]
  return None
