import unittest
from testSugarcrm import SugarcrmTest

class TestGetEntriesCount(SugarcrmTest):	
	def runTest(self):
		result = self.response.get_entries_count(SugarcrmTest.module)
		self.assertIsNotNone(result)
		
if __name__ == '__main__':
    unittest.main()