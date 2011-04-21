#
#   sugarmodule.py
#
#   KSU capstone project
#

from sugarentrylist import SugarEntryList
import sugarbean

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

        self._cachedFields = sugarconnection.get_module_fields(module_name)['module_fields']

        for field_name in self._cachedFields:
            self.__dict__["find_by_"+field_name] = lambda q, n=field_name: self.get_entries_where("%s.%s = '%s' " % (self.name.lower(), n.lower(), q))

        self.name = module_name
        self.prev_get_entries = {}

    def get_entry_with_id(self, id, fields = [], link_name_to_fields_array = []):
        raw_bean = self.connection.get_entry(self.name, id, fields, link_name_to_fields_array)
        print sugarbean.SugarBean(raw_bean)

    def get_entries(self, ids, fields = [], link_name_to_fields_array = []):
        raw_bean_list = self.connection.get_entries(self.name, ids, fields, link_name_to_fields_array)
        return sugarentrylist.SugarEntryList(raw_bean_list)

    def get_entries_where(self, query, fields = [], offset = 0):
        result = self.connection.get_entry_list( self.name, query, "", "", fields)
        self.prev_get_entries['next_offset'] = result['next_offset']
        self.prev_get_entries['query'] = query
        self.prev_get_entries['fields'] = fields
        return SugarEntryList(result)

    def get_fields(self):
        if self._cachedFields:
            return self._cachedFields
        fields = self.sugarconnection.get_module_fields(self.name)
        self._cachedFields = fields
        return fields
        
    def get_next(self):
        result = self.get_entries_where(self.prev_get_entries['query'], self.prev_get_entries['fields'], self.prev_get_entries['next_offset'])
        return result
        
    def get_all_entries_where(self, query = '', fields = []):
        result = self.get_entries_where(query, fields)
        while True:
            result.data.extend(self.get_next().data)
            if not self.prev_get_entries['next_offset']: break
        return result
