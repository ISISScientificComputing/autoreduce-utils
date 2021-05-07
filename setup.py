# pylint:skip-file
"""
Wrapper for the functionality for various installation and project setup commands
see:
    `python setup.py help`
for more details
"""
from setuptools import setup, find_packages

setup(name='autoreduce_utils',
      version='1.0.0',
      description='ISIS Autoreduce ',
      author='ISIS Autoreduction Team',
      url='https://github.com/ISISScientificComputing/autoreduce-utils/',
      install_requires=[
          'Django==3.2',
          'gitpython==3.1.14',
          'python-icat==0.18.1',
          'suds-py3==1.4.4.1',
          'stomp.py==6.1.0',
      ],
      packages=find_packages(),
      package_data={"autoreduce_utils": ["test_credentials.ini"]},
      entry_points={"console_scripts": ["autoreduce-creds-migrate = autoreduce_utils.migrate_credentials:main"]})
