#
#   sugarmodule.py
#
#   KSU capstone project
#

from sugarentrylist import SugarEntryList
from sugarbean import SugarBean
import sugarcrm

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
            self.__dict__["find_by_"+field_name] = lambda q, _n=field_name: self.get_entries_where("%s.%s = '%s' " % (self.name.lower(), _n.lower(), q))

        self.relationships = m_fields['link_fields'].copy()

        for link in self.relationships.values():
            self.__dict__['link_to_'+link['name']] = lambda bean, fields = [], query = '', _a = link: self.get_relationships(bean = bean, module = _a['name'], query = query, fields = fields)

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

    ## get_relationships
    #   Retrieves the relationships between a specified bean and module 
    #
    def get_relationships(self, bean, module, query = '', fields = []):
        if isinstance(bean, SugarBean): ids = [bean.id]
        elif isinstance(bean, list): ids = [b.id for b in bean]
        else: ids = [str(bean)]
        link_name = ''
        if isinstance(module, Sugarmodule):
            for i,j in self.relationships.iteritems():
                if j['module'] == module.name: link_name = j['name']; break
        else: link_name = str(module).lower()

        if not link_name:
            raise InvalidRelationship

        if len(ids) == 1:
            result = self.connection.get_relationships(module = self.name, module_id = ids[0], link_field_name = link_name, related_module_query = fields)
        else:
            result = [self.connection.get_relationships(module = self.name, module_id = id, link_field_name = link_name, related_module_query = fields) for id in ids];
        return SugarEntryList(result)

    ## info
    # print a list of attributes describing the module
    #
    def info(self):
        result  = 'name : %s\n' % (self.name)
        result += '_'*6+'Fields'+'_'*18+'\t____Relationships'+'_'*10+'\n'
        zzz = lambda s1,s2 : '%-29s\t%s\n' % ({True: s1, False: ''}[s1 != None], {True: s2, False: ''}[s2 != None])
        for x in map(zzz, self._cachedFields, self.relationships) : result += x
        print result

    def newBean(self, fields, values = None):
        if isinstance(fields,dict): data = fields
        else: data = dict( (f,v) for f,v in zip(fields, values) )
        x = self.connection.set_entry(self.name, sugarcrm.toNameValueList(data) )
        return x

if __name__ == "__main__":
    pass
