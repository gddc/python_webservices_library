import unittest
from testSugarcrm import SugarcrmTest

class TestSetEntry(SugarcrmTest):

	module = "Contacts"
	query = [{'name': 'first_name', 'value': 'Jim'},
		{'name': 'last_name', 'value': 'Ball'},
		{'name': 'title', 'value': 'CEO'}]
	query2 = [{'name': 'name', 'value': 'Test Company'}]	
	linkName = [{'name': 'email_addresses', 'value': ['id', 'email_address']}]
	selectFields = ['first_name', 'last_name', 'title']
	link_field_name = "accounts"
	relatedIds = [{'name': 'name', 'value': ''}]

	def runTest(self):
		result = self.response.set_entry(self.module, self.query)
		self.assertIsNotNone(result)
		checkForEntry = self.response.get_entry(self.module, result['id'], self.selectFields, self.linkName)
		self.assertIsNotNone(checkForEntry)
		result2 = self.response.set_entry('Accounts', self.query2)
		relation = self.response.set_relationship(self.module, result['id'], self.link_field_name, [result2['id']])
		self.assertIsNotNone(relation)
		print 'checking get_relationships'
		checkForRelation = self.response.get_relationships(self.module, result['id'], self.link_field_name,"", ['name'],[{'name': 'email', 'value': ['id', 'email_address']}])

if __name__ == '__main__':
    unittest.main()