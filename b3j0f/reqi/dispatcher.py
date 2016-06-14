# -*- coding: utf-8 -*-

# --------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2014 Jonathan Labéjof <jonathan.labejof@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# --------------------------------------------------------------------

"""Specification of the dispatcher interface."""

from b3j0f.schema import Schema
from b3j0f.schema.prop import SchemaProperty

from re import compile as re_compile

NAME_SEPARATOR = '/'


class Dispatcher(object):
    """In charge of dispatching requests."""

    class QueryAnalyzer(object):

        def __init__(
                self, dispatcher, *args, **kwargs
        ):

            super(QueryAnalyzer, self).__init__(*args, **kwargs)

            self.query = query
            self.dispatcher = dispatcher
            self.alias = {}

    def __init__(self, systems, *args, **kwargs):
        """
        :param list systems: systems to handle.
        """

        super(Dispatcher, self).__init__(*args, **kwargs)

        self.systems = systems

    def getsystemswithschemas(
            self, system=None, schema=None, prop=None,
            defaultsystems=None, defaultschemas=None
    ):
        """Get systems and schemas corresponding to input system, schema and
        prop if not given.

        :param str system: system name.
        :param str schema: schema name.
        :param str prop: property name.
        :param list defaultsystems: default system names.
        :param list defaultschemas: default schema names.
        :return: corresponding (systems, schemas)
        :rtype: tuple
        """

        if defaultsystems is None:
            if defaultschemas is None:
                defaultsystems = list(self._schemasbysystem)

            else:
                defaultsystems = [
                    system
                    for schema in defaultschemas
                    for system in self._systemsbyschema[schema]
                ]

        if defaultschemas is None:
            defaultschemas = [
                schema
                for system in defaultsystems
                for schema in self._schemasbysystem[system]
            ]

        if system is not None:
            systems = [system]

        if schema is not None:
            schemas = [schema]

        if prop is None:
            if schema is None:
                if system is None:
                    systems = defaultsystems
                    schemas = defaultschemas

                else:
                    schemas = [
                        schema for schema in self._schemasbysystem[system]
                        if schema in defaultschemas
                    ]

            else:
                if system is None:
                    systems = [
                        system for system in self._systemsbyschema[schema]
                        if system in defaultsystems
                    ]

        else:
            if schema is None:
                if system is None:
                    schemas = [
                        schema
                        for schema in self._schemasbyprop[prop]
                        if schema in defaultschemas
                    ]
                    systems = [
                        system
                        for schema in schemas
                        for system in self._systemsbyschema[schema]
                            if system in defaultsystems
                    ]

                else:
                    schemas = [
                        schema
                        for schemas in self._schemasbyprop[prop]
                            if schema in self._schemasbysystem[system]
                                and schema in defaultschemas
                    ]

            else:
                if system is None:
                    systems = [
                        system for system in self._systemsbyschema[schema]
                        if system in defaultsystems
                    ]

        _removeoccurences(systems)
        _removeoccurences(schemas)

        return systems, schemas

    def getdependencysystemswithschemas(systems=None, schemas=None):

        result = []

        if props is None:
            props = set()

        elif isinstance(props, string_types):
            props = set([props])

        else:
            props = set(props)

        if schemas is None:
            schemas = set()

        elif isinstance(schemas, string_types):
            schemas = set([schemas])

        else:
            props = set(props)

        if systems is None:
            systems = set()

        elif isinstance(systems, string_types):
            systems = set([systems])

        else:
            systems = set(systems)

        for prop in props
            if prop not in self._propsperschemas:
                raise ValueError('Unknown property name {0}'.format(prop))

            schema |= set(self._propsperschemas[prop])

        for schema in schemas:
            if schema not in self._schemasdependencies:
                raise ValueError('Unknown schema name {0}'.format(schema))

            result |= set(self._schemasdependencies[schema])
            systems |= set(self._schemasdependencies[schema])

        for system in systems:


        if system is not None:
            result += self._systemdependencies[system.name]

        return result

    def getsysschpro(self, name):

        parts = name.split(NAME_SEPARATOR)

        len_parts = len(parts)

        sys, sch, pro = None, None, None

        if len_parts == 1:
            pro = parts[0]

        elif len_parts == 2:
            sch, pro = tuple(parts)

        elif len_parts == 3:
            sys, sch, pro = tuple(parts)

        if sch is None:
            if pro not in self._schemasbyprop:
                raise ValueError(pro)
            self._schemasbyprop[pro]

        return sys, sch, pro

    def _loadsystems(self):
        """Load self systems, schemas, properties and dimensions."""

        self._dependenciesbysystem = {}
        self._systemsbyschema = {}
        self._schemasbysystem = {}
        self._schemasbyprop = {}
        self._propsbyschema = {}
        self._dimensionsbysystem = {}
        self._systemsbydimension = {}

        systems = list(self.systems)

        i = 0

        while i < len(systems):

            system = systems[i]
            i+= 1

            sname = system.name

            # add dependencies
            dependencies = system.dependencies()

            for dependency in dependencies:
                if dependency not in systems:
                    systems.append(dependency)

            self._dependenciesbysystem[system] = dependencies

            # add schemas
            for schema in system.schemas():
                suid = schema.uid
                self._systemsbyschema.setdefault(suid, {})[sname] = system
                self._schemasbysystem.setdefault(sname, {})[suid] = schema

                # add properties
                for pname in schema:
                    prop = schema[prop]
                    self._propsbyschema.setdefault(suid, {})[pname] = prop
                    self._schemasbyprop.setdefault(pname, {})[suid] = schema

                    if isinstance(prop, SchemaProperty)

            # add dimensions
            for dimension in system.dimensions():
                dname = dimension.name
                self._dimensionsbysystem.setdefault(sname, {})[dname] = dimension
                self._systemsbydimension.setdefault(dname, {})[sname] = system

    def run(
            self, scope=None, filter=None, read=None, create=None, update=None,
            delete=None
    ):
        """Run input query.

        :param Node(s) scope:
        :param C(s) filter:
        :param Expression(s) read:
        :param A(s) create:
        :param A(s) update;"""

        dsystem = query.system  # get default system

        scopespersystem = {}

        for pname in ['scope', 'select', 'where', 'update', 'create', 'delete']:

            parts = getattr(query, pname)

            for part in parts:
                psystem = part.system
                if psystem is None:
                    psystem = dsystem

                if psystem is None:
                    raise RuntimeError()

                scopespersystem.setdefault(psystem)


def _removeoccurences(l):
    """Ensure to have one item value in removing multi-occurences from the end
    of the input list.

    :param list l: list from where remove multi-occurences.
    """

    if len(l) != len(set(l)):
        l.reverse()
        for item in list(l):
            for _ in range(1, l.count(l)):
                l.remove(l)

        l.reverse()
