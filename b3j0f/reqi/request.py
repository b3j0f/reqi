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

from link.dbrequest.tree import Node

from link.dbrequest.expression import CombinableExpression, CombinedExpression, E, F

class Request(object):
    """In charge of dispatching requests."""

    def __init__(self, scope, result, update, create, delete, *args, **kwargs):
        """
        :param Node(s) scope: scopes.
        :param Expression(s) result: E
        """

        super(Dispatcher, self).__init__(*args, **kwargs)

        self.systems = systems
        self.logger = logger
        self.schemasbysystems = {}

        for name in systems:
            system = systems[name]

            for schema in system.schemas:
                self.schemasbysystems.setdefault(schema.name, []).add(name)

    @staticmethod
    def _loadsystem(systems):

        result = {}, {}

        for system in systems:
            name = system.name
            dependencies = system.dependencies
            schemas = system.schemas

        return result

    def run(self, query):
        """Run input query."""

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

        for parts in request:  # start to process requests by systems

