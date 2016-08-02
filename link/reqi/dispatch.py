# -*- coding: utf-8 -*-

# --------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2016 Jonathan Labéjof <jonathan.labejof@gmail.com>
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

__all__ = ['Dispatcher']

from b3j0f.utils.version import OrderedDict

from .urils import getidentifiers, getname

from link.middleware import Middleware

from link.dbrequest.assignment import A
from link.dbrequest.comparison import CombinedCondition, C
from link.dbrequest.expression import E, F, CombinedExpression
from link.dbrequest.tree import Value

from uuid import uuid4 as uuid


_CTXNAME = '_ctxname'  #: ctx name for nodes.


def ctxname(node):
    """Get/Set a context name from input node.

    The context name is setted to the _CTXNAME attribute."""

    result = getattr(node, _CTXNAME, None)

    if result is None:

        if isinstance(node, E):
            result = node.name

            if isinstance(node, F):
                result = '{0}{1}'.format(
                    result, ','.join(map(ctxname, node.arguments))
                )

        else:
            result = uuid()

        setattr(node, _CTXNAME, result)

    return result


class Dispatcher(object):
    """In charge of dispatching requests."""

    __slots__ = ['systems']

    def __init__(self, systems, *args, **kwargs):
        """
        :param dict systems: systems by name to handle.
        """

        super(Dispatcher, self).__init__(*args, **kwargs)

        self.systems = systems

        self._loadsystems()

    def subdivise(self, node):
        """Subdivise input query to queries by systems.

        :param link.dbrequest.tree.Node node: node from where create system
            nodes.
        :return: nodes by system.
        :rtype: dict"""

        result = {}

        def updateresult(toupdate):

            for key in toupdate:
                result.setdefault(key, []).__radd__(toupdate[key])

        def registernode(node, **kwargs):

            system, schema, prop = getidentifiers(node.propname)
            newnode = A(prop, **kwargs)
            result.setdefault(system, []).append(newnode)

        system, _, _ = getidentifiers(node.name)

        if isinstance(node, A):
            registernode(unset=node.unset, val=node.val)

        elif isinstance(node, CombinedCondition):

            lsubdivise = self.subdivise(node.left)
            rsubdivise = self.subdivise(node.right)

            updateresult(lsubdivise)
            updateresult(rsubdivise)

        elif isinstance(node, C):

            value = node.value

            if not isinstance(value, Value):
                vsubdivise = self.subdivise(value)
                updateresult(vsubdivise)

            registernode(node, value=node.value, operator=node.operator)

        elif isinstance(node, (E, F, CombinedExpression)):

            if isinstance(node, F):

                for arg in node.arguments:
                    subdivision = self.subdivise(arg)
                    updateresult(subdivision)

                system, _, _ = getidentifiers(node.name)

                if system:
                    self.processnode(node)

            elif isinstance(node, E):

                pass

            raise NotImplementedError()

        return result

    def processnode(node, command=None):

        result = {}

        subdivision = self.subdivise(node)

        for name in subdivision:
            system = self.systems[name]
            sysresult = getattr(system, command)(node)

            result.update(sysresult)

        return result

    def getsystemswithschemas(
            self, system=None, schema=None, prop=None,
            defsystems=None, defschemas=None
    ):
        """Get systems and schemas corresponding to input system, schema and
        prop if not given.

        :param str system: system name.
        :param str schema: schema name.
        :param str prop: property name.
        :param list defsystems: default system names.
        :param list defschemas: default schema names.
        :return: corresponding (systems, schemas)
        :rtype: tuple
        """

        if defsystems is None:

            if defschemas is None:
                defsystems = list(self._schemaspersystem)

            else:
                defsystems = [
                    _system
                    for _schema in defschemas
                    for _system in self._systemsperschema[_schema]
                ]

        if defschemas is None:

            defschemas = [
                _schema
                for _system in defsystems
                for _schema in self._schemaspersystem[_system]
            ]

        if system is not None:
            systems = [system]

        if schema is not None:
            schemas = [schema]

        if prop is None:

            if schema is None:

                if system is None:
                    systems = defsystems
                    schemas = defschemas

                else:
                    schemas = [
                        schema for schema in self._schemaspersystem[system]
                        if schema in defschemas
                    ]

            else:
                if system is None:
                    systems = [
                        system for system in self._systemsperschema[schema]
                        if system in defsystems
                    ]

        else:

            if schema is None:

                if system is None:
                    schemas = [
                        schema
                        for schema in self._schemasperprop[prop]
                        if schema in defschemas
                    ]
                    systems = [
                        system
                        for schema in schemas
                        for system in self._systemsperschema[schema]
                        if system in defsystems
                    ]

                else:
                    schemas = [
                        schema
                        for schemas in self._schemasperprop[prop]
                        if schema in self._schemaspersystem[system]
                        and schema in defschemas
                    ]

            else:

                if system is None:
                    systems = [
                        system for system in self._systemsperschema[schema]
                        if system in defsystems
                    ]

        _removeoccurences(systems)
        _removeoccurences(schemas)

        return systems, schemas

    def queue(self):
        """Create a new Request Queue.

        :rtype: RequestQueue"""

        return RequestQueue(dispatcher=self)


def _removeoccurences(l):
    """Ensure to have one item value in removing multi-occurences from the end
    of the input list.

    :param list l: list from where remove multi-occurences.
    """

    if len(l) != len(set(l)):
        l.reverse()

        for item in list(l):
            for _ in range(1, l.count(item)):
                l.remove(item)

        l.reverse()
