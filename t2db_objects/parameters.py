import argparse
from t2db_objects import objects
from t2db_objects.utilities import readConfigFile2 as readConfigFile
from t2db_objects.utilities import formatHash

def generate_config(config_fields, conf_file_path):
  raw_config_no_format = readConfigFile(conf_file_path)
  raw_config = formatHash(raw_config_no_format, conf_fields)
  return objects.Configuration(conf_fields, raw_config)

def generate_parameters(param_fields, description, epilog):
  args = param_fields_2_parser(param_fields, description, epilog)
  raw_param = parser_2_values(args, param_fields)
  param = objects.Configuration(param_fields, raw_param)
  return param 

def param_fields_2_parser(param_fields, description, epilog):
  #TODO validate parameter fields.
  parser = argparse.ArgumentParser(description = description, epilog = epilog)
  for parameter in param_fields:
    if parameter['default'] != None:
      parser.add_argument(
        parameter['abbr'],
        action = "store",
        dest = parameter['name'],
        help = parameter['help'],
        type = parameter['type'],
        default = parameter['default'],
        required = False)
    else:
      parser.add_argument(
        parameter['abbr'],
        action = "store",
        dest = parameter['name'],
        help = parameter['help'],
        type = parameter['type'],
        required = True)
  return parser.parse_args()

def parser_2_values(args, param_fields):
  raw_param = {}
  for parameter in param_fields:
    raw_param[parameter['name']] = getattr(args, parameter['name'])
  return raw_param
