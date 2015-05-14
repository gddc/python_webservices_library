from __future__ import print_function
import six
from six.moves.html_parser import HTMLParser
from collections import defaultdict
from itertools import count

HTMLP = HTMLParser()

class SugarEntry:
    """Define an entry of a SugarCRM module."""
    _hashes = defaultdict(count(1).next if hasattr(count(1), 'next') else count(1).__next__)


    def __init__(self, module, fmap = None):
        """Represents a new or an existing entry.

        Keyword arguments:
        module -- SugarModule object the entry belongs to
        """

        # Keep a reference to the parent module.
        self._module = module

        # Keep a mapping 'field_name' => value for every valid field retrieved.
        self._fields = {}
        self._dirty_fields = []

        # Allow initial fields in constructor.
        if fmap is not None:
            self._fields.update(fmap)

        # Make sure that the 'id' field is always defined.
        if 'id' not in list(self._fields.keys()):
            self._fields['id'] = ''

    def __hash__(self):
        return self._hashes['%s-%s' % (self._module._name, self['id'])]

    def __unicode__(self):
        return "<SugarCRM %s entry '%s'>" % \
                    (self._module._name.rstrip('s'), self['name'])

    def __str__(self):
        return str(self).encode('utf-8')

    def __contains__(self, key):
        return key in self._module._fields

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
        for prop, obj in list(res['entry_list'][0]['name_value_list'].items()):
            if obj['value']:
                self[prop] = HTMLP.unescape(obj['value'])
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
            print(result)
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

    def get_related(self, module, fields = None, relateby = None, links_to_fields = None):
        """Return the related entries in another module.

        Keyword arguments:
        module -- related SugarModule object
        relateby -- custom relationship name (defaults to module.lower())
        links_to_fields -- Allows retrieval of related fields from addtional related modules for retrieved records.
        """

        if fields is None:
            fields = ['id']
        if links_to_fields is None:
            links_to_fields = []
        connection = self._module._connection
        # Accomodate retrieval of modules by name.
        if isinstance(module, six.string_types):
            module = connection[module]
        result = connection.get_relationships(self._module._name,
                                              self['id'],
                                              relateby or module._name.lower(),
                                              '',  # Where clause placeholder.
                                              fields,
                                              links_to_fields)
        entries = []
        for idx, elem in enumerate(result['entry_list']):
            entry = SugarEntry(module)
            for name, field in list(elem['name_value_list'].items()):
                val = field['value']
                entry._fields[name] = HTMLP.unescape(val) if isinstance(val, basestring) else val
                entry.related_beans = defaultdict(list)
#                 try:
                linked = result['relationship_list'][idx]
                for relmod in linked:
                    for record in relmod['records']:
                        relentry = {}
                        for fname, fmap in record.items():
                            rfield = fmap['value']
                            relentry[fname] = HTMLP.unescape(rfield) if isinstance(rfield, six.string_types) else val
                        entry.related_beans[relmod['name']].append(relentry)
#                 except:
#                     pass

            entries.append(entry)

        return entries

