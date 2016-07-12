#!/usr/bin/env python
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


from unittest import main

from b3j0f.utils.ut import UTCase

from ..read import Read
from ...base import Node
from ...test.base import TestNode


class TestRead(UTCase):

    def test_constructor(self):

        exprs = [Node(), Node()]
        offset = 36
        limit = 50
        groupby = ['groupby']
        sort = []

        read = Read(
            exprs=exprs, offset=offset, limit=limit, groupby=groupby, sort=sort
        )

        self.assertIs(read.exprs, exprs)
        self.assertIs(read.offset, offset)
        self.assertIs(read.limit, limit)
        self.assertIs(read.groupby, groupby)
        self.assertIs(read.sort, sort)

    def test_exprs(self):

        node = TestNode(alias='3')

        ctx = {
            '1': [1],
            '2': [2]
        }

        read = Read(exprs=['1', node])

        cursor = read.cursor(ctx=ctx, dispatcher=None)

        for item in cursor:
            self.assertEqual(
                item,
                {'1': 1, '3': {'system': None, 'schema': None, 'count': 0}}
            )

    def test_offset_limit(self):

        nodes = [TestNode(alias='test') for i in range(5)]

        ctx = {}

        for node in nodes:
            node.run(ctx=ctx, dispatcher=None)

        read = Read(exprs=['test'], offset=1, limit=2)

        cursor = read.cursor(ctx=ctx, dispatcher=None)

        self.assertEqual(len(cursor), 3)

        items = iter(cursor)

        for i in range(1, 4):
            item = next(items)

            self.assertEqual(item['test']['count'], i)

if __name__ == '__main__':
    main()
