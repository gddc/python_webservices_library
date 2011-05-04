import unittest
import sugarcrm

class SugarcrmTest(unittest.TestCase):
	
	server = "http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php"
	user = "class"
	password = "class123"
	
	def setUp(self):
		self.response = sugarcrm.Sugarcrm(self.server, self.user, self.password)

	def tearDown(self):
		self.response.logout


if __name__ == '__main__':
    unittest.main()