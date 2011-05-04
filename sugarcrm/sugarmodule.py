#
#   sugarmodule.py
#
#   KSU capstone project
#

from sugarentrylist import SugarEntryList
from sugarbean import SugarBean

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

#        print "Creating module: "+module_name

        m_fields = sugarconnection.get_module_fields(module_name)
        self._cachedFields = m_fields['module_fields']

        for field_name in self._cachedFields:
            self.__dict__["find_by_"+field_name] = lambda q, n=field_name: self.get_entries_where("%s.%s = '%s' " % (self.name.lower(), n.lower(), q))

        self.relationships = m_fields['link_fields'].copy()

#        print "LINK_NAMES:", type(m_fields['link_fields'])
#        for link_name,i in m_fields['link_fields'].iteritems():
#            print link_name,i

        self.name = module_name
        self.prev_get_entries = {}

    def get_entry_with_id(self, id, fields = [], link_name_to_fields_array = []):
        raw_bean = self.connection.get_entry(self.name, id, fields, link_name_to_fields_array)
        print SugarBean(raw_bean)

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

    def get_relationships(self, bean, module, query = '', fields = []):
        if isinstance(bean, SugarBean): id = bean.id
        else: id = str(bean)
        link_name = ''
        if isinstance(module, Sugarmodule):
            for i,j in self.relationships.iteritems():
                if j['module'] == module.name: link_name = j['name']; break
        else: link_name = str(module).lower()

        if not link_name:
            raise InvalidRelationship

#  get_relationships(module, module_id, link_field_name, related_module = '', related_module_query = '', related_fields = [], related_module_link = [], delete = False):
        result = self.connection.get_relationships(module = self.name, module_id = id, link_field_name = link_name, related_module_query = fields)

#        print "result:",result
        return SugarEntryList(result)
