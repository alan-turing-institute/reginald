# 10.x.0 (OPTIONAL):  Domain specific languages

*Estimated time for this notebook: 25 minutes*

## Lex and Yacc

Let's go back to our nice looks-like LaTeX file format:


```python
%%writefile system.py


class Element:
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return str(self.symbol)


class Molecule:
    def __init__(self):
        self.elements = {}  # Map from element to number of that element in the molecule

    def add_element(self, element, number):
        if not isinstance(element, Element):
            element = Element(element)
        self.elements[element] = number

    @staticmethod
    def as_subscript(number):
        if number == 1:
            return ""
        if number < 10:
            return "_" + str(number)
        return "_{" + str(number) + "}"

    def __str__(self):
        return "".join(
            [
                str(element) + Molecule.as_subscript(self.elements[element])
                for element in self.elements
            ]
        )


class Side:
    def __init__(self):
        self.molecules = {}

    def add(self, reactant, stoichiometry):
        self.molecules[reactant] = stoichiometry

    @staticmethod
    def print_if_not_one(number):
        if number == 1:
            return ""
        else:
            return str(number)

    def __str__(self):
        return " + ".join(
            [
                Side.print_if_not_one(self.molecules[molecule]) + str(molecule)
                for molecule in self.molecules
            ]
        )


class Reaction:
    def __init__(self):
        self.reactants = Side()
        self.products = Side()

    def __str__(self):
        return str(self.reactants) + " \\rightarrow " + str(self.products)


class System:
    def __init__(self):
        self.reactions = []

    def add_reaction(self, reaction):
        self.reactions.append(reaction)

    def __str__(self):
        return "\\\\ \n".join(map(str, self.reactions))
```

    Writing system.py



```python
from system import Element, Molecule, Reaction, System

s2 = System()

c = Element("C")
o = Element("O")
h = Element("H")

co2 = Molecule()
co2.add_element(c, 1)
co2.add_element(o, 2)

h2o = Molecule()
h2o.add_element(h, 2)
h2o.add_element(o, 1)

o2 = Molecule()
o2.add_element(o, 2)

h2 = Molecule()
h2.add_element(h, 2)

glucose = Molecule()
glucose.add_element(c, 6)
glucose.add_element(h, 12)
glucose.add_element(o, 6)

combustion_glucose = Reaction()
combustion_glucose.reactants.add(glucose, 1)
combustion_glucose.reactants.add(o2, 6)
combustion_glucose.products.add(co2, 6)
combustion_glucose.products.add(h2o, 6)
s2.add_reaction(combustion_glucose)


combustion_hydrogen = Reaction()
combustion_hydrogen.reactants.add(h2, 2)
combustion_hydrogen.reactants.add(o2, 1)
combustion_hydrogen.products.add(h2o, 2)
s2.add_reaction(combustion_hydrogen)

print(s2)
```

    C_6H_{12}O_6 + 6O_2 \rightarrow 6CO_2 + 6H_2O\\
    2H_2 + O_2 \rightarrow 2H_2O



```python
from IPython.display import Math, display

display(Math(str(s2)))
```


$\displaystyle C_6H_{12}O_6 + 6O_2 \rightarrow 6CO_2 + 6H_2O\\
2H_2 + O_2 \rightarrow 2H_2O$


How might we write a parser for this? Clearly we'll encounter the problems we previously solved in ensuring each molecule is the
and atom only gets one object instance, but we solved this by using an appropriate primary key. (The above implementation is designed to make this easy, learning from the previous lecture.)

But we'll also run into a bunch of problems which are basically string parsing : noting, for example, that `_2` and `_{12}` make a number of atoms in a molecule, or that `+` joins molecules.

This will be very hard to do with straightforward python string processing.

Instead, we will use a tool called `ply` (Python Lex-Yacc) which contains `Lex` (for generating lexical analysers) and `Yacc` (Yet Another Compiler-Compiler). Together these allow us to define the **grammar** of our file format.

The theory of "context free grammars" is rich and deep, and we will just scratch the surface here.

## Tokenising with Lex

