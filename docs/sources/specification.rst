=============
Specification
=============

This document presents mechanisms and algorithms useful to understand reqi and to write your own drivers.

-----------
description
-----------

The reqi system processes crud requests in dispatching them to (several) sub-system(s).

-----------
Dispatching
-----------

First, you can see a request such as a Abstract Syntax Tree.

Every node has a name which is composed of those elements.

Node name
=========

``[[system '/'] model '/'] property``

..remark:: in order to ensure than the character '/' is not in system, model or node, three identifiers are encoded with an url encnding.

where system, model and property are identifiers (corresponding to the regex ``\w+``).

system and model are obsolete because reqi might be able to resolve them at runtime, depending on system descriptions.

Examples of node names :

- car.color : designates the property `color` of the model `car`.
- > : property '>' which might be resolved by a default model ``operator``.

Let two functions useful to identify properties from a name:

.. csv-table::
	- name, description

	- getidentifiers(name), "get three system, model and property identifiers from a request name.""
	- getname(system=None, model=None, property=None), "get a request name from system, model and property identifiers.""

Node systems
============

Some nodes are composed of other nodes. For example, the function 'mean' is composed of other properties and numerical values.

In such case, we can define the function ``getsystems`` which returns all systems used by a node. The default system is ``None``, and can be understood by all systems.

Once systems are identified, the reqi dispatcher will use this property to dispatch requests to all systems...

Request processing
==================

The resquest processing follows two steps.

1 - request dispatching.
2 - request resolving.

Dispatching
-----------

The request dispatching consists to get sub-requests and give them to respective systems.

Let methods:

- csv-table::

	name, description

	getsystems(request), get all request systems
	getcontent(request), get all request content
	getrequest(request, system), get all sub requests related to input system.

.. code-block:: python

	def getsystems(request)

Three cases : getsystems(Node)

.. csv-table::

	systems, process

	0, custom resolution.
	1, send the request to the right system.
	2+, several systems, parse child nodes and repeat the dispatching where the parent node is the root.



