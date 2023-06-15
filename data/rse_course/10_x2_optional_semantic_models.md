# 10.x.2 (OPTIONAL):  Semantic file formats

*Estimated time for this notebook: 25 minutes*

## The dream of a semantic web

So how can we fulfill the dream of a file-format which is **self-documenting**:
universally unambiguous and interpretable?

(Of course, it might not be true, but we don't have capacity to discuss how to model reliability
and contested testimony.)

By using URIs to define a controlled vocabulary, we can be unambiguous.

But the number of different concepts to be labelled is huge: so we need a **distributed** solution:
a global structure of people defining ontologies, (with methods for resolving duplications and inconsistencies.)

Humanity has a technology that can do this: the world wide web. We've seen how many different
actors are defining ontologies.

We also need a shared semantic structure for our file formats. XML allows everyone to define their
own schema. Our universal file format requires a restriction to a basic language, which allows us
to say the things we need:

## The Triple

We can then use these defined terms to specify facts, using a URI for the subject, verb, and object of our sentence.


```python
%%writefile reaction.ttl

<http://dbpedia.org/ontology/water>
    <http://purl.obolibrary.org/obo/PATO_0001681>
        "18.01528"^^<http://purl.obolibrary.org/obo/UO_0000088>
            .
```

    Overwriting reaction.ttl


