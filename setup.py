"""
Functionality for project setup and various installations. Enter the following
for more details:
    `python setup.py --help`
"""
# pylint:skip-file
from os import path
from setuptools import setup, find_packages

# Read the contents of the README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='autoreduce_utils',
    version='22.0.0.dev20',
    description='ISIS Autoreduce',
    author='ISIS Autoreduction Team',
    url='https://github.com/autoreduction/autoreduce-utils/',
    install_requires=[
        'pydantic==1.9.0', 'gitpython<=3.1.26', 'python-icat==0.20.1', 'suds-py3==1.4.5.0', 'confluent-kafka==1.8.2'
    ],
    packages=find_packages(),
    package_data={},
    entry_points={},
    long_description=long_description,
    long_description_content_type='text/markdown',
)
