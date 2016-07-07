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

__all__ = ['SetSlice', 'GetSlice', 'DelSlice']


from .base import Expression
from .func import Function
from ..utils import updateitems

from ..update import Update, Slice


class GetSlice(Function):
    pass


Expression.__getslice__ = lambda self, i, j: GetSlice(params=[self, Slice(i, j)])

class SetSlice(Function):

    def _run(self):

        expr, i, j, seq = self.params

        updateitems(
            self.ctx, expr, lambda item: item[expr.prop].__setslice__(i, j, seq)
        )


Expression.__setslice__ = lambda self, i, j, seq: Update(
    pset={self.prop: Slice(i, j, seq)}
)


class DelSlice(Function):

    def _run(self):

        expr, i, j = self.params

        updateitems(
            self.ctx, expr, lambda item: item[expr.prop].__delslice__(i, j)
        )

Expression.__delslice__ = lambda self, i, j: DelSlice(params=[self, i, j])