First, we need to turn our file into a "token stream", using regular expressions to match the kinds of symbol in our source:


```python
%%writefile lexreactions.py

from ply import lex

tokens = (
    "ELEMENT",
    "NUMBER",
    "SUBSCRIPT",
    "LBRACE",
    "RBRACE",
    "PLUS",
    "ARROW",
    "NEWLINE",
    "TEXNEWLINE",
)

# Tokens
t_PLUS = r"\+"
t_SUBSCRIPT = r"_"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_TEXNEWLINE = r"\\\\"
t_ARROW = r"\\rightarrow"
t_ELEMENT = r"[A-Z][a-z]?"
t_NEWLINE = r"\n+"


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


t_ignore = " "


def t_error(t):
    print(f"Did not recognise character '{t.value[0]:s}' as part of a valid token")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
```

    Writing lexreactions.py



```python
from lexreactions import lexer
```


```python
tokens = []
lexer.input(str(s2))
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    tokens.append(tok)
```


```python
print(str(s2))
```

    C_6H_{12}O_6 + 6O_2 \rightarrow 6CO_2 + 6H_2O\\
    2H_2 + O_2 \rightarrow 2H_2O



```python
tokens
```




    [LexToken(ELEMENT,'C',1,0),
     LexToken(SUBSCRIPT,'_',1,1),
     LexToken(NUMBER,6,1,2),
     LexToken(ELEMENT,'H',1,3),
     LexToken(SUBSCRIPT,'_',1,4),
     LexToken(LBRACE,'{',1,5),
     LexToken(NUMBER,12,1,6),
     LexToken(RBRACE,'}',1,8),
     LexToken(ELEMENT,'O',1,9),
     LexToken(SUBSCRIPT,'_',1,10),
     LexToken(NUMBER,6,1,11),
     LexToken(PLUS,'+',1,13),
     LexToken(NUMBER,6,1,15),
     LexToken(ELEMENT,'O',1,16),
     LexToken(SUBSCRIPT,'_',1,17),
     LexToken(NUMBER,2,1,18),
     LexToken(ARROW,'\\rightarrow',1,20),
     LexToken(NUMBER,6,1,32),
     LexToken(ELEMENT,'C',1,33),
     LexToken(ELEMENT,'O',1,34),
     LexToken(SUBSCRIPT,'_',1,35),
     LexToken(NUMBER,2,1,36),
     LexToken(PLUS,'+',1,38),
     LexToken(NUMBER,6,1,40),
     LexToken(ELEMENT,'H',1,41),
     LexToken(SUBSCRIPT,'_',1,42),
     LexToken(NUMBER,2,1,43),
     LexToken(ELEMENT,'O',1,44),
     LexToken(TEXNEWLINE,'\\\\',1,45),
     LexToken(NEWLINE,'\n',1,48),
     LexToken(NUMBER,2,1,49),
     LexToken(ELEMENT,'H',1,50),
     LexToken(SUBSCRIPT,'_',1,51),
     LexToken(NUMBER,2,1,52),
     LexToken(PLUS,'+',1,54),
     LexToken(ELEMENT,'O',1,56),
     LexToken(SUBSCRIPT,'_',1,57),
     LexToken(NUMBER,2,1,58),
     LexToken(ARROW,'\\rightarrow',1,60),
     LexToken(NUMBER,2,1,72),
     LexToken(ELEMENT,'H',1,73),
     LexToken(SUBSCRIPT,'_',1,74),
     LexToken(NUMBER,2,1,75),
     LexToken(ELEMENT,'O',1,76)]



Note that the parser will reject invalid tokens:


