
#    Copyright 2012 Luis Barrueco
#
#    This file is part of sugarcrm/python_webservices_library.
#

import sugarcrm

# This is the URL for the v4 REST API in your SugarCRM server.
url = 'http://127.0.0.1/sugarcrm-6.5.0/service/v4/rest.php'
username = 'admin'
password = 'admin'

# This way you log-in to your SugarCRM instance.
conn = sugarcrm.Sugarcrm(url, username, password)

# This way you query all the Contacts in your CRM...
query = conn['Contacts'].query()
# ... but we just show the first ten of them.
for contact in query[:10]:
    print ' '.join(contact['first_name', 'last_name'])

# OUTPUT:
# Darrin Adger
# Gilbert Adkins
# Maritza Bail
# Morris Balmer
# Polly Barahona
# Claude Barksdale
# Merrill Barragan
# Aimee Bassler
# Rosario Bassler
# Gil Batten

# We define a new query, but this time we specify a couple of query exclusions.
query = conn['Contacts'].query()
new_query = query.exclude(last_name__exact = 'Bassler')
new_query = new_query.exclude(first_name__exact = 'Morris')
for contact in new_query[:10]:
    print ' '.join(contact['first_name', 'last_name'])

# OUTPUT:
# Darrin Adger
# Gilbert Adkins
# Maritza Bail
# Polly Barahona
# Claude Barksdale
# Merrill Barragan
# Gil Batten
# Rodrigo Baumeister
# Lakesha Bernhard
# Bryon Bilbo

# This new query has a filter. Please notice that the filter parameter is the
# field name in the SugarCRM module, followed by a double underscore, and then
# an operator (it can be 'exact', 'contains', 'gt', 'gte', 'lt', 'lte' or 'in').
new_query = query.filter(last_name__contains = 'ass')
for contact in new_query[:10]:
    print ' '.join(contact['first_name', 'last_name'])

# OUTPUT:
# Aimee Bassler
# Rosario Bassler
# Blake Cassity
# Ann Hassett

new_query = query.filter(last_name__in = ['Bassler', 'Everitt'])
for contact in new_query[:10]:
    print ' '.join(contact['first_name', 'last_name'])

# OUTPUT:
# Aimee Bassler
# Rosario Bassler
# Stanford Everitt

query = conn['Cases'].query()
new_query = query.filter(case_number__lt = '7')
for case in new_query[:10]:
    print ' / ' .join(case['case_number', 'name', 'description'])

# OUTPUT:
# 1 / Having trouble adding new items /
# 2 / Warning message when using the wrong browser /
# 3 / Having trouble adding new items /
# 4 / Having trouble adding new items /
# 5 / Need assistance with large customization /
# 6 / Need to purchase additional licenses /


# Search the first case and relate it to the first contact
query = conn['Cases'].query()
case = query[0]
query = conn['Contacts'].query()
query = query.filter(last_name__exact = 'Stampley')
contact = query[0]
case.relate(contact)

case.get_related(conn['Contacts'])

# OUTPUT:
# [<SugarCRM Contact entry 'Amelia Stampley'>]

# 'contact' holds a Contacts entry with last name 'Stampley'. We can modify some
# fields and then save it
contact['birthdate'] = '1978-05-10'
contact.save()

