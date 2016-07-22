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

__STACK__ = '__STACK__'  #: stack of function by parents


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
                result += param.getsystems(*args, **kwargs)

        return result

    def _run(self, dispatcher, ctx, *args, **kwargs):

        result = super(Function, self)._run(
            dispatcher=dispatcher, ctx=ctx, *args, **kwargs
        )

        systems = self.getsystems()

        selfsystem = self.system
        __stack__ = ctx.setdefault(__STACK__, [])

        if not __stack__:
            __stack__.append(self)

        elif __stack__[-1].system != selfsystem:
            if selfsystem is None:
                __stack__.append(self)

            elif len(__stack__) > 1 and __stack__[-2] != selfsystem:
                __stack__.append(self)

        if systems:  # if execution might be delegated to a system

            ssys = set(systems)
            _systems = systems
            if len(ssys) > 1:

                for param in self.params:

                    if isinstance(param, Node):

                            # stop execution when systems is unique
                            if len(set(_systems)) <= 1:

                                if _systems:
                                    laststack = __stack__[-1]

                                    if (
                                            laststack.system is not None
                                            and laststack.system != systocall
                                    ):
                                        result = param.run(
                                            dispatcher=dispatcher, ctx=result
                                        )

                                break

                            else:
                                psystems = param.getsystems()
                                print('param', param.alias)
                                _systems = _systems[len(psystems):]
                                result = param.run(
                                    dispatcher=dispatcher, ctx=result
                                )

        if self is __stack__[-1]:
            __stack__.pop()

            if selfsystem is None:
                sname = systems[-1] if systems else None

            else:
                sname = selfsystem
            print(self.alias)
            if sname is None:
                result = self._prun(dispatcher=dispatcher, ctx=result)

            else:
                system = dispatcher.systems[sname]
                result = system.run(
                    nodes=[self], dispatcher=dispatcher, ctx=result
                )

        return result

    def _prun(self, dispatcher, ctx):
        """Function behavior."""

    def getctxname(self, *args, **kwargs):

        result = super(Function, self).getctxname(*args, **kwargs)

        if self.alias is None:

            for param in self.params:
                result = ''.join([result, ',', str(param)])

            result = ''.join(['(', result, ')'])

        return result


class PropertyFunction(Function):
    """Function which uses the first parameter such as an expression."""

    def _run(self, dispatcher, ctx):

        updateitems(
            ctx, self.params[0], self._convert
        )

    def _convert(self, item, node, ctx):

        raise NotImplementedError()
