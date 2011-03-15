import sugarcrm
import unittest

class TestSetEntry(unittest.TestCase):

	hostname = "http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php"
	login = "class"
	password = "class123"
	module = "Contacts"
	query = [{'name': 'first_name', 'value': 'Jim'},
		{'name': 'last_name', 'value': 'Ball'},
		{'name': 'title', 'value': 'CEO'}]

	def test_set_entry(self):
		response = sugarcrm.Sugarcrm(self.hostname, self.login, self.password)
		result = response.set_entry(self.module, self.query)
		self.assertIsNotNone(result)
		
if __name__ == '__main__':
    unittest.main()