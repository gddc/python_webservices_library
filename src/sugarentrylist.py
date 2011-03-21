#
#   sugarentrylist.py
#
#   KSU capstone project
#

import pprint
import sugarbean

## SugarEntryList
#	takes response from server and creates a nice python data structure
#
class SugarEntryList:
    
    ## SugarEntryList Constructor
    #  @param self the object pointer
    #  @param data server response to be parsed
    def __init__(self, data):
        self.data = []
    	for i in data['entry_list']:
			self.data.append(sugarbean.SugarBean(i))

    def __iter__(self):
    	return self.data.__iter__()
    	
    def next(self):
        return self.data.next()
