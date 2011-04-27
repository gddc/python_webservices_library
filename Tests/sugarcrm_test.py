import unittest
import sugarcrm

class SugarcrmTest(unittest.TestCase):
	
	response = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php", "class", "class123")
	module = "Contacts"
	query = [{'name': 'first_name', 'value': 'Jim'},
		{'name': 'last_name', 'value': 'Ball'},
		{'name': 'title', 'value': 'CEO'}]
	query2 = [{'name': 'name', 'value': 'Test Company'}]	
	linkName = [{'name': 'email_addresses', 'value': ['id', 'email_address']}]
	selectFields = ['first_name', 'last_name', 'title']
	link_field_name = "accounts"
	relatedIds = [{'name': 'name', 'value': ''}]
	
	
	def setUp(self):
		self.response = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php", "class", "class123")

	def tearDown(self):
		self.response.logout

	def test_login(self):
		response = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php", "class", "class123")
		self.assertIsNotNone(response)
		self.assertEquals(1, response.connected)
		self.assertIsNotNone(response.id)
		
	def test_GetEntriesCount(self):
		response = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php", "class", "class123")
		result = response.get_entries_count(self.module)
		self.assertIsNotNone(result)
	
	def test_GetModuleFields(self):
		response = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php", "class", "class123")
		results = response.get_module_fields(self.module)
		self.assertIsNotNone(results)

	def test_GetAvailableModuleFields(self):
		response = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php", "class", "class123")
		results = self.response.get_available_modules()
		self.assertIsNotNone(results)

	def test_SetEntry(self):
		response = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php", "class", "class123")
		result = response.set_entry(self.module, self.query)
		self.assertIsNotNone(result)
		checkForEntry = response.get_entry(self.module, result['id'], self.selectFields, self.linkName)
		self.assertIsNotNone(checkForEntry)
		result2 = response.set_entry('Accounts', self.query2)
		relation = response.set_relationship(self.module, result['id'], self.link_field_name, [result2['id']])
		self.assertIsNotNone(relation)
		print 'checking get_relationships'
		checkForRelation = response.get_relationships(self.module, result['id'], self.link_field_name,"", ['name'],[{'name': 'email', 'value': ['id', 'email_address']}])

	def test_GetUserId(self):
		response = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php", "class", "class123")
		result = self.response.get_user_id()
		self.assertIsNotNone(result)
		
	def test_GetUserTeamId(self):
		response = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php", "class", "class123")
		result = self.response.get_user_team_id()
		print result
		
	def test_SetEntries(self):
		response = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php", "class", "class123")
		result = response.set_entry(self.module, self.query)
		self.assertIsNotNone(result)
		checkForEntry = response.get_entries(self.module, result['id'], self.selectFields, self.linkName)
		self.assertIsNotNone(result)
		
	def test_GetServerInfo(self):
		response = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php", "class", "class123")
		result = response.get_server_info()
		self.assertIsNotNone(result)
		
	def test_GetUserId(self):
		response = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php", "class", "class123")
		result = response.get_user_id([response['id']])
		print result
if __name__ == '__main__':
    unittest.main()