```python
lexer.input("""2H_2 + O_2 \\leftarrow 2H_2O""")
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)
```

    LexToken(NUMBER,2,1,0)
    LexToken(ELEMENT,'H',1,1)
    LexToken(SUBSCRIPT,'_',1,2)
    LexToken(NUMBER,2,1,3)
    LexToken(PLUS,'+',1,5)
    LexToken(ELEMENT,'O',1,7)
    LexToken(SUBSCRIPT,'_',1,8)
    LexToken(NUMBER,2,1,9)
    Did not recognise character '\' as part of a valid token
    Did not recognise character 'l' as part of a valid token
    Did not recognise character 'e' as part of a valid token
    Did not recognise character 'f' as part of a valid token
    Did not recognise character 't' as part of a valid token
    Did not recognise character 'a' as part of a valid token
    Did not recognise character 'r' as part of a valid token
    Did not recognise character 'r' as part of a valid token
    Did not recognise character 'o' as part of a valid token
    Did not recognise character 'w' as part of a valid token
    LexToken(NUMBER,2,1,22)
    LexToken(ELEMENT,'H',1,23)
    LexToken(SUBSCRIPT,'_',1,24)
    LexToken(NUMBER,2,1,25)
    LexToken(ELEMENT,'O',1,26)


## Writing a grammar

So, how do we express our algebra for chemical reactions as a grammar?

We write a series of production rules, expressing how a system is made up of equations, an equation is made up of molecules etc:

```
system : equation
system : system TEXNEWLINE NEWLINE equation
equation : side ARROW side
side : molecules
molecules : molecule
molecules : NUMBER molecule
side : side PLUS molecules
molecule : countedelement
countedelement : ELEMENT
countedelement : ELEMENT atomcount
molecule : molecule countedelement
atomcount : SUBSCRIPT NUMBER
atomcount : SUBSCRIPT LBRACE NUMBER RBRACE
```

Note how we right that a system is made of more than one equation:

```
system : equation # A system could be one equation
system : system NEWLINE equation # Or it could be a system then an equation
```

... which implies, recursively, that a system could also be:

```
system: equation NEWLINE equation NEWLINE equation ...
```

This is an **incredibly** powerful idea. The full grammar for Python 3 can be defined in only a few hundred lines of specification: https://docs.python.org/3/reference/grammar.html

## Parsing with Yacc

A parser defined with Yacc builds up the final object, by breaking down the
file according to the rules of the grammar, and then building up objects
as the individual tokens coalesce into the full grammar.

Here, we will for clarity not attempt to solve the problem of having multiple molecule instances for the same molecule - the normalisation problem solved last lecture.

In Yacc, each grammar rule is defined by a Python function where the docstring for the function contains the appropriate grammar specification.

Each function accepts an argument `p` that is a list of symbols in the grammar. It must implement the actions of that rule. For example:

```python
def p_expression_plus(p):
    'expression : expression PLUS term'
    #   ^            ^        ^    ^
    #  p[0]         p[1]     p[2] p[3]
    p[0] = p[1] + p[3]
```


```python
%%writefile parsereactions.py

# Yacc example
import ply.yacc as yacc

# Get the components of our system
from system import Element, Molecule, Side, Reaction, System

# Get the token map from the lexer.  This is required.
from lexreactions import tokens


def p_expression_system(p):
    "system : equation"
    p[0] = System()
    p[0].add_reaction(p[1])


def p_expression_combine_system(p):
    "system : system TEXNEWLINE NEWLINE equation"
    p[0] = p[1]
    p[0].add_reaction(p[4])


def p_equation(p):
    "equation : side ARROW side"
    p[0] = Reaction()
    p[0].reactants = p[1]
    p[0].products = p[3]


def p_side(p):
    "side : molecules"
    p[0] = Side()
    p[0].add(p[1][0], p[1][1])


def p_molecules(p):
    "molecules : molecule"
    p[0] = (p[1], 1)


def p_stoichiometry(p):
    "molecules : NUMBER molecule"
    p[0] = (p[2], p[1])


def p_plus(p):
    "side : side PLUS molecules"
    p[0] = p[1]
    p[0].add(p[3][0], p[3][1])


def p_molecule(p):
    "molecule : countedelement"
    p[0] = Molecule()
    p[0].add_element(p[1][0], p[1][1])


def p_countedelement(p):
    "countedelement : ELEMENT"
    p[0] = (p[1], 1)


def p_ncountedelement(p):
    "countedelement : ELEMENT atomcount"
    p[0] = (p[1], p[2])


def p_multi_element(p):
    "molecule : molecule countedelement"
    p[0] = p[1]
    p[0].add_element(p[2][0], p[2][1])


def p_multi_atoms(p):
    "atomcount : SUBSCRIPT NUMBER"
    p[0] = int(p[2])


def p_many_atoms(p):
    "atomcount : SUBSCRIPT LBRACE NUMBER RBRACE"
    p[0] = int(p[3])


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


# Build the parser
parser = yacc.yacc()
```

    Writing parsereactions.py



