import sugarcrm, unittest

class TestLogin(unittest.TestCase):

	login = "class"
	password = "class123"
	
	def test_login(self):
		response = sugarcrm.login(self, login, password)
		self.assertIsNotNone(response)
		
if __name__ == '__main__':
    unittest.main()
