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

"""Specification of the dispatcher interface."""

__all__ = ['Request']

from .base import Node
from .expr import And, Expression
from .utils import getcontext, updateref
from .update import Update

from collections import Iterable

NAME_SEPARATOR = '/'


class Request(Node):
    """In charge of dispatching requests."""

    __slots__ = (
        'dispatcher', 'scope', 'cond', 'read', 'updates', 'ctx', 'logger'
    )

    def __init__(
            self, dispatcher=None,
            scope=None, cond=None, read=None, updates=None, ctx=None,
            logger=None, *args, **kwargs
    ):

        super(Request, self).__init__(*args, **kwargs)

        self.dispatcher = dispatcher
        self.scope = scope
        self.cond = cond
        self.read = read
        self.updates = updates
        self.ctx = ctx
        self.logger = logger

    def __iadd__(self, other):

        items = other if isinstance(other, Iterable) else [other]

        for item in items:

            if isinstance(item, Update):
                self.update(item)

            elif isinstance(item, Expression):
                self.where(item)

            else:
                self.models(item)

        return self

    def models(self, *models):

        models = list(models)

        if self.scope is None:
            self.scope = models

        else:
            self.scope += models

        return self

    def where(self, *expr):
        """Apply where conditions.

        :param tuple expr: expressions to add to this where.
        :return: this.
        :rtype: Request"""

        expr = list(expr)

        if self.cond is None:
            self.cond = And(params=list(expr))

        else:
            self.cond = [And(params=[item] + expr) for item in self.cond]

        return self

    def update(self, *updates):

        if self.updates:
            self.updates = list(updates)

        else:
            self.updates += list(updates)

        return self

    def run(
            self, dispatcher=None, scope=None, cond=None, updates=None,
            read=None, ctx=None
        ):
        """Run input requests.

        The processing order is as follow :

        1. scope
        2. cond
        3. updates
        4. read

        :param b3j0f.reqi.dispatch.Dispatcher dispatcher: dispatcher to use.
            Default is self.dispatcher.
        :param list scope: list of nodes where default system and schemas will
            be given.
        :param list cond: list of conditional Expressions.
        :param list updates: list of updates (creation, update and deletion).
        :param list read: list of result Expressions.
        :param dict ctx: context to share with requests.
        :return: read objects where keys are alias/prop name and values are
            model values.
        :rtype: list of dict."""

        result = []

        dispatcher = dispatcher or self.dispatcher
        scope = scope or self.scope
        cond = cond or self.cond
        updates = updates or self.updates
        read = read or self.read
        ctx = ctx or self.ctx or {}

        if scope is not None:
            updateref(scope)
            systems, schemas = getcontext(scope)

        if cond is not None:
            updateref(cond)
            systems, schemas = getcontext(cond, systems, schemas)

            for item in cond:
                item.run(dispatcher=dispatcher, ctx=ctx)

        if updates is not None:
            updateref(updates)
            systems, schemas = getcontext(cond, systems, schemas)

            for item in updates:
                item.run(dispatcher=dispatcher, ctx=ctx)

        if read is not None:
            updateref(read)
            systems, schemas = getcontext(cond, systems, schemas)

            for item in read:
                itemresult = read.run(dispatcher=dispatcher, ctx=ctx)
                result.append(itemresult)

        return result
