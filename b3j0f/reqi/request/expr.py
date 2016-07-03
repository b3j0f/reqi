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

"""Specification of the request object."""

from .base import Node

from numbers import Number

from time import time

from re import match

def updatecond(ctx, schema, cond):
    if schema in ctx:
        ctx[schema] = [item for item in ctx[schema] if cond(item)]
        return True

    else:
        return False

def updateitem(ctx, schema, update):
    if schema in ctx:
        ctx[schema] = [update(item) for item in ctx[schema]]
        return True

    else:
        return False


# list of default function names (prop is None).
# existing property
EXISTS = 'exists'

class Exists(Func):
    def _run(self):
        updatecond(self.ctx, self.schema, lambda item: self.prop in item)

# regex functions
LIKE = 'like'

class Like(Func):
    def _run(self):
        updatecond(self.ctx, self.schema, lambda item: match(item))

# boolean functions
AND = '&&'
OR = '||'
XOR = '^^'
NOT = '!'

# binary functions
BAND = '&'
BOR = '|'
BXOR = '^'

# time functions
NOW = 'now'

class Now(Func):
    def _run(self):
        self.ctx['NOW'] = time()

# array functions
COUNT = 'count'

class Count(Func):
    def _run(self):
        self.ctx['COUNT({0})'.format(self.schema)] = len(self.ctx[self.schema])

IN = 'in'

class In(Func):
    def _run(self):
        updatecond(self.ctx, self.schema, lambda item: item[self.prop] in self.params[0])

REVERSE = 'reverse'

class Reverse(Func):
    def _run(self):
        self.ctx[self.schema] = reversed(self.ctx[self.schema])

GETITEM = 'getitem'

SETITEM = 'setitem'

class SetItem(Func):
    def _run(self):
        updateitem(self.ctx, self.schema, lambda item: item.__setitem__(self.params[0], self.params[1]))

DELITEM = 'delitem'

class DelItem(Func):
    def _run(self):
        updateitem(self.ctx, self.schema, lambda item: item.__delitem__(self.params[0]))

GETSLICE = 'getslice'

SETSLICE = 'setslice'

class SetSlice(Func):
    def _run(self):
        updateitem(self.ctx, self.schema, lambda item: item.__setslice__(self.params[0], self.params[1], self.params[2]))

DELSLICE = 'delslice'

class DelSlice(Func):
    def _run(self):
        updateitem(self.ctx, self.schema, lambda item: item.__delslice__[self.params[0], self.params[1]])

# numerical functions
ADD = '+'
SUB = '-'
MUL = '*'
DIV = '/'
FLOORDIV = '//'
MOD = '%'
DIVMOD = '/%'
POW = '**'
LSHIFT = '<<'
RSHIFT = '>>'
LT = '<'
LTE = '<='
EQ = '='
NEQ = '!='
GTE = '>='
GT = '>'
NEG = '--'
POS = '++'
ABS = 'abs'
INVERT = '~'
FLOOR = 'floor'
INT = 'int'
FLOAT = 'float'
OCT = 'oct'
HEX = 'hex'


