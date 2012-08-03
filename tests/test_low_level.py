import unittest
import sys
sys.path.insert(1, "..")

import sugarcrm
import sugarcrm_config


class LoginTest(unittest.TestCase):
    def test_login(self):
        response = sugarcrm.Sugarcrm(sugarcrm_config.url,
                                        sugarcrm_config.username,
                                        sugarcrm_config.password)
        self.assertNotEqual(response._session, '')


class BaseTests(unittest.TestCase):

    def setUp(self):
        self._conn = sugarcrm.Sugarcrm(sugarcrm_config.url,
                                        sugarcrm_config.username,
                                        sugarcrm_config.password)


class BasicTesting(BaseTests):

    def test_get_module_fields(self):
        response = self._conn.get_module_fields(sugarcrm_config.test_module)
        self.assertIn('module_fields', response.keys())
        self.assertIn('id', response['module_fields'])

    def test_get_entries_count(self):
        response = self._conn.get_entries_count(sugarcrm_config.test_module)
        self.assertGreaterEqual(int(response['result_count']), 0)

    def test_get_available_modules(self):
        response = self._conn.get_available_modules()
        self.assertIn(sugarcrm_config.test_module, [module['module_key'] for
                                            module in response['modules']])


class EntryTesting(BaseTests):

    def setUp(self):
        BaseTests.setUp(self)

        contacts = self._conn.modules['Contacts']
        contact = sugarcrm.SugarEntry(contacts)
        contact['first_name'] = 'John'
        contact['last_name'] = 'Smith'
        contact['birthdate'] = '1970-01-10'

        contact.save()
        self._contact = contact

    def test_rename_contact(self):
        self._contact['first_name'] = 'Paul'
        self._contact.save()

        search_result = self._conn.modules['Contacts'].query().filter(
                                            id__exact = self._contact['id'])
        contact = search_result[0]

        self.assertEqual(self._contact['first_name'],
                            contact['first_name'])

    def test_relationship(self):
        accounts = self._conn.modules['Accounts']
        account = sugarcrm.SugarEntry(accounts)
        account['name'] = u'John\'s Account'
        account['website'] = 'http//www.hash-tag.com.ar/'

        account.save()

        self._contact.relate(account)
        self._contact.save()
        account.save()

        rel_accounts = self._contact.get_related(accounts)
        rel_account = rel_accounts[0]
        self.assertEqual(account['name'], rel_account['name'])

        rel_contacts = account.get_related(self._conn.modules['Contacts'])
        rel_contact = rel_contacts[0]
        self.assertEqual(self._contact['first_name'], rel_contact['first_name'])

        account['deleted'] = 1
        account.save()

    def tearDown(self):
        contact = self._contact
        contact['deleted'] = 1
        contact.save()
        pass


if __name__ == '__main__':
    unittest.main()
