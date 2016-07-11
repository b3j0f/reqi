#!/usr/bin/env python
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


from unittest import main

from b3j0f.utils.ut import UTCase
from b3j0f.utils.version import OrderedDict
from b3j0f.schema import Schema, Property
from b3j0f.schema.prop import SchemaProperty

from ..dispatch import Dispatcher, _removeoccurences
from ..sys import System


class RemoveOccurencesTest(UTCase):

    def test_empty(self):

        l = []

        _removeoccurences(l)

        self.assertFalse(l)

    def test_full(self):

        l = [0, 1, 2, 1, 3, 0, 0, 2, 1]

        _removeoccurences(l)

        self.assertEqual(l, [0, 1, 2, 3])



class DispatcherTest(UTCase):

    def setUp(self):

        self.systems = OrderedDict()

        self.allschemas = []

        self.count = 5

        for i in range(self.count):

            syskwargs = {}

            sysn = str(i)

            schemas = []

            syskwargs['schemas'] = schemas

            self.allschemas.append(schemas)

            for j in range(self.count):

                schemakwargs = {'name': '{0}'.format(j)}

                properties = [
                    SchemaProperty(
                        name='{0}'.format(k), schema=schemas[k]
                    ) for k in range(j)
                ]
                properties.append(Property('id'))
                schemakwargs['properties'] = properties
                schemakwargs['ids'] = ['id']
                schema = Schema('', **schemakwargs)
                schemas.append(schema)

                if j > 0:
                    schema[str(j - 1)] = schemas[j - 1]

            system = System(**syskwargs)

            self.systems[sysn] = system

        self.dispatcher = Dispatcher(systems=self.systems)


class DispatcherConstructor(DispatcherTest):

    def test_systemsperschema(self):

        _systemsperschema = self.dispatcher._systemsperschema

        for schn in _systemsperschema:

            systems = _systemsperschema[schn]

            self.assertEqual(systems, [str(i) for i in range(self.count)])

    def test_schemaspersystem(self):

        _schemaspersystem = self.dispatcher._schemaspersystem

        for sysn in _schemaspersystem:

            schemas = _schemaspersystem[sysn]

            self.assertEqual(schemas, [str(i) for i in range(self.count)])

    def test_schemasperprop(self):

        _schemasperprop = self.dispatcher._schemasperprop

        for propn in _schemasperprop:

            schemas = _schemasperprop[propn]

            if propn == 'id':
                count = 5

            else:
                count = self.count - int(propn) - 1

            self.assertEqual(count, len(schemas) / 5)


class GetSystemsWithSchemasTest(DispatcherTest):

    def test_default(self):

        systems, schemas = self.dispatcher.getsystemswithschemas()

        self.assertEqual(systems, [str(i) for i in range(self.count)])

        self.assertEqual(schemas, [str(i) for i in range(self.count)])

    def test_defaultsystems(self):

        systems, schemas = self.dispatcher.getsystemswithschemas(
            defsystems=['2', '3']
        )

        self.assertEqual(systems, ['2', '3'])

        self.assertEqual(schemas, [str(i) for i in range(self.count)])

    def test_defaultschemas(self):

        systems, schemas = self.dispatcher.getsystemswithschemas(
            defschemas=['2', '3']
        )

        self.assertEqual(systems, [str(i) for i in range(self.count)])

        self.assertEqual(schemas, ['2', '3'])


    def test_defaultsystemsandschemas(self):

        systems, schemas = self.dispatcher.getsystemswithschemas(
            defsystems=['2', '3'], defschemas=['2', '3']
        )

        self.assertEqual(systems, ['2', '3'])

        self.assertEqual(schemas, ['2', '3'])

    def test_system(self):

        systems, schemas = self.dispatcher.getsystemswithschemas(
            system='2'
        )

        self.assertEqual(systems, ['2'])

        self.assertEqual(schemas, [str(i) for i in range(self.count)])

    def test_schema(self):

        systems, schemas = self.dispatcher.getsystemswithschemas(
            schema='2'
        )

        self.assertEqual(systems, [str(i) for i in range(self.count)])

        self.assertEqual(schemas, ['2'])

    def test_systemandschema(self):

        systems, schemas = self.dispatcher.getsystemswithschemas(
            system='1', schema='2'
        )

        self.assertEqual(systems, ['1'])

        self.assertEqual(schemas, ['2'])


if __name__ == '__main__':
    main()
