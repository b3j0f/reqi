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

DEFAULT_OPTIMIZE = True  #: default value for optimization
ALIAS = 'ALIAS'  #: ctx key used to store alias


class Node(object):
    """Elementary part of request.

    An elementary part is linked to a system and/or a schema.
    For easying its use, it can be referee to an alias, and be refered by
    another node using the attribute `ref`."""

    __slots__ = ['system', 'schema', 'alias', 'ref', 'ctx']

    def __init__(
            self, system=None, schema=None, alias=None, ref=None, ctx=None,
            *args, **kwargs
    ):
        """
        :param str system: system name.
        :param str schema: schema name.
        :param str alias: alias name for the couple system/schema.
        :param ref: alias reference. Alias name or reference to a request.
        :param dict ctx: node execution context.
        """

        super(Node, self).__init__(*args, **kwargs)

        self.system = system
        self.schema = schema
        self.alias = alias
        self.ref = ref
        self.ctx = ctx

    def updateref(self, ctx):
        """Update this node related to input ctx.

        Optimizations are updating of references.

        :raises: KeyError if ref is not None and corresponding alias does not
        exist."""

        if self.alias is not None:
            ctx.setdefault(ALIAS, {})[self.alias] = self

        if ALIAS in ctx and self.ref in ctx[ALIAS]:
            self.ref = ctx[ALIAS][self.ref]

    def getctxname(self):
        """Get node context name.

        :rtype: str
        """

        result = None

        if self.alias:
            result = self.alias

        elif self.ref is None:
            if self.system:
                result = self.system
                if self.schema:
                    result = ''.join([result, '.', self.schema])

            elif self.schema:
                result = self.schema

        return result

    def getsystems(self):
        """Get all this system names.

        :rtype: set
        """

        result = [] if self.system is None else [self.system]

        if self.ref is not None:

            systems = self.ref.getsystems()

            result += [
                system for system in systems if system not in result
            ]

        return result

    def copy(self, system):
        """Copy this node in keeping sub nodes where system equals input system
        or None.

        :param str system: system name.
        """

        kwargs = {}

        for slot in self.__slots__:

            kwargs[slot] = getattr(self, slot)

        result = type(self)(**kwargs)

        return result

    def run(self, dispatcher, ctx=None, optimize=DEFAULT_OPTIMIZE):
        """Run this node and return the context.

        :param b3j0f.reqi.dispatch.Dispatcher dispatcher: dispatcher to run.
        :param dict ctx: execution context.
        :param bool optimize: if True (default), optimize this node.
        :return: execution context.
        :rtype: dict"""

        if ctx is None:
            ctx = {}

        if optimize:
            self.updateref(ctx=ctx)

        ctx = self._run(dispatcher=dispatcher, ctx=ctx)

        self.ctx = ctx

        return ctx

    def _run(self, dispatcher, ctx):
        """Custom run method."""

        if self.system is not None:
            system = dispatcher.systems[self.system]
            ctx = system.run(nodes=[self], ctx=ctx)

        return ctx
