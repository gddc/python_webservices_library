import unittest
from testSugarcrm import SugarcrmTest

class TestGetModuleFields(SugarcrmTest):	
	def runTest(self):
		results = self.response.get_module_fields(SugarcrmTest.module)
		self.assertIsNotNone(results)
		
if __name__ == '__main__':
    unittest.main()