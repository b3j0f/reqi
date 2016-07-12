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

"""Specification of the request object."""

__all__ = ['And', 'Or']

from ..base import Node
from .base import Expression
from .func import Function


class And(Function):
    """Function dedicated to process conjonction of expressions."""

    def _run(self, dispatcher, ctx, *args, **kwargs):

        systems = self.getsystems()

        for sysname in systems:

            system = dispatcher.systems[sysname]

            cnode = self.copy(system=system)

            ctx = system.run(node=cnode, dispatcher=dispatcher, ctx=ctx)

        self.ctx = ctx

        return self.ctx

Expression.__and__ = lambda self, value: And(params=[self, value])
Expression.__rand__ = lambda self, value: And(params=[value, self])


class Or(Function):
    """Function dedicated to process union of expressions."""

    def _run(self, dispatcher, ctx, *args, **kwargs):

        params = list(self.params)

        while params:
            param = params.pop(params)

            if isinstance(param, Function):

                if isinstance(param, Or):
                    params = params[0:1] + param.params + params[1:]

                pctx = ctx.copy()
                param.run(dispatcher=dispatcher, ctx=pctx)

            for mname in pctx:
                if mname in self.ctx:
                    self.ctx[mname] += pctx[mname]

                else:
                    self.ctx[mname] = pctx[mname]

Expression.__or__ = lambda self, value: Or(params=[self, value])
Expression.__ror__ = lambda self, value: Or(params=[value, self])
