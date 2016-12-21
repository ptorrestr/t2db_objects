import unittest

from t2db_objects.parameters import generate_config_yaml

class TestParameters(unittest.TestCase):
  def setUp(self):
    pass

  def test_generate_config_yaml_1(self):
    conf_fields = [
      {'name':'name','kind':'mandatory','type':str,'default':None},
      {'name':'sex','kind':'mandatory','type':str,'default':None},
      {'name':'hp','kind':'mandatory','type':list,'default':None},
      {'name':'gold','kind':'mandatory','type':int,'default':None},
      {'name':'inventory','kind':'mandatory','type':list,'default':None},
    ]
    conf_file_path = './etc/example.yaml'
    config = generate_config_yaml(conf_fields, conf_file_path)
    self.assertEqual(config.name, 'Vorlin Laruknuzum')
    self.assertEqual(config.sex, 'Male')
    self.assertEqual(config.gold, 423)
    self.assertListEqual(config.hp, [32, 71])
    self.assertListEqual(config.inventory, ['a Holy Book of Prayers (Words of Wisdom)','a Silver Wand of Wonder'])

  def test_generate_config_yaml_2(self):
    conf_fields = [
      {'name':'name','kind':'mandatory','type':str,'default':None},
      {'name':'sex','kind':'mandatory','type':str,'default':None},
      {'name':'hp','kind':'mandatory','type':list,'default':None},
      {'name':'gold','kind':'mandatory','type':int,'default':None},
      {'name':'inventory','kind':'mandatory','type':list,'default':None},
      {'name':'other','kind':'non-mandatory','type':str,'default':'This one'},
    ]
    conf_file_path = './etc/example.yaml'
    config = generate_config_yaml(conf_fields, conf_file_path)
    self.assertEqual(config.name, 'Vorlin Laruknuzum')
    self.assertEqual(config.sex, 'Male')
    self.assertEqual(config.gold, 423)
    self.assertListEqual(config.hp, [32, 71])
    self.assertListEqual(config.inventory, ['a Holy Book of Prayers (Words of Wisdom)','a Silver Wand of Wonder'])
    self.assertEqual(config.other, 'This one')