* [Water](http://dbpedia.org/ontology/water)
* [Molar mass](http://purl.obolibrary.org/obo/PATO_0001681)
* [Grams per mole](http://purl.obolibrary.org/obo/UO_0000088)

This is an unambiguous statement, consisting of a subject, a verb, and an object, each of which is either a URI or a literal value. Here, the object is a *literal* with a type.

## RDF file formats

We have used the RDF (Resource Description Framework) **semantic** format, in its "Turtle" syntactic form:

```
subject verb object .
subject2 verb2 object2 .
```

We can parse it:


```python
from rdflib import Graph

graph = Graph()
graph.parse("reaction.ttl", format="ttl")

print(len(graph))

for statement in graph:
    print(statement)
```

    1
    (rdflib.term.URIRef('http://dbpedia.org/ontology/water'), rdflib.term.URIRef('http://purl.obolibrary.org/obo/PATO_0001681'), rdflib.term.Literal('18.01528', datatype=rdflib.term.URIRef('http://purl.obolibrary.org/obo/UO_0000088')))


The equivalent in **RDF-XML** is:


```python
print(graph.serialize(format="xml"))
```

    <?xml version="1.0" encoding="UTF-8"?>
    <rdf:RDF
       xmlns:ns1="http://purl.obolibrary.org/obo/"
       xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    >
      <rdf:Description rdf:about="http://dbpedia.org/ontology/water">
        <ns1:PATO_0001681 rdf:datatype="http://purl.obolibrary.org/obo/UO_0000088">18.01528</ns1:PATO_0001681>
      </rdf:Description>
    </rdf:RDF>



We can also use namespace prefixes in Turtle:


```python
print(graph.serialize(format="ttl"))
```

    @prefix ns1: <http://purl.obolibrary.org/obo/> .

    <http://dbpedia.org/ontology/water> ns1:PATO_0001681 "18.01528"^^ns1:UO_0000088 .




## Normal forms and Triples

How do we encode the sentence "water has two hydrogen atoms" in RDF?

See [Defining N-ary Relations on the Semantic Web](https://www.w3.org/TR/swbp-n-aryRelations/) for the definitive story.

I'm not going to search carefully here for existing ontologies for the relationships we need:
later we will understand how to define these as being the same as or subclasses of concepts
in other ontologies. That's part of the value of a distributed approach: we can define
what we need, and because the Semantic Web tools make rigorous the concepts of `rdfs:sameAs` and `rdfs:subclassOf` this will be OK.

However, there's a problem. We can do:


```python
%%writefile reaction.ttl

@prefix disr: <http://www.turing.ac.uk/rsd-engineering/ontologies/reactions/> .
@prefix dbo: <http://dbpedia.org/ontology/> .
@prefix obo: <http://purl.obolibrary.org/obo/> .

dbo:water obo:PATO_0001681 "18.01528"^^obo:UO_0000088 ;
          disr:containsElement obo:CHEBI_33260 .
```

    Overwriting reaction.ttl


* [ElementalHydrogen](http://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:33260)

We've introduced the semicolon in Turtle to say two statements about the same entity. The equivalent RDF-XML is:


```python
graph = Graph()
graph.parse("reaction.ttl", format="ttl")
print(len(graph))
print(graph.serialize(format="xml"))
```

    2
    <?xml version="1.0" encoding="UTF-8"?>
    <rdf:RDF
       xmlns:disr="http://www.turing.ac.uk/rsd-engineering/ontologies/reactions/"
       xmlns:obo="http://purl.obolibrary.org/obo/"
       xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    >
      <rdf:Description rdf:about="http://dbpedia.org/ontology/water">
        <obo:PATO_0001681 rdf:datatype="http://purl.obolibrary.org/obo/UO_0000088">18.01528</obo:PATO_0001681>
        <disr:containsElement rdf:resource="http://purl.obolibrary.org/obo/CHEBI_33260"/>
      </rdf:Description>
    </rdf:RDF>



However, we can't express `hasTwo` in this way without making an infinite number of properties!

RDF doesn't have a concept of adverbs. Why not?

It turns out there's a fundamental relationship between the RDF triple and a RELATION in
the relational database model.

* The **subject** corresponds to the relational primary key.
* The **verb** (RDF "property") corresponds to the relational column name.
* The **object** corresponds to the value in the corresponding column.

We already found out that to model the relationship of atoms to molecules we needed a join table, and the
number of atoms was metadata on the join.

So, we need an entity type (RDF **class**) which describes an `ElementInMolecule`.

Fortunately, we don't have to create a universal URI for every single relationship, thanks to RDF's concept of an anonymous entity: something which is uniquely defined by its relationships.

Imagine if we had to make a URN for oxygen-in-water, hydrogen-in-water etc!


```python
%%writefile reaction.ttl

@prefix disr: <http://www.turing.ac.uk/rsd-engineering/ontologies/reactions/> .
@prefix dbo: <http://dbpedia.org/ontology/> .
@prefix obo: <http://purl.obolibrary.org/obo/> .
@prefix xs: <http://www.w3.org/2001/XMLSchema> .

dbo:water obo:PATO_0001681 "18.01528"^^obo:UO_0000088 ;
          disr:containsElement obo:CHEBI_33260 ;
          disr:hasElementQuantity [
              disr:countedElement obo:CHEBI_33260 ;
              disr:countOfElement "2"^^xs:integer
          ] .
```

    Overwriting reaction.ttl


Here we have used `[ ]` to indicate an anonymous entity, with no subject. We then define
two predicates on that subject, using properties corresponding to our column names in the join table.

Another turtle syntax for an anonymous "blank node" is this:


```python
%%writefile reaction.ttl

@prefix disr: <http://www.turing.ac.uk/rsd-engineering/ontologies/reactions/> .
@prefix dbo: <http://dbpedia.org/ontology/> .
@prefix obo: <http://purl.obolibrary.org/obo/> .
@prefix xs: <http://www.w3.org/2001/XMLSchema> .

dbo:water obo:PATO_0001681 "18.01528"^^obo:UO_0000088 ;
          disr:containsElement obo:CHEBI_33260 ;
          disr:hasElementQuantity _:a .

_:a disr:countedElement obo:CHEBI_33260 ;
    disr:countOfElement "2"^^xs:integer .
```

    Overwriting reaction.ttl


## Serialising to RDF

Here's code to write our model to Turtle:


```python
%%writefile chemistry_turtle_template.mko

@prefix disr: <http://www.turing.ac.uk/rsd-engineering/ontologies/reactions/> .
@prefix obo: <http://purl.obolibrary.org/obo/> .
@prefix xs: <http://www.w3.org/2001/XMLSchema> .

[
%for reaction in reactions:
    disr:hasReaction [
        %for molecule in reaction.reactants.molecules:
            disr:hasReactant [
                %for element in molecule.elements:
                    disr:hasElementQuantity [
                        disr:countedElement [
                            a obo:CHEBI_33259;
                            disr:symbol "${element.symbol}"^^xs:string
                        ] ;
                        disr:countOfElement "${molecule.elements[element]}"^^xs:integer
                    ];
                %endfor
                a obo:CHEBI_23367
            ] ;
        %endfor
        %for molecule in reaction.products.molecules:
            disr:hasProduct [
                %for element in molecule.elements:
                    disr:hasElementQuantity [
                        disr:countedElement [
                            a obo:CHEBI_33259;
                            disr:symbol "${element.symbol}"^^xs:string
                        ] ;
                        disr:countOfElement "${molecule.elements[element]}"^^xs:integer
                    ] ;
                %endfor
                a obo:CHEBI_23367
            ] ;
        %endfor
        a disr:reaction
    ] ;
%endfor
a disr:system
].
```

    Overwriting chemistry_turtle_template.mko


"a" in Turtle is an always available abbreviation for https://www.w3.org/1999/02/22-rdf-syntax-ns#type


We've also used:

* [Molecular entity](http://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI%3A23367)
* [Elemental molecular entity](http://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI%3A33259)

I've skipped serialising the stoichiometries: to do that correctly I also need to create a
relationship class for molecule-in-reaction.

And we've not attempted to relate our elements to their formal definitions, since our model
isn't recording this at the moment. We could add this statement later.


```python
from IPython.display import Math, display
from parsereactions import parser

with open("system.tex", "r") as texfile:
    system = parser.parse(texfile.read())
display(Math(str(system)))
```


$\displaystyle C_6H_{12}O_6 + 6O_2 \rightarrow 6CO_2 + 6H_2O\\
2H_2 + O_2 \rightarrow 2H_2O$



```python
from mako.template import Template

mytemplate = Template(filename="chemistry_turtle_template.mko")
with open("system.ttl", "w") as ttlfile:
    ttlfile.write((mytemplate.render(**vars(system))))
```


```python
!cat system.ttl
```


    @prefix disr: <http://www.turing.ac.uk/rsd-engineering/ontologies/reactions/> .
    @prefix obo: <http://purl.obolibrary.org/obo/> .
    @prefix xs: <http://www.w3.org/2001/XMLSchema> .

    [
        disr:hasReaction [
                disr:hasReactant [
                        disr:hasElementQuantity [
                            disr:countedElement [
                                a obo:CHEBI_33259;
                                disr:symbol "C"^^xs:string
                            ] ;
                            disr:countOfElement "6"^^xs:integer
                        ];
                        disr:hasElementQuantity [
                            disr:countedElement [
                                a obo:CHEBI_33259;
                                disr:symbol "H"^^xs:string
                            ] ;
                            disr:countOfElement "12"^^xs:integer
                        ];
                        disr:hasElementQuantity [
                            disr:countedElement [
                                a obo:CHEBI_33259;
                                disr:symbol "O"^^xs:string
                            ] ;
                            disr:countOfElement "6"^^xs:integer
                        ];
                    a obo:CHEBI_23367
                ] ;
                disr:hasReactant [
                        disr:hasElementQuantity [
                            disr:countedElement [
                                a obo:CHEBI_33259;
                                disr:symbol "O"^^xs:string
                            ] ;
                            disr:countOfElement "2"^^xs:integer
                        ];
                    a obo:CHEBI_23367
                ] ;
                disr:hasProduct [
                        disr:hasElementQuantity [
                            disr:countedElement [
                                a obo:CHEBI_33259;
                                disr:symbol "C"^^xs:string
                            ] ;
                            disr:countOfElement "1"^^xs:integer
                        ] ;
                        disr:hasElementQuantity [
                            disr:countedElement [
                                a obo:CHEBI_33259;
                                disr:symbol "O"^^xs:string
                            ] ;
                            disr:countOfElement "2"^^xs:integer
                        ] ;
                    a obo:CHEBI_23367
                ] ;
                disr:hasProduct [
                        disr:hasElementQuantity [
                            disr:countedElement [
                                a obo:CHEBI_33259;
                                disr:symbol "H"^^xs:string
                            ] ;
                            disr:countOfElement "2"^^xs:integer
                        ] ;
                        disr:hasElementQuantity [
                            disr:countedElement [
                                a obo:CHEBI_33259;
                                disr:symbol "O"^^xs:string
                            ] ;
                            disr:countOfElement "1"^^xs:integer
                        ] ;
                    a obo:CHEBI_23367
                ] ;
            a disr:reaction
        ] ;
        disr:hasReaction [
                disr:hasReactant [
                        disr:hasElementQuantity [
                            disr:countedElement [
                                a obo:CHEBI_33259;
                                disr:symbol "H"^^xs:string
                            ] ;
                            disr:countOfElement "2"^^xs:integer
                        ];
                    a obo:CHEBI_23367
                ] ;
                disr:hasReactant [
                        disr:hasElementQuantity [
                            disr:countedElement [
                                a obo:CHEBI_33259;
                                disr:symbol "O"^^xs:string
                            ] ;
                            disr:countOfElement "2"^^xs:integer
                        ];
                    a obo:CHEBI_23367
                ] ;
                disr:hasProduct [
                        disr:hasElementQuantity [
                            disr:countedElement [
                                a obo:CHEBI_33259;
                                disr:symbol "H"^^xs:string
                            ] ;
                            disr:countOfElement "2"^^xs:integer
                        ] ;
                        disr:hasElementQuantity [
                            disr:countedElement [
                                a obo:CHEBI_33259;
                                disr:symbol "O"^^xs:string
                            ] ;
                            disr:countOfElement "1"^^xs:integer
                        ] ;
                    a obo:CHEBI_23367
                ] ;
            a disr:reaction
        ] ;
    a disr:system
    ].



```python
graph = Graph()
graph.parse("system.ttl", format="ttl")
print(graph.serialize(format="xml"))
```

    <?xml version="1.0" encoding="UTF-8"?>
    <rdf:RDF
       xmlns:disr="http://www.turing.ac.uk/rsd-engineering/ontologies/reactions/"
       xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    >
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb15">
        <rdf:type rdf:resource="http://purl.obolibrary.org/obo/CHEBI_33259"/>
        <disr:symbol rdf:datatype="http://www.w3.org/2001/XMLSchemastring">C</disr:symbol>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb23">
        <disr:hasReactant rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb24"/>
        <disr:hasReactant rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb27"/>
        <disr:hasProduct rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb30"/>
        <rdf:type rdf:resource="http://www.turing.ac.uk/rsd-engineering/ontologies/reactions/reaction"/>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb19">
        <disr:countedElement rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb20"/>
        <disr:countOfElement rdf:datatype="http://www.w3.org/2001/XMLSchemainteger">2</disr:countOfElement>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb22">
        <rdf:type rdf:resource="http://purl.obolibrary.org/obo/CHEBI_33259"/>
        <disr:symbol rdf:datatype="http://www.w3.org/2001/XMLSchemastring">O</disr:symbol>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb21">
        <disr:countedElement rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb22"/>
        <disr:countOfElement rdf:datatype="http://www.w3.org/2001/XMLSchemainteger">1</disr:countOfElement>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb6">
        <disr:countedElement rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb7"/>
        <disr:countOfElement rdf:datatype="http://www.w3.org/2001/XMLSchemainteger">12</disr:countOfElement>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb13">
        <disr:hasElementQuantity rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb14"/>
        <disr:hasElementQuantity rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb16"/>
        <rdf:type rdf:resource="http://purl.obolibrary.org/obo/CHEBI_23367"/>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb5">
        <rdf:type rdf:resource="http://purl.obolibrary.org/obo/CHEBI_33259"/>
        <disr:symbol rdf:datatype="http://www.w3.org/2001/XMLSchemastring">C</disr:symbol>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb34">
        <rdf:type rdf:resource="http://purl.obolibrary.org/obo/CHEBI_33259"/>
        <disr:symbol rdf:datatype="http://www.w3.org/2001/XMLSchemastring">O</disr:symbol>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb1">
        <disr:hasReaction rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb2"/>
        <disr:hasReaction rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb23"/>
        <rdf:type rdf:resource="http://www.turing.ac.uk/rsd-engineering/ontologies/reactions/system"/>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb8">
        <disr:countedElement rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb9"/>
        <disr:countOfElement rdf:datatype="http://www.w3.org/2001/XMLSchemainteger">6</disr:countOfElement>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb32">
        <rdf:type rdf:resource="http://purl.obolibrary.org/obo/CHEBI_33259"/>
        <disr:symbol rdf:datatype="http://www.w3.org/2001/XMLSchemastring">H</disr:symbol>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb2">
        <disr:hasReactant rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb3"/>
        <disr:hasReactant rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb10"/>
        <disr:hasProduct rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb13"/>
        <disr:hasProduct rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb18"/>
        <rdf:type rdf:resource="http://www.turing.ac.uk/rsd-engineering/ontologies/reactions/reaction"/>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb20">
        <rdf:type rdf:resource="http://purl.obolibrary.org/obo/CHEBI_33259"/>
        <disr:symbol rdf:datatype="http://www.w3.org/2001/XMLSchemastring">H</disr:symbol>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb25">
        <disr:countedElement rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb26"/>
        <disr:countOfElement rdf:datatype="http://www.w3.org/2001/XMLSchemainteger">2</disr:countOfElement>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb9">
        <rdf:type rdf:resource="http://purl.obolibrary.org/obo/CHEBI_33259"/>
        <disr:symbol rdf:datatype="http://www.w3.org/2001/XMLSchemastring">O</disr:symbol>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb27">
        <disr:hasElementQuantity rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb28"/>
        <rdf:type rdf:resource="http://purl.obolibrary.org/obo/CHEBI_23367"/>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb29">
        <rdf:type rdf:resource="http://purl.obolibrary.org/obo/CHEBI_33259"/>
        <disr:symbol rdf:datatype="http://www.w3.org/2001/XMLSchemastring">O</disr:symbol>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb28">
        <disr:countedElement rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb29"/>
        <disr:countOfElement rdf:datatype="http://www.w3.org/2001/XMLSchemainteger">2</disr:countOfElement>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb7">
        <rdf:type rdf:resource="http://purl.obolibrary.org/obo/CHEBI_33259"/>
        <disr:symbol rdf:datatype="http://www.w3.org/2001/XMLSchemastring">H</disr:symbol>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb11">
        <disr:countedElement rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb12"/>
        <disr:countOfElement rdf:datatype="http://www.w3.org/2001/XMLSchemainteger">2</disr:countOfElement>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb16">
        <disr:countedElement rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb17"/>
        <disr:countOfElement rdf:datatype="http://www.w3.org/2001/XMLSchemainteger">2</disr:countOfElement>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb12">
        <rdf:type rdf:resource="http://purl.obolibrary.org/obo/CHEBI_33259"/>
        <disr:symbol rdf:datatype="http://www.w3.org/2001/XMLSchemastring">O</disr:symbol>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb24">
        <disr:hasElementQuantity rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb25"/>
        <rdf:type rdf:resource="http://purl.obolibrary.org/obo/CHEBI_23367"/>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb18">
        <disr:hasElementQuantity rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb19"/>
        <disr:hasElementQuantity rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb21"/>
        <rdf:type rdf:resource="http://purl.obolibrary.org/obo/CHEBI_23367"/>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb31">
        <disr:countedElement rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb32"/>
        <disr:countOfElement rdf:datatype="http://www.w3.org/2001/XMLSchemainteger">2</disr:countOfElement>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb17">
        <rdf:type rdf:resource="http://purl.obolibrary.org/obo/CHEBI_33259"/>
        <disr:symbol rdf:datatype="http://www.w3.org/2001/XMLSchemastring">O</disr:symbol>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb10">
        <disr:hasElementQuantity rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb11"/>
        <rdf:type rdf:resource="http://purl.obolibrary.org/obo/CHEBI_23367"/>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb33">
        <disr:countedElement rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb34"/>
        <disr:countOfElement rdf:datatype="http://www.w3.org/2001/XMLSchemainteger">1</disr:countOfElement>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb4">
        <disr:countedElement rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb5"/>
        <disr:countOfElement rdf:datatype="http://www.w3.org/2001/XMLSchemainteger">6</disr:countOfElement>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb3">
        <disr:hasElementQuantity rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb4"/>
        <disr:hasElementQuantity rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb6"/>
        <disr:hasElementQuantity rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb8"/>
        <rdf:type rdf:resource="http://purl.obolibrary.org/obo/CHEBI_23367"/>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb26">
        <rdf:type rdf:resource="http://purl.obolibrary.org/obo/CHEBI_33259"/>
        <disr:symbol rdf:datatype="http://www.w3.org/2001/XMLSchemastring">H</disr:symbol>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb14">
        <disr:countedElement rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb15"/>
        <disr:countOfElement rdf:datatype="http://www.w3.org/2001/XMLSchemainteger">1</disr:countOfElement>
      </rdf:Description>
      <rdf:Description rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb30">
        <disr:hasElementQuantity rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb31"/>
        <disr:hasElementQuantity rdf:nodeID="n30bcf0899e964c6c824f00a74af7f01bb33"/>
        <rdf:type rdf:resource="http://purl.obolibrary.org/obo/CHEBI_23367"/>
      </rdf:Description>
    </rdf:RDF>



We can see why the group of triples is called a *graph*: each node is an entity and each arc a property relating entities.

Note that this format is very very verbose. It is **not** designed to be a nice human-readable format.

Instead, the purpose is to maximise the capability of machines to reason with found data.

## Formalising our ontology: RDFS

Our http://www.turing.ac.uk/rsd-engineering/ontologies/reactions/ namespace now contains the following properties:

* disr:hasReaction
* disr:hasReactant
* disr:hasProduct
* disr:containsElement
* disr:countedElement
* disr:hasElementQuantity
* disr:countOfElement
* disr:symbol

And two classes:

* disr:system
* disr:reaction

We would now like to find a way to formally specify some of the relationships between these.

The **type** (`http://www.w3.org/1999/02/22-rdf-syntax-ns#type` or `a`) of the subject of hasReaction
must be `disr:system`.



[RDFS](https://www.w3.org/TR/rdf-schema/) will allow us to specify which URNs define classes and which properties,
and the domain and range (valid subjects and objects) of our properties.

For example:


```python
%%writefile turing_ontology.ttl

@prefix disr: <http://www.turing.ac.uk/rsd-engineering/ontologies/reactions/> .
@prefix obo: <http://purl.obolibrary.org/obo/> .
@prefix xs: <http://www.w3.org/2001/XMLSchema> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

disr:system a rdfs:Class .
disr:reaction a rdfs:Class .
disr:hasReaction a rdf:Property .
disr:hasReaction rdfs:domain disr:system .
disr:hasReaction rdfs:range disr:reaction .
```

    Overwriting turing_ontology.ttl


This will allow us to make our file format briefer: given this schema, if

`_:a hasReaction _:b`

then we can **infer** that

`_:a a disr:system .
_:b a disr:reaction .`

without explicitly stating it.

Obviously there's a lot more to do to define our other classes, including defining a class for our anonymous element-in-molecule nodes.

This can get very interesting:


```python
%%writefile turing_ontology.ttl

@prefix disr: <http://www.turing.ac.uk/rsd-engineering/ontologies/reactions/> .
@prefix obo: <http://purl.obolibrary.org/obo/> .
@prefix xs: <http://www.w3.org/2001/XMLSchema> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

disr:system a rdfs:Class .
disr:reaction a rdfs:Class .
disr:hasReaction a rdf:Property .
disr:hasReaction rdfs:domain disr:system .
disr:hasReaction rdfs:range disr:reaction .

disr:hasParticipant a rdf:Property .
disr:hasReactant rdfs:subPropertyOf disr:hasParticipant .
disr:hasProduct rdfs:subPropertyOf disr:hasParticipant
```

    Overwriting turing_ontology.ttl


[OWL](https://www.w3.org/TR/owl-ref/) extends RDFS even further.

Inferring additional rules from existing rules and schema is very powerful: an interesting branch of AI. (Unfortunately the [python tool](https://github.com/RDFLib/OWL-RL) for doing this automatically is currently not updated to python 3 so I'm not going to demo it. Instead, we'll see in a moment how to apply inferences to our graph to introduce new properties.)

## SPARQL

So, once I've got a bunch of triples, how do I learn anything at all from them? The language
is so verbose it seems useless!

SPARQL is a very powerful language for asking questions of knowledge bases defined in RDF triples:


```python
results = graph.query(
    """
    SELECT DISTINCT ?asymbol ?bsymbol
    WHERE {
        ?molecule disr:hasElementQuantity ?a .
        ?a disr:countedElement ?elementa .
        ?elementa disr:symbol ?asymbol .
        ?molecule disr:hasElementQuantity ?b .
        ?b disr:countedElement ?elementb .
        ?elementb disr:symbol ?bsymbol
    }
    """
)

for row in results:
    print(f"Elements {row[0]} and %s are found in the same molecule" % row)
```

    Elements C and C are found in the same molecule
    Elements C and H are found in the same molecule
    Elements C and O are found in the same molecule
    Elements H and C are found in the same molecule
    Elements H and H are found in the same molecule
    Elements H and O are found in the same molecule
    Elements O and C are found in the same molecule
    Elements O and H are found in the same molecule
    Elements O and O are found in the same molecule


We can see how this works: you make a number of statements in triple-form, but with some
quantities as dummy-variables. SPARQL finds all possible subgraphs of the triple graph which
are compatible with the statements in your query.



We can also use SPARQL to specify **inference rules**:


```python
graph.update(
    """
    INSERT { ?elementa disr:inMoleculeWith ?elementb }
    WHERE {
        ?molecule disr:hasElementQuantity ?a .
        ?a disr:countedElement ?elementa .
        ?elementa disr:symbol ?asymbol .
        ?molecule disr:hasElementQuantity ?b .
        ?b disr:countedElement ?elementb .
        ?elementb disr:symbol ?bsymbol
    }
    """
)
```


```python
graph.query(
    """
    SELECT DISTINCT ?asymbol ?bsymbol
    WHERE {
          ?elementa disr:inMoleculeWith ?elementb .
          ?elementa disr:symbol ?asymbol .
          ?elementb disr:symbol ?bsymbol
    }
    """
)

for row in results:
    print(f"Elements {row[0]} and {row[1]} are found in the same molecule")
```

    Elements C and C are found in the same molecule
    Elements C and H are found in the same molecule
    Elements C and O are found in the same molecule
    Elements H and C are found in the same molecule
    Elements H and H are found in the same molecule
    Elements H and O are found in the same molecule
    Elements O and C are found in the same molecule
    Elements O and H are found in the same molecule
    Elements O and O are found in the same molecule


Exercise for reader: express "If x is the subject of a hasReaction relationship, then x must be a system"
in SPARQL.

Exercise for reader: search for a SPARQL endpoint knowledge base in your domain.

Connect to it using [Python RDFLib's SPARQL endpoint wrapper](https://github.com/RDFLib/sparqlwrapper) and ask it a question.
