#
#   sugarcrm.py
#
#   KSU capstone project
#

import urllib, hashlib, json

class GeneralException(Exception): pass
class InvalidConnection(Exception): pass
class InvalidLogin(Exception): pass

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
        self.id = ""

        ## @var host
        # host url which is is called every time a request is made
        self.host = hostname

        ## @var last_call
        # The results of the last function called
        self.last_call = 0

        ## @var quiet
        # The connection will print errors messages to stdout if false 
        self.quiet = True

        ## @var debug
        # 
        self.debug = False
        
        # Fake login to make sure the host is valid
        try:
            x = self.login("BLANK", "FAKE")
        except InvalidLogin:
            pass
        except ValueError:
            raise InvalidConnection

        self.quiet = False

        # If the username and password are set, attempt to login
        if username and password:
            self.login(username, password)

    ## sendRequest sends all requests to the server
    # @param params parameters to the function being called,
    #     should be urlencoded (eg. params = urllib.urlencode(args))
    # @return dictionary object of server response 
    def sendRequest(self, method, data):
        args = {'method': method, 'input_type': 'JSON', 'response_type' : 'JSON', 'rest_data' : data}
#        params = urllib.urlencode(args)
        params = str(args)
        print str(type(params))
        response = urllib.urlopen(self.host, params)
        try:
            result = json.load(response)
        except TypeError:
            raise InvalidConnection

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
    	if isinstance(obj, dict):
			if obj.has_key("name"):
				if self.quiet == False:
					print "ERROR: "+obj["name"]+" : "+obj["description"]+"\n"
				raise GeneralException


    ## Login function to estabilsh connection with a server
    # @param username string of sugarcrm user
    # @param password plaintext string of the users password
    def login(self, username, password):
        args = {'user_auth' : {'user_name' : username, 'password' : passencode(password)}}

        try:
            x = self.sendRequest('login', args)
        except GeneralException:
            raise InvalidLogin

        try:
            self.id = x["id"]
        except KeyError:
            raise InvalidConnection

        # If all goes well we've successfully connected
        self.connected = 1
            
    ## get_user_id Returns the ID of the user who is logged into the server
    # @return string of the user's id
    def get_user_id(self):
    	args = {'session' : self.id}
        result = self.sendRequest('get_user_id', args)
        return result

    ## get_user_team_id
    # Retrieves the ID of the default team of the user who is logged into the current session.
    def get_user_team_id(self):
        args = {'session':self.id}
        result = self.sendRequest('get_user_team_id', args)
        return result


    ## get_module_fields Retrieves variable definitions for fields of the specified sugarbean
    # @param module_name
    # @param fields Optional list of fields
    # @return 
    def get_module_fields(self, module_name, fields = []):
        args = {'session':self.id, 'module_name':module_name, 'fields':fields}
        result = self.sendRequest('get_module_fields', args)
        return result

    def get_entries_count(self, module_name, query = "", deleted = False):
    	args = {'session':self.id, 'module_name':module_name, 'query':query, 'deleted':{True:1,False:0}[deleted]}
        result = self.sendRequest('get_entries_count', args)
        return result



    def seamless_login(self):
        args = {'session':self.id, 'module_name':module_name, 'fields':fields}
        return self.sendRequest('seamless_login', args)

    def set_note_attachment(self, note):
        args = {'session':self.id, 'module_name':module_name, 'fields':fields}
        return self.sendRequest('set_note_attachement', args)


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

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        a = sys.argv[1]
        if a == "test":
            "you typed test!"

