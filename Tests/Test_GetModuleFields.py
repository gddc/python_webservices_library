import sugarcrm
import unittest

class TestGetModuleFields(unittest.TestCase):

	hostname = "http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php"
	login = "class"
	password = "class123"
	module = "Contacts"
				
	def test_getModuleFields(self):
		response = sugarcrm.Sugarcrm(self.hostname, self.login, self.password)
		results = response.get_module_fields(self.module)
		self.assertIsNotNone(results)
		
	
		
if __name__ == '__main__':
    unittest.main()