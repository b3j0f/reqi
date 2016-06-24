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

"""Specification of the System interface."""

from b3j0f.schema import getschema


class System(object):
    """In charge of dispatching requests."""

    def __init__(
    		self, name,
            schema=None, dependencies=None, schemas=None, dimensions=None,
            *args, **kwargs
    ):
        """
        :param str name: system name.
        :param b3j0f.schema.Schema schema: system schema. Default is getschema
            of this.
        :param list of System dependencies: list of system dependencies.
        :param list schemas: supported schemas.
        :param list dimensions: list of supported dimensions.
        """

        super(System, self).__init__(*args, **kwargs)

        self.name = name
        self.schema = schema or getschema(type(self))
        self.dependencies = dependencies or []
        self.schemas = schemas or []
        self.dimensions = dimensions or []
