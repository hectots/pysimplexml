# File: pysimplexml.py
# Summmary: A simpler version of SimpleXML for Python.
# Web-Site: http://code.google.com/p/pysimplexml/

#TODO: Use custom class (NodeList?) instead of list() for handling collections of nodes.
#TODO: Add XPath support

"""
pySimpleXML parses XML into a structure that is easy to traverse using common
object and collections notation.

An XML file like so:

<store>
	<product category="Vehicles">
		<name>Car</name>
		<price>$5,000</price>
	</product>
	<product category="Electronics">
		<name>Video Game Console</name>
		<price>$250</price>
	</product>
</store>

Can be parsed into an object using the parse function:

>> store = pysimplexml.parse("store.xml")

Elements in the array are nested objects within the root object (eg. store) forming 
a tree structure. Elements within the root are list of Nodes. Attributes 
are keys on those objects. For example:

>>> print store.product[0].name
Car
>>> print store.product[0].price
$5,000
>>> for product in store.product:
...     print product.name[0], product.price[0]
... 
Car $5,000
Video Game Console $250
>>> print store.product[0]["category"]
Vehicles
>>> for product in store.product:
...     print product["category"]
... 
Vehicles
Electronics
>>>

To get the value of a node use getValue(), which uses automatic type 
conversion to return the appropiate type. For example:

<!-- File: config.xml -->
<config>
	<id>1450060</id>
	<name>Project Alpha</name>
	<version>2.7</version>
	<tested>true</tested>
</config>

>>> config = pysimplexml.parse("config.xml")
>>> config.id[0].getValue()
1450060
>>> config.name[0].getValue()
u'Project Alpha'
>>> config.version[0].getValue()
2.7000000000000002
>>> config.tested[0].getValue()
True
>>> config.id[0].getValue() + 1000
1451060
>>> if config.tested[0].getValue():
...     print "It's tested alright!"
... 
It's tested alright!
>>>

You can switch automatic type conversion off by passing False to getValue()
(eg. node.getValue(False)).
"""

import xml.sax		

class Node(dict):
	def __init__(self, tag, arg):
		dict.__init__(self, arg)
		
		self.tag = tag
	
	def __str__(self):
		if self.__dict__.has_key('value'):
			return self.value.strip()
		else:
			return ""
	
	def __repr__(self):
		return "<Node '" + self.tag + "'>"
	
	def getValue(self, automatic_type_conversion=True):
		"""Returns the value of the node. If automatic_type_conversion is True
		(default) then the value will be converted to the correspoding type."""
		self.value = self.value.strip()
		if automatic_type_conversion:
			if self.value[0].isdigit() or (self.value[0] in '-+' and self.value[1].isdigit()):
				if self.value.find('.') != -1:
					return float(self.value)
				else:
					return int(self.value)
			if self.value.lower() == "true" or self.value.lower() == "false":
				return bool(self.value.lower().capitalize())
		return self.value
	
	def hasAttribute(self, name):
		"""Check if the none have an attribute with the name specified."""
		return self.has_key(name)
	
	def hasChild(self, name):
		"""Check if the none have a child with the name specified."""
		return hasattr(self, name)
	
	def hasChildren(self):
		"""Returns true if the node has children; false otherwise."""
		for member in self.__dict__.values():
			if isinstance(member, Node):
				return True
		return False
	
	def getChildren(self, childs_filter=None):
		"""Returns a list of the children of this node."""
		childs = []
		for member in self.__dict__.values():
			if isinstance(member, Node):
				childs.append(member)
			elif isinstance(member, list):
				if all(map(lambda m: isinstance(m, Node), member)):
					childs.append(member)
		
		if childs_filter is not None:
			childs = filter(childs_filter, childs)
		
		return childs

class SimpleXmlHandler(xml.sax.ContentHandler):
	def startDocument(self):
		self.root = None
		self.MARKER = ">"
	
	def endDocument(self):
		pass
	
	def startElement(self, tag, attrs):
		if self.root is None: # initialize root element
			self.root = Node(tag, attrs)
			self.current_node = self.root
			self.ancestors = {tag:self.root}
		else:
			if not self.ancestors.has_key(tag):
				self.ancestors[tag] = self.current_node
			else:
				multiplier = 1
				while self.ancestors.has_key(tag + (self.MARKER * multiplier)):
					multiplier += 1
				self.ancestors[tag + (self.MARKER * multiplier)] = self.current_node
			
			if hasattr(self.current_node, tag): # if a child with that name exists in the current node append the new node
				self.current_node.__getattribute__(tag).append(Node(tag, attrs))
				self.current_node = self.current_node.__getattribute__(tag)[-1]
			else: # else create a new child node list
				self.current_node.__setattr__(tag, [Node(tag, attrs)])
				self.current_node = self.current_node.__getattribute__(tag)[0]
	
	def endElement(self, tag):
		if self.ancestors.has_key(tag + self.MARKER):
			tag += self.MARKER
			while self.ancestors.has_key(tag + self.MARKER):
				tag += self.MARKER
		
		self.current_node = self.ancestors[tag]
		del self.ancestors[tag]
		
	def characters(self, data):
		if hasattr(self.current_node, 'value'):
			self.current_node.value += data
		else:
			self.current_node.value = data

def parse(filename):
	handler = SimpleXmlHandler()
	xml.sax.parse(filename, handler)
	return handler.root