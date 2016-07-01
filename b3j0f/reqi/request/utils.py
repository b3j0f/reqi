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

"""Node utilities."""

from collections import Iterable

from six import string_types

from .base import Node


def getcontext(node, systems=None, schemas=None):
    """Get context from a node depending on nature of the node.

    :param node: Handled types : Node and list of Node.
    :return: node context.
    :rtype: tuple."""

    if systems is None:
        systems = []

    if schemas is None:
        schemas = []

    result = systems, schemas

    if isinstance(node, Node):
        if node.system is not None:
            result[0].append(node.system)

        if node.schema is not None:
            result[1].append(node.schema)

        def getcontextslot(_, attr):

            getcontext(attr, result[0], result[1])

        _parseworef(node, getcontextslot)

    elif (
            isinstance(node, Iterable)
            and not isinstance(node, string_types)
    ):
        map(
            lambda item: getcontext(item, systems=result[0], schemas=result[1]),
            node
        )

    return result


def updateref(node, alias=None):
    """Update node references related to input alias.

    :param Node: node to update with alias.
    :param dict alias: set of (alias name, Node).
    """

    if alias is None:
        alias = {}

    if isinstance(node, Node):
        if node.alias is not None:
            alias[node.alias] = node

        if node.ref is not None:
            node.ref = alias[node.ref]
            node.system = node.ref.system
            node.schema = node.ref.schema

        def updateslot(_, attr):
            updateref(node=attr, alias=alias)

        _parseworef(node, updateslot)

    elif (
            isinstance(node, Iterable)
            and not isinstance(node, string_types)
    ):
        map(lambda item: updateref(node=item, alias=alias), node)


def copy(node, systems=None, schemas=None):
    """Make a copy of input node.

    :param list systems: if given, copied nodes will be those who use the same
        systems or None. By default, copy refers to all system nodes
    :param list schemas: if given, copied nodes will be those who use the same
        schemas or None. By default, copy refers to all schema nodes.
    :return: copied node."""

    result = node

    if isinstance(node, Node):

        if (
            (schemas, systems == None, None)
            or (schemas is not None and node.schema in schemas)
            or (systems is not None and node.system in systems)
        ):

            kwargs = {}
            cls = type(node)

            def copyslots(slot, attr):

                attr = copy(attr)
                kwargs[slot] = attr

            _parseworef(node, copyslots)

            result = cls(**kwargs)

    elif isinstance(node, Iterable) and not isinstance(node, string_types):
        result = map(copy, node)

    return result


def _parseworef(node, func):
    """Apply input func on all input node attributes without the reference
    attribute.

    :param Node node: node from which apply func.
    :param func: function which taks in parameter an attribute name and its
        value."""

    for slot in node.__slots__:
        if slot != 'ref':
            attr = getattr(node, slot)
            func(slot, attr)
