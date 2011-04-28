import unittest
import sugarcrm

class SugarcrmTest(unittest.TestCase):
	
	module = "Contacts"
	query = [{'name': 'first_name', 'value': 'Jim'},
		{'name': 'last_name', 'value': 'Ball'},
		{'name': 'title', 'value': 'CEO'}]
	query2 = [{'name': 'name', 'value': 'Test Company'}]	
	linkName = [{'name': 'email_addresses', 'value': ['id', 'email_address']}]
	selectFields = ['first_name', 'last_name', 'title']
	link_field_name = "accounts"
	relatedIds = [{'name': 'name', 'value': ''}]
		
	def setUp(self):
		self.response = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/emarsh/service/v2/rest.php", "admin", "class123")

	def tearDown(self):
		self.response.logout


if __name__ == '__main__':
    unittest.main()