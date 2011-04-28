import unittest
from testSugarcrm import SugarcrmTest

class TestGetAvailableModuleFields(SugarcrmTest):
	def testGetAvailableFields(self):
		results = self.response.get_available_modules()
		self.assertIsNotNone(results)
		
if __name__ == '__main__':
    unittest.main()