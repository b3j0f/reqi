# -*- coding: utf-8 -*-

from link.dbrequest.model import Model, Cursor
from link.dbrequest.driver import Driver
from link.dbrequest.expression import F, CombinedExpression
from link.dbrequest.assignment import A
from link.dbrequest.comparison import C, CombinedCondition
from link.dbrequest.query import Lazy

from link.feature import Feature

from .utils import smartexecution, getidentifiers, getname


class REQIDriver(Feature):
    """This driver aims to modify queries in parsing them and identifies which
    ones are related to specific dispatcher systems.

    System/schema/property names are retrieved from node names related to the
    function getidentifiers."""

    name = 'query'

    QUERY_COUNT = 'count'
    QUERY_CREATE = 'save'
    QUERY_READ = 'find'
    QUERY_UPDATE = 'update'
    QUERY_DELETE = 'delete'

    model_class = Model
    cursor_class = Cursor

    def process_query(self, query, *args, **kwargs):

        result = None

        if query['type'] in Driver.QUERY_CREATE, Driver.QUERY_UPDATE:
            key = 'update'

        else:
            key = 'filter'

        nodes = self.qm.from_ast(query[key])

        nodes = self.cook(nodes)

        result = smartexecution(nodes)

        return result

    def cook(self, nodes):
        raise NotImplementedError()
