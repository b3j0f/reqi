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

"""Specification of the class Read.

Equivalent to the SELECT statement in SQL."""

__all__ = ['Read', 'Cursor']

from ..base import Node

from six import string_types

from sys import maxsize

ASCENDING = 1  #: ascending sort order.
DESCENDING = -1  #: descending sort order.


class Read(Node):
    """In charge of selecting data to retrieve."""

    __slots__ = ['exprs', 'offset', 'limit', 'groupby', 'sort']

    def __init__(
            self, exprs, offset=None, limit=None, groupby=None, sort=None,
            *args, **kwargs
    ):
        """
        :param list exprs: list of expressions to select. expressions are Node
            or context key names. It becomes possible to retrieve all alias in
            using the expression 'ALIAS'.
        :param int offset: starting index of data to retrieve.
        :param int limit: maximal number of elements to retrieve.
        :param list groupby: list of expressions to groupy by.
        :param list sort: list of field to sort.
        """

        super(Read, self).__init__(*args, **kwargs)

        self.exprs = exprs
        self.offset = offset
        self.limit = limit
        self.groupby = groupby
        self.sort = sort

    def cursor(self, dispatcher, ctx, *args, **kwargs):
        """Process this read method and returns a cursor.

        :param dict ctx: execution context.
        :return: read result.
        :rtype: Cursor
        """

        newctx = {}

        for expr in self.exprs:

            ctxname = expr

            if isinstance(expr, Node):

                ctx = expr.run(dispatcher=dispatcher, ctx=ctx)
                ctxname = expr.getctxname()

            newctx[ctxname] = ctx[ctxname]

        if self.offset or self.limit:
            offset = self.offset or 0
            limit = self.limit or maxsize

            for key in list(newctx):
                newctx[key] = newctx[key][offset:offset+limit+1]

        if self.groupby:
            raise NotImplementedError()

        if self.sort:
            for sortp in self.sort:
                if isinstance(sortp, string_types):
                    sortp = (sortp, ASCENDING)

                for key in list(newctx):
                    newctx[key] = sorted(
                        newctx[key], key=sortp[0], reverse=sortp==DESCENDING
                    )

        result = Cursor(ctx=newctx)

        return result


class Cursor(object):
    """Read object processing result."""

    __slots__ = ['_ctx', '_index', '_len']

    def __init__(self, ctx, *args, **kwargs):

        super(Cursor, self).__init__(*args, **kwargs)

        self._ctx = ctx
        self._index = 0
        self._len = None

    def __len__(self):

        result = self._len

        if result is None:
            result = maxsize if self._ctx else 0

            for key in self._ctx:
                result = min(result, len(self._ctx[key]))

        return result

    def __getitem__(self, key):

        result = {}

        for name in self._ctx:
            result[name] = self._ctx[name][key]

        return result

    def __iter__(self):

        while self._index < len(self):

            yield self.__getitem__(self._index)

            self._index += 1

        raise StopIteration()
