from HTMLParser import HTMLParser
from collections import defaultdict
from itertools import count

class SugarEntry:
    """Define an entry of a SugarCRM module."""
    _hashes = defaultdict(count(1).next)
    

    def __init__(self, module):
        """Represents a new or an existing entry.

        Keyword arguments:
        module -- SugarModule object the entry belongs to
        """

        # Keep a reference to the parent module.
        self._module = module

        # Keep a mapping 'field_name' => value for every valid field retrieved.
        self._fields = {}
        self._dirty_fields = []

        # Make sure that the 'id' field is always defined.
        if 'id' not in self._fields.keys():
            self._fields['id'] = ''
            
            
    def __hash__(self):
        return self._hashes['%s-%s' % (self._module._name, self['id'])] 


    def __unicode__(self):
        return "<SugarCRM %s entry '%s'>" % \
                    (self._module._name.rstrip('s'), self['name'])


    def __str__(self):
        return unicode(self).encode('utf-8')


    def _retrieve(self, fieldlist, force = False):
        qstring = "%s.id = '%s'" % (self._module._table, self['id'])
        if not force:
            fieldlist = set(fieldlist) - set(self._fields.keys())
        if not fieldlist:
            return
        res = self._module._connection.get_entry_list(self._module._name,
                                                      qstring, '', 0,
                                                      list(fieldlist), 1, 0)
        if not res['entry_list'] or not res['entry_list'][0]['name_value_list']:
            for field in fieldlist:
                self[field] = ''
            return
        for prop, obj in res['entry_list'][0]['name_value_list'].items():
            if obj['value']:
                self[prop] = HTMLParser().unescape(obj['value'])
            else:
                self[prop] = ''


    def __getitem__(self, field_name):
        """Return the value of the field 'field_name' of this SugarEntry.

        Keyword arguments:
        field_name -- name of the field to be retrieved. Supports a tuple
                      of fields, in which case the return is a tuple.
        """

        if isinstance(field_name, tuple):
            self._retrieve(field_name)
            return tuple(self[n] for n in field_name)

        if field_name not in self._module._fields:
            raise AttributeError("Invalid field '%s'" % field_name)

        if field_name not in self._fields:
            self._retrieve([field_name])
        return self._fields[field_name]


    def __setitem__(self, field_name, value):
        """Set the value of a field of this SugarEntry.

        Keyword arguments:
        field_name -- name of the field to be updated
        value -- new value for the field
        """

        if field_name in self._module._fields:
            self._fields[field_name] = value
            if field_name not in self._dirty_fields:
                self._dirty_fields.append(field_name)
        else:
            raise AttributeError("Invalid field '%s'" % field_name)


    def save(self):
        """Save this entry in the SugarCRM server.

        If the 'id' field is blank, it creates a new entry and sets the
        'id' value.
        """

        # If 'id' wasn't blank, it's added to the list of dirty fields; this
        # way the entry will be updated in the SugarCRM connection.
        if self['id'] != '':
            self._dirty_fields.append('id')

        # nvl is the name_value_list, which has the list of attributes.
        nvl = []
        for field in set(self._dirty_fields):
            # Define an individual name_value record.
            nv = dict(name = field, value = self[field])
            nvl.append(nv)

        # Use the API's set_entry to update the entry in SugarCRM.
        result = self._module._connection.set_entry(self._module._name, nvl)
        try:
            self._fields['id'] = result['id']
        except:
            print result
        self._dirty_fields = []

        return True


    def relate(self, *related, **kwargs):
        """
		Relate this SugarEntry with other Sugar Entries.

		Positional Arguments:
		  related -- Secondary SugarEntry Object(s) to relate to this entry.
		Keyword arguments:
          relateby -> iterable of relationship names.  Should match the
                      length of *secondary.  Defaults to secondary
                      module table names (appropriate for most
                      predefined relationships).
        """

        self._module._connection.relate(self, *related, **kwargs)


    def get_related(self, module, fields = None):
        """Return the related entries in another module.

        Keyword arguments:
        module -- related SugarModule object
        """

        if fields is None:
            fields = ['id']
        connection = self._module._connection
        # Accomodate retrieval of modules by name.
        if isinstance(module, basestring):
            module = connection[module]
        result = connection.get_relationships(self._module._name, self['id'],
                                              module._name.lower(), '', fields)
        entries = []
        for elem in result['entry_list']:
            entry = SugarEntry(module)
            for name, field in elem['name_value_list'].items():
                entry._fields[name] = field['value']
            entries.append(entry)

        return entries


