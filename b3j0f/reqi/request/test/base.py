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

from ..base import Node


class NodeTest(UTCase):

    def test_constructor(self):

        system = 'system'
        schema = 'schema'
        alias = 'alias'
        ref = 'ref'
        ctx = {}

        node = Node(system=system, schema=schema, alias=alias, ref=ref, ctx=ctx)

        self.assertEqual(node.system, system)
        self.assertEqual(node.schema, schema)
        self.assertEqual(node.alias, alias)
        self.assertEqual(node.ref, ref)
        self.assertEqual(node.ctx, ctx)


class GetSystems(UTCase):

    def test_default(self):

        node = Node()

        systems = node.getsystems()

        self.assertFalse(systems)

    def test_system(self):

        system = 'test'

        node = Node(system=system)

        systems = node.getsystems()

        self.assertEqual(systems, [system])

    def test_defaultrefdefault(self):

        node = Node(ref=Node())

        systems = node.getsystems()

        self.assertFalse(systems)

    def test_defaultref(self):

        system = 'test'

        node = Node(ref=Node(system=system))

        systems = node.getsystems()

        self.assertEqual(systems, [system])

    def test_refdefault(self):

        system = 'test'

        node = Node(ref=Node(), system=system)

        systems = node.getsystems()

        self.assertEqual(systems, [system])

    def test_ref(self):

        system = 'test'
        refsystem = 'example'

        node = Node(ref=Node(system=refsystem), system=system)

        systems = node.getsystems()

        self.assertEqual(systems, [system, refsystem])


class GetCtxName(UTCase):
    """Test the method getctxname."""

    def _assert(self, ctxname=None, **kwargs):

        node = Node(**kwargs)

        self.assertEqual(node.getctxname(), ctxname)

    def test_default(self):

        self._assert()

    def test_system(self):

        self._assert('system', system='system')

    def test_schema(self):

        self._assert('schema', schema='schema')

    def test_systemschema(self):

        self._assert('system.schema', system='system', schema='schema')

    def test_ref(self):

        self._assert(ref=Node(alias='test'))


if __name__ == '__main__':
    main()
