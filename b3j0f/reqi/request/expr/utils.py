# -*- coding: utf-8 -*-

# --------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2016 Jonathan Labéjof <jonathan.labejof@gmail.com>
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

"""Specification of expression utilities."""

__all__ = ['getctxname', 'getsysscheprop']

from six.moves.urllib.parse import quote, unquote

NAME_SEPARATOR = '/'  #: context name element separator.


def getctxname(system=None, schema=None, prop=None):
    """Get context name from system, schema and property names.

    :param str system: system name.
    :param str schema: schema name.
    :param str prop: property name.
    :rtype: str"""

    return '{1}{0}{2}{0}{3}'.format(
        NAME_SEPARATOR,
        quote(system, safe='') if system else '',
        quote(schema, safe='') if schema else '',
        quote(prop, safe='') if prop else ''
    )


def getsysschprop(ctxname):
    """Get names of system, schema and prop from ctxname.

    :param str ctxname: context name to convert to sys, schema and prop names
    :rtype: tuple"""

    system, schema, prop = ctxname.split(NAME_SEPARATOR)

    system = unquote(system) if system else None
    schema = unquote(schema) if schema else None
    prop = unquote(prop) if prop else None

    return system, schema, prop