import sugarcrm
import unittest

class TestGetEtriesCount(unittest.TestCase):

	hostname = "http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php"
	login = "class"
	password = "class123"
	module = "Contacts"

	def test_getEntriesCount(self):
		response = sugarcrm.Sugarcrm(self.hostname, self.login, self.password)
		result = response.get_entries_count(self.module)
		self.assertIsNotNone(result)
					
		
if __name__ == '__main__':
    unittest.main()