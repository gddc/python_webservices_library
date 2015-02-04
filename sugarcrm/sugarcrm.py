#
#   sugarcrm.py
#
#   KSU capstone project
#

from six.moves import urllib
import hashlib
try:
    import simplejson as json # Needs to be installed manually
except ImportError:
    import json # Works with python 2.7+

from .sugarerror import SugarError, SugarUnhandledException, is_error
from .sugarmodule import *

class Sugarcrm:
    """Sugarcrm main interface class.

    This class is what is used to connect to and interact with the SugarCRM
    server.
    """

    def __init__(self, url, username, password, is_ldap_member = False):
        """Constructor for Sugarcrm connection.

        Keyword arguments:
        url -- string URL of the sugarcrm REST API
        username -- username to allow login upon construction
        password -- password to allow login upon construction
        """

        # String which holds the session id of the connection, required at
        # every call after 'login'.
        self._session = ""

        # url which is is called every time a request is made.
        self._url = url

        self._username = username
        self._password = password
        self._isldap = is_ldap_member

        # Attempt to login.
        self._login()

        # Dynamically add the API methods to the object.
        for method in ['get_user_id', 'get_user_team_id',
                       'get_available_modules', 'get_module_fields',
                       'get_entries_count', 'get_entry', 'get_entries',
                       'get_entry_list', 'set_entry', 'set_entries',
                       'set_relationship', 'set_relationships',
                       'get_relationships', 'get_server_info',
                       'set_note_attachment', 'get_note_attachment',
                       'set_document_revision', 'get_document_revision',
                       'search_by_module', 'get_report_entries', 'logout']:
            # Use this to be able to evaluate "method".
            def gen(method_name):
                def f(*args):
                    try:
                        result = self._sendRequest(method_name,
                                              [self._session] + list(args))
                    except SugarError as error:
                        if error.is_invalid_session:
                            # Try to recover if session ID was lost
                            self._login()
                            result = self._sendRequest(method_name,
                                              [self._session] + list(args))
                        elif error.is_missing_module:
                            return None
                        elif error.is_null_response:
                            return None
                        elif error.is_invalid_request:
                            print method_name, args
                        else:
                            raise SugarUnhandledException('%d, %s - %s' %
                                                          (error.number,
                                                           error.name,
                                                           error.description))

                    return result
                f.__name__ = method_name
                return f
            self.__dict__[method] = gen(method)

        # Add modules containers
        self.modules = {}
        self.rst_modules = dict((m['module_key'], m)
                                for m in self.get_available_modules()['modules'])
    def __getitem__(self, key):
        if key not in self.rst_modules:
            raise KeyError("Invalid Key '%s'" % key)
        if key in self.rst_modules and key not in self.modules:
            self.modules[key] = SugarModule(self, key)
        return self.modules[key]

    def _sendRequest(self, method, data):
        """Sends an API request to the server, returns a dictionary with the
        server's response.

        It should not need to be called explicitly by the user, but rather by
        the other functions.

        Keyword arguments:
        method -- name of the method being called.
        data -- parameters to the function being called, should be in a list
                sorted by order of items
        """

        data = json.dumps(data)
        args = {'method': method, 'input_type': 'json',
                'response_type' : 'json', 'rest_data' : data}
        params = urllib.parse.urlencode(args).encode('utf-8')
        response = urllib.request.urlopen(self._url, params)
        response = response.read().strip()
        if not response:
            raise SugarError({'name': 'Empty Result',
                              'description': 'No data from SugarCRM.',
                              'number': 0})
        result = json.loads(response.decode('utf-8'))
        if is_error(result):
            raise SugarError(result)
        return result

    def _login(self):
        """
            Establish connection to the server.
        """

        args = {'user_auth': {'user_name': self._username,
                              'password': self.password}}

        x = self._sendRequest('login', args)
        try:
            self._session = x['id']
        except KeyError:
            raise SugarUnhandledException

    def relate(self, main, *secondary, **kwargs):
        """
          Relate two or more SugarEntry objects.

          Supported Keywords:
          relateby -> iterable of relationship names.  Should match the
                      length of *secondary.  Defaults to secondary
                      module table names (appropriate for most
                      predefined relationships).
        """

        relateby = kwargs.pop('relateby', [s._module._table for s in secondary])
        args = [[main._module._name] * len(secondary),
                [main['id']] * len(secondary),
                relateby,
                [[s['id']] for s in secondary]]
        # Required for Sugar Bug 32064.
        if main._module._name == 'ProductBundles':
            args.append([[{'name': 'product_index',
                          'value': '%d' % (i + 1)}] for i in range(len(secondary))])
        return self.set_relationships(*args)

    @property
    def password(self):
        """
            Returns an appropriately encoded password for this connection.
            - md5 hash for standard login.
            - plain text for ldap users
        """
        if self._isldap:
            return self._password
        encode = hashlib.md5(self._password.encode('utf-8'))
        result = encode.hexdigest()
        return result
