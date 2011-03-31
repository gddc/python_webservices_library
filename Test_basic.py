import sugarcrm, unittest, getpass

# Test_basic.py is used to show the basic functionality of the sugarcrm.py class

# Testing different log in methods, as well as not wanting to store my own personal password in the code
user = raw_input('Please enter your user name: ')
# password input isn't shown on the prompt
password = getpass.getpass()

# this sets the url to the users login info, if the users name is class it leaves the user portion empty
url = "http://ruttanvm.cs.kent.edu:4080/"+user+"/service/v2/rest.php"
if user == 'class':
	url = "http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php"
	password = "class123"

session = sugarcrm.Sugarcrm(url, user, password)	

if session.connected == 1:
	print "Connection successful to "+url

if session.id != 0:
	print "Login Successful!"

module = raw_input('Pick a module to test (Accounts, Bugs, Calls, Cases, Contacts, Leads, Opportunities, Projects, Project Task, and Quotes) ')

# just puts in the field name, a fields array goes after
results = session.get_module_fields(module)

in_str = "Would you like to see all of the fields in the "+module+" module? "
choice = raw_input(in_str)

if (choice == ('yes' or 'y')):
	print results
