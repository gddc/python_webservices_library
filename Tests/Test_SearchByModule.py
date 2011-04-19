import sugarcrm
import unittest

class TestSearchByModule(unittest.TestCase):

	hostname = "http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php"
	login = "class"
	password = "class123"
	module = "Contacts"
	string = "John"
	offset = ""
	maxresult = "1"

	def test_searchbymodule(self):
		response = sugarcrm.Sugarcrm(self.hostname, self.login, self.password)
		results = response.search_by_module(self.module,self.string,self.offset,self.maxresult)
		self.assertIsNotNone(results)
		print results

if __name__ == '__main__':
    unittest.main()
