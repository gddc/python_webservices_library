#
#   sugarcrm.py
#
#   KSU capstone project
#

import sugarcrm, getpass

# Test_basic.py is used to show the basic functionality of the sugarcrm.py class

# Accepts user input for logging into the server
user = raw_input('Please enter your user name: ')
# password input isn't shown on the prompt
password = getpass.getpass()

# this sets the url to the users login info, if the users name is class it leaves the user portion empty
url = "http://ruttanvm.cs.kent.edu:4080/"+user+"/service/v2/rest.php"
if user == 'class':
	url = "http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php"
	password = "class123"

# sugarcrm.py session object
session = sugarcrm.Sugarcrm(url, user, password)

if session.connected == 1:
	print ""
	print "Connection successful to "+url
	print session.get_server_info()

print "Outputting all of the current modules from the sugarcrm database:\n"
results = session.get_available_modules()
for module in results["modules"]:
	print module+',',

# Asks the user which module they would like to view and stores it in module
module = raw_input('\n\nPick a module to view from the above list. ')

# just puts in the field name, a fields array goes after
results = session.get_module_fields(module)

# Asks user if they would like to view the fields in module, stored in in_str
mod_field = "\nWould you like to see all of the fields in the "+module+" module? "
choice = raw_input(mod_field)

# Simple yes no if statement
if (choice == ('yes' or 'y')):
	print results
