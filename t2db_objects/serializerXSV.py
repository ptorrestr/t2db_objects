"""
=====
SerializerXSV
=====
This module controls the methods used to parse, get and store the data stored in CSV or TSV format.
"""

from itertools import islice
import logging
from os import remove
from os.path import isfile
import re
import csv
import codecs

logger = logging.getLogger("t2db_objects")

class BufferedReader(object):
  """
  Read a Text file using a buffering aproach. This means that the information is read in chunk of data, 
  one by one, rather than read the whole file. Buffering readings are needed when the XSV file is 
  large.
  """
  def __init__(self, filePath, lines = 100):
    """
    Create a new bufferReader. The filePath points to the file and lines indicates the number of line to
    read in each iteration.
    """
    self.lines = lines
    self.f = open(filePath, 'r')
 
  def close(self):
    """
    Close the file descriptor.
    """
    self.f.close()
 
  def nextLines(self):
    """
    Get the next lines(declared in the constructor) in the file. If there is no more line, a None object
    is returned.
    """
    nextLines = list(islice(self.f, self.lines))
    if not nextLines:
      self.close()
    return nextLines

def append(filePath, lines):
  """
  Add lines to a already existing file. FilePath points to a file. If the file doesn't exist, the function 
  creates it, otherwise the data is added just at the end of the file.
  """
  with open(filePath, 'a') as a:
    a.write(lines)

class Serializer(object):
  """
  The fine a abstract serializer object
  """
  pass

class SerializerXSV(Serializer):
  """
  This class can serialize a XSV file (CSV or TSV)
  """
  def __init__(self, filePath, overwrite,  fields, criteria = "\t"):
    """
    Constructor. FilePath points to the XSV file, overwrite indicates if the file should be rewrite if
    already exist, fields are the list fields which the file should have and critieria is the
    token used to divied fields from other fields.
    """
    self.fields = fields
    self.criteria = criteria
    self.filePath = filePath
    self.overwrite = overwrite
    self.count = 0
    if overwrite and isfile(filePath):
      logger.debug("Overwriting file: " + filePath)
      remove(filePath)

  def serializeLine(self, rawObject):
    """
    Given a object, it create a line (string) which each field following the definition expressed in the
    field attibute. 
    """
    columns = []
    for field in self.fields:
      try:
        columns.append(rawObject[field])
      except Exception as e:
        raise ColumnsNotEquivalentException("Field missing: " + field + " obj = " + str(rawObject))
    line = columns[0]
    for i in range(1, len(columns)):
      line += self.criteria + columns[i]
    return line

  def pushObjects(self, rawObjectList):
    """
    Store in a file, new objects defined in rawObjectList.
    """
    lines = []
    for rawObject in rawObjectList:
      lines.append(self.serializeLine(rawObject))      
    logger.debug("Objects serialized : " + str(len(rawObjectList)))
    #If they are already data before, add a new line
    if self.count == 0 and self.overwrite:
      contentFile = lines[0]
    else:
      contentFile = "\n" + lines[0]
    for i in range(1, len(lines)):
      contentFile += "\n" + lines[i]
    append(self.filePath, contentFile)
    self.count += len(lines)
    logger.debug("Current lines output : " + str(self.count))
     

class Parser(object):
  """
  Abstract parser
  """
  pass

class BufferedParserXSV(Parser):
  """
  This class can parse a XSV fifle
  """
  def __init__(self, fields, filePath, lines = 100, criteria = "\t"):
    """
    Constructor: The fields contains the list of fields of the XSV file, filePath point to the file, lines
    inidicates the number of line to store in the buffere and criteria is the token defintion to divide
    fields from fields. It does not support quouting in string text.
    """
    self.fields = fields
    self.reader = BufferedReader(filePath, lines)
    self.criteria = criteria
    self.count = 0

  def close(self):
    """
    Close file descriptior.
    """
    self.reader.close()
    logger.debug("Close reader")
 
  def parseLine(self, line, lineNum):
    """
    Parse a file line (string) and get a object.
    """
    columns = line.strip().split(self.criteria)
    if len(self.fields) > len(columns):
      raise ColumnsNotEquivalentException("Line " + str(lineNum) + ": Column missing, fields = " 
        + str(len(self.fields)) + ", columns = " + str(len(columns)))
    if len(self.fields) < len(columns):
      logger.warning("Line " + str(lineNum) + ": Some columns are not considered")
    rawObject = {}
    i = 0
    for field in self.fields:
      rawObject[field] = columns[i]
      i += 1
    return rawObject

  def nextObjects(self):
    """
    Return the N next objects (genereted from the N next lines).
    """
    lines = self.reader.nextLines()
    if not lines:
      return lines
    rawObjectList = []
    text = ""
    for line in lines:
      text += line
    for line in lines:
      self.count += 1
      if line == "":
        logger.warning("Empty line found at: " + str(countLine))
      rawObject = self.parseLine(line, self.count)
      rawObjectList.append(rawObject)
    logger.debug("Objects read = " + str(len(rawObjectList)))
    return rawObjectList

  def nextObjects2(self):
    lines = self.reader.nextLines()
    if not lines:
      return lines
    r = lineMatcher(len(self.fields), self.criteria)
    rawObjectList = []
    self.countLine = 1
    previous = False
    previousLine = ""
    for line in lines:
      if previous:
        previous = False
        line = previousLine + line
        previousLine = ""
      if line == "":
        logger.warning("Empty line found at: " + str(self.countLine))
      try:
        logger.debug(line)
        groups = r.match(line).groups()
        rawObject = {}
        for i in range(0, len(self.fields)):
          rawObject[self.fields[i]] = groups[i]
        logger.debug(rawObject)
        rawObjectList.append(rawObject)
      except Exception as e:
        logger.warning("error " + str(e))
        previous = True
        previousLine = line
        logger.warning("Training to match line: " + str(self.countLine))
      self.countLine += 1
    return rawObjectList

def lineMatcher(numFields, criteria):
  regexField = '([^"'+criteria+'\n]+|"[^"]*")'
  regexLine = '^'
  for i in range(0, numFields - 1):
    regexLine += regexField + criteria
  regexLine += regexField + '$'
  return re.compile(regexLine)

class ParserXSV(Parser):
  def __init__(self, fields, filePath, criteria = "\t"):
    super(ParserXSV, self).__init__()
    self.fields = fields
    self.path = filePath
    self.criteria = criteria

  def nextObjects(self):
    output = []
    with codecs.open(self.path, "r") as csvFile:
      try:
        dialect = csv.Sniffer().sniff(csvFile.read(1024), self.criteria)
      except csv.Error as e:
        logger.warning(e)
        logger.warning("Using defautl excel format")
        if self.criteria == "\t":
          dialect = csv.excel_tab
        else:
          dialect = csv.excel
      csvFile.seek(0)
      reader = csv.DictReader(csvFile, dialect = dialect, fieldnames = self.fields)
      for line in reader:
        output.append(line)
    return output 

# Exceptions
class ColumnsNotEquivalentException(Exception):
  """
  It controls when some object has less or more fields that the XSV file declaration.
  """
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)
