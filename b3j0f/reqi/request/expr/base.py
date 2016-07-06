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

"""Specification of the expression object."""

__all__ = ['Expression']

from sys import maxsize

from ..base import Node


class Expression(Node):
    """Expression request object."""

    __slots__ = ['prop', 'offset', 'limit', 'groupby', 'sort', 'ctxnames']

    def __init__(
            self, prop=None, offset=None, limit=None, groupby=None, sort=None,
            ctxnames=None,
            *args, **kwargs
    ):
        """
        :param str prop: property name.
        :param int offset: minimal offset to get. 0 by default.
        :param int limit: max number of elements to get. Infinite by default.
        :param list groupby: list of property names to group by.
        :param list sort: list of property name by (de/a)scendant order to sort.
        :param list ctxnames: list of context names to keep. All by default.
        """

        super(Expression, self).__init__(*args, **kwargs)

        self.prop = prop or type(self).__name__
        self.offset = offset
        self.limit = limit
        self.groupby = groupby
        self.sort = sort
        self.ctxnames = ctxnames

    def run(self, *args, **kwargs):

        result = super(Expression, self).run(*args, **kwargs)

        if self.ctxnames:
            result, oldresult = {}, result

            for ctxname in self.ctxnames:
                result[ctxname] = oldresult[ctxname]

        if self.offset or self.limit:
            offset = self.offset or 0
            limit = self.limit or maxsize

            for key in list(result):
                result[key] = result[offset:limit]

        if self.groupby:
            raise NotImplementedError()

        if self.sort:
            raise NotImplementedError()

        return result