class Expression(Node):
    """Expression request object."""

    __slots__ = ['prop', 'offset', 'limit', 'groupby', 'sort']

    def __init__(
            self, prop, offset=None, limit=None, groupby=None, sort=None,
            *args, **kwargs
    ):
        """
        :param str prop: property name.
        :param int offset: minimal offset to get. 0 by default.
        :param int limit: maximal number of elements to get. Infinite by default.
        :param list groupby: list of property names to group by.
        :param list sort: list of property name by (de/a)scendant order to sort.
        """

        super(Expression, self).__init__(*args, **kwargs)

        self.prop = prop
        self.offset = offset
        self.limit = limit
        self.groupby = groupby
        self.sort = sort

    # boolean functions
    def __and__(self, value):
        return Func(prop=AND, params=[self, value])

    def __rand__(self, value):
        return Func(prop=AND, params=[value, self])

    def __or__(self, value):
        return Func(prop=OR, params=[self, value])

    def __ror__(self, value):
        return Func(prop=OR, params=[value, self])

    def __xor__(self, value):
        return Func(prop=XOR, params=[self, value])

    def __rxor__(self, value):
        return Func(prop=XOR, params=[value, self])

    def __invert__(self):
        return Func(prop=NOT, params=[self])

    # array functions
    def __len__(self):
        return Func(prop=COUNT, params=[self])

    def __contains__(self, item):
        return Func(prop=IN, params=[item, self])

    def __reversed__(self):
        return Func(prop=REVERSE, params=[self])

    def __getitem__(self, key):
        return Func(prop=GETITEM, params=[self, key])

    def __setitem__(self, key, item):
        return Func(prop=SETITEM, params=[self, key, item])

    def __delitem__(self, key):
        return Func(prop=DELITEM, params=[self, key])

    def __getslice__(self, i, j):
        return Func(prop=GETSLICE, params=[self, i, j])

    def __setslice__(self, i, j, seq):
        return Func(prop=SETSLICE, params=[self, i, j, seq])

    def __delslice__(self, i, j):
        return Func(prop=DELSLICE, params=[self, i, j])

    # numeric functions
    def __add__(self, value):
        return Func(prop=ADD, params=[self, value])

    def __radd__(self, value):
        return Func(prop=ADD, params=[value, self])

    def __sub__(self, value):
        return Func(prop=SUB, params=[self, value])

    def __rsub__(self, value):
        return Func(prop=SUB, params=[value, self])

    def __mul__(self, value):
        return Func(prop=MUL, params=[self, value])

    def __rmul__(self, value):
        return Func(prop=MUL, params=[value, self])

    def __div__(self, value):
        return Func(prop=DIV, params=[self, value])

    def __rdiv__(self, value):
        return Func(prop=DIV, params=[value, self])

    def __mod__(self, value):
        return Func(
            prop=MOD if isinstance(value, Number) else LIKE,
            params=[self, value]
        )

    def __rmod__(self, value):
        return Func(
            prop=MOD if isinstance(value, Number) else LIKE,
            params=[value, self]
        )

    def __pow__(self, value):
        return Func(prop=POW, params=[self, value])

    def __rpow__(self, value):
        return Func(prop=POW, params=[value, self])

    def __lshift__(self, value):
        return Func(prop=LSHIFT, params=[self, value])

    def __rlshift__(self, value):
        return Func(prop=LSHIFT, params=[value, self])

    def __rshift__(self, value):
        return Func(prop=RSHIFT, params=[self, value])

    def __rrshift__(self, value):
        return Func(prop=RSHIFT, params=[value, self])

    def __lt__(self, value):
        return Func(prop=LT, params=[self, value])

    def __le__(self, value):
        return Func(prop=LTE, params=[self, value])

    def __eq__(self, value):
        return Func(prop=EQ, params=[self, value])

    def __ne__(self, value):
        return Func(prop=NEQ, params=[self, value])

    def __gt__(self, value):
        return Func(prop=GT, params=[self, value])

    def __ge__(self, value):
        return Func(prop=GTE, params=[self, value])

    def __nonzero__(self):
        return Func(prop=AND, params=[self, True])

    def __oct__(self):
        return Func(prop=OCT, params=[self])

    def __hex__(self):
        return Func(prop=HEX, params=[self])

    def __int__(self):
        return Func(prop=INT, params=[self])

    def __float__(self):
        return Func(prop=FLOAT, params=[self])

    def __neg__(self):
        return Func(prop=NEG, params=[self])

    def __pos__(self):
        return Func(prop=POS, params=[self])

    def __abs__(self):
        return Func(prop=ABS, params=[self])


class Property(Expression):
    """Expression dedicated to design a property."""


class Func(Expression):
    """Func request object.

    The function name is the expression property name."""

    __slots__ = ['params', 'rtype', 'ctx']

    def __init__(self, params=None, rtype=None, ctx=None, *args, **kwargs):
        """
        :param list params: list of values.
        :param type rtype: return type.
        :param dict ctx: context which will contain all expression result after
            this running. expression results are registered by schema names.
        """

        super(Func, self).__init__(*args, **kwargs)

        self.params = [] if params is None else params
        self.rtype = rtype

    def run(self, dispatcher, ctx=None):

        if ctx is None:
            ctx = {}

        self.ctx = ctx

        self._run(dispatcher=dispatcher, ctx=ctx)

    def _run(self, dispatcher, ctx):

        systems, _ = getcontext(self)

        if len(systems) == 1:
            system = dispatcher.getsystem(systems[0])
            system.run(self, ctx)

        else:
            for param in self.params:

                if isinstance(param, Expression):

                    if isinstance(param, Property):

                        system = param.system

                        system = dispatcher.getsystem(param.system)

                        system.run(self, ctx=ctx)

                    else:
                        val = param.run(dispatcher=dispatcher, ctx=ctx)

                else:
                    val = param


class And(Func):
    """Func dedicated to process conjonction of expressions."""

    def __init__(self, *args, **kwargs):

        super(And, self).__init__(prop=AND, *args, **kwargs)

    def _run(self, dispatcher, ctx):

        params = list(self.params)

        while params:
            param = params.pop(params)

            if isinstance(param, Func):

                if isinstance(param, And):
                    params = params[0:1] + param.params + params[1:]

                param.run(dispatcher=dispatcher, ctx=ctx)


class Or(Func):
    """"""

    __slots__ = ['ctxs']

    def __init__(self, *args, **kwargs):

        super(Or, self).__init__(prop=OR, *args, **kwargs)

    def _run(self, dispatcher, ctx=None):

        params = list(self.params)

        while params:
            param = params.pop(params)

            if isinstance(param, Func):

                if isinstance(param, Or):
                    params = params[0:1] + param.params + params[1:]

                pctx = ctx.copy()
                param.run(dispatcher=dispatcher, ctx=pctx)

            for mname in pctx:
                if mname in self.ctx:
                    self.ctx[mname] += pctx[mname]

                else:
                    self.ctx[mname] = pctx[mname]
