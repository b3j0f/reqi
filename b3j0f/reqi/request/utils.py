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

__all__ = ['getcontext', 'updateref', 'copy']

"""Specification of the request object."""

from collections import Iterable

from six import string_types

from .core import Request


def getcontext(req, systems=None, schemas=None):
    """Get context from a request depending on nature of the request.

    :param req: Handled types : Request and list of Request.
    :return: request context.
    :rtype: tuple."""

    if systems is None:
        systems = []

    if schemas is None:
        schemas = []

    result = systems, schemas

    if isinstance(req, Request):
        if req.system is not None:
            result[0].append(req.system)

        if req.schema is not None:
            result[1].append(req.schema)

        def getcontextslot(_, attr):

            getcontext(attr, result[0], result[1])

        _parseworef(req, getcontextslot)

    elif (
            isinstance(req, Iterable)
            and not isinstance(req, string_types)
    ):
        map(
            lambda item: getcontext(item, systems=result[0], schemas=result[1]),
            req
        )

    return result


def updateref(req, alias=None):
    """Update request references related to input alias.

    :param Request: req to update with alias.
    :param dict alias: set of (alias name, Request).
    """

    if alias is None:
        alias = {}

    if isinstance(req, Request):
        if req.alias is not None:
            alias[req.alias] = req

        if req.ref is not None:
            req.ref = alias[req.ref]

        def updateslot(_, attr):

            updateref(req=attr, alias=alias)

        _parseworef(req, updateslot)

    elif (
            isinstance(req, Iterable)
            and not isinstance(req, string_types)
    ):
        map(lambda item: updateref(req=item, alias=alias), req)


def copy(req, schemas=None, systems=None):
    """Make a copy of input request."""

    result = req

    if isinstance(req, Request):

        if (
            (schemas, systems == None, None)
            or (schemas is not None and req.schema in schemas)
            or (systems is not None and req.system in systems)
        ):

            kwargs = {}
            cls = type(req)

            def copyslots(slot, attr):

                attr = copy(attr)
                kwargs[slot] = attr

            _parseworef(req, copyslots)

            result = cls(**kwargs)

    elif isinstance(req, Iterable) and not isinstance(req, string_types):
        result = map(copy, req)

    return result


def _parseworef(req, func):

    for slot in req.__slots__:
        if slot != 'ref':
            attr = getattr(req, slot)
            func(slot, attr)
