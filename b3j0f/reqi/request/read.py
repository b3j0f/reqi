# -*- coding: utf-8 -*-

# --------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2014 Jonathan Labéjof <jonathan.labejof@gmail.com>
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

"""Specification of the class Read."""

from .base import AliasedRequest

from sys import maxsize

class Read(AliasedRequest):
    """Base Read object.

    Equivalent to the SELECT part in SQL"""

    def __init__(self, limit=maxsize, offset=0, groupby=None, order=None, *args, **kwargs):
        """
        :param int limit: max number of elements to retrieve.
        :param int offset: lower element position.
        :param list groupby: array of read names.
        :param list order: list of tuple of read resource with (de/a)scending
            order.
        """

        super(Read, self).__init__(*args, **kwargs)

        self.limit = limit
        self.offset = offset
        self.groupby = groupby
        self.order = order


class FunctionRead(Read):
    """Function reading."""

    def __init__(self, function, params=None, *args, **kwargs):
        """
        :param str function: function name.
        :param list params: list of Read objects such as parameter of function.
        """
        super(FunctionRead, self).__init__(*args, **kwargs)

        self.function = function
        self.params = params

    def context(self):

        result = (set(), set())

        for param in self.params:

            if isinstance(param, Read):
                psystems, pmodels = param.context()

                result[0] |= psystems
                result[1] |= pmodels

        return result


class ModelRead(Read):
    """Model Reading."""

    def __init__(self, system=None, model=None, prop=None, *args, **kwargs):
        """
        :param str system: system name.
        :param str model: model name.
        :param str prop: model property name.
        """

        super(ModelRead, self).__init__(*args, **kwargs)

        self.system = system
        self.model = model
        self.prop = prop

    def context(self):

        result = set(), set()
        if self.system:
            result[0].add(self.system)

        if self.model:
            result[1].add(self.model)

        return result
