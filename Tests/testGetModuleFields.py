import unittest
from testSugarcrm import SugarcrmTest


class TestGetModuleFields(SugarcrmTest):

	module = "Contacts"
	
	def runTest(self):
		results = self.response.get_module_fields(self.module)
		self.assertIsNotNone(results)
		
if __name__ == '__main__':
    unittest.main()