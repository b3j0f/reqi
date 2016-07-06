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

"""Specification of the request object."""

from ..base import Node
from .base import Expression


class Function(Expression):
    """Function request object.

    The function name is the expression property name."""

    __slots__ = ['params', 'rtype']

    def __init__(
            self, params=None, rtype=None, prop=None, *args, **kwargs
    ):
        """
        :param list params: list of values.
        :param type rtype: return type.
        :param dict ctx: context which will contain all expression result after
            this running. expression results are registered by schema names.
        """

        super(Function, self).__init__(*args, **kwargs)

        self.params = [] if params is None else params
        self.rtype = rtype
        self.prop = prop or type(self).PROP or type(self).__name__

    def _run(self, dispatcher, ctx):

        for param in self.params:

            if isinstance(param, Node):

                param.run(dispatcher=dispatcher, ctx=ctx)
