#
#   sugarmodule.py
#
#   KSU capstone project
#

import sugarentrylist

## Sugarmodule
#  Abstract class which has ability to access and modify all entries in
#    a sugarcrm module.
class Sugarmodule:

	## Sugarmodule constructor
	# @param sugarconnection A sugarcrm connection
    # @param module_name string of the correct module name
    # @return object encapsulating various data connections
    def __init__(self, sugarconnection, module_name):
        if (sugarconnection.connected == 0):
			raise GeneralException()

        self.connection = sugarconnection

        print "Creating module: "+module_name

        fields = sugarconnection.get_module_fields(module_name)
        self.name = module_name
        
        for (field, i) in fields['module_fields'].iteritems():
#            print field+" = "+str(i)
 #           print ""
    		pass

    def get_entry_with_id(self, id):
        pass

    def get_entries_where(self, query, fields = []):
    	result = self.connection.get_entry_list(self.name,query, "", "", fields)
    	return sugarentrylist.SugarEntryList(result)

