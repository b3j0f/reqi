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

from ..base import Node, ALIAS, Ref


class TestNode(Node):

    def _run(self, dispatcher, ctx, *args, **kwargs):

        super(TestNode, self)._run(
            dispatcher=dispatcher, ctx=ctx, *args, **kwargs
        )

        nodes = ctx.setdefault(self.getctxname(), [])

        nodes.append({'count': len(nodes)})

        return ctx


class NodeTest(UTCase):

    def test_constructor(self):

        alias = 'alias'
        ctx = {}

        node = Node(alias=alias, ctx=ctx)

        self.assertEqual(node.alias, alias)
        self.assertEqual(node.ctx, ctx)

    def test_elements(self):

        alias = 'test'
        elements = [1, 2]

        ctx = {alias: elements}

        node = Node(alias=alias)

        nodeelements = node.elements(ctx)

        self.assertIs(nodeelements, elements)

    def test_notelements(self):

        self.assertIsNone(Node().elements({}))

    def test_getsystems(self):

        self.assertFalse(Node().getsystems())

    def test_getctxname(self):

        self.assertEqual('test', Node(alias='test').getctxname())

    def test_defaultgetctxname(self):

        node = Node()

        self.assertEqual(str(node), node.getctxname())

    def test_run(self):

        ctx = {}
        node = Node(alias='test')
        node.run(dispatcher=None, ctx=ctx)

        self.assertEqual(ctx, {ALIAS: {node.alias: node}})


class RefTest(UTCase):

    def test_constructor(self):

        alias = 'alias'
        node = Node()

        ref = Ref(alias=alias, ref=node)

        self.assertIs(ref.alias, alias)
        self.assertIs(ref.ref, node)

    def test_systems(self):

        system = 'system'

        class TestNode(Node):

            def getsystems(self):

                return ['system']

        ref = Ref(ref=TestNode())

        self.assertEqual(ref.getsystems(), [system])

    def test_defaultrefdefault(self):

        self.assertFalse(Ref(ref=Node()).getsystems())

    def test_run(self):

        alias = 'test'

        node = Node(alias=alias)

        ctx = {ALIAS: {alias: node}}

        ref = Ref(alias=alias)
        ref.run(dispatcher=None, ctx=ctx)

        self.assertIs(ref.ref, node)

    def test_getctxname(self):

        ctxname = 'test'

        ref = Ref(ref=Node(alias=ctxname))

        self.assertEqual(ref.getctxname(), ctxname)

if __name__ == '__main__':
    main()
