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
class SugarEntryList (list):
    
    ## SugarEntryList Constructor
    #  @param self the object pointer
    #  @param data server response to be parsed
    def __init__(self, data, connection = None):
        if not isinstance(data, list):
            data = [data]

        for datum in data:
            if not isinstance(datum,dict): continue
            try:
                d = datum['entry_list']
            except KeyError:
                d = datum
    
            for i in d:
                self.append(SugarBean(i, connection))

    def __str__(self):
        result = [str(bean) for bean in self]
        return str(result)
        
    