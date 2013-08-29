from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='t2db_objects',
      version='0.1',
      description='Bases objects for t2db',
      long_description=readme(),
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.2',
      ],
      url='http://github.com/ptorrest/t2db_objects',
      author='Pablo Torres',
      author_email='pablo.torres@deri.org',
      license='GNU',
      packages=['t2db_objects'],
      install_requires=[
      ],
      test_suite='t2db_objects.tests',
      #tests_require=['nose', 'nose-cover3'],
      #entry_points={
      #    'console_scripts': ['funniest-joke=funniest.cmd:main'],
      #},
      zip_safe=False)