import sugarcrm
import unittest

class TestGetModuleFields(unittest.TestCase):

	hostname = "http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php"
	login = "class"
	password = "class123"
	module = "Contacts"
	
	def test_login(self):
		response = sugarcrm.Sugarcrm(self.hostname, self.login, self.password)
		self.assertIsNotNone(response)
		self.assertEquals(1, response.connected)
		self.assertIsNotNone(response.id)
				
	def test_getModuleFields(self):
		response = sugarcrm.Sugarcrm(self.hostname, self.login, self.password)
		results = response.get_module_fields(self.module)
		self.assertIsNotNone(results)
		
if __name__ == '__main__':
    unittest.main()