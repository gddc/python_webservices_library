#
#   sugarcrm.py
#
#   KSU capstone project
#

import urllib
import hashlib
import json
import sys

from sugarerror import *
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
                    except GeneralException:
                        # Try to recover if session ID was lost
                        self._login(self._username, self._password)
                        result = self._sendRequest(method_name,
                                              [self._session] + list(args))

                    return result

                return f
            self.__dict__[method] = gen(method)


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
        try:
            result = json.loads(response)
        except (TypeError, ValueError):
            raise InvalidConnection

        self.testForError(result)
        return result


    def testForError(self, obj):
        ## Test any returned object for an error
        # @param self the object pointer
        # @param obj the object which will be identified as an error or not
        # @return Sugarcrm.GeneralException if 'obj' is an error.
        # This function ought to be obsolete after creating classes which
        #   handle all returned objects from the server

        if isinstance(obj, dict) and obj.has_key("name"):
            print "ERROR: %s:%s \n" % (obj["name"], obj["description"])
            raise GeneralException


    def _login(self, username, password):
        """Estabilsh connection to the server.

        Keyword arguments:
        username -- SugarCRM user name.
        password -- plaintext string of the user's password.
        """

        args = {'user_auth' : {'user_name' : username,
                               'password' : _passencode(password)}}

        try:
            x = self._sendRequest('login', args)
        except GeneralException:
            raise InvalidLogin

        try:
            self._session = x["id"]
        except KeyError:
            raise InvalidConnection


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


## Remove utf-8 encoding returned from JSON 
# @param obj object which is supposedly in unicode
# @return same object in ascii
def stripUnicode(obj):
    if isinstance(obj, unicode):
        return str(obj)
    if isinstance(obj, dict):
        return dict( (str(key), stripUnicode(value)) for (key, value) in obj.items())
    if isinstance(obj, list):
        return list( stripUnicode(x) for x in obj )
    return obj

def toNameValueList(obj):
    result = obj
    if isinstance(obj, dict):
        result = list( {"name" : name, "value" : value} for (name, value) in obj.items() )
    return result

def fromNameValueList(obj):

    if isinstance(obj, list):
        result = dict( (i["name"], i['value']) for i in obj )
    elif isinstance(obj, dict):
        result = dict( (i['name'], i['value']) for i in obj.values())
    else:
    	#might want to make this a error instead of returning none
        result = None
    return result

if __name__ == "__main__":
    pass

