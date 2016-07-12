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

from ..core import Request
from ..base import Node, ALIAS
from ...dispatch import Dispatcher
from ...test.sys import TestSystem as TS


class RequestTest(UTCase):

    def setUp(self):

        self.dispatcher = Dispatcher(systems={'1': TS(), '2': TS()})

    def test_constructor(self):

        nodes = 'nodes'
        ctx = {}
        dispatcher = 'dispatcher'

        request = Request(nodes=nodes, ctx=ctx, dispatcher=self.dispatcher)

        self.assertEqual(request.nodes, nodes)
        self.assertEqual(request.ctx, ctx)
        self.assertEqual(request.dispatcher, self.dispatcher)


class RequestRunTest(UTCase):

    def setUp(self):

        self.dispatcher = Dispatcher(systems={'1': TS(), '2': TS()})

    def test_default(self):

        request = Request(dispatcher=self.dispatcher, nodes=[])

        self.assertFalse(request.run())

    def test_ctx(self):

        ctx = {'1': None}

        request = Request(dispatcher=self.dispatcher, nodes=[], ctx=ctx)

        self.assertEqual(request.run(), ctx)

    def test_nodes(self):

        nodes = [Node(alias='1', system='1'), Node(alias='2', system='2')]

        request = Request(dispatcher=self.dispatcher, nodes=nodes)

        ctx = request.run()

        self.assertEqual(
            ctx,
            {
                '1': [nodes[0]],
                '2': [nodes[1]],
                ALIAS: {
                    '1': nodes[0],
                    '2': nodes[1]
                }
            }
        )

    def test_nodes_nooptimize(self):

        nodes = [Node(alias='1', system='1'), Node(alias='2', system='2')]

        request = Request(dispatcher=self.dispatcher, nodes=nodes)

        ctx = request.run(optimize=False)

        self.assertEqual(
            ctx,
            {
                '1': [nodes[0]],
                '2': [nodes[1]]
            }
        )

    def test_nodes_wosystem(self):

        nodes = [Node(alias='1'), Node(alias='2')]

        request = Request(dispatcher=self.dispatcher, nodes=nodes)

        ctx = request.run()

        self.assertEqual(
            ctx,
            {
                ALIAS: {
                    '1': nodes[0],
                    '2': nodes[1]
                }
            }
        )

    def test_nodes_wosystem_notoptimize(self):

        nodes = [Node(alias='1'), Node(alias='2')]

        request = Request(dispatcher=self.dispatcher, nodes=nodes)

        ctx = request.run(optimize=False)

        self.assertFalse(ctx)

    def test_force(self):

        request = Request(dispatcher=self.dispatcher, nodes=[])

        result = request.run()

        result2 = request.run()

        self.assertIs(result, result2)

        result3 = request.run(force=True)

        self.assertIsNot(result, result3)


if __name__ == '__main__':
    main()
