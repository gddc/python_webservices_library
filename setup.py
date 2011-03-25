"""
    setupTools based setup script for
 
    To install: python setup.py install
    
"""

import os
#from setuptools import setup, find_packages
from distutils.core import setup

version = '0.1.0'

PACKAGES = ['sugarcrm'] #,'sugarcrm.Sugarcrm','sugarcrm.sugarbean']
            

setup(name = 'sugarcrm',
      version = version,
      description = "SugarCRM Python wrapper",
      author="Capstone Class, Kent State University",
      url="http://github.com/jmertic/KSU_Capstone_Spring_2011_Python",
      classifiers=["Programming Language :: Python",
                   "Inteded Audience :: Developers",
                   "Topic :: Office/Business"],
      keywords="Customer Relationship Management SugarCRM CRM",
      packages=PACKAGES,
      install_requires=['urllib','json','hashlib','sys']
)
