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

"""Specification of the Scope.

Equivalent of the FROM in SQL"""

from .base import AliasedRequest

class Scope(AliasedRequest):
    """Equivalent of FROM in SQL."""


class ElementaryScope(Scope):
    """Elementary scope."""

    def __init__(self, system=None, model=None, *args, **kwargs):
        """
        :param str system: system name.
        :param str model: model name.
        """

        super(ElementaryScope, self).__init__(*args, **kwargs)

        self.system = system
        self.model = model

    def context(self):

        return set([self.system]), set([self.model])


class CompositeScope(Scope):
    """Scope composed of a read."""

    def __init__(self, read, *args, **kwargs):
        """
        :param Read read: read from where get elements to CRUD.
        """

        super(CompositeScope, self).__init__(*args, **kwargs)

        self.read = read

    def context(self):

        return self.read.context()
