import unittest
from testSugarcrm import SugarcrmTest

class TestGetUserTeamId(SugarcrmTest):		
	def runTest(self):
		result = self.response.get_user_team_id()
		print result
		
if __name__ == '__main__':
    unittest.main()