"""
    setupTools based setup script for

    To install: python setup.py install

"""

from distutils.core import setup

version = '0.3.0'

PACKAGES = ['sugarcrm']


setup(name = 'sugarcrm',
      version = version,
      description = "SugarCRM Python library",
      author="Capstone Class, Kent State University",
      author_email="luis.barrueco@hash-tag.com.ar",
      url="http://github.com/sugarcrm/python_webservices_library",
      classifiers=["Programming Language :: Python",
                   "Inteded Audience :: Developers",
                   "Topic :: Office/Business"],
      keywords="Customer Relationship Management SugarCRM CRM",
      packages=PACKAGES,
      install_requires=['simplejson>=2.2', 'six>=1.4.1']
)
