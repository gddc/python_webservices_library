import unittest
from testSugarcrm import SugarcrmTest

class TestLogin(SugarcrmTest):
	def runTest(self):
		self.assertIsNotNone(self.response)
		self.assertEquals(1, self.response.connected)
		self.assertIsNotNone(self.response.id)
		
if __name__ == '__main__':
    unittest.main()