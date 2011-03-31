#
#   sugarcrm.py
#
#   KSU capstone project
#

import urllib, hashlib, json, sys
from sugar_error import *

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
        self.last_call = None

        ## @var quiet
        # The connection will print errors messages to stdout if false 
        self.quiet = True

        ## @var debug
        # TODO: implement debug flag which will print entire traceback if set, else it will only state error and die.
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

    ## sendRequest
    # sends all requests to the server, should not need to be called explicitly by the user, but 
    #    rather by the other functions
    # @param method String of the method name being called
    # @param data parameters to the function being called, should be in a list sorted by order of items
    # @return dictionary object of server response
    def sendRequest(self, method, data):
        args = {'method': method, 'input_type': 'JSON', 'response_type' : 'JSON', 'rest_data' : data}
        params = urllib.urlencode(args)
        response = urllib.urlopen(self.host, params)	
        try:
            result = json.load(response)
        except TypeError:
            raise InvalidConnection
            
        # check version of python, if lower than 2.7.2 strip unicode
        if sys.version_info[0] < 2 or (sys.version_info[0] == 2 and (sys.version_info[1] <= 7 or (sys.version_info[1] == 7 and sys.version_info[2] < 2))):
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
            self.id = x["id"]
        except KeyError:
            raise InvalidConnection

        # If all goes well we've successfully connected
        self.connected = 1
            
    ## get_user_id
    # Returns the ID of the user who is logged into the server
    # @return string of the user's id
    def get_user_id(self):
    	args = {"session":self.id}
        result = self.sendRequest('get_user_id', args)
        return result

    ## get_user_team_id
    # Retrieves the ID of the default team of the user who is logged into the current session.
    # @return string of user's team id
    def get_user_team_id(self):
        args = [self.id]
        result = self.sendRequest('get_user_team_id', args)
        return result

    ## get_available_modules
    # Retrieves the list of modules available to the current user logged into the system.
    # @returns list of module names
    def get_available_modules(self):
        data = [self.id]
        return self.sendRequest('get_available_modules', data)

    ## get_module_fields
    # Retrieves variable definitions (vardefs) for fields of the specified SugarBean.
    # @param module_name which Module to request fields
    # @param fields Optional list of fields
    # @return list of fields
    def get_module_fields(self, module_name, fields = []):
        args = [self.id, module_name, fields]
        result = self.sendRequest('get_module_fields', args)
        return result

    ## get_entries_count
    # Retrieves the specified number of records in a module.
    # @param module_name Module containing entries to count
	# @param query Optional query to impose conditions on which entries are counted
	# @param deleted Optional parameter to specify whether to count deleted entries
	# @return integer count of number 
    def get_entries_count(self, module_name, query = "", deleted = False):
        args = [self.id, module_name, query, {True:1,False:0}[deleted]]
        result = self.sendRequest('get_entries_count', args)
        return result

    ## get_entry
    # Retrieves a single SugarBean based on ID.
    # @param module_name The name of the module from which to retrieve records.
    # @param id The SugarBean's ID
    # @param select_fields optional list of fields to be returned
    # @param link_name_to_fields_array A list of link names and the fields to be returned for each link name.
    # @return A list of entries and list of relationships
    def get_entry(self, module_name, id, select_fields = [], link_name_to_fields_array = []):
        args = [self.id, module_name, id, select_fields, link_name_to_fields_array]
        return self.sendRequest('get_entry', args)

	## get_entries
	# Retrieves a list of SugarBeans based on the specified IDs.
    # @param module_name The name of the module from which to retrieve records.
    # @param id The SugarBean's ID
    # @param select_fields optional list of fields to be returned
    # @param link_name_to_fields_array A list of link names and the fields to be returned for each link name.
    # @return Array containing list of entries specified and a list of their link data
    def get_entries(self, module_name, ids, select_fields, link_name_to_fields_array):
        args = [self.id, module_name, select_fields, link_name_to_fields_array]
        return self.sendRequest('get_entries', args)

	## get_entry_list
	# Retrieves a list of SugarBeans.
    # @param module_name The name of the module from which to retrieve records.
    # @param query The SQL WHERE clause without the word "where".
    # @param order_by The SQL ORDER BY clause without the phrase "order by".
    # @param offset The record offset from which to start.
    # @param select_fields Optional Array of fields to include in result
    # @param link_name_to_fields_array A list of link names and the fields to be returned for each link name.
    # @param max_results The maximum number of results to return.
	# @param deleted Set True to include deleted records
	# @return [result_count, next_offset, entry_list, relationship_list] 
    def get_entry_list(self, module_name, query ="", order_by ="", offset = 0, select_fields = [], link_name_to_fields_array = []):
        args = [self.id, module_name, query, order_by, offset, select_fields, link_name_to_fields_array]
        return self.sendRequest('get_entry_list', args)

    ## set_entry
    # Creates or updates a SugarBean.
    # @param module_name module being updated
    # @param list of names and values to describe a new entry in module
    def set_entry(self, module_name, name_value_list):
        args = [self.id, module_name, name_value_list]
        return self.sendRequest('set_entry', args)

    ## set_entries
    # Creates or updates a list of SugarBeans.
    # @param module_name module being updated
    # @param name_value_lists list of arrays referring to created/updated entries
    def set_entries(self,module_name, name_value_lists):
        args = [self.id, module_name, name_value_lists]
        return self.sendRequest('set_entries', args)

    ## set_relationship
    # Sets a single relationship between two SugarBeans.
    # @param module_name The name of the module from which to retrieve records
    # @param module_id The ID of sepcified module bean
    # @param link_field_name The name of the field related to the other module.
    # @param related_ids Array of related records
    # @return number of entries created, failed and deleted
    def set_relationship(self, module_name, module_id, link_field_name, related_ids):
        data = [self.id, module_name, module_id, link_field_name, related_ids]
        x = self.sendRequest('set_relationship',data)
        return x

    ## set_relationships
    # Sets multiple relationships between two SugarBeans.
    # @param module_name The name of the module from which to retrieve records.
    # @param module_ids The ID of sepcified module bean
    # @param link_field_names The name of the field related to the other module.
    # @param related_id Array of related records' IDs
    # @return number of entries created, failed and deleted
    def set_relationships(self, module_names, module_ids, link_field_names, related_id):
        data = [self.id, module_name, module_id, link_field_name, related_ids]
        x = self.sendRequest('set_relationship',data)
        return x

    ## get_relationships
    # Retrieves a collection of beans that are related to the specified bean and, optionally, returns relationship data.
    # @param module The name of the module from which to retrieve records.
    # @param module_id The ID of the specified module bean.
    # @param link_field_name The relationship name of the linked field from which to return records.
    # @param related_module The portion of the WHERE clause from the SQL statement used to find the related items.
    # @param related_feilds The related fields to be returned.
    # @param related_module_link For every related bean returned, specify link field names to field information.
    # @param deleted To exclude deleted records.
    # @return records of entry list, and relationship list
    def get_relationships(self, module, module_id, link_field_name, related_module, related_fields = [], related_module_link = [], delete = False):
        args = [self.id, module, module_id, link_field_name, related_module, related_fields, related_module_link, {True:1, False:0}[delete]]
        x = self.sendRequest('get_relationships', args)
        return x

    ## get_server_info
    # Returns server information such as version, flavor, and gmt_time.
    # @return Sugar edition such as Enterprise, Professional, or Community Edition. The version number of the Sugar application that is running on the server. gmt_time The current GMT time on the server in Y-m-d H:i:s format.
    def get_server_info(self):
        return self.sendRequest('get_server_info','')

    ## logout
    # Logs out of the sugar user session
    def logout(self):
       args = [self.id]
       self.sendRequest('logout', args)
       self.connected = 0
       self.last_call = None

    def seamless_login(self):
