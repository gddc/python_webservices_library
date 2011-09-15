#
#   sugarcrm.py
#
#   KSU capstone project
#

import urllib, hashlib, json, sys
from sugar_error import *
from sugarmodule import *

## Sugarcrm main interface class
#
# This class is what is used to connect to and interact with the sugarcrm framework
#
class Sugarcrm:
    
    ## Constructor for Sugarcrm
    # @param self The object pointer
    # @param hostname String url of the sugarcrm framework
    # @param username Optional username to allow login upon construction
    # @param password Optional password to allow login upon construction
    #
    # The constructor requires a hostname url which may or may not include the port number,
    #   example: "http://www.example.com:8080/service/v2/rest.php"
    # The optional username and password removes the otherwise mandatory job of
    #   logging into the server after connection.
    def __init__(self, hostname, username=None, password=None):

        print "Connecting to: "+hostname

        ## @var connected
        # Boolean value to ensure that the object has connected and logged on properly to the server,
        #   may be unnecessary due to 'id' variable
        self.connected = 0

        ## @var id
        # String which holds the session id of the connection, requierd at every call after 'login'
        self._session = ""

        ## @var host
        # host url which is is called every time a request is made
        self.host = hostname

        ## @var last_call
        # The results of the last function called
        self.last_call = None

        ## @var quiet
        # The connection will print errors messages to stdout if false 
        self.quiet = False

        ## @var debug
        # TODO: implement debug flag which will print entire traceback if set, else it will only state error and die.
        self.debug = False

        # If the username and password are set, attempt to login
        if username and password:
            self.login(username, password)

        # Dynamically add the API methods to the object
        for method in ['get_user_id', 'get_user_team_id',
                        'get_available_modules', 'get_module_fields',
                        'get_entries_count', 'get_entry', 'get_entries',
                        'get_entry_list', 'set_entry', 'set_entries',
                        'set_relationship', 'set_relationships',
                        'get_relationships', 'get_server_info',
                        'set_note_attachment', 'get_note_attachment',
                        'set_document_revision', 'get_document_revision',
                        'search_by_module', 'get_report_entries', 'logout']:
            # Use this to be able to evaluate "method"
            def gen(method_name):
                def f(*args):
                    return self.sendRequest(method_name,
                                            [self._session] + list(args))
                return f
            self.__dict__[method] = gen(method)


    ## sendRequest
    # sends all requests to the server, should not need to be called explicitly by the user, but 
    #    rather by the other functions
    # @param method String of the method name being called
    # @param data parameters to the function being called, should be in a list sorted by order of items
    # @return dictionary object of server response
    def sendRequest(self, method, data):
        data = json.dumps(data)
        args = {'method': method, 'input_type': 'json', 'response_type' : 'json', 'rest_data' : data}
        params = urllib.urlencode(args)
        response = urllib.urlopen(self.host, params)
        response = response.read()
        try:
            result = json.loads(response)
        except TypeError:
            raise InvalidConnection
        except ValueError:
                raise InvalidConnection

        # check version of python, if lower than 2.7.2 strip unicode
        if sys.version_info < (2, 7, 2):
            result = stripUnicode(result)

        self.testForError(result)
        return result

    ## Test any returned object for an error
    # @param self the object pointer
    # @param obj the object which will be identified as an error or not
    # @return Sugarcrm.GeneralException if 'obj' is an error.
    # This function ought to be obsolete after creating classes which
    #   handle all returned objects from the server
    def testForError(self, obj):
        if isinstance(obj, dict) and obj.has_key("name"):
            if self.quiet == False:
                print "ERROR: %s:%s \n" % (obj["name"], obj["description"])
            raise GeneralException


    ## Login
    # Estabilsh connection to a server
    # @param username string of sugarcrm user
    # @param password plaintext string of the user's password
    def login(self, username, password):
        args = {'user_auth' : {'user_name' : username, 'password' : passencode(password)}}

        try:
            x = self.sendRequest('login', args)
        except GeneralException:
            raise InvalidLogin

        try:
            self._session = x["id"]
        except KeyError:
            raise InvalidConnection

        # If all goes well we've successfully connected
        self.connected = 1

    def relate(self, main, secondary):
        """Relate two SugarEntry objects."""

        self.set_relationship(main._module._name,
                            main['id'], secondary._module._name.lower(),
                            [secondary['id']])

## Creates md5 hash to send as a password
# @param password string to be encoded
# @return string md5-hex encoded string 
def passencode(password):
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

