# 10.x.1 (OPTIONAL): Controlled Vocabularies

*Estimated time for this notebook: 15 minutes*

## Saying the same thing in multiple ways

What happens when someone comes across a file in our file format?
How do they know what it means?

If we can make the tag names in our model globally unique, then the meaning of the file can be made understandable not just to us, but to people and computers all over the world.

Two file formats which give the same information, in different ways, are *syntactically* distinct, but so long as they are **semantically** compatible, I can convert from one to the other.

This is the goal of the technologies introduced this lecture.

## The URI

The key concept that underpins these tools is the URI: uniform resource **indicator**.

These look like URLs:

`www.turing.ac.uk/rsd-engineering/schema/reaction/element`

But, if I load that as a web address, there's nothing there!

That's fine.

A UR**N** indicates a **name** for an entity, and, by using organisational web addresses as a prefix,
is likely to be unambiguously unique.

A URI might be a URL or a URN, or both.

## XML Namespaces

It's cumbersome to use a full URI every time we want to put a tag in our XML file.
XML defines *namespaces* to resolve this:


```python
%%writefile system.xml
<?xml version="1.0" encoding="UTF-8"?>
<system xmlns="http://www.turing.ac.uk/rsd-engineering/schema/reaction">
    <reaction>
        <reactants>
            <molecule stoichiometry="2">
                <atom symbol="H" number="2"/>
            </molecule>
            <molecule stoichiometry="1">
                <atom symbol="O" number="2"/>
            </molecule>
        </reactants>
        <products>
            <molecule stoichiometry="2">
                <atom symbol="H" number="2"/>
                <atom symbol="O" number="1"/>
            </molecule>
        </products>
    </reaction>
</system>
```

    Overwriting system.xml



```python
from lxml import etree

with open("system.xml") as xmlfile:
    tree = etree.parse(xmlfile)
```


```python
print(etree.tostring(tree, pretty_print=True, encoding=str))
```

    <system xmlns="http://www.turing.ac.uk/rsd-engineering/schema/reaction">
        <reaction>
            <reactants>
                <molecule stoichiometry="2">
                    <atom symbol="H" number="2"/>
                </molecule>
                <molecule stoichiometry="1">
                    <atom symbol="O" number="2"/>
                </molecule>
            </reactants>
            <products>
                <molecule stoichiometry="2">
                    <atom symbol="H" number="2"/>
                    <atom symbol="O" number="1"/>
                </molecule>
            </products>
        </reaction>
    </system>



Note that our previous XPath query no longer finds anything.


```python
tree.xpath("//molecule/atom[@number='1']/@symbol")
```




    []




```python
namespaces = {"r": "http://www.turing.ac.uk/rsd-engineering/schema/reaction"}
```


```python
tree.xpath("//r:molecule/r:atom[@number='1']/@symbol", namespaces=namespaces)
```




    ['O']



Note the prefix `r` used to bind the namespace in the query: any string will do - it's just a dummy variable.

The above file specified our namespace as a default namespace: this is like doing `from numpy import *` in python.

It's often better to bind the namespace to a prefix:


```python
%%writefile system.xml
<?xml version="1.0" encoding="UTF-8"?>
<r:system xmlns:r="http://www.turing.ac.uk/rsd-engineering/schema/reaction">
    <r:reaction>
        <r:reactants>
            <r:molecule stoichiometry="2">
                <r:atom symbol="H" number="2"/>
            </r:molecule>
            <r:molecule stoichiometry="1">
                <r:atom symbol="O" number="2"/>
            </r:molecule>
        </r:reactants>
        <r:products>
            <r:molecule stoichiometry="2">
                <r:atom symbol="H" number="2"/>
                <r:atom symbol="O" number="1"/>
            </r:molecule>
        </r:products>
    </r:reaction>
</r:system>
```

    Overwriting system.xml


## Namespaces and Schema

It's a good idea to serve the schema itself from the URI of the namespace treated as a URL, but it's *not a requirement*: it's a URN not necessarily a URL!



```python
%%writefile reactions.xsd

<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
    targetNamespace="http://www.turing.ac.uk/rsd-engineering/schema/reaction"
    xmlns:r="http://www.turing.ac.uk/rsd-engineering/schema/reaction">

<xs:element name="atom">
    <xs:complexType>
        <xs:attribute name="symbol" type="xs:string"/>
        <xs:attribute name="number" type="xs:integer"/>
    </xs:complexType>
</xs:element>

<xs:element name="molecule">
    <xs:complexType>
        <xs:sequence>
            <xs:element ref="r:atom" maxOccurs="unbounded"/>
        </xs:sequence>
        <xs:attribute name="stoichiometry" type="xs:integer"/>
    </xs:complexType>
</xs:element>

<xs:element name="reactants">
    <xs:complexType>
        <xs:sequence>
            <xs:element ref="r:molecule" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
</xs:element>

<xs:element name="products">
    <xs:complexType>
        <xs:sequence>
            <xs:element ref="r:molecule" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
</xs:element>

<xs:element name="reaction">
    <xs:complexType>
        <xs:sequence>
            <xs:element ref="r:reactants"/>
            <xs:element ref="r:products"/>
        </xs:sequence>
    </xs:complexType>
</xs:element>

<xs:element name="system">
    <xs:complexType>
        <xs:sequence>
            <xs:element ref="r:reaction" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
</xs:element>

</xs:schema>
```

    Overwriting reactions.xsd