```python
from parsereactions import parser

roundtrip_system = parser.parse(str(s2))
```

    Generating LALR tables



```bash
%%bash
# Read the first 100 lines from the file
head -n 100 parser.out
```

    Created by PLY version 3.11 (http://www.dabeaz.com/ply)

    Grammar

    Rule 0     S' -> system
    Rule 1     system -> equation
    Rule 2     system -> system TEXNEWLINE NEWLINE equation
    Rule 3     equation -> side ARROW side
    Rule 4     side -> molecules
    Rule 5     molecules -> molecule
    Rule 6     molecules -> NUMBER molecule
    Rule 7     side -> side PLUS molecules
    Rule 8     molecule -> countedelement
    Rule 9     countedelement -> ELEMENT
    Rule 10    countedelement -> ELEMENT atomcount
    Rule 11    molecule -> molecule countedelement
    Rule 12    atomcount -> SUBSCRIPT NUMBER
    Rule 13    atomcount -> SUBSCRIPT LBRACE NUMBER RBRACE

    Terminals, with rules where they appear

    ARROW                : 3
    ELEMENT              : 9 10
    LBRACE               : 13
    NEWLINE              : 2
    NUMBER               : 6 12 13
    PLUS                 : 7
    RBRACE               : 13
    SUBSCRIPT            : 12 13
    TEXNEWLINE           : 2
    error                :

    Nonterminals, with rules where they appear

    atomcount            : 10
    countedelement       : 8 11
    equation             : 1 2
    molecule             : 5 6 11
    molecules            : 4 7
    side                 : 3 3 7
    system               : 2 0

    Parsing method: LALR

    state 0

        (0) S' -> . system
        (1) system -> . equation
        (2) system -> . system TEXNEWLINE NEWLINE equation
        (3) equation -> . side ARROW side
        (4) side -> . molecules
        (7) side -> . side PLUS molecules
        (5) molecules -> . molecule
        (6) molecules -> . NUMBER molecule
        (8) molecule -> . countedelement
        (11) molecule -> . molecule countedelement
        (9) countedelement -> . ELEMENT
        (10) countedelement -> . ELEMENT atomcount

        NUMBER          shift and go to state 6
        ELEMENT         shift and go to state 8

        system                         shift and go to state 1
        equation                       shift and go to state 2
        side                           shift and go to state 3
        molecules                      shift and go to state 4
        molecule                       shift and go to state 5
        countedelement                 shift and go to state 7

    state 1

        (0) S' -> system .
        (2) system -> system . TEXNEWLINE NEWLINE equation

        TEXNEWLINE      shift and go to state 9


    state 2

        (1) system -> equation .

        TEXNEWLINE      reduce using rule 1 (system -> equation .)
        $end            reduce using rule 1 (system -> equation .)


    state 3

        (3) equation -> side . ARROW side
        (7) side -> side . PLUS molecules

        ARROW           shift and go to state 10
        PLUS            shift and go to state 11


    state 4

        (4) side -> molecules .

        ARROW           reduce using rule 4 (side -> molecules .)
        PLUS            reduce using rule 4 (side -> molecules .)



```python
display(Math(str(roundtrip_system)))
```


$\displaystyle C_6H_{12}O_6 + 6O_2 \rightarrow 6CO_2 + 6H_2O\\
2H_2 + O_2 \rightarrow 2H_2O$



```python
with open("system.tex", "w") as texfile:
    texfile.write(str(roundtrip_system))
```


```python
!cat system.tex
```

    C_6H_{12}O_6 + 6O_2 \rightarrow 6CO_2 + 6H_2O\\
    2H_2 + O_2 \rightarrow 2H_2O

## Internal DSLs

In doing the above, we have defined what is called an "external DSL":
    our code is in Python, but the file format is a language with a grammar
    of its own.

However, we can use the language itself to define something almost
as fluent, without having to write our own grammar,
by using operator overloading and metaprogramming tricks:


```python
%%writefile reactionsdsl.py


class Element:
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return str(self.symbol)

    def __mul__(self, other):
        """Let Molecule handle the multiplication"""
        return (self / 1) * other

    def __truediv__(self, number):
        """`Element / number => Molecule`"""
        res = Molecule()
        res.add_element(self, number)
        return res


class Molecule:
    def __init__(self):
        self.elements = {}  # Map from element to number of that element in the molecule

    def add_element(self, element, number):
        if not isinstance(element, Element):
            element = Element(element)
        self.elements[element] = number

    @staticmethod
    def as_subscript(number):
        if number == 1:
            return ""
        if number < 10:
            return "_" + str(number)
        return "_{" + str(number) + "}"

    def __str__(self):
        return "".join(
            [
                str(element) + Molecule.as_subscript(self.elements[element])
                for element in self.elements
            ]
        )

    def __mul__(self, other):
        """`Molecule * Element => Molecule`
        `Molecule * Molecule => Molecule`
        """
        if type(other) == Molecule:
            self.elements.update(other.elements)
        else:
            self.add_element(other, 1)
        return self

    def __rmul__(self, stoich):
        """`Number * Molecule => Side`"""
        res = Side()
        res.add(self, stoich)
        return res

    def __add__(self, other):
        """`Molecule + X => Side`"""
        if type(other) == Side:
            other.molecules[self] = 1
            return other
        res = Side()
        res.add(self, 1)
        res.add(other, 1)
        return res


class Side:
    def __init__(self):
        self.molecules = {}

    def add(self, reactant, stoichiometry):
        self.molecules[reactant] = stoichiometry

    @staticmethod
    def print_if_not_one(number):
        if number == 1:
            return ""
        else:
            return str(number)

    def __str__(self):
        return " + ".join(
            [
                Side.print_if_not_one(self.molecules[molecule]) + str(molecule)
                for molecule in self.molecules
            ]
        )

    def __add__(self, other):
        """Side + X => Side"""
        self.molecules.update(other.molecules)
        return self

    def __eq__(self, other):
        res = Reaction()
        res.reactants = self
        res.products = other
        current_system.add_reaction(res)  # Closure!
        return f"Added: '{res}'"


class Reaction:
    def __init__(self):
        self.reactants = Side()
        self.products = Side()

    def __str__(self):
        return str(self.reactants) + " \\rightarrow " + str(self.products)


class System:
    def __init__(self):
        self.reactions = []

    def add_reaction(self, reaction):
        self.reactions.append(reaction)

    def __str__(self):
        return "\\\\ \n".join(map(str, self.reactions))


current_system = System()
```

    Writing reactionsdsl.py



```python
from reactionsdsl import Element, current_system
```


```python
# Here we add new symbols to the global scope
# This is *not* good practice, we do it here to demonstrate that it is possible to do
for symbol in ("C", "O", "H"):
    globals()[symbol] = Element(symbol)
```


```python
O / 2 + 2 * (H / 2) == 2 * (H / 2 * O)
```




    "Added: '2H_2 + O_2 \\rightarrow 2H_2O'"




```python
(C / 6) * (H / 12) * (O / 6) + 6 * (O / 2) == 6 * (H / 2 * O) + 6 * (C * (O / 2))
```




    "Added: '6O_2 + C_6H_{12}O_6 \\rightarrow 6H_2O + 6CO_2'"




```python
display(Math(str(current_system)))
```


$\displaystyle 2H_2 + O_2 \rightarrow 2H_2O\\
6O_2 + C_6H_{12}O_6 \rightarrow 6H_2O + 6CO_2$


Python is not perfect for this, because it lacks the idea of parenthesis-free function dispatch and other things that make internal DSLs pretty.
