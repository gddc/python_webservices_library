
import itertools

from sugarentry import SugarEntry


class SugarModule:
    """Defines a SugarCRM module.

    This is used to perform module related tasks, such as queries and creating
    new entries.
    """
    
    def __init__(self, connection, name):
        """Constructor for SugarCRM module.

        Keyword arguments:
        connection -- Sugarcrm object to connect to a server
        name -- name of SugarCRM module that this class will represent
        """
        self._name = name
        self._connection = connection
        
        # Get the module fields through SugarCRM API.
        result = self._connection.get_module_fields(self._name)

        self._fields = result['module_fields']
        
        # In order to ensure that queries target the correct tables.
        # Necessary to replace a call to self._name.lower() which
        # was resulting in broken modules (ProductTemplates, etc).
        self._table = result['table_name']
        # If there aren't relationships the result here is an empty list
        # which has no copy method.  Fixing to provide an empty default.
        self._relationships = (result['link_fields'] or {}).copy()


    def _search(self, query_str, start = 0, total = 20, fields = []):
        """Return a list of SugarEntry objects that match the query.

        Keyword arguments:
        query_str -- SQL query to be passed to the API
        start -- Record offset to start from
        total -- Maximum number of results to return
        fields -- If set, return only the specified fields
        """

        if 'id' not in fields:
            fields.append('id')
        
        entry_list = []
        count = 0
        offset = 0
        while count < total:
            result = self._connection.get_entry_list(self._name,
                            query_str, '', start + offset, fields,
                            total - count, 0)
            if result['result_count'] == 0:
                break
            else:
                offset += result['result_count']
                for i in range(result['result_count']):
                    
                    new_entry = SugarEntry(self)

                    nvl = result['entry_list'][i]['name_value_list']
                    for attribute in nvl:
                        new_entry._fields[attribute] = nvl[attribute]['value']
            
                    # SugarCRM seems broken, because it retrieves several copies
                    #  of the same contact for every opportunity related with
                    #  it. Check to make sure we don't return duplicate entries.
                    if new_entry['id'] not in [entry['id']
                                                for entry in entry_list]:
                        entry_list.append(new_entry)
                        count += 1
        
        return entry_list


    def query(self):
        """
        Return a QueryList object for this SugarModule.

        Initially, it describes all the objects in the module. One can find
        specific objects by calling 'filter' and 'exclude' on the returned
        object.
        """

        return QueryList(self)


class QueryList:
    """Query a SugarCRM module for specific entries."""

    def __init__(self, module, query = ''):
        """Constructor for QueryList.

        Keyword arguments:
        module -- SugarModule object to query
        query -- SQL query to be passed to the API
        """

        self._module = module
        self._query = query
        self._next_items = []
        self._offset = 0


    def __iter__(self):
        return self


    def next(self):
        try:
            item = self._next_items[0]
            self._next_items = self._next_items[1:]
            return item
        except IndexError:
            self._next_items = self._module._search(self._query,
                                                start = self._offset, total = 5)
            self._offset += len(self._next_items)
            if len(self._next_items) == 0:
                raise StopIteration
            else:
                return self.next()

    def __getitem__(self, index):
        try:
            return next(itertools.islice(self, index, index + 1))
        except TypeError:
            return list(itertools.islice(self, index.start, index.stop,
                                            index.step))


    def _build_query(self, **query):
        """Build the API query string.
        """

        q_str = ''
        for key in query.keys():
            # Get the field and the operator from the query
            key_field, key_sep, key_oper = key.partition('__')
            if q_str != '':
                q_str += ' AND '

            if_cstm = ''
            if key_field.endswith('_c'):
                if_cstm = '_cstm'

            field = self._module._name.lower() + if_cstm + '.' + key_field

            if key_oper == 'exact':
                q_str += '%s = "%s"' % (field, query[key])
            elif key_oper == 'contains':
                q_str += '%s LIKE "%%%s%%"' % (field, query[key])
            elif key_oper == 'in':
                q_str += '%s IN (' % field
                for elem in query[key]:
                    q_str += "'%s'," % elem
                q_str = q_str.rstrip(',')
                q_str += ')'
            elif key_oper == 'gt':
                q_str += '%s > "%s"' % (field, query[key])
            elif key_oper == 'gte':
                q_str += '%s >= "%s"' % (field, query[key])
            elif key_oper == 'lt':
                q_str += '%s < "%s"' % (field, query[key])
            elif key_oper == 'lte':
                q_str += '%s <= "%s"' % (field, query[key])
            else:
                raise LookupError('Unsupported operator')

        return q_str


    def filter(self, **query):
        """Filter this QueryList, returning a new QueryList.

        Keyword arguments:
        query -- kwargs dictionary where the filters are specified:
            The keys should be some of the module's field names, suffixed by
            '__' and one of the following operators: 'exact', 'contains', 'in',
            'gt', 'gte', 'lt' or 'lte'. When the operator is 'in', the
            corresponding value MUST be a list.
        """

        if self._query != '':
            query = '(%s) AND (%s)' % (self._query, self._build_query(**query))
        else:
            query = self._build_query(**query)

        return QueryList(self._module, query)


    def exclude(self, **query):
        """Filter this QueryList, returning a new QueryList, as in filter(),
        but excluding the entries that match the query.
        """

        if self._query != '':
            query = '(%s) AND NOT (%s)' % (self._query, self._build_query(**query))
        else:
            query = 'NOT (%s)' % self._build_query(**query)

        return QueryList(self._module, query)


    def __len__(self):
        result = self._module._connection.get_entries_count(
                        self._module._name, self._query, 0)
        return int(result['result_count'])

