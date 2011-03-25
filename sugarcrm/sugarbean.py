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
        for (k,i) in data['name_value_list'].iteritems():
			self.__dict__[k] = str(i['value'])
