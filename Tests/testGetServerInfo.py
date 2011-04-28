import unittest
from testSugarcrm import SugarcrmTest

class TestGetServerInfo(SugarcrmTest):		
	def runTest(self):
		result = self.response.get_server_info()
		self.assertIsNotNone(result)
		
if __name__ == '__main__':
    unittest.main()