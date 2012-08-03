#
#   sugarcrm.py
#
#   KSU capstone project
#

import urllib
import hashlib
import json
import sys

from sugarerror import SugarError, SugarUnhandledException, is_error
from sugarmodule import *

class Sugarcrm:
    """Sugarcrm main interface class.

    This class is what is used to connect to and interact with the SugarCRM
    server.
    """
    
    def __init__(self, url, username, password):
        """Constructor for Sugarcrm connection.

        Keyword arguments:
        url -- string URL of the sugarcrm REST API
        username -- username to allow login upon construction
        password -- password to allow login upon construction
        """

        # String which holds the session id of the connection, requierd at
        # every call after 'login'.
        self._session = ""

        # url which is is called every time a request is made.
        self._url = url

        self._username = username
        self._password = password

        # Attempt to login.
        self._login(username, password)

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
                    except SugarError, error:
                        if error.is_invalid_session():
                            # Try to recover if session ID was lost
                            self._login(self._username, self._password)
                            result = self._sendRequest(method_name,
                                              [self._session] + list(args))
                        else:
                            raise SugarUnhandledException

                    return result

                return f
            self.__dict__[method] = gen(method)

        # Add modules shortcuts
        self.modules = {}
        rst_modules = self.get_available_modules()
        for module_name in [module['module_key'] for
                                            module in rst_modules['modules']]:
            try:
                module = SugarModule(self, module_name)
                self.modules[module_name] = module
            except:
                pass


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
        params = urllib.urlencode(args)
        response = urllib.urlopen(self._url, params)
        response = response.read()

        result = json.loads(response)

        if is_error(result):
            raise SugarError(result)

        return result


    def _login(self, username, password):
        """Estabilsh connection to the server.

        Keyword arguments:
        username -- SugarCRM user name.
        password -- plaintext string of the user's password.
        """

        args = {'user_auth' : {'user_name' : username,
                               'password' : _passencode(password)}}

        x = self._sendRequest('login', args)
        try:
            self._session = x["id"]
        except KeyError:
            raise SugarUnhandledException


    def relate(self, main, secondary):
        """Relate two SugarEntry objects."""

        self.set_relationship(main._module._name,
                            main['id'], secondary._module._name.lower(),
                            [secondary['id']])


def _passencode(password):
    """Returns md5 hash to send as a password.

    Keyword arguments:
    password -- string to be encoded
    """

    encode = hashlib.md5(password)
    result = encode.hexdigest()

    return result

