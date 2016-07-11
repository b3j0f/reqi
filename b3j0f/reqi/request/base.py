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

from uuid import uuid4 as uuid


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
        """Get all systems used by this node.

        :rtype: set
        """

        result = [] if self.system is None else [self.system]

        if self.ref is not None:

            systems = self.ref.getsystems()

            result = result + [
                system for system in systems if system not in result
            ]

        return result

    def run(self, dispatcher, ctx=None):
        """Run this node and return the context.

        :param b3j0f.reqi.dispatch.Dispatcher dispatcher: dispatcher to run.
        :param dict ctx: execution context.
        :return: execution context.
        :rtype: dict"""

        if ctx is None:
            ctx = {}

        systems = self.getsystems()

        sname = None

        if systems:

            if len(systems) == 1:
                sname = systems[0]
                system = dispatcher.systems[sname]
                ctx = system.run(nodes=[self], ctx=ctx)

            else:
                ctx = self._run(dispatcher=dispatcher, ctx=ctx)

        else:
            ctx.setdefault(self.getctxname(), []).append(self)

        self.ctx = ctx

        return self.ctx

    def _run(self, dispatcher, ctx):

        raise NotImplementedError()

    def __str__(self):

        return self.getctxname()

    def __repr__(self):

        return self.getctxname()
