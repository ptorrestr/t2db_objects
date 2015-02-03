import unittest
from os import remove
from os import popen
from os.path import isfile

from t2db_objects.serializerXSV import BufferedReader
from t2db_objects.serializerXSV import append
from t2db_objects.serializerXSV import SerializerXSV
from t2db_objects.serializerXSV import BufferedParserXSV
from t2db_objects.serializerXSV import ParserXSV
from t2db_objects.serializerXSV import ColumnsNotEquivalentException

def lineCount(filePath):
  p = popen("cat " + filePath + " | awk \'BEGIN{n=0}{n++}END{print n}\'")
  pOut = p.read()
  return int(pOut)

class TestBufferedReaderClass(unittest.TestCase):
  def setUp(self):
    pass

  def testInitClose(self):
    filePath = "./etc/example.tsv"
    r = BufferedReader(filePath, 10)
    lines = r.nextLines()
    self.assertEqual(len(lines), 10)
    r.close()

  def testNextLinesCuadraticBufferSize(self):
    filePath = "./etc/example.tsv"
    r = BufferedReader(filePath, 10)
    count = 0
    while True:
      lines = r.nextLines()
      count += len(lines)
      if not lines:
        break
    self.assertEqual(count, 100)

  def testNextLinesLargerBufferSize(self):
    filePath = "./etc/example.tsv"
    r = BufferedReader(filePath, 15)
    count = 0
    while True:
      lines = r.nextLines()
      count += len(lines)
      if not lines:
        break
    self.assertEqual(count, 100)

  def testNextLinesSmallerBufferSize(self):
    filePath = "./etc/example.tsv"
    r = BufferedReader(filePath, 7)
    count = 0
    while True:
      lines = r.nextLines()
      count += len(lines)
      if not lines:
        break
    self.assertEqual(count, 100)

class TestAppendFunction(unittest.TestCase):
  def setUp(self):
    pass

  def testWrite(self):
    outputFilePath = "./etc/output.tsv"
    if isfile(outputFilePath):
      remove(outputFilePath)
    line = "an example line"
    append(outputFilePath, line)
    self.assertTrue(isfile(outputFilePath))
    self.assertEqual(lineCount(outputFilePath), 1)
    remove(outputFilePath)

class TestSerializerXSVClass(unittest.TestCase):
  def setUp(self):
    pass

  def testInit(self):
    fields = ["date", "id", "hash", "user_id", "status"]
    filePath = "./etc/output.tsv"
    s = SerializerXSV(filePath, True, fields)
    rawObject = { "date": "2011-08-07T05:57:45Z", "id":"100068086551543808", "hash":"18974170"
      , "user_id":"293331739", "status": "@ShesDopeTho good myself.."}
    s.pushObjects([rawObject])
    self.assertTrue(isfile(filePath))
    s = SerializerXSV(filePath, True, fields)
    self.assertFalse(isfile(filePath))

  
  def testInitNotOverwrite(self):
    fields = ["date", "id", "hash", "user_id", "status"]
    filePath = "./etc/output.tsv"
    s = SerializerXSV(filePath, True, fields)
    rawObject = { "date": "2011-08-07T05:57:45Z", "id":"100068086551543808", "hash":"18974170"
      , "user_id":"293331739", "status": "@ShesDopeTho good myself.."}
    s.pushObjects([rawObject])
    self.assertTrue(isfile(filePath))
    s = SerializerXSV(filePath, False, fields)
    self.assertTrue(isfile(filePath))

  def testSerializeLine(self):
    fields = ["date", "id", "hash", "user_id", "status"]
    filePath = "./etc/output.tsv"
    s = SerializerXSV(filePath, True, fields)
    rawObject = { "date": "2011-08-07T05:57:45Z", "id":"100068086551543808", "hash":"18974170"
      , "user_id":"293331739", "status": "@ShesDopeTho good myself.."}
    goldenLine = "2011-08-07T05:57:45Z\t100068086551543808\t18974170\t293331739\t@ShesDopeTho good myself.."
    self.assertEqual(s.serializeLine(rawObject), goldenLine)

  def testSerializerLineLessColumns(self):
    fields = ["date", "id", "hash", "user_id", "status"]
    filePath = "./etc/output.tsv"
    s = SerializerXSV(filePath, True, fields)
    rawObject = { "date": "2011-08-07T05:57:45Z", "id":"100068086551543808", "hash":"18974170" }
    self.assertRaises(ColumnsNotEquivalentException, s.serializeLine, rawObject)

  def testSerializerLineMissingField(self):
    fields = ["date", "id", "hash", "user_id", "other"]
    filePath = "./etc/output.tsv"
    s = SerializerXSV(filePath, True, fields)
    rawObject = { "date": "2011-08-07T05:57:45Z", "id":"100068086551543808", "hash":"18974170"
       , "user_id":"293331739", "status": "@ShesDopeTho good myself.."}
    self.assertRaises(ColumnsNotEquivalentException, s.serializeLine, rawObject)

  def testPushObjects(self):
    fields = ["date", "id", "hash", "user_id", "status"]
    filePath = "./etc/output.tsv"
    if isfile(filePath):
      remove(filePath)
    s = SerializerXSV(filePath, True, fields)
    rawObject1 = { "date": "2011-08-07T05:57:45Z", "id":"100068086551543808", "hash":"18974170"
       , "user_id":"293331739", "status": "@ShesDopeTho good myself.."}
    rawObject2 = { "date": "2011-08-07T05:57:45Z", "id":"100068086551543808", "hash":"18974170"
       , "user_id":"293331739", "status": "@ShesDopeTho good myself.."}
    rawObjectList = [rawObject1, rawObject2]
    s.pushObjects(rawObjectList)
    self.assertTrue(isfile(filePath))
    self.assertEqual(lineCount(filePath), 2)
    remove(filePath)

