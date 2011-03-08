import os
from setuptools import setup, find_packages

version = '0.1.0'

setup(name = 'sugarcrm',
      version = version,
      description = "SugarCRM Python wrapper",
      classifiers=["Programming Language :: Python"],
      keywords="Customer Relationship Management SugarCRM CRM",
      packages=find_packages(),
      namespace_packages=['sugarcrm'],
      install_requires=['urllib','json']
)
