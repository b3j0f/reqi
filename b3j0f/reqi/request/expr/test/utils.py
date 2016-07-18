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

from ..utils import NAME_SEPARATOR, getctxname, getsysschprop


class Test(UTCase):

    def test(self):

        system = '{0}sys{0}tem{0}'.format(NAME_SEPARATOR)
        schema = '{0}sch{0}ema{0}'.format(NAME_SEPARATOR)
        prop = '{0}pr{0}op{0}'.format(NAME_SEPARATOR)

        sys, sch, pro = getsysschprop(
            getctxname(system=system, schema=schema, prop=prop)
        )

        self.assertEqual(sys, system)
        self.assertEqual(sch, schema)
        self.assertEqual(pro, prop)

    def test_system(self):

        system = '{0}sys{0}tem{0}'.format(NAME_SEPARATOR)

        sys, sch, pro = getsysschprop(getctxname(system=system))

        self.assertEqual(sys, system)
        self.assertIsNone(sch)
        self.assertIsNone(pro)

    def test_schema(self):

        schema = '{0}sch{0}ema{0}'.format(NAME_SEPARATOR)

        sys, sch, pro = getsysschprop(getctxname(schema=schema))

        self.assertIsNone(sys)
        self.assertEqual(sch, schema)
        self.assertIsNone(pro)

    def test_prop(self):

        prop = '{0}pr{0}op{0}'.format(NAME_SEPARATOR)

        sys, sch, pro = getsysschprop(getctxname(prop=prop))

        self.assertIsNone(sys)
        self.assertIsNone(sch)
        self.assertEqual(pro, prop)


if __name__ == '__main__':
    main()
