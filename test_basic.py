#
#   sugarcrm.py
#
#   KSU capstone project
#

import sugarcrm, getpass

# Test_basic.py is used to show the basic functionality of the sugarcrm.py class

# Accepts user input for logging into the server
user = raw_input('\nPlease enter your user name: ')
# password input isn't shown on the prompt
# password = getpass.getpass()

# injects the username into the sugarcrm url for login purposes
url = "http://ruttanvm.cs.kent.edu:4080/"+user+"/service/v2/rest.php"

# if the user is class it skips password prompting
if user == "class":
	url = "http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php"
	password = "class123"
else:
	password = getpass.getpass()

# sugarcrm.py session object
session = sugarcrm.Sugarcrm(url, user, password)	

if session.connected == 1:
	print "\nConnection successful to "+url

if session.id != 0:
	print "\nLogin Successful!"

print "\nOutputting all of the current modules from the sugarcrm database.\n"
results = session.get_available_modules()
print results

# Asks the user which module they would like to view and stores it in module
module = raw_input('\nPick a module to view from the above list. ')

# just puts in the field name, a fields array goes after
results = session.get_module_fields(module)

# Asks user if they would like to view the fields in module, stored in in_str
mod_field = "\nWould you like to see all of the fields in the "+module+" module? yes/no "
choice = raw_input(mod_field)

# Simple yes no if statement
if (choice == ('yes' or 'y')):
	print results

	
# Prints the sugar crm server info
s_info = session.get_server_info()
print "\nOutputting the server info: "
print s_info

# Outputs the user id
id = session.get_user_id()
print "\nOutputting the id of the current user: "
print id

# logs out of the server
log_out = raw_input('\nWould you like to log out of the server? ')

# Checks to see if the user wants to log out of the server, if yes outputs that a logout was successful
if (log_out == ('yes' or 'y')):
	session.logout()
	if session.connected == 0:
		print "\nLogout successful."