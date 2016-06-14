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

from uuid import uuid4 as uuid

class Request(object):
    """Default request object."""

    def context(self):
        """Get used system and model names.

        :return: this system and model names.
        :rtype: tuple of 2 sets
        """

        raise NotImplementedError()


class AliasedRequest(Request):
    """Request with an alias."""

    def __init__(self, alias=None, *args, **kwargs):
        """
        :param str alias: alias name.
        """

        super(AliasedRequest, self).__init__(*args, **kwargs)

        self.alias = uuid() if alias is None else alias


class ContextRequest(AliasedRequest):
    """Request dedicated in managing a system and a model."""

    def __init__(self, system=None, model=None, *args, **kwargs):
        """
        :param str system: system name.
        :param str model: model name.
        """

        super(ContextRequest, self).__init__(*args, **kwargs)

        self.system = system
        self.model = model

    def context(self):

        result = set(), set()

        if self.system:
            result[0].add(self.system)

        if self.model:
            result[1].add(self.model)

        return result


class ConditionalRequest(ContextRequest):

    def __init__(self, conditions=None, *args, **kwargs):
        """
        :param list conditions: list of Condition.
        """

        super(ConditionalRequest, self).__init__(*args, **kwargs)

        self.conditions = conditions
