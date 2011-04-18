

import sugarcrm
import unittest

class TestGetUserId(unittest.TestCase):

	hostname = "http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php"
	login = "class"
	password = "class123"

	def test_getuserid(self):
		response = sugarcrm.Sugarcrm(self.hostname, self.login, self.password)
		results = response.get_user_id()
		self.assertIsNotNone(results)
		print results

if __name__ == '__main__':
    unittest.main()
