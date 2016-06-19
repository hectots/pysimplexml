# pySimpleXML

pySimpleXML parses XML into a structure that is easy to traverse using common
object and collections notation.

An XML file like so:

```xml
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
```

Can be parsed into an object using the parse function:

```python
>>> store = pysimplexml.parse("store.xml")
```

Elements in the array are nested objects within the root object (eg. store) forming 
a tree structure. Elements within the root are list of Nodes. Attributes 
are keys on those objects. For example:

```python
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
```

To get the value of a node use getValue(), which uses automatic type 
conversion to return the appropiate type. For example:

```xml
<!-- File: config.xml -->
<config>
    <id>1450060</id>
    <name>Project Alpha</name>
    <version>2.7</version>
    <tested>true</tested>
</config>
```

```python
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
```

You can switch automatic type conversion off by passing False to getValue()
(eg. node.getValue(False)).