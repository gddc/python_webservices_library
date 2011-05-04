import unittest
from testSugarcrm import SugarcrmTest

class TestSetEntries(SugarcrmTest):		

	module = "Contacts"
	query = [{'name': 'first_name', 'value': 'Jim'},
		{'name': 'last_name', 'value': 'Ball'},
		{'name': 'title', 'value': 'CEO'}]
	selectFields = ['first_name', 'last_name', 'title']
	linkName = [{'name': 'email_addresses', 'value': ['id', 'email_address']}]

	def runTest(self):
		result = self.response.set_entry(self.module, self.query)
		self.assertIsNotNone(result)
		checkForEntry = self.response.get_entries(self.module, result['id'], self.selectFields, self.linkName)
		self.assertIsNotNone(result)
		
if __name__ == '__main__':
    unittest.main()