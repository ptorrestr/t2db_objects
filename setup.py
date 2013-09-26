from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name = 't2db_objects',
    version = '0.2.1',
    description = 'Bases objects for t2db',
    long_description = readme(),
    classifiers = [
       'Programming Language :: Python :: 3.2',
    ],
    url = 'http://github.com/ptorrest/t2db_objects',
    author = 'Pablo Torres',
    author_email = 'pablo.torres@deri.org',
    license = 'GNU',
    packages = ['t2db_objects', 't2db_objects.tests'],
    install_requires = [
    ],
    test_suite = 't2db_objects.tests',
    zip_safe = False,
)