Note we're now defining the target namespace for our schema.


```python
with open("reactions.xsd") as xsdfile:
    schema_xsd = xsdfile.read()
schema = etree.XMLSchema(etree.XML(schema_xsd))
```


```python
parser = etree.XMLParser(schema=schema)
```


```python
with open("system.xml") as xmlfile:
    tree = etree.parse(xmlfile, parser)
    print(tree)
```

    <lxml.etree._ElementTree object at 0x1107f2780>


Note the power of binding namespaces when using XML files addressing more than one namespace.
Here, we can clearly see which variables are part of the schema defining XML schema itself (bound to `xs`)
and the schema for our file format (bound to `r`)

## Using standard vocabularies

The work we've done so far will enable someone who comes across our file format to track down something about its significance, by following the URI in the namespace. But it's still somewhat ambiguous. The word "element" means (at least) two things: an element tag in an XML document, and a chemical element. (It also means a heating element in a toaster, and lots of other things.)

To make it easier to not make mistakes as to the meaning of **found data**, it is helpful to use
standardised namespaces that already exist for the concepts our file format refers to.

So that when somebody else picks up one of our data files, the meaning of the stuff it describes is obvious. In this example, it would be hard to get it wrong, of course, but in general, defining file formats so that they are meaningful as found data should be desirable.

For example, the concepts in our file format are already part of the "DBPedia ontology",
among others. So, we could redesign our file format to exploit this, by referencing for example [https://dbpedia.org/ontology/ChemicalCompound](https://dbpedia.org/ontology/ChemicalCompound):


```python
%%writefile chemistry_template3.mko
<?xml version="1.0" encoding="UTF-8"?>
<system xmlns="https://www.turing.ac.uk/rsd-engineering/schema/reaction"
        xmlns:dbo="https://dbpedia.org/ontology/">
%for reaction in reactions:
    <reaction>
        <reactants>
        %for molecule in reaction.reactants.molecules:
            <dbo:ChemicalCompound stoichiometry="${reaction.reactants.molecules[molecule]}">
                %for element in molecule.elements:
                    <dbo:ChemicalElement symbol="${element.symbol}"
                                         number="${molecule.elements[element]}"/>
                %endfor
            </dbo:ChemicalCompound>
        %endfor
        </reactants>
        <products>
        %for molecule in reaction.products.molecules:
            <dbo:ChemicalCompound stoichiometry="${reaction.products.molecules[molecule]}">
            %for element in molecule.elements:
                <dbo:ChemicalElement symbol="${element.symbol}"
                                     number="${molecule.elements[element]}"/>
            %endfor
            </dbo:ChemicalCompound>
        %endfor
        </products>
    </reaction>
%endfor
</system>
```

    Writing chemistry_template3.mko


However, this won't work properly, because it's not up to us to define the XML schema for somebody
else's entity type: and an XML schema can only target one target namespace.

Of course we should use somebody else's file format for chemical reaction networks: compare [SBML](http://sbml.org) for example. We already know not to reinvent the wheel - and this whole lecture series is just reinventing the wheel for pedagogical purposes. But what if we've already got a bunch of data in our own format. How can we lock down the meaning of our terms?

So, we instead need to declare that our `r:element` *represents the same concept* as `dbo:ChemicalElement`. To do this formally we will need the concepts from the next lecture, specifically `rdf:sameAs`, but first, let's understand the idea of an ontology.

## Taxonomies and ontologies

An Ontology (in computer science terms) is two things: a **controlled vocabulary** of entities (a set of URIs in a namespace), the definitions thereof, and the relationships between them.

People often casually use the word to mean any formalised taxonomy, but the relation of terms in the ontology to the concepts they represent, and the relationships between them, are also critical.

Have a look at another example: [https://dublincore.org/documents/dcmi-terms/](https://dublincore.org/documents/dcmi-terms/#terms-creator)

Note each concept is a URI, but some of these are also stated to be subclasses or superclasses of the others.

Some are properties of other things, and the domain and range of these verbs are also stated.

Why is this useful for us in discussing file formats?

One of the goals of the **semantic web** is to create a way to make file formats which are universally meaningful
as found data: if I have a file format defined using any formalised ontology, then by tracing statements
through *rdf:sameAs* relationships, I should be able to reconstruct the information I need.

That will be the goal of the next lecture.
