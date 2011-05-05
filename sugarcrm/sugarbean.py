#
#   sugarbean.py
#
#   KSU capstone project
#

## SugarEntryList
#	takes response from server and creates a nice python data structure
#
class SugarBean:
    
    ## SugarBean Constructor
    #  @param self the object pointer
    #  @param data server response to be parsed
    def __init__(self, data, connection = None):
#        print type(data)
        
        try:
            entry_list = data['entry_list']
        except KeyError:
            entry_list = data

        self.module = data['module_name']
        
        self.con = connection

        for (k,i) in entry_list['name_value_list'].iteritems():
			self.__dict__[k] = str(i['value'])

        try:
            self.id = data['id']
        except Exception:
            pass

    def __str__(self):
        return str(self.module)+':'+str(self.id)

    ## 

    def setValue(self, fields, values):
        if not self.con: raise InvalidConnection
        data = dict( (k,v) for (k,v) in zip(fields, values) )
        data['id'] = self.id
        x = self.con.set_entry(self.module, toNameValueList(data))
        return x
        
    def getFields(self, fields):
        if not self.con: raise InvalidConnection
        x = self.con.get_entry(self.module, self.id, select_fields = fields)
        print x

