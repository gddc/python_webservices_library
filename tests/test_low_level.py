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

    def test_deletecontact(self):
        contact = self._contact
        contact['deleted'] = 1
        contact.save()


if __name__ == '__main__':
    unittest.main()
