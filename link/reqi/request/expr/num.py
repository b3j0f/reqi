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

from numbers import Number

from .base import Expression
from .func import Function

from .re import Re

from ..utils import updateitems


class Numerical(Function):
    """Base class for all numerical expressions."""

    def _convert(self, item):

        raise NotImplementedError()

    def _run(self, dispatcher, ctx):

        updateitems(ctx, self.params[0], self._convert)


class Add(Numerical):

    def _convert(self, item):

        item[self.params[0]] += self.params[1]

Expression.__add__ = lambda self, value: Add(params=[self, value])

Expression.__radd__ = lambda self, value: Add(params=[value, self])


class Sub(Numerical):

    def _convert(self, item):

        item[self.params[0]] -= self.params[1]

Expression.__sub__ = lambda self, value: Sub(params=[self, value])
Expression.__rsub__ = lambda self, value: Sub(params=[value, self])


class Mul(Numerical):

    def _convert(self, item):

        item[self.params[0]] *= self.params[1]

Expression.__mul__ = lambda self, value: Mul(params=[self, value])
Expression.__rmul__ = lambda self, value: Mul(params=[value, self])


class Div(Numerical):

    def _convert(self, item):

        item[self.params[0]] /= self.params[1]

Expression.__div__ = lambda self, value: Div(params=[self, value])
Expression.__rdiv__ = lambda self, value: Div(params=[value, self])


class Mod(Numerical):

    def _convert(self, item):

        item[self.params[0]] %= self.params[1]

Expression.__mod__ = lambda self, value: \
    (Mod if isinstance(value, Number) else Re)(params=[self, value])

Expression.__rmod__ = lambda self, value: \
    (Mod if isinstance(value, Number) else Re)(params=[value, self])

class Pow(Numerical):

    def _convert(self, item):

        item[self.params[0]] **= self.params[1]

Expression.__pow__ = lambda self, value: Pow(params=[self, value])
Expression.__rpow__ = lambda self, value: Pow(params=[value, self])


class LShift(Numerical):

    def _convert(self, item):

        item[self.params[0]] <<= self.params[1]

Expression.__lshift__ = lambda self, value: LShift(params=[self, value])

Expression.__rlshift__ = lambda self, value: LShift(params=[value, self])


class RShift(Numerical):

    def _convert(self, item):

        item[self.params[0]] >>= self.params[1]

Expression.__rshift__ = lambda self, value: RShift(params=[self, value])
Expression.__rrshift__ = lambda self, value: RShift(params=[value, self])


class LT(Numerical):

    def _convert(self, item):

        item[self.params[0]] = item[self.params[0]] < self.params[1]


class LTE(Numerical):

    def _convert(self, item):

        item[self.params[0]] = item[self.params[0]] <= self.params[1]

Expression.__lt__ = lambda self, value: LT(params=[self, value])
Expression.__le__ = lambda self, value: LTE(params=[self, value])


class EQ(Numerical):

    def _convert(self, item):

        item[self.params[0]] = item[self.params[0]] == self.params[1]


Expression.__eq__ = lambda self, value: EQ(params=[self, value])

class NEQ(Numerical):

    def _convert(self, item):

        item[self.params[0]] = item[self.params[0]] != self.params[1]

Expression.__ne__ = lambda self, value: NEQ(params=[self, value])


class GT(Numerical):

    def _convert(self, item):

        item[self.params[0]] = item[self.params[0]] > self.params[1]

Expression.__gt__ = lambda self, value: GT(params=[self, value])


class GTE(Numerical):

    def _convert(self, item):

        item[self.params[0]] = item[self.params[0]] >= self.params[1]

Expression.__ge__ = lambda self, value: GTE(params=[self, value])


class Bool(Numerical):

    def _convert(self, item):

        item[self.params[0]] = bool(item[self.params[0]])

Expression.__nonzero__ = lambda self: Bool(params=[self])
Expression.__bool__ = lambda self: Bool(params=[self])


class Oct(Numerical):

    def _convert(self, item):

        item[self.params[0]] = oct(item[self.params[0]])

Expression.__oct__ = lambda self: Oct(params=[self])


class Hex(Numerical):

    def _convert(self, item):

        item[self.params[0]] = hex(item[self.params[0]])

Expression.__hex__ = lambda self: Hex(params=[self])


class Int(Numerical):

    def _convert(self, item):

        item[self.params[0]] = int(item[self.params[0]])

Expression.__int__ = lambda self: Int(params=[self])


class Float(Numerical):

    def _convert(self, item):

        item[self.params[0]] = float(item[self.params[0]])

Expression.__float__ = lambda self: Float(params=[self])


class NEG(Numerical):

    def _convert(self, item):

        item[self.params[0]] = -item[self.params[0]]

Expression.__neg__ = lambda self: NEG(params=[self])


class Pos(Numerical):

    def _convert(self, item):

        item[self.params[0]] = +item[self.params[0]]

Expression.__pos__ = lambda self: Pos(params=[self])


class Abs(Numerical):

    def _convert(self, item):

        item[self.params[0]] = abs(item[self.params[0]])

Expression.__abs__ = lambda self: Abs(params=[self])


class Invert(Numerical):

    def _convert(self, item):

        if isinstance(item[self.params[0]], Number):
            item[self.params[0]] = ~item[self.params[0]]

        elif isinstance(item[self.params[0]], bool):
            item[self.params[0]] = not item[self.params[0]]

Expression.__invert__ = lambda self: Invert(params=[self])
