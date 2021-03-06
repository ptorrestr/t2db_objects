"""
===
Logger
===
"""
import os
import logging.config
import yaml


def setup_logging( default_path='etc/logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
  """ Setup logging configuration. The logging name used is clean_text.
  """
  path = default_path
  value = os.getenv(env_key, None)
  if value:
    path = value
  if os.path.exists(path):
    with open(path, 'rt') as f:
      config = yaml.load(f.read())
    logging.config.dictConfig(config)
  else:
    logging.basicConfig(level=default_level)
