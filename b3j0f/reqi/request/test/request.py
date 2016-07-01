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
from ..dispatch import Dispatcher

from ..core import Request


class RequestTest(UTCase):

    def setUp(self):

        class A(object):
            __slots__ = ['a']
        class B(object):
            __slots__ = ['b']
        class C(object):
            __slots__ = ['c']

        a = getschema(A)
        b = getschema(B)
        c = getschema(C)

        class SA(System):
            def __init__(self, *args, **kwargs):
                self.schemas = (a, )
                self.models = [{'i': i, 'j': 2 * i} for i in range(10)]
            def run(self, request, ctx):
                if request.prop == 'COUNT':
                    return len(self.run(request.params[0], ctx=ctx))

                elif request.prop == '=':

        sa = SA()
        class SBC(System):
            def __init__(self, *args, **kwargs):
                self.schemas = (b, c)
                self.dependencies = [sa]
                self.models = [{'i': i, 'j': 2 * i} for i in range(10, 20)]
        sbc = SBC()

        self.dispatcher = Dispatcher(systems=[sa, sbc])

    def resolve(self):




    def test_constructor(self):

        system = 'system'
        schema = 'schema'
        alias = 'alias'
        ref = 'ref'

        request = Request(system=system, schema=schema, alias=alias, ref=ref)

        self.assertEqual(request.system, system)
        self.assertEqual(request.schema, schema)
        self.assertEqual(request.alias, alias)
        self.assertEqual(request.ref, ref)

if __name__ == '__main__':
    main()
