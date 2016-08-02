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

__all__ = ['Reverse', 'GetItem', 'SetItem', 'DelItem']

from .base import Expression
from .func import Function

from ..utils import updateitems


class Reverse(Function):

    def _run(self, dispatcher, ctx):

        updateitems(
            ctx, self.params[0], lambda item: reversed(item[self.params[1]])
        )

Expression.__reverse__ = lambda self: Reverse(params=[self])

class GetItem(Function):
    pass


class SetItem(Function):

    def _run(self, dispatcher, ctx):

        updateitems(
            ctx, self.params[0],
            lambda item: item.__setitem__(self.params[1], self.params[2])
        )


Expression.__setitem__ = lambda self, key, value: SetItem(params=[self, key, value])

class DelItem(Function):

    def _run(self, dispatcher, ctx):

        updateitems(
            ctx, self.params[0], lambda item: item.__delitem__(self.params[1])
        )


Expression.__delitem__ = lambda self, key: DelItem(params=[self, key])
