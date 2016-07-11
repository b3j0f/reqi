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
from b3j0f.schema import getschema

from ..sys import System
from ..dim.base import Dimension
from ..request.base import Node


class TestSystem(System):

    def __init__(self, *args, **kwargs):

        super(TestSystem, self).__init__(*args, **kwargs)

        self.schemas = [
            getschema(TestSystem, name='a'), getschema(TestSystem, name='b')
        ]

        self.dimensions = [Dimension('a'), Dimension('b')]

    def run(self, nodes, ctx=None, *args, **kwargs):

        result = ctx or {}

        for node in nodes:
            ctxname = node.getctxname()

            result.setdefault(ctxname, []).append(node)

        return result

class SystemTest(UTCase):

    def setUp(self):

        self.system = TestSystem()

    def test_constructor(self):

        schema = getschema(TestSystem)

        for prop in self.system.schema:
            self.assertIn(prop, schema)

    def test_run(self):

        nodes = [Node(alias='1'), Node(alias='2')]

        ctx = self.system.run(nodes=nodes)

        self.assertEqual(ctx, {'1': [nodes[0]], '2': [nodes[1]]})


if __name__ == '__main__':
    main()
