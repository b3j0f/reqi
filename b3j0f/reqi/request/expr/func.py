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

"""Specification of the function object."""

__all__ = ['Function', 'PropertyFunction']

from .base import Expression
from ..base import Node
from ..utils import updateitems


class Function(Expression):
    """Function request object.

    The function name is the expression property name."""

    __slots__ = ['params', 'rtype']

    def __init__(self, params=None, rtype=None, *args, **kwargs):
        """
        :param list params: list of values.
        :param type rtype: return type.
        :param dict ctx: context which will contain all expression result after
            this running. expression results are registered by schema names.
        """

        super(Function, self).__init__(*args, **kwargs)

        self.params = [] if params is None else params
        self.rtype = rtype

    def getsystems(self, *args, **kwargs):

        result = super(Function, self).getsystems(*args, **kwargs)

        for param in self.params:
            if isinstance(param, Node):
                result += [
                    sys for sys in param.getsystems(*args, **kwargs)
                    if sys not in result
                ]

        return result

    def _run(self, dispatcher, ctx, *args, **kwargs):

        ctx = super(Function, self)._run(
            dispatcher=dispatcher, ctx=ctx, *args, **kwargs
        )

        systems = self.getsystems()

        if systems:

            if len(systems) == 1:
                system = dispatcher.systems[systems[0]]

                ctx = system.run(node=self, ctx=ctx)

            else:
                for param in self.params:
                    if isinstance(param, Node):
                        ctx = param.run(
                            dispatcher=dispatcher, ctx=ctx, optimize=False
                        )

        else:
            ctx = self.__run(ctx=ctx)

        return ctx

    def __run(self, ctx):
        """Function behavior."""

        raise NotImplementedError()

    def getctxname(self, *args, **kwargs):

        result = super(Function, self).getctxname(*args, **kwargs)

        ''.join(result, '(')

        for param in self.params:
            result = ''.join(result, ',', str(param))

        ''.join(result, '(')

        return result


class PropertyFunction(Function):
    """Function which uses the first parameter such as an expression."""

    def _run(self, dispatcher, ctx):

        updateitems(
            ctx, self.params[0], self._convert
        )

    def _convert(self, item, node, ctx):

        raise NotImplementedError()
