#
#   sugarcrm.py
#
#   KSU capstone project
#

import urllib, hashlib, json

class GeneralException(Exception): pass
class InvalidConnection(Exception): pass
class InvalidLogin(Exception): pass
##

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

        ## @var host
        # host url which is is called every time a request is made
        self.host = hostname
        
        # Fake login to make sure the host is valid
        try:
            x = self.login("BLANK", "FAKE")
        except InvalidLogin:
            pass
        except IOError:
            raise InvalidConnection

        self.connected = 1

        # If the username and password are set, attempt to login
        if username and password:
            self.login(username, password)

    def login(self, username, password):
        print "trying username: "+username+", password: "+password
        data = {'user_auth' : {'user_name' : username, 'password' : passencode(password)}}
        args = {'method': 'login', 'input_type': 'JSON', 'response_type' : 'JSON', 'rest_data' : data}
        params = urllib.urlencode(args)
        response = urllib.urlopen(self.host, params)
        try:
            x = json.load(response)
        except TypeError:
            raise InvalidConnection

        try:
            self.testForError(x)
        except GeneralException:
            raise InvalidLogin

        try:
            print "ID: "+x["id"]
            self.id = x["id"]
        except KeyError:
            raise InvalidConnection

    def testForError(self, obj):
        if obj.has_key("name"):
            print "ERROR: "+obj["name"]+" : "+obj["description"]
            raise GeneralException
        

def passencode(password):
	encode = hashlib.md5("class123")
       	result = encode.hexdigest()
	return result

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        a = sys.argv[1]
        print "argument: "+a

