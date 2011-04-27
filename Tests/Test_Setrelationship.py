import sugarcrm
import unittest

class TestSetRelationship(unittest.TestCase):

    hostname = "http://ruttanvm.cs.kent.edu:4080/jdang/service/v2/rest.php"
    login = "jdang"
    password = "lebron23"
    module = "Accounts"
    module2 = "Contacts"
    query1 = "'Contacts', [{'name':'first_name', 'value': 'John'}, {'name':'last_name', 'value':'Mertic'}]"
    query2 = "'Accounts', [{'name':'name', 'value':'brand new account!'},{'name':'description','value':'a new account to test python package'}]"
    
    def test_setrelationship(self):
        response = sugarcrm.Sugarcrm(self.hostname, self.login, self.password)
        data1 = response.set_entry(self.module,self.query1)
        self.assertIsNotNone(data1)
        data2 = response.set_entry(self.module2,self.query2)
        self.assertIsNotNone(data2)
        results = response.set_relationship(self.module, data1["id"], self.module2, [data2["id"]])
        self.assertIsNotNone(results)


if __name__ == '__main__':
    unittest.main()
