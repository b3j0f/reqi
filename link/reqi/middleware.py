from .dispatch import Dispatcher
from .sys import System

from link.middleware import Middleware

from link.feature import getfeature

from six.moves.urllib.parse import urlparse


class MiddlewareDispatcher(Dispatcher):
    """Dispatcher specific to middleware instanciation from uris.

    Middleware must be link.dbrequest.QueryManager with the feature 'model'
    leading to a link.model.Model object."""

    def __init__(self, uris, *args, **kwargs):
        """
        :param list uris: list of uris from where get middleware and protocols.
        """

        systems = {}

        for uri in uris:

            query = Middleware.get_middleware_by_uri(uri)
            model = getfeature(query, 'model')
            system = System(model=model, querymanager=query)

            for name in urlparse(uri).scheme.split('+'):
                sysbyname[name] = sys

        super(MiddlewareDispatcher, self).__init__(
            systems=systems, *args, **kwargs
        )
