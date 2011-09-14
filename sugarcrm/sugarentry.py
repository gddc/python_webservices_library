
class SugarEntry:
    """Defines an entry of a SugarCRM module."""
    
    def __init__(self, module):
        """Represents a new or an existing entry."""

        # Keep a reference to the parent module.
        self._module = module
        
        # Keep a mapping 'field_name' => value for every valid field retrieved.
        self._fields = {}
        self._dirty_fields = []
        
        # Make sure that the 'id' field is always defined.
        if 'id' not in self._fields.keys():
            self._fields['id'] = ''


    def __str__(self):
        return "<SugarCRM %s entry '%s'>" % \
                    (self._module._name.rstrip('s'), self['name'])


    def __getitem__(self, field_name):
        """Return the value of the field 'field_name' of this SugarEntry."""

#        if field_name in [item['name'] for item in self._module._fields]:
        # CAMBIAR! XXXXXXXXXXXXXXXXXX
        if field_name in self._module._fields.keys():
            try:
                return self._fields[field_name]
            except KeyError:
                if self['id'] == '':
                    # If this is a new entry, the 'id' field is yet undefined.
                    return ''
                else:
                    # Retrieve the field from the SugarCRM connection.
                    
                    q_str = self._module._name.lower() + \
                                ".id='%s'" % self['id']
                    res = self._module._connection.get_entry_list(
                            self._module._name,
                            q_str, '', 0, [field_name], 1, 0)
                    for attribute in res['entry_list'][0]['name_value_list']:
                        if attribute == field_name:
                            # CAMBIAR! XXXXXXXXXXXXXXXXXX
                            self._fields[attribute] = res['entry_list'][0]['name_value_list'][attribute]['value']
                            return res['entry_list'][0]['name_value_list'][attribute]['value']

        else:
            raise AttributeError


    def __setitem__(self, field_name, value):
        """Set the value of the field 'field_name' of this SugarEntry."""

        if field_name in self._module._fields.keys():
            self._fields[field_name] = value
            if field_name not in self._dirty_fields:
                self._dirty_fields.append(field_name)
        else:
            raise AttributeError


    def save(self):
        """Saves this entry in SugarCRM through SOAP. If the 'id' field is
        blank, it creates a new entry and sets the 'id' value."""
        
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


    def relate(self, related):
        """Relate this SugarEntry with the one passed as a parameter."""

        self._module._connection.relate(self, related)


    def get_related(self, module):
        """Return the related entries in the module 'module_name'"""

        connection = self._module._connection
        result = connection.get_relationships(self._module._name,
                                                self['id'], module._name.lower())

        entries = []
        for elem in result['entry_list']:
#            entry = SugarEntry(connection.modules[module_name])
            entry = SugarEntry(module)
            entry._fields['id'] = elem['id']
            entries.append(entry)

        return entries


