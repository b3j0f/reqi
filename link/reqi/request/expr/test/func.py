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

from ..func import Function, Expression


class FunctionTest(UTCase):

    def test_defaultconstructor(self):

        func = Function()

        self.assertFalse(func.params)
        self.assertIsNone(func.rtype)
        self.assertEqual(func.prop, type(func).__name__)

    def test_constructor(self):

        params = [1, 2]
        rtype = bool

        func = Function(params=params, rtype=rtype)

        self.assertIs(func.params, params)
        self.assertIs(func.rtype, rtype)

    def test_getsystems(self):

        self.assertFalse(Function().getsystems())

    def test_getonesystems(self):

        self.assertEqual(Function(system='system').getsystems(), ['system'])

    def test_getparamssystems(self):

        params = [Expression(system=str(i)) for i in range(5)]

        systems = ['test'] + [str(i) for i in range(5)]

        self.assertEqual(
            Function(system='test', params=params).getsystems(), systems
        )


class TestFunction(Function):

    def _prun(self, dispatcher, ctx):

        ctx['exec'].append(self.alias)

        return ctx

class ParamsTest(UTCase):

    def setUp(self):

        self.ctx = {'exec': []}

        class Dispatcher(object):
            def __init__(self):

                class System(object):

                    def __init__(self, name):

                        self.name = name

                    def run(self, nodes, dispatcher, ctx):

                        ctx['exec'].append((nodes[0].alias, self.name))

                        return ctx

                class Systems(object):

                    def __getitem__(self, key):

                        return System(key)

                self.systems = Systems()

        self.dispatcher = Dispatcher()

    def assert_func(self, func, res):

        ctx = func.run(dispatcher=self.dispatcher, ctx=self.ctx)

        self.assertEqual(ctx['exec'], res)

    def test_noparams(self):

        func = TestFunction(alias='1')

        self.assert_func(func, [('1')])

    def test_params(self):

        func = TestFunction(
            alias='parent',
            params=[TestFunction(alias=str(i)) for i in range(5)]
        )

        self.assert_func(func, [('parent')])

    def test_params_fsys(self):

        params = [TestFunction(system='sys')] + [TestFunction(alias=str(i)) for i in range(5)]

        func = TestFunction(alias='parent', params=params)

        self.assert_func(func, [('parent', 'sys')])

    def test_params_msys(self):

        params = [TestFunction(alias=str(i)) for i in range(5)]
        params.insert(2, TestFunction(system='sys'))

        func = TestFunction(alias='parent', params=params)

        self.assert_func(func, [('parent', 'sys')])

    def test_params_esys(self):

        params = [TestFunction(alias=str(i)) for i in range(5)] + [TestFunction(system='sys')]

        func = TestFunction(alias='parent', params=params)

        self.assert_func(func, [('parent', 'sys')])

    def test_params_multisys(self):

        params = [
            TestFunction(alias='a', system='a'),
            TestFunction(alias='b', system='b'),
            TestFunction(alias='c', system='c')
        ]
        func = TestFunction(alias='parent', params=params)

        self.assert_func(func, [('a', 'a'), ('b', 'b'), ('parent', 'c')])


if __name__ == '__main__':
    main()
