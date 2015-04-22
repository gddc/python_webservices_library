#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Jan 10, 2013

@author: daniel

This utility file provides a method for moving information between Sugar
instances.
'''

from collections import defaultdict
from sugarcrm import Sugarcrm
from code import interact
from sugarcrm.sugarentry import SugarEntry

com_url = 'http://<host>:<port>/service/v4_1/rest.php'
com_usr = '<user>'
com_pwd = '<pass>'

pro_url = 'http://<host>:<port>/service/v4_1/rest.php'
pro_usr = '<user>'
pro_pwd = '<pass>'

modules = ['Accounts', 'Contacts', 'Opportunities', 'Leads', 'Notes',
           'Prospects', 'Tasks']

cache = defaultdict(dict)
# Fill in user values from one system to the other here.
#   The mapping is From -> To.  Ie: Old System -> New System.
cache['Users']['1'] = '1'

# This map holds fields that need to pull from other cached values.
relate = {
  'Contacts': {
    'account_id': 'Accounts',
    'assigned_user_id': 'Users'
  },
  'Opportunities': {
    'account_id': 'Accounts',
    'assigned_user_id': 'Users'
  },
  'Leads': {
    'account_id': 'Accounts',
    'assigned_user_id': 'Users',
    'contact_id': 'Contacts',
    'opportunity_id': 'Opportunities',
  },
  'Prospects': {
    'assigned_user_id': 'Users',
    'lead_id': 'Leads'
  },
  'Tasks': {
    'assigned_user_id': 'Users',
    'contact_id': 'Contacts'
  },
  'Calls': {
    'assigned_user_id': 'Users',
    'contact_id': 'Contacts'
  },
  'Notes': {
    'account_id': 'Accounts',
    'assigned_user_id': 'Users',
    'contact_id': 'Contacts',
    'lead_id': 'Leads',
    'opportunity_id': 'Opportunities'
  },
  'Accounts': {
    'assigned_user_id': 'Users'
  }
}

SPro = Sugarcrm(pro_url, pro_usr, pro_pwd)
SCom = Sugarcrm(com_url, com_usr, com_pwd)

# A second lookup, this one for required module level connections that
# must be generated.
mod_links = {
  'Tasks': [SCom.modules['Leads'],
            SCom.modules['Notes'],
            SCom.modules['Opportunities'],
            SCom.modules['Accounts']],
  'Notes': [SCom.modules['Opportunities'],
            SCom.modules['Leads'], ]
}

def makeProEntry(oldEntry, oldID = None):
  module = oldEntry._module
  mod_name = module._name
  newEntry = SugarEntry(SPro, mod_name)
  for field in module._fields.keys():
    if field == 'id':
      oldID = oldEntry[field]
      continue
    if field in relate[mod_name]:
      ref_mod = relate[mod_name][field]
      newEntry[field] = cache[ref_mod].get(oldEntry[field], '')
      continue
    newEntry[field] = oldEntry[field]
  newEntry.save()
  for relmod in mod_links.get(mod_name, []):
    for relentry in oldEntry.get_related(relmod):
      if relentry['id'] in cache[relmod._name]:
        newrelentry = SPro.newSugarEntry(relmod._name)
        newrelentry['id'] = cache[relmod._name][relentry['id']]
        newEntry.relate(newrelentry)
  if oldID is not None:
    cache[mod_name][oldID] = newEntry['id']

if __name__ == '__main__':
  interact(local = globals())

