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

"""Specification of the node object."""

__all__ = ['Node']

from uuid import uuid4 as uuid

from inspect import getmembers, isroutine


ALIAS = 'ALIAS'  #: ctx key used to store alias


class Node(object):
    """Elementary part of request.

    An elementary part is linked to a system and/or a schema.
    For easying its use, it can be referee to an alias, and be refered by
    another node using the attribute `ref`."""

    __slots__ = ['alias', 'ctx']

    def __init__(self, alias=None, ref=None, ctx=None, *args, **kwargs):
        """
        :param str alias: alias name for the couple system/schema.
        :param dict ctx: node execution context.
        """

        super(Node, self).__init__(*args, **kwargs)

        self.alias = alias
        self.ctx = ctx

    def getctxname(self):
        """Get node context name.

        :rtype: str
        """

        result = None

        if self.alias:
            result = self.alias

        else:
            result = str(self)

        return result

    def elements(self, ctx):
        """Return elements from ctx corresponding to this node.

        :param dict ctx: execution context.
        :return: elements corresponding to this.
        :rtype: collections.Iterable"""

        ctxname = self.getctxname()

        return ctx.get(ctxname)

    def getsystems(self):
        """Get all systems accessible from this.

        :rtype: set
        """

        return []

    def run(self, dispatcher, ctx=None):
        """Run this node and return the context.

        :param b3j0f.reqi.dispatch.Dispatcher dispatcher: dispatcher to run.
        :param dict ctx: execution context.
        :return: execution context.
        :rtype: dict"""

        if ctx is None:
            ctx = {}

        ctx = self._run(dispatcher=dispatcher, ctx=ctx) or ctx

        self.ctx = ctx

        return ctx

    def _run(self, dispatcher, ctx):
        """Custom run method.

        :param b3j0f.reqi.dispatch.Dispatcher dispatcher: dispatcher to process.
        :param dict ctx: execution context.
        :return: ctx."""

        if self.alias:
            if ALIAS not in ctx:
                ctx[ALIAS] = {}
            ctx[ALIAS][self.alias] = self

        return ctx


class Ref(Node):
    """Node reference to an aliased node."""

    __slot__ = ['alias', 'ref']

    def __init__(self, alias=None, ref=None, *args, **kwargs):
        """
        :param str alias: alias name from to where update ref.
        :param Node ref: reference to another node.
        """

        super(Ref, self).__init__(*args, **kwargs)

        self.alias = alias
        self.ref = ref

    def getsystems(self, *args, **kwargs):

        result = super(Ref, self).getsystems(*args, **kwargs)

        if self.ref is not None:

            systems = self.ref.getsystems()

            result += [
                system for system in systems if system not in result
            ]

        return result

    def _run(self, dispatcher, ctx, *args, **kwargs):

        if self.ref is None:
            if ALIAS in ctx and self.alias in ctx[ALIAS]:
                self.ref = ctx[ALIAS][self.alias]

            else:
                raise ValueError('Alias {0} is missing.'.format(self.alias))

        return ctx

    def getctxname(self, *args, **kwargs):

        if self.ref is None:
            result = super(Ref, self).getctxname(*args, **kwargs)

        else:
            result = self.ref.getctxname(*args, **kwargs)

        return result