class TestBufferedParserXSVClass(unittest.TestCase):
  def setUp(self):
    pass

  def testInit(self):
    fields = ["date", "id", "hash", "user_id", "status"]
    filePath = "./etc/example.tsv"
    p = BufferedParserXSV(fields, filePath)
    p.close()

  def testParseLine(self):
    fields = ["date", "id", "hash", "user_id", "status"]
    filePath = "./etc/example.tsv"
    line = "2011-08-07T05:57:45Z\t100068086551543808\t18974170\t293331739\t@ShesDopeTho good myself.."
    p = BufferedParserXSV(fields, filePath)
    obj = p.parseLine(line, 1)
    self.assertEqual(obj["date"], "2011-08-07T05:57:45Z")
    self.assertEqual(obj["id"], "100068086551543808")
    self.assertEqual(obj["hash"], "18974170")
    self.assertEqual(obj["user_id"], "293331739")
    self.assertEqual(obj["status"], "@ShesDopeTho good myself..")
    p.close()

  def testParseLineMoreColumns(self):
    fields = ["date", "id", "hash", "user_id", "status"]
    filePath = "./etc/example.tsv"
    line = "2011-08-07T05:57:45Z\t100068086551543808\t18974170\t293331739\t@ShesDopeTho good myself..\tother column"
    p = BufferedParserXSV(fields, filePath)
    obj = p.parseLine(line, 1)
    self.assertEqual(obj["date"], "2011-08-07T05:57:45Z")
    self.assertEqual(obj["id"], "100068086551543808")
    self.assertEqual(obj["hash"], "18974170")
    self.assertEqual(obj["user_id"], "293331739")
    self.assertEqual(obj["status"], "@ShesDopeTho good myself..")
    p.close()

  def testParseLineMoreFields(self):
    fields = ["date", "id", "hash", "user_id", "status", "otherfield"]
    filePath = "./etc/example.tsv"
    line = "2011-08-07T05:57:45Z\t100068086551543808\t18974170\t293331739\t@ShesDopeTho good myself.."
    p = BufferedParserXSV(fields, filePath)
    self.assertRaises(ColumnsNotEquivalentException, p.parseLine, line, 1)
    p.close()

  def testNextLines(self):
    fields = ["date", "id", "hash", "user_id", "status"]
    filePath = "./etc/example.tsv"
    p = BufferedParserXSV(fields, filePath)
    count = 0
    while True:
      rawObjects = p.nextObjects()
      if not rawObjects:
        break
      count += len(rawObjects)
    self.assertEqual(count, 100)

  def testNextLines2(self):
    fields = ["date", "id", "hash", "user_id", "status"]
    filePath = "./etc/example2.tsv"
    p = BufferedParserXSV(fields, filePath)
    count = 0
    while True:
      rawObjects = p.nextObjects2()
      if not rawObjects:
        break
      count += len(rawObjects)
    self.assertEqual(count, 7)

  def testNextLines3(self):
    fields = ["date", "id", "hash", "user_id", "status"]
    filePath = "./etc/example3.tsv"
    p = BufferedParserXSV(fields, filePath, criteria = ",")
    count = 0
    while True:
      rawObjects = p.nextObjects2()
      if not rawObjects:
        break
      count += len(rawObjects)
    self.assertEqual(count, 7)

  def testNextLinesGreaterBuffer(self):
    fields = ["date", "id", "hash", "user_id", "status"]
    filePath = "./etc/example.tsv"
    p = BufferedParserXSV(fields, filePath, 200)
    while True:
      rawObjects = p.nextObjects()
      if not rawObjects:
        break
    self.assertEqual(p.count, 100)

  def testNextLinesSmallerBuffer(self):
    fields = ["date", "id", "hash", "user_id", "status"]
    filePath = "./etc/example.tsv"
    p = BufferedParserXSV(fields, filePath, 50)
    while True:
      rawObjects = p.nextObjects()
      if not rawObjects:
        break
    self.assertEqual(p.count, 100)

  def testNextLinesBufferFile2(self):
    fields = ["id","name","asciiname","alternatenames","latitude","longitude","feature_class","feature_code","country_code","cc2","admin1_code","admin2_code","admin3_code","admin4_code","population","elevation","dem","timezone","modification_date"]
    filePath = "./etc/example6.tsv"
    p = BufferedParserXSV(fields, filePath, 50)
    while True:
      rawObjects = p.nextObjects()
      if not rawObjects:
        break
    self.assertEqual(p.count, 100)

class TestParserXSVClass(unittest.TestCase):
  def setUp(self):
    pass

  def testNextLines1(self):
    fields = ['id','status','hash','created_at', 'c1','c2','user_id','name','screen_name','image']
    filePath = "./etc/example4.csv"
    p = ParserXSV(fields, filePath, criteria = ",")
    count = 0
    rawObjects = p.nextObjects()
    count += len(rawObjects)
    self.assertEqual(count, 5)

  def testNextLines2(self):
    fields = ['id','status','hash','created_at', 'c1','c2','user_id','name','screen_name','image']
    filePath = "./etc/example5.csv"
    p = ParserXSV(fields, filePath, criteria = ",")
    count = 0
    rawObjects = p.nextObjects()
    count += len(rawObjects)
    self.assertEqual(count, 89) 

