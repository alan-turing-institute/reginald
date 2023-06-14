# 10.4 Markup Languages

*Estimated time for this notebook: 10 minutes*

XML and its relatives (including HTML) are based on the idea of *marking up* content with labels on its purpose:
    
    <name>James</name> is a <job>Programmer</job>

We want to represent the chemical reactions:
$C_6H_{12}O_6 + 6O_2 \rightarrow 6CO_2 + 6H_2O\\ 
2H_2 + O_2 \rightarrow 2H_2O$

In xml this might look like:


```python
%%writefile system.xml
<?xml version="1.0" encoding="UTF-8"?>
<system>
    <reaction>
        <reactants>
            <molecule stoichiometry="1">
                <atom symbol="C" number="6"/>
                <atom symbol="H" number="12"/>
                <atom symbol="O" number="6"/>
            </molecule>
            <molecule stoichiometry="6">
                <atom symbol="O" number="2"/>
            </molecule>
        </reactants>
        <products>
            <molecule stoichiometry="6">
                <atom symbol="C" number="1"/>
                <atom symbol="O" number="2"/>
            </molecule>
            <molecule stoichiometry="6">
                <atom symbol="H" number="2"/>
                <atom symbol="O" number="1"/>
            </molecule>
        </products>
    </reaction>
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


Markup languages are verbose (jokingly called the "angle bracket tax") but very clear.

## Parsing XML

XML is normally parsed by building a tree-structure of all the `tags` in the file, called a `DOM` or Document Object Model.


```python
from lxml import etree

with open("system.xml", "r") as xmlfile:
    tree = etree.parse(xmlfile)
print(etree.tostring(tree, pretty_print=True, encoding=str))
```

    <system>
        <reaction>
            <reactants>
                <molecule stoichiometry="1">
                    <atom symbol="C" number="6"/>
                    <atom symbol="H" number="12"/>
                    <atom symbol="O" number="6"/>
                </molecule>
                <molecule stoichiometry="6">
                    <atom symbol="O" number="2"/>
                </molecule>
            </reactants>
            <products>
                <molecule stoichiometry="6">
                    <atom symbol="C" number="1"/>
                    <atom symbol="O" number="2"/>
                </molecule>
                <molecule stoichiometry="6">
                    <atom symbol="H" number="2"/>
                    <atom symbol="O" number="1"/>
                </molecule>
            </products>
        </reaction>
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
    


We can navigate the tree, with each **element** being an iterable yielding its children: 


```python
tree.getroot()[0][0][1].attrib["stoichiometry"]
```




    '6'



## Searching XML

`xpath` is a sophisticated tool for searching XML DOMs:

There's a good explanation of how it works here: https://www.w3schools.com/xml/xml_xpath.asp but the basics are reproduced below.

| XPath Expression | Result |
| :- | :- |
| `/bookstore/book[1]` | Selects the first `book` that is the child of a `bookstore` |
| `/bookstore/book[last()]` | Selects the last `book` that is the child of a `bookstore` |
| `/bookstore/book[last()-1]` | Selects the last but one `book` that is the child of a `bookstore` |
| `/bookstore/book[position()<3]`| Selects the first two `book`s that are children of a `bookstore` |
| `//title[@lang]` | Selects all `title`s that have an attribute named "lang" |
| `//title[@lang='en']` | Selects all `title`s that have a "lang" attribute with a value of "en" |
| `/bookstore/book[price>35.00]` | Selects all `book`s that are children of a `bookstore` and have a `price` with a value greater than 35.00 |
| `/bookstore/book[price>35.00]/title` | Selects all the `title`s of a `book` of a `bookstore` that have a `price` with a value greater than 35.00 |


```python
# For all molecules
# ... with a child atom whose number attribute is '1'
# ... return the symbol attribute of that child
tree.xpath("//molecule/atom[@number='1']/@symbol")
```




    ['C', 'O', 'O']



It is useful to understand grammars like these using the "FOR-LET-WHERE-ORDER-RETURN" (pronounced Flower) model.

The above says: "For element in molecules where number is one, return symbol", roughly equivalent to `[element.symbol for element in molecule for molecule in document if element.number==1]` in Python.

## Transforming XML : XSLT

Two technologies (XSLT and XQUERY) provide capability to produce text output from an XML tree.

We'll look at XSLT as support is more widespread, including in the python library we're using. XQuery is probably easier to use and understand, but with less support.

However, XSLT is a beautiful functional declarative language, once you read past the angle-brackets.

Here's an XSLT to transform our reaction system into a LaTeX representation:


