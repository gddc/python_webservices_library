import unittest
from testSugarcrm import SugarcrmTest

class TestGetUserId(SugarcrmTest):
	def runTest(self):
		result = self.response.get_user_id()
		self.assertIsNotNone(result)
		
if __name__ == '__main__':
    unittest.main()