"""
    Python data layer generator
    Author: Juan MAnuel Garcia <jmg.utn@gmail.com>
"""

import re

class ObjectMapper(object):

    SQL_PARAM_SYMBOL = "?"

    def __init__(self, entity):
        self.entity = entity

    def _get_pairs(self):
        return [(k,str(v)) for k,v in self.entity.__dict__.iteritems() if not k.startswith("_")]

    def _get_names(self):
        return [pair[0] for pair in self._get_pairs()]

    def _get_values(self):
        return [pair[1] for pair in self._get_pairs()]

    def _get_names_values(self):
        return self._get_names(), self._get_values()

    def insert(self):
        names, values = self._get_names_values()
        names = ",".join(names)
        params = ",".join(["'?'"] * len(values))
        return ("INSERT INTO %s(%s) VALUES (%s)" % (self.get_table(), names, params), ) + tuple(values)

    def update(self, id):
        pairs = self._get_pairs()
        fields = ", ".join(["%s = '%s'" % (k, self.SQL_PARAM_SYMBOL) for k,v in pairs])
        values = self._get_values()
        return ("UPDATE %s SET %s WHERE %s = %s" % (self.get_table(), fields, self.get_id(), self.SQL_PARAM_SYMBOL), ) + tuple(values) + (id, )

    def delete(self, id):
        return ("DELETE FROM %s WHERE %s = %s" % (self.get_table(), self.get_id(), self.SQL_PARAM_SYMBOL), id)

    def get_all(self, fields=[]):
        names = self._get_names()
        # ignore the invalid fileds
        fields = [k for k in fields if k in names]
        if fields:
            names = ", ".join(fields)
        else:
            names = ", ".join(names)
        return "SELECT %s FROM %s" % (names, self.get_table())

    def get_by_id(self, id, fields=[]):
        names = self._get_names()
        # ignore the invalid fileds
        fields = [k for k in fields if k in names]
        if fields:
            names = ", ".join(fields)
        else:
            names = ", ".join(names)
        return ("SELECT %s FROM %s WHERE %s = %s" % (names, self.get_table(), self.get_id(), self.SQL_PARAM_SYMBOL), id)

    #Overridables

    #You can Extend from this class and override the following methods in order to configurate
    #the table name and the id_name

    def get_table(self):
        # a more reasonable name
        return re.sub('((?<=[a-z])(?=[A-Z]))', '_', self.entity.__class__.__name__).lower()

    def get_id(self):
        return "id_%s" % re.sub('((?<=[a-z])(?=[A-Z]))', '_', self.entity.__class__.__name__).lower()
