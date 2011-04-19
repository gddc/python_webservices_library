#
#   sugarentrylist.py
#
#   KSU capstone project
#

import pprint
from sugarbean import SugarBean

## SugarEntryList
#	takes response from server and creates a nice python data structure
#
class SugarEntryList:
    
    ## SugarEntryList Constructor
    #  @param self the object pointer
    #  @param data server response to be parsed
    def __init__(self, data):
        try:
            d = data['entry_list']
        except KeyError:
            d = data
        self.data = []
        for i in d:
            self.data.append(SugarBean(i))

    def __iter__(self):
    	return self.data.__iter__()
    	
    def next(self):
        return self.data.next()

    def __str__(self):
        result = '['
        for bean in self.data:
            result += str(bean)+", "
        result += ']'
        return result
        
    def __getitem__(self, i):
        pass