```python
%%writefile xmltotex.xsl

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" indent="yes" omit-xml-declaration="yes" />
        
    <!-- Decompose reaction into "reactants \rightarrow products" -->
    <xsl:template match="//reaction">
        <xsl:apply-templates select="reactants"/>
        <xsl:text> \rightarrow </xsl:text>
        <xsl:apply-templates select="products"/>
        <xsl:text>\\&#xa;</xsl:text>
    </xsl:template>
        
    <!-- For a molecule anywhere except the first position write " + " and the number of molecules-->
    <xsl:template match="//molecule[position()!=1]">
        <xsl:text> + </xsl:text>
        <xsl:apply-templates select="@stoichiometry"/>
        <xsl:apply-templates/>
    </xsl:template>

    <!-- For a molecule in first position write the number of molecules -->
    <xsl:template match="//molecule[position()=1]">
        <xsl:apply-templates select="@stoichiometry"/>
        <xsl:apply-templates/>
    </xsl:template>

    <!-- If the stoichiometry is one then ignore it -->
    <xsl:template match="@stoichiometry[.='1']"/>
    
    <!-- Otherwise, use the default template for attributes, which is just to copy value -->
    
    <!-- Decompose element into "symbol number" -->
    <xsl:template match="//atom">
        <xsl:value-of select="@symbol"/>
        <xsl:apply-templates select="@number"/>
    </xsl:template>
        
    <!-- If the number of elements/molecules is one then ignore it -->        
    <xsl:template match="@number[.=1]"/>
    
    <!-- ... otherwise replace it with "_ value" -->        
    <xsl:template match="@number[.!=1][10>.]">
        <xsl:text>_</xsl:text>
        <xsl:value-of select="."/>
    </xsl:template>
        
    <!-- If a number is greater than 10 then wrap it in "{}" -->        
    <xsl:template match="@number[.!=1][.>9]">
        <xsl:text>_{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>          
    </xsl:template>
        
    <!-- Do not copy input whitespace to output -->
    <xsl:template match="text()" />
</xsl:stylesheet>
```

    Overwriting xmltotex.xsl



```python
with open("xmltotex.xsl") as xslfile:
    transform_xsl = xslfile.read()
transform = etree.XSLT(etree.XML(transform_xsl))
```


```python
print(str(transform(tree)))
```

    C_6H_{12}O_6 + 6O_2 \rightarrow 6CO_2 + 6H_2O\\
    2H_2 + O_2 \rightarrow 2H_2O\\
    
    


Which is back to the LaTeX representation of our reactions.

## Validating XML : Schema

XML Schema is a way to define how an XML file is allowed to be: which attributes and tags should exist where.
    
You should always define one of these when using an XML file format.


```python
%%writefile reactions.xsd

<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">

<xs:element name="atom">
    <xs:complexType>
        <xs:attribute name="symbol" type="xs:string"/>
        <xs:attribute name="number" type="xs:integer"/>
    </xs:complexType>
</xs:element>
    
<xs:element name="molecule">
    <xs:complexType>
        <xs:sequence>
            <xs:element ref="atom" maxOccurs="unbounded"/>
        </xs:sequence>
        <xs:attribute name="stoichiometry" type="xs:integer"/>
    </xs:complexType>
</xs:element>
    
<xs:element name="reaction">
    <xs:complexType>
        <xs:sequence>
            <xs:element name="reactants">
                <xs:complexType>
                    <xs:sequence>
                        <xs:element ref="molecule" maxOccurs="unbounded"/>
                    </xs:sequence>
                </xs:complexType>
            </xs:element>
            <xs:element name="products">
                <xs:complexType>
                    <xs:sequence>
                        <xs:element ref="molecule" maxOccurs="unbounded"/>
                    </xs:sequence>
                </xs:complexType>
            </xs:element>
        </xs:sequence>
    </xs:complexType>
</xs:element>

<xs:element name="system">
    <xs:complexType>
        <xs:sequence>
            <xs:element ref="reaction" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
</xs:element>
    
</xs:schema>
```

    Overwriting reactions.xsd



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
# For all atoms return their symbol attribute
tree.xpath("//atom/@symbol")
```




    ['C', 'H', 'O', 'O', 'C', 'O', 'H', 'O', 'H', 'O', 'H', 'O']



Compare parsing something that is not valid under the schema:


```python
%%writefile invalid_system.xml

<system>
    <reaction>
        <reactants>
            <molecule stoichiometry="two">
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

    Overwriting invalid_system.xml



```python
try:
    with open("invalid_system.xml") as xmlfile:
        tree = etree.parse(xmlfile, parser)
    tree.xpath("//element//@symbol")
except etree.XMLSyntaxError as e:
    print(e)
```

    Element 'molecule', attribute 'stoichiometry': 'two' is not a valid value of the atomic type 'xs:integer'. (<string>, line 0)


This shows us that the validation has failed and why.
