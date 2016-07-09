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

"""Specification of the request queue object."""

__all__ = ['RequestQueue']

from .core import Request


class RequestQueue(list):
    """In charge of processing multi requests with historization of requests."""

    def __init__(self, dispatcher, *args, **kwargs):
        """
        :param Dispatcher dispatcher: default dispatcher.
        :param dict ctx: default expression execution context.
        :param list nodes: nodes to execute.
        """

        super(RequestQueue, self).__init__(*args, **kwargs)

        self.dispatcher = dispatcher

    @property
    def ctx(self):
        """Get last (calculated) ctx.

        :rtype: dict"""

        return self[-1].resctx if self else None

    def run(self, nodes, ctx=None, dispatcher=None):
        """Run input nodes in adding a new request to this queue.

        :param list nodes: nodes to process.
        :param dict ctx: execution context.
        :param Dispatcher dispatcher: dispatcher to use. Default is this
            dispatcher.
        """

        if dispatcher is None:
            dispatcher = self.dispatcher

        if ctx is None:
            ctx = self.ctx

        elif self.ctx is not None:
            ctx.update(self.ctx)

        req = Request(nodes=nodes, ctx=ctx, dispatcher=dispatcher)

        self.append(req)

        self.ctx = req.run()

        return self

    def drop(self, count):
        """Drop last ``count`` requests.

        :param int count: count requests to drop off.
        :return: this.
        :rtype: RequestQueue"""

        if count > 0:

            self[:] = self[:-count]

        return self
