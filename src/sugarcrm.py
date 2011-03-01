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
        # Boolean value to ensure that the object has connected and logged on properly to the server 
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
        
        # Fake login to make sure the host is valid
        '''try:
            x = self.login("BLANK", "FAKE")
        except InvalidLogin:
            pass
        except ValueError:
            raise InvalidConnection'''

        # If the username and password are set, attempt to login
        if username and password:
            self.login(username, password)

    ## Login function to estabilsh connection with a server
    # @param username string of sugarcrm user
    # @param password plaintext string of the users password
    def login(self, username, password):
        data = {'user_auth' : {'user_name' : username, 'password' : passencode(password)}}
        args = {'method': 'login', 'input_type': 'JSON', 'response_type' : 'JSON', 'rest_data' : data}
        params = urllib.urlencode(args)
        
        x = self.sendRequest(params)
        
        try:
            print "ID: "+x["id"]
            self.id = x["id"]
        except KeyError:
            raise InvalidConnection

        # If all goes well we've successfully connected
        self.connected = 1

    ## sendRequest sends all requests to the server
    # @param params parameters to the function being called, should be urlencoded (eg. params = urllib.urlencode(args))
    # @return dictionary object of server response 
    def sendRequest(self, params):
        response = urllib.urlopen(self.host, params)
        try:
            x = json.load(response)
        except TypeError:
            raise InvalidConnection
        
        try:
            self.testForError(x)
        except GeneralException:
            raise InvalidLogin
        return x
                
    ## Test any returned object for an error
    # @param self the object pointer
    # @param obj the object which will be identified as an error or not
    #
    # @return Sugarcrm.GeneralException if 'obj' is an error.
    # 
    # This function ought to be obsolete after creating classes which
    #   handle all returned objects from the server
    #
    def testForError(self, obj):
        if obj.has_key("name"):
            print "ERROR: "+obj["name"]+" : "+obj["description"]
            raise GeneralException

## Creates md5 hash to send as a password
# @param password string to be encoded
# @return string md5-hex encoded string 
def passencode(password):
    encode = hashlib.md5(password)
    result = encode.hexdigest()
    return result

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        a = sys.argv[1]
        if a == "test":
            "you typed test!"


