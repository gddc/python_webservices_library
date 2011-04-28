import unittest
from testSugarcrm import SugarcrmTest

class TestSetEntry(SugarcrmTest):
	def runTest(self):
		result = self.response.set_entry(SugarcrmTest.module, SugarcrmTest.query)
		self.assertIsNotNone(result)
		checkForEntry = self.response.get_entry(SugarcrmTest.module, result['id'], SugarcrmTest.selectFields, SugarcrmTest.linkName)
		self.assertIsNotNone(checkForEntry)
		result2 = self.response.set_entry('Accounts', SugarcrmTest.query2)
		relation = self.response.set_relationship(SugarcrmTest.module, result['id'], SugarcrmTest.link_field_name, [result2['id']])
		self.assertIsNotNone(relation)
		print 'checking get_relationships'
		checkForRelation = self.response.get_relationships(SugarcrmTest.module, result['id'], SugarcrmTest.link_field_name,"", ['name'],[{'name': 'email', 'value': ['id', 'email_address']}])

if __name__ == '__main__':
    unittest.main()