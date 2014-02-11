import itertools
from HTMLParser import HTMLParser
from sugarentry import SugarEntry
from collections import deque

HTMLP = HTMLParser()

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
        if result is None:
            return

        self._fields = result['module_fields']

        # In order to ensure that queries target the correct tables.
        # Necessary to replace a call to self._name.lower() which
        # was resulting in broken modules (ProductTemplates, etc).
        self._table = result['table_name']
        # If there aren't relationships the result here is an empty list
        # which has no copy method.  Fixing to provide an empty default.
        self._relationships = (result['link_fields'] or {}).copy()


    def _search(self, query_str, start = 0, total = 20, fields = None, query = None):
        """
          Return a dictionary of records as well as pertinent query
          statistics.


        Keyword arguments:
        query_str -- SQL query to be passed to the API
        start -- Record offset to start from
        total -- Maximum number of results to return
        fields -- If set, return only the specified fields
        query -- The actual query class instance.
        """

        if fields is None:
            fields = []
        if 'id' not in fields:
            fields.append('id')
        if 'name' not in fields:
            fields.append('name')

        result = {}

        entry_list = []
        offset = 0
        while len(entry_list) < total:
            resp_data = self._connection.get_entry_list(self._name,
                            query_str, '', start + offset, fields,
                            total - len(entry_list), 0)
            if resp_data['total_count']:
                result['total'] = int(resp_data['total_count'], 10)
            else:
                result['total'] = 0
            if resp_data['result_count'] == 0:
                result['offset'] = 0
                break

            offset = result['offset'] = resp_data['next_offset']

            for record in resp_data['entry_list']:
                entry = SugarEntry(self)
                for key, obj in record['name_value_list'].items():
                    entry[key] = HTMLP.unescape(obj['value'])
                entry_list.append(entry)

            if resp_data['result_count'] == int(resp_data['total_count'], 10):
                break

        result['entries'] = entry_list
        return result


    def query(self, fields = None):
        """
        Return a QueryList object for this SugarModule.

        Initially, it describes all the objects in the module. One can find
        specific objects by calling 'filter' and 'exclude' on the returned
        object.
        """

        return QueryList(self, fields = fields)

    def search(self, value):
        """
        Attempt to search for matching records for this module.
        """

        resp_data = self._connection.search_by_module(value, [self._name])
        results = []
        for mod_results in resp_data['entry_list']:
            if mod_results['name'] != self._name:
                continue
            for record in mod_results['records']:
                entry = SugarEntry(self)
                for key, obj in record.items():
                    entry[key] = HTMLP.unescape(obj['value'])
                results.append(entry)
        return results



class QueryList:
    """Query a SugarCRM module for specific entries."""

    def __init__(self, module, query = '', fields = None):
        """Constructor for QueryList.

        Keyword arguments:
        module -- SugarModule object to query
        query -- SQL query to be passed to the API
        """

        self._module = module
        self._query = query
        self._next_items = deque()
        self._offset = 0
        self._total = -1
        self._sent = 0
        self._fields = fields

    def __iter__(self):
        return self

    def next(self):
        if self._sent == self._total:
            raise StopIteration
        try:
            entry = self._next_items.popleft()
            self._sent += 1
            return entry
        except IndexError:
            result = self._module._search(self._query, self._offset, 5, self._fields)
            self._total = result['total']
            self._offset = result['offset']
            self._next_items.extend(result['entries'])
            return self.next()

    def __getitem__(self, index):
        try:
            return next(itertools.islice(self, index, index + 1))
        except TypeError:
            return list(itertools.islice(self,
                                         index.start,
                                         index.stop,
                                         index.step))


    def _build_query(self, **query):
        """Build the API query string.
        """

        q_str = ''
        for key, val in query.items():
            # Get the field and the operator from the query
            key_field, key_sep, key_oper = key.partition('__')
            if q_str != '':
                q_str += ' AND '

            if_cstm = ''
            if key_field.endswith('_c'):
                if_cstm = '_cstm'

            field = self._module._name.lower() + if_cstm + '.' + key_field

            if key_oper in ('exact', 'eq'):
                q_str += '%s = "%s"' % (field, val)
            elif key_oper == 'contains':
                q_str += '%s LIKE "%%%s%%"' % (field, val)
            elif key_oper == 'sw':
                q_str += '%s LIKE "%s%%"' % (field, val)
            elif key_oper == 'in':
                q_str += '%s IN (' % field
                for elem in val:
                    q_str += "'%s'," % elem
                q_str = q_str.rstrip(',')
                q_str += ')'
            elif key_oper == 'gt':
                q_str += '%s > "%s"' % (field, val)
            elif key_oper == 'gte':
                q_str += '%s >= "%s"' % (field, val)
            elif key_oper == 'lt':
                q_str += '%s < "%s"' % (field, val)
            elif key_oper == 'lte':
                q_str += '%s <= "%s"' % (field, val)
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

        return QueryList(self._module, query, fields = self._fields)


    def exclude(self, **query):
        """Filter this QueryList, returning a new QueryList, as in filter(),
        but excluding the entries that match the query.
        """

        if self._query != '':
            query = '(%s) AND NOT (%s)' % (self._query, self._build_query(**query))
        else:
            query = 'NOT (%s)' % self._build_query(**query)

        return QueryList(self._module, query, fields = self._fields)


    def __len__(self):
        if self._total == -1:
            result = self._module._connection.get_entries_count(self._module._name, self._query, 0)

            self._total = int(result['result_count'], 10)
        return self._total
