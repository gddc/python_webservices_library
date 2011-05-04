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
    def __init__(self, data):
#        print type(data)
        
        try:
            entry_list = data['entry_list']
        except KeyError:
            entry_list = data

        self.module = data['module_name']
        

        for (k,i) in entry_list['name_value_list'].iteritems():
			self.__dict__[k] = str(i['value'])

        try:
            self.id = data['id']
        except Exception:
            pass

    def __str__(self):
        return str(self.module)+':'+str(self.id)
        
