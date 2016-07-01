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

from .base import Node


class Update(Node):
    """In charge of refering model properties to create/update.

    Properties are:

    - pset: used to set model properties.
    - punset: used only if this is an update element (ref must be not None).
    - ref: referes to a filter for update elements. If None, this is just an
        element creation (and punset is useless)."""

    __slots__ = ['pset', 'punset', 'ref']

    def __init__(self, pset=None, punset=None, *args, **kwargs):
        """
        :param dict pset: properties to set. Key are property name, values are
            constant values or
        :param list punset: property names to unset.
        :param ref: refers to a filter (function) or an alias of a filter.
        """

        super(Update, self).__init__(*args, **kwargs)

        self.pset = pset or {}
        self.punset = punset or {}

    @property
    def create(self):
        """True if this update is for creation."""

        return self.ref is None and self.punset is None

    @property
    def delete(self):
        """True if this update is for deletion."""
        return self.punset is True

    @property
    def update(self):
        """True if this update is for updating."""

        return self.ref is not None and (self.pset or (self.punset is not True))
