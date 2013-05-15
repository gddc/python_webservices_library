from HTMLParser import HTMLParser

class SugarEntry:
    """Define an entry of a SugarCRM module."""
    
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


    def __unicode__(self):
        return "<SugarCRM %s entry '%s'>" % \
                    (self._module._name.rstrip('s'), self['name'])


    def __str__(self):
        return unicode(self).encode('utf-8')


    def __getitem__(self, field_name):
        """Return the value of the field 'field_name' of this SugarEntry.

        Keyword arguments:
        field_name -- name of the field to be retrieved
        """

        if field_name in self._module._fields.keys():
            try:
                return self._fields[field_name]
            except KeyError:
                if self['id'] == '':
                    # If this is a new entry, the 'id' field is yet undefined.
                    return ''
                else:
                    # Retrieve the field from the SugarCRM connection.
                    
                    q_str = "%s.id='%s'" % (self._module._table, self['id'])
                    res = self._module._connection.get_entry_list(
                                                    self._module._name, q_str,
                                                    '', 0, [field_name], 1, 0)

                    nvl = res['entry_list'][0]['name_value_list']
                    for attribute in nvl:
                        if attribute == field_name:
                            value = nvl[attribute]['value']
                            if value:
                                self._fields[attribute] = \
                                                HTMLParser().unescape(
                                                    nvl[attribute]['value'])
                            else:
                                self._fields[attribute] = ''

                            return self._fields[attribute]

        else:
            raise AttributeError


    def __setitem__(self, field_name, value):
        """Set the value of a field of this SugarEntry.

        Keyword arguments:
        field_name -- name of the field to be updated
        value -- new value for the field
        """

        if field_name in self._module._fields.keys():
            self._fields[field_name] = value
            if field_name not in self._dirty_fields:
                self._dirty_fields.append(field_name)
        else:
            raise AttributeError


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
            nv = {}
            nv['name'] = field
            nv['value'] = self[field]
            nvl.append(nv)
        
        # Use the API's set_entry to update the entry in SugarCRM.
        result = self._module._connection.set_entry(self._module._name, nvl)
        self._fields['id'] = result['id']
        self._dirty_fields = []

        return True


    def relate(self, related, relation=None):
        """Relate this SugarEntry with the one passed as a parameter.

        Keyword arguments:
        related -- the secondary SugarEntry object in the relationship
        relation -- the name of the relationship, if it can't be derived
        """

        self._module._connection.relate(self, related, relation)


    def get_related(self, module, relation=None):
        """Return the related entries in another module.

        Keyword arguments:
        module -- related SugarModule object
        """

        connection = self._module._connection
        if relation == None:
            relation = connection._get_relation_names(self._module, module)

        result = connection.get_relationships(self._module._name, self['id'],
                                              relation, '', ['id'])

        entries = []
        for elem in result['entry_list']:
            entry = SugarEntry(module)
            entry._fields['id'] = elem['id']
            entries.append(entry)

        return entries


