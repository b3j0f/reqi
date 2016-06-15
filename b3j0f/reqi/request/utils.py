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

__all__ = ['getcontext', 'updaterequest']

"""Specification of the request object."""

from collections import Iterable

from six import string_types

from .core import Request


def getcontext(request, systems=None, schemas=None):
    """Get context from a request depending on nature of the request.

    :param request: Handled types : Request and list of Request.
    :return: request context.
    :rtype: tuple."""

    result = (systems or [], schemas or [])

    if isinstance(request, Request):
        rsystems, rschemas = request.context()

        result[0] += [item for item in rsystems if item not in result[0]]
        result[1] += [item for item in rschemas if item not in result[1]]

    elif (
            isinstance(request, Iterable)
            and not isinstance(request, string_types)
    ):
        for item in request:
            getcontext(item, systems=result[0], schemas=result[1])

    return result


def updaterequest(request, alias):
    """Update request properties related to alias.

    :param Request: request to update with alias.
    :param dict alias: set of (alias name, Request).
    """

    if isinstance(request, Request):
        request.update(alias)

    elif (
            isinstance(request, Iterable)
            and not isinstance(request, string_types)
    ):

        for item in request:
            updaterequest(item, alias)
