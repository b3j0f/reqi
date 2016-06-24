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

from b3j0f.utils.version import OrderedDict

from .utils import getcontext, updateref, copy

NAME_SEPARATOR = '/'


class Query(object):
    """In charge of dispatching requests."""

    __slots__ = ('dispatcher', 'scope', 'cond', 'read', 'updattes', 'logger')

    def __init__(
            self, dispatcher, scope, cond, read, updates, logger,
            *args, **kwargs
    ):

        super(Query, self).__init__(*args, **kwargs)

        self.dispatcher = dispatcher
        self.scope = scope
        self.cond = cond
        self.read = read
        self.updates = updates
        self.logger = logger

    def run(self, scope=None, cond=None, updates=None, read=None):
        """Run input query.

        :param list scope: list of Requests.
        :param list cond: list of Expressions.
        :param list read: list of Expressions.
        :param list create: list of Assignments.
        :param list update: list of Assignments.
        :return: read objects where keys are alias/prop name and values are
            model values.
        :rtype: list of dict."""

        if scope is not None:
            updateref(scope)
            systems, schemas = getcontext(scope)

        if cond is not None:
            updateref(cond)
            systems, schemas = getcontext(cond, systems, schemas)

        if updates is not None:
            updateref(updates)
            systems, schemas = getcontext(cond, systems, schemas)

        if read is not None:
            updateref(read)
            systems, schemas = getcontext(cond, systems, schemas)

        # A -> C -> D, E
        # B -> E

        commands = {}  # command by system names
        rcommands = OrderedDict()  # root commands

        vsystems = set()  # visited systems
        vschemas = set()  # visited schemas

        dsystems, dschemas = self.dispatcher.getdependencies(
            systems=systems, schemas=schemas
        )

        class Node(object):
            def __init__(self, system, dependencies=None, *args, **kwargs):
                super(Node, self).__init__(*args, **kwargs)
                self.system = system
                self.dependencies = dependencies

        for system in dsystems:

            dependencies = dsystems[system]

            if not dependencies:
                node = Node(system)
                commands[system] = rcommands[system] = node

            else:
                for dependency in dependencies:

                    if dependency in commands:  # is already registered
                        commands[dependency].dependencies.append(system)  # add system
                        continue

                    if dependency not in systems:  # not resolved by the request
                        self.logger.warning(
                            'Dependency {0} to {1} not given'.format(
                                dependency, system
                            )
                        )
                        rcommands[system] = commands[system] = Node(system)

                    else:
                        commands[dependency] = Node(system, node=[system])

        for name in rcommands:
            rcommand = rcommands[name]

            for request in requests:

                copiedrequest = copy(request, systems=[rcommand])

