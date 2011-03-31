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

if session.id != 0:
	print ""
	print "Login Successful!"


print ""
print "Outputting all of the current modules from the sugarcrm database."
results = session.get_available_modules()
print results

print ""
# Asks the user which module they would like to view and stores it in module
module = raw_input('Pick a module to view from the above list. ')

# just puts in the field name, a fields array goes after
results = session.get_module_fields(module)

# Asks user if they would like to view the fields in module, stored in in_str
print ""
mod_field = "Would you like to see all of the fields in the "+module+" module? "
choice = raw_input(mod_field)

# Simple yes no if statement
if (choice == ('yes' or 'y')):
	print results

# Prints the sugar crm server info
print ""
s_info = session.get_server_info()
print "Outputting the server info: "
print s_info

# Outputs the user id
# Not sure if the values getting are correct, but leaving it here since it doesn't output garbage
print ""
print "Outputting the id of the current user: "
id = session.get_user_id()
print id

# Outputs garbage
# group_id = session.get_user_team_id()
# print group_id

print ""
log_out = raw_input('Would you like to log out of the server? ')

# Checks to see if the user wants to log out of the server, if yes outputs that a logout was successful
if (log_out == ('yes' or 'y')):
	session.logout()
	if session.connected == 0:
		print ""
		print "Logout successful."

	