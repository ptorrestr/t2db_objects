#TODO: add tests!
import unittest

from t2db_objects.utilities import read_env_variable

class TestUtilities(unittest.TestCase):
  def setUp(self):
    pass

  def testReadEnvVariable(self):
    flag = "HOME"
    value = read_env_variable(flag)
    self.assertNotEqual(value, None)
