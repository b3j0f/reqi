__all__ = ['getidentifiers', 'getname']

from six.moves.urllib.parse import quote, unquote

from link.dbrequest.condition import CombinedCondition
from link.dbrequest.query import Lazy
from link.dbrequest.expression import F, CombinedExpression

IDENTIFIER_SEPARATOR = '/'
ALIAS_SEPARATOR = ':'


def getidentifiers(name):
    """Get system, schema, property and alias identifiers from a query name.

    :param str name: query name.

    :return: system, schema, property and alias identifiers.
    :rtype: tuple"""

    identifiers = name.split(ALIAS_SEPARATOR)

    if len(identifiers) == 2:
        identifiers, alias = identifiers

    else:
        alias = None

    system, schema, prop = name.split(IDENTIFIER_SEPARATOR)

    if system:
        system = unquote(system)

    if schema:
        schema = unquote(schema)

    if prop:
        prop = unquote(prop)

    return system, schema, prop, alias


def getname(system='', schema='', prop='', alias=''):
    """Get a query name from a system, schema and property identifiers.

    :param str system: system identifier.
    :param str schema: model identifier.
    :param str prop: property identifier.
    :param str alias: alias identifier.

    :return: query identifier.
    :rtype: str"""

    if system:
        system = quote(system, '')

    if schema:
        schema = quote(schema, '')

    if prop:
        prop = quote(prop, '')

    result = '{0}{1}{2}'.format(
        IDENTIFIER_SEPARATOR.join([system, schema, prop]),
        ALIAS_SEPARATOR,
        alias
    )

    return result


def getqm(node):
    """Get the first query manager by doing a deep searching from the left.

    :param Node node: node from where get the query manager """

    result = None

    if isinstance(node, F):

        for arg in node.arguments:
            result = getqm(arg)

            if result is not None:
                break

    elif isinstance(node, Lazy):
        result = node.querymanager

    elif isinstance(node, (CombinedExpression, CombinedExpression)):

        result = getqm(node.left) or getqm(node.right)

    return result


def smartexecution(node, stack=None):
    """Execute input node in doing a smart execution related to existing
    query managers.

    The execution consists to delegate execution of sub-queries to query
    managers, in parsing the instructions deeply by the right.

    For example, let Q:M an instruction M driven by the query manager Q,
    and N an instruction without query manager.
    If the query is Q:M = 1, then the execution is delegated to the query
    manager Q, because this is the only one query manager.
    If the query is Q:M = P:N, the the execution is first P:N, then Q:M = P:N,
    because the execution is first done by the right.
    """

    result = None

    if stack is None:
        stack = []

    qm = getqm(node)

    if qm is not None:
        if stack:
            if qm != stack[-1][1]:
                stack.append((node, qm))

        else:
            stack.append((node, qm))

    subnodes = []

    if isinstance(node, (CombinedExpression, CombinedCondition)):
        subnodes = [node.right, node.left]

    elif isinstance(node, F):
        subnodes = node.arguments

    for subnode in reversed(subnodes):
        rsubnode = smartexecution(subnode, stack=stack)

        if rsubnode is not None:
            result = rsubnode

    if stack:
        if stack[-1][0] is node:
            result = qm.execute(node.to_ast())
            stack.pop()

    return result
