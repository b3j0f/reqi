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

from ...dispatch import Dispatcher
from ...sys import System

from ..base import Node
from ..queue import RequestQueue


class RequestQueueTest(UTCase):

    def setUp(self):

        dispatcher = Dispatcher(systems={'1': System()})

        self.queue = RequestQueue(dispatcher=dispatcher)


class CTXTest(RequestQueueTest):

    def test_default(self):

        ctx = self.queue.ctx

        self.assertIsNone(ctx)

    def test_one(self):

        ctx = self.queue.run(nodes=[]).ctx

        self.assertFalse(ctx)

    def test_onectx(self):

        ctx = {None: None}

        _ctx = self.queue.run(nodes=[], ctx=ctx).ctx

        self.assertEqual(ctx, _ctx)

    def test_two(self):

        ctx = self.queue.run(nodes=[]).run(nodes=[]).ctx

        self.assertFalse(ctx)

    def test_twoctx(self):

        ctx = {None: None}

        _ctx = self.queue.run(nodes=[], ctx=ctx).run(nodes=[]).ctx

        self.assertEqual(_ctx, ctx)


class DropTest(RequestQueueTest):

    def test_empty(self):

        self.queue.drop()

        self.assertFalse(self.queue)

    def test_one(self):

        self.queue.run(nodes=[]).drop()

        self.assertFalse(self.queue)

    def test_many(self):

        self.queue.run(nodes=[]).run(nodes=[]).run(nodes=[]).drop()

        self.assertEqual(len(self.queue), 2)


class RunTest(RequestQueueTest):

    def test_default(self):

        nodes = [Node()]

        self.queue.run(nodes=nodes)

        self.assertEqual(nodes, self.queue[0].nodes)

    def test_two(self):

        nodes0 = [Node()]
        nodes1 = [Node()]

        self.assertIsNone(nodes0[0].ctx)
        self.assertIsNone(nodes1[0].ctx)

        self.queue.run(nodes=nodes0).run(nodes=nodes1)

        self.assertEqual(nodes0, self.queue[0].nodes)
        self.assertEqual(nodes1, self.queue[1].nodes)
        self.assertNotEqual(nodes0, nodes1)

        self.assertIsNotNone(nodes0[0].ctx)
        self.assertIsNotNone(nodes1[0].ctx)


if __name__ == '__main__':
    main()