#        args = {'session':self.id, 'module_name':module_name, 'fields':fields}
        args = [self.id, module_name, fields]
        return self.sendRequest('seamless_login', args)

    def set_note_attachment(self, note):
#        args = {'session':self.id, 'module_name':module_name, 'fields':fields}
        args = [self.id, module_name, fields]
        return self.sendRequest('set_note_attachement', args)

    ## get_note_attachment
    #Retrieves an attachment from a note.
    #@param session The ID of the session
    #@param id The id of the note
    #@return The id of the note
    # containing the attachment, the file name of the attachment, the
    # binary contents of the file, the id of the module to which this note
    # is releated, the name of the module to which this note is related.
    def get_note_attachment(self, id):
        args = [self.id, id]
        result = self.sendRequest('get_note_attachment', args)
        return result

    ##set_document_revision
    #Sets a new revision for a document
    #@param session The ID of the session
    #@param document_revision The document ID, document name,
    # the revision number, the file name of the attachment,
    # the binary contents of the file
    #@param id The document revision ID
    #@return The ID of the document revision
    def set_document_revision(self, document_revision, id):
        args = [self.id, document_revision, id]
        result = self.sendRequest('set_document_revision', args)
        return result

    ##get_document_revision
    #Allows an authenticated user with the appropriate permission to
    #download a document.
    #@param id The ID of the revised document
    #@return The ID of the document revision containing the
    #attachment, The name of the revised document, the revision value,
    #the file name of the attachment, the binary contents of the file
    def get_document_revision(self, id):
        args =[self.id, id]
        result =self.sendRequest('get_document_revision', args)
        return result
    
    ##search_by_module
    #Returns the ID, module_name, and fields for the specified modules
    #as specified in the search string.
    #@param search_string The string to search for
    #@param modules The modules to query
    #@param offset The specified offset in the query
    #@param max_results The maximum number of records to return
    #@return The records returned by the search results
    def search_by_module(self, search_string, modules, offset, max_result):
        args =[self.id, search_string, modules, modules, offset, max_result]
        result =self.sendRequest('search_by_module', args)
        return result

    def module(self, module_name):
        return Sugarmodule(module_name)


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

def toNameValueList(obj):
	if isinstance(obj, dict):
		return list( {"name" : name, "value" : value} for (name, value) in obj.items() )

def fromNameValueList(obj):
	#might want to make this a error instead of returning none
	if not isinstance(obj, list):
		return None

	result = {}

	for nvpair in obj:
		result[nvpair["name"]] = nvpair["value"]
	return result

if __name__ == "__main__":
    pass

