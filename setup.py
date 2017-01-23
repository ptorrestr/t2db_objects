import subprocess
from setuptools import setup

def readme():
  with open('README.md') as f:
    return f.read()

def version():
  out = subprocess.Popen(['git','describe','--tags'], stdout = subprocess.PIPE, universal_newlines = True)
  out.wait()
  if out.returncode == 0:
    m_version = out.stdout.read().strip()
    version = m_version.split("-")
    if len(version) > 0:
      print(version[0])
      return version[0]
  return "0.0.1" #default version

setup(
  name = 't2db_objects',
  version = version(),
  description = 'Bases objects for t2db',
  long_description = readme(),
  classifiers = [
    'Programming Language :: Python :: 3.5',
  ],
  url = 'http://github.com/ptorrest/t2db_objects',
  author = 'Pablo Torres',
  author_email = 'pablo.torres.t@gmail.com',
  license = 'GNU',
  packages = ['t2db_objects', 't2db_objects.tests'],
  test_suite = 't2db_objects.tests',
  zip_safe = False,
)
