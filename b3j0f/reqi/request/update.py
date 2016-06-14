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

"""Specification of the class Update.

Equivalent to the UPDATE statement in SQL."""

from .base import ConditionalRequest


class Properties(object):
    """In charge of refering model properties to update."""

    def __init__(self, pset=None, punset=None, *args, **kwargs):
        """
        :param dict pset: properties to set. Key are property name, values are
            constant values or
        :param list punset: property names to unset.

        In both parameters, dictionaries are a set of key, value where key are
        property names to update, and
        """

        super(Properties, self).__init__(*args, **kwargs)

        self.pset = pset
        self.unset = punset


class Update(ConditionalRequest):
    """In charge of updating models."""

    def __init__(self, props, conditions=None, *args, **kwargs):
        """
        :param Properties props: props to set.

        """
        super(Update, self).__init__(*args, **kwargs)

        self.props = props
