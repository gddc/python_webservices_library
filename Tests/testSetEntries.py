import unittest
from testSugarcrm import SugarcrmTest

class TestSetEntries(SugarcrmTest):		
	def runTest(self):
		result = self.response.set_entry(SugarcrmTest.module, SugarcrmTest.query)
		self.assertIsNotNone(result)
		checkForEntry = self.response.get_entries(SugarcrmTest.module, result['id'], SugarcrmTest.selectFields, SugarcrmTest.linkName)
		self.assertIsNotNone(result)
		
if __name__ == '__main__':
    unittest.main()