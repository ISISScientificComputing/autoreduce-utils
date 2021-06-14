# pylint:skip-file
"""
Wrapper for the functionality for various installation and project setup commands
see:
    `python setup.py help`
for more details
"""
from os import path
from setuptools import setup, find_packages

# read the contents of the README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='autoreduce_utils',
      version='22.0.0.dev1',
      description='ISIS Autoreduce',
      author='ISIS Autoreduction Team',
      url='https://github.com/ISISScientificComputing/autoreduce-utils/',
      install_requires=[
          'attrs==21.2.0',
          'gitpython==3.1.14',
          'python-icat==0.18.1',
          'suds-py3==1.4.4.1',
          'stomp.py==6.1.0',
      ],
      packages=find_packages(),
      package_data={"autoreduce_utils": ["test_credentials.ini"]},
      entry_points={"console_scripts": ["autoreduce-creds-migrate = autoreduce_utils.migrate_credentials:main"]},
      long_description=long_description,
      long_description_content_type='text/markdown')
