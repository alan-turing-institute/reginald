# 1.2 Using Functions

*Estimated time for this notebook: 20 minutes*

## 1.2.1 Calling functions

We often want to do things to our objects that are more complicated than just assigning them to variables.


```python
len("pneumonoultramicroscopicsilicovolcanoconiosis")
```




    45



Here we have "called a function".

The function `len` takes one input, and has one output. The output is the length of whatever the input was.

Programmers also call function inputs "parameters" or, confusingly, "arguments".

Here's another example:


```python
sorted("Python")
```




    ['P', 'h', 'n', 'o', 't', 'y']



Which gives us back a *list* of the letters in Python, sorted alphabetically (more specifically, according to their [Unicode order](https://www.ssec.wisc.edu/~tomw/java/unicode.html#x0000)).

The input goes in brackets after the function name, and the output emerges wherever the function is used.

So we can put a function call anywhere we could put a "literal" object or a variable. 


```python
len("Jim") * 8
```




    24




```python
x = len("Mike")
y = len("Bob")
z = x + y
```


```python
print(z)
```

    7


## 1.2.2 Using methods

Objects come associated with a bunch of functions designed for working on objects of that type. We access these with a dot, just as we do for data attributes:


```python
"shout".upper()
```




    'SHOUT'



These are called methods. If you try to use a method defined for a different type, you get an error:


```python
x = 5
```


```python
type(x)
```




    int




```python
x.upper()
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    /var/folders/q7/nl3w6z854711jwsdy0hj7sxhwypcgh/T/ipykernel_63968/1145191538.py in <module>
    ----> 1 x.upper()
    

    AttributeError: 'int' object has no attribute 'upper'


If you try to use a method that doesn't exist, you get an error:


```python
x.wrong
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    /var/folders/q7/nl3w6z854711jwsdy0hj7sxhwypcgh/T/ipykernel_63968/64132422.py in <module>
    ----> 1 x.wrong
    

    AttributeError: 'int' object has no attribute 'wrong'


Methods and properties are both kinds of **attribute**, so both are accessed with the dot operator.

Objects can have both properties and methods:


```python
z = 1 + 5j
```


```python
z.real
```




    1.0




```python
z.conjugate()
```




    (1-5j)




```python
z.conjugate
```




    <function complex.conjugate>



## 1.2.3 Functions are just a type of object!

Now for something that will take a while to understand: don't worry if you don't get this yet, we'll
look again at this in much more depth later in the course.

If we forget the (), we realise that a *method is just a property which is a function*!


```python
z.conjugate
```




    <function complex.conjugate>




```python
type(z.conjugate)
```




    builtin_function_or_method




```python
somefunc = z.conjugate
```


```python
somefunc()
```




    (1-5j)



Functions are just a kind of variable, and we can assign new labels to them:


```python
sorted([1, 5, 3, 4])
```




    [1, 3, 4, 5]




```python
magic = sorted
```


```python
type(magic)
```




    builtin_function_or_method




```python
magic(["Technology", "Advanced"])
```




    ['Advanced', 'Technology']



## 1.2.4 Getting help on functions and methods

The 'help' function, when applied to a function, gives help on it!


```python
help(sorted)
```

    Help on built-in function sorted in module builtins:
    
    sorted(iterable, /, *, key=None, reverse=False)
        Return a new list containing all items from the iterable in ascending order.
        
        A custom key function can be supplied to customize the sort order, and the
        reverse flag can be set to request the result in descending order.
    


The 'dir' function, when applied to an object, lists all its attributes (properties and methods):


```python
dir("Hexxo")
```




    ['__add__',
     '__class__',
     '__contains__',
     '__delattr__',
     '__dir__',
     '__doc__',
     '__eq__',
     '__format__',
     '__ge__',
     '__getattribute__',
     '__getitem__',
     '__getnewargs__',
     '__gt__',
     '__hash__',
     '__init__',
     '__init_subclass__',
     '__iter__',
     '__le__',
     '__len__',
     '__lt__',
     '__mod__',
     '__mul__',
     '__ne__',
     '__new__',
     '__reduce__',
     '__reduce_ex__',
     '__repr__',
     '__rmod__',
     '__rmul__',
     '__setattr__',
     '__sizeof__',
     '__str__',
     '__subclasshook__',
     'capitalize',
     'casefold',
     'center',
     'count',
     'encode',
     'endswith',
     'expandtabs',
     'find',
     'format',
     'format_map',
     'index',
     'isalnum',
     'isalpha',
     'isascii',
     'isdecimal',
     'isdigit',
     'isidentifier',
     'islower',
     'isnumeric',
     'isprintable',
     'isspace',
     'istitle',
     'isupper',
     'join',
     'ljust',
     'lower',
     'lstrip',
     'maketrans',
     'partition',
     'replace',
     'rfind',
     'rindex',
     'rjust',
     'rpartition',
     'rsplit',
     'rstrip',
     'split',
     'splitlines',
     'startswith',
     'strip',
     'swapcase',
     'title',
     'translate',
     'upper',
     'zfill']



Most of these are confusing methods beginning and ending with __, part of the internals of python.

Again, just as with error messages, we have to learn to read past the bits that are confusing, to the bit we want:


```python
"Hexxo".replace("x", "l")
```




    'Hello'




```python
help("FIsh".replace)
```

    Help on built-in function replace:
    
    replace(old, new, count=-1, /) method of builtins.str instance
        Return a copy with all occurrences of substring old replaced by new.
        
          count
            Maximum number of occurrences to replace.
            -1 (the default value) means replace all occurrences.
        
        If the optional argument count is given, only the first count occurrences are
        replaced.
    


## 1.2.5 Operators

Now that we know that functions are a way of taking a number of inputs and producing an output, we should look again at
what happens when we write:


```python
x = 2 + 3
```


```python
print(x)
```

    5


This is just a pretty way of calling an "add" function. Things would be more symmetrical if add were actually written

    x = +(2, 3)
    
Where '+' is just the name of the name of the adding function.

In python, these functions **do** exist, but they're actually **methods** of the first input: they're the mysterious `__` functions we saw earlier (Two underscores.)


```python
x.__add__(7)
```




    12



We call these symbols, `+`, `-` etc, "operators".

The meaning of an operator varies for different types:


```python
"Hello" + "Goodbye"
```




    'HelloGoodbye'




```python
[2, 3, 4] + [5, 6]
```




    [2, 3, 4, 5, 6]



Sometimes we get an error when a type doesn't have an operator:


```python
7 - 2
```




    5




```python
[2, 3, 4] - [5, 6]
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    /var/folders/q7/nl3w6z854711jwsdy0hj7sxhwypcgh/T/ipykernel_63968/929060672.py in <module>
    ----> 1 [2, 3, 4] - [5, 6]
    

    TypeError: unsupported operand type(s) for -: 'list' and 'list'


The word "operand" means "thing that an operator operates on"!

Or when two types can't work together with an operator:


```python
[2, 3, 4] + 5
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    /var/folders/q7/nl3w6z854711jwsdy0hj7sxhwypcgh/T/ipykernel_63968/708834880.py in <module>
    ----> 1 [2, 3, 4] + 5
    

    TypeError: can only concatenate list (not "int") to list


To do this, put:


```python
[2, 3, 4] + [5]
```




    [2, 3, 4, 5]



Just as in Mathematics, operators have a built-in precedence, with brackets used to force an order of operations:


```python
print(2 + 3 * 4)
```

    14



```python
print((2 + 3) * 4)
```

    20


*Supplementary material*: https://docs.python.org/3/reference/expressions.html#operator-precedence
