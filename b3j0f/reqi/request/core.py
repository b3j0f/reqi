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


class Request(object):
    """Default request object."""

    def __init__(
            self, system=None, schema=None, alias=None,
            *args, **kwargs
    ):
        """
        :param str system: system name.
        :param str schema: schema name.
        :param str alias: alias name.
        """

        super(Request, self).__init__(*args, **kwargs)

        self.system = system
        self.schema = schema
        self.alias = alias

    def context(self):
        """Get used system and model names.

        :return: this system and model names.
        :rtype: tuple of 2 sets
        """

        systems = [] if self.system is None else [self.system]
        schemas = [] if self.schema is None else [self.schema]

        return systems, schemas

    def update(self, alias):
        """Update this request related to input alias.

        :param dict alias: set of (alias name, request)."""

        if self.alias is not None:

            if self.alias in alias:
                toupdate = alias[self.alias]
                self._update(request=toupdate)

            alias[self.alias] = self

    def _update(self, request):
        """to override in order to update this context from input request.

        :param request: """

        self.system = request.system or self.system
        self.schema = request.schema or self.schema
