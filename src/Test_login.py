import sugarcrm
import unittest

class TestLogin(unittest.TestCase):
	
	hostname = "http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php"
	login = "class"
	password = "class123"
	
	def test_login(self):
		response = sugarcrm.Sugarcrm(self.hostname, self.login, self.password)
		self.assertIsNotNone(response)
		self.assertEquals(1, response.connected)
		self.assertIsNotNone(response.id)
		
if __name__ == '__main__':
    unittest.main()