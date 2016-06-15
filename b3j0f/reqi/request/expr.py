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

from .core import Request

from .utils import getcontext, updaterequest

from numbers import Number

# list of default function names (prop is None).
# existing property
EXISTS = 'exists'

# regex functions
LIKE = 'like'

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

# array functions
COUNT = 'count'
IN = 'in'
REVERSE = 'reverse'
GETITEM = 'getitem'
SETITEM = 'setitem'
DELITEM = 'delitem'
GETSLICE = 'getslice'
SETSLICE = 'setslice'
DELSLICE = 'delslice'

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


class Expression(Request):
    """Expression request object."""

    def __init__(self, prop, *args, **kwargs):
        """
        :param str prop: property name.
        """

        super(Expression, self).__init__(*args, **kwargs)

        self.prop = prop

    def _update(self, request, *args, **kwargs):

        super(Expression, self)._update(request=request, *args, **kwargs)

        self.prop = request.prop or self.prop

    # boolean functions
    def __and__(self, value):
        return FuncRequest(prop=AND, params=[self, value])

    def __rand__(self, value):
        return FuncRequest(prop=AND, params=[value, self])

    def __or__(self, value):
        return FuncRequest(prop=OR, params=[self, value])

    def __ror__(self, value):
        return FuncRequest(prop=OR, params=[value, self])

    def __xor__(self, value):
        return FuncRequest(prop=XOR, params=[self, value])

    def __rxor__(self, value):
        return FuncRequest(prop=XOR, params=[value, self])

    def __invert__(self):
        return FuncRequest(prop=NOT, params=[self])

    # array functions
    def __len__(self):
        return FuncRequest(prop=COUNT, params=[self])

    def __contains__(self, item):
        return FuncRequest(prop=IN, params=[item, self])

    def __reversed__(self):
        return FuncRequest(prop=REVERSE, params=[self])

    def __getitem__(self, key):
        return FuncRequest(prop=GETITEM, params=[self, key])

    def __setitem__(self, key, item):
        return FuncRequest(prop=SETITEM, params=[self, key, item])

    def __delitem__(self, key):
        return FuncRequest(prop=DELITEM, params=[self, key])

    def __getslice__(self, i, j):
        return FuncRequest(prop=GETSLICE, params=[self, i, j])

    def __setslice__(self, i, j, seq):
        return FuncRequest(prop=SETSLICE, params=[self, i, j, seq])

    def __delslice__(self, i, j):
        return FuncRequest(prop=DELSLICE, params=[self, i, j])

    # numeric functions
    def __add__(self, value):
        return FuncRequest(prop=ADD, params=[self, value])

    def __radd__(self, value):
        return FuncRequest(prop=ADD, params=[value, self])

    def __sub__(self, value):
        return FuncRequest(prop=SUB, params=[self, value])

    def __rsub__(self, value):
        return FuncRequest(prop=SUB, params=[value, self])

    def __mul__(self, value):
        return FuncRequest(prop=MUL, params=[self, value])

    def __rmul__(self, value):
        return FuncRequest(prop=MUL, params=[value, self])

    def __div__(self, value):
        return FuncRequest(prop=DIV, params=[self, value])

    def __rdiv__(self, value):
        return FuncRequest(prop=DIV, params=[value, self])

    def __mod__(self, value):
        return FuncRequest(
            prop=MOD if isinstance(value, Number) else LIKE,
            params=[self, value]
        )

    def __rmod__(self, value):
        return FuncRequest(
            prop=MOD if isinstance(value, Number) else LIKE,
            params=[value, self]
        )

    def __pow__(self, value):
        return FuncRequest(prop=POW, params=[self, value])

    def __rpow__(self, value):
        return FuncRequest(prop=POW, params=[value, self])

    def __lshift__(self, value):
        return FuncRequest(prop=LSHIFT, params=[self, value])

    def __rlshift__(self, value):
        return FuncRequest(prop=LSHIFT, params=[value, self])

    def __rshift__(self, value):
        return FuncRequest(prop=RSHIFT, params=[self, value])

    def __rrshift__(self, value):
        return FuncRequest(prop=RSHIFT, params=[value, self])

    def __lt__(self, value):
        return FuncRequest(prop=LT, params=[self, value])

    def __le__(self, value):
        return FuncRequest(prop=LTE, params=[self, value])

    def __eq__(self, value):
        return FuncRequest(prop=EQ, params=[self, value])

    def __ne__(self, value):
        return FuncRequest(prop=NEQ, params=[self, value])

    def __gt__(self, value):
        return FuncRequest(prop=GT, params=[self, value])

    def __ge__(self, value):
        return FuncRequest(prop=GTE, params=[self, value])

    def __nonzero__(self):
        return FuncRequest(prop=AND, params=[self, True])

    def __oct__(self):
        return FuncRequest(prop=OCT, params=[self])

    def __hex__(self):
        return FuncRequest(prop=HEX, params=[self])

    def __int__(self):
        return FuncRequest(prop=INT, params=[self])

    def __float__(self):
        return FuncRequest(prop=FLOAT, params=[self])

    def __neg__(self):
        return FuncRequest(prop=NEG, params=[self])

    def __pos__(self):
        return FuncRequest(prop=POS, params=[self])

    def __abs__(self):
        return FuncRequest(prop=ABS, params=[self])


class FuncRequest(Expression):
    """Func request object.

    The function name is the property name."""

    def __init__(self, params=None, rtype=None, *args, **kwargs):
        """
        :param list params: list of values.
        :param type rtype: return type.
        """

        super(FuncRequest, self).__init__(*args, **kwargs)

        self.params = [] if params is None else params
        self.rtype = rtype

    def context(self, *args, **kwargs):

        systems, schemas = super(FuncRequest, self).context(*args, **kwargs)

        getcontext(self.params, systems, schemas)

        return systems, schemas

    def update(self, *args, **kwargs):

        super(FuncRequest, self).update(*args, **kwargs)

        updaterequest(self.params, *args, **kwargs)
