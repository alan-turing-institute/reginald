# 1.3 Types

*Estimated time for this notebook: 20 minutes*

We have seen that Python objects have a 'type':


```python
type(5)
```




    int



## 1.3.1 Floats and integers

Python has two core numeric types, `int` for integer, and `float` for real number.


```python
one = 1
ten = 10
one_float = 1.0
ten_float = 10.0
```

Zero after a point is optional. But the **Dot** makes it a float.


```python
tenth = one_float / ten_float
```


```python
tenth
```




    0.1




```python
type(one)
```




    int




```python
type(one_float)
```




    float



The meaning of an operator varies depending on the type it is applied to!


```python
print(one // ten)
```

    0



```python
one_float / ten_float
```




    0.1




```python
print(type(one / ten))
```

    <class 'float'>



```python
type(tenth)
```




    float



The divided by operator when applied to floats, and integers means divide by for real numbers.

The `//` operator means divide and then round down


```python
10 // 3
```




    3




```python
10.0 / 3
```




    3.3333333333333335




```python
10 / 3.0
```




    3.3333333333333335



There is a function for every type name, which is used to convert the input to an output of the desired type.


```python
x = float(5)
type(x)
```




    float




```python
10 / float(3)
```




    3.3333333333333335



I lied when I said that the `float` type was a real number. It's actually a computer representation of a real number
called a "floating point number". Representing $\sqrt 2$ or $\frac{1}{3}$ perfectly would be impossible in a computer, so we use a finite amount of memory to do it.


```python
N = 10000.0
sum([1 / N] * int(N))
```




    0.9999999999999062



*Supplementary material*:

* https://docs.python.org/3/tutorial/floatingpoint.html
* http://floating-point-gui.de/formats/fp/
* Advanced: http://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html

## 1.3.2 Strings

Python has a built in `string` type, supporting many
useful methods.


```python
given = "James"
family = "Hetherington"
full = given + " " + family
```

So `+` for strings means "join them together" - *concatenate*.


```python
print(full.upper())
```

    JAMES HETHERINGTON


As for `float` and `int`, the name of a type can be used as a function to convert between types:


```python
ten, one
```




    (10, 1)




```python
print(ten + one)
```

    11



```python
print(float(str(ten) + str(one)))
```

    101.0


We can remove extraneous material from the start and end of a string:


```python
"    Hello  ".strip()
```




    'Hello'



Note that you can write strings in Python using either single (`' ... '`) or double (`" ... "`) quote marks. The two ways are equivalent. However, if your string includes a single quote (e.g. an apostrophe), you should use double quotes to surround it:


```python
"James's Class"
```




    "James's Class"



And vice versa: if your string has a double quote inside it, you should wrap the whole string in single quotes.


```python
'"Wow!", said Bob.'
```




    '"Wow!", said Bob.'



## 1.3.3 Lists

Python's basic **container** type is the `list`.

We can define our own list with square brackets:


```python
[1, 3, 7]
```




    [1, 3, 7]




```python
type([1, 3, 7])
```




    list



Lists *do not* have to contain just one type:


```python
various_things = [1, 2, "banana", 3.4, [1, 2]]
```

We access an **element** of a list with an `int` in square brackets:


```python
various_things[2]
```




    'banana'




```python
index = 0
various_things[index]
```




    1



Note that list indices start from zero.

We can use a string to join together a list of strings:


```python
name = ["James", "Philip", "John", "Hetherington"]
print("==".join(name))
```

    James==Philip==John==Hetherington


And we can split up a string into a list:


```python
"Ernst Stavro Blofeld".split(" ")
```




    ['Ernst', 'Stavro', 'Blofeld']




```python
"Ernst Stavro Blofeld".split("o")
```




    ['Ernst Stavr', ' Bl', 'feld']



And combine these:


```python
"->".join("John Ronald Reuel Tolkien".split(" "))
```




    'John->Ronald->Reuel->Tolkien'



A matrix can be represented by **nesting** lists -- putting lists inside other lists.


```python
identity = [[1, 0], [0, 1]]
```


```python
identity[0][0]
```




    1



... but later we will learn about a better way of representing matrices.

## 1.3.4 Ranges

Another useful type is range, which gives you a sequence of consecutive numbers. In contrast to a list, ranges generate the numbers as you need them, rather than all at once.

If you try to print a range, you'll see something that looks a little strange: 


```python
range(5)
```




    range(0, 5)



We don't see the contents, because *they haven't been generatead yet*. Instead, Python gives us a description of the object - in this case, its type (range) and its lower and upper limits.

We can quickly make a list with numbers counted up by converting this range:


```python
count_to_five = range(5)
print(list(count_to_five))
```

    [0, 1, 2, 3, 4]


Ranges in Python can be customised in other ways, such as by specifying the lower limit or the step (that is, the difference between successive elements). You can find more information about them in the [official Python documentation](https://docs.python.org/3/library/stdtypes.html#ranges).

## 1.3.5 Sequences

Many other things can be treated like `lists`. Python calls things that can be treated like lists `sequences`.

A string is one such *sequence type*.

Sequences support various useful operations, including:
- Accessing a single element at a particular index: `sequence[index]`
- Accessing multiple elements (a *slice*): `sequence[start:end_plus_one]`
- Getting the length of a sequence: `len(sequence)`
- Checking whether the sequence contains an element: `element in sequence`

The following examples illustrate these operations with lists, strings and ranges.


```python
print(count_to_five[1])
```

    1



```python
print("James"[2])
```

    m



```python
count_to_five = range(5)
```


```python
count_to_five[1:3]
```




    range(1, 3)




```python
"Hello World"[4:8]
```




    'o Wo'




```python
len(various_things)
```




    5




```python
len("Python")
```




    6




```python
name
```




    ['James', 'Philip', 'John', 'Hetherington']




```python
"John" in name
```




    True




```python
3 in count_to_five
```




    True



## 1.3.6 Unpacking

Multiple values can be **unpacked** when assigning from sequences, like dealing out decks of cards.


```python
mylist = ["Hello", "World"]
a, b = mylist
print(b)
```

    World



```python
range(4)
```




    range(0, 4)




```python
zero, one, two, three = range(4)
```


```python
two
```




    2



If there is too much or too little data, an error results:


```python
zero, one, two, three = range(7)
```


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    /var/folders/q7/nl3w6z854711jwsdy0hj7sxhwypcgh/T/ipykernel_63975/2891450249.py in <module>
    ----> 1 zero, one, two, three = range(7)
    

    ValueError: too many values to unpack (expected 4)



```python
zero, one, two, three = range(2)
```


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    /var/folders/q7/nl3w6z854711jwsdy0hj7sxhwypcgh/T/ipykernel_63975/4218591722.py in <module>
    ----> 1 zero, one, two, three = range(2)
    

    ValueError: not enough values to unpack (expected 4, got 2)


Python provides some handy syntax to split a sequence into its first element ("head") and the remaining ones (its "tail"):


```python
head, *tail = range(4)
print("head is", head)
print("tail is", tail)
```

    head is 0
    tail is [1, 2, 3]


Note the syntax with the \*. The same pattern can be used, for example, to extract the middle segment of a sequence whose length we might not know:


```python
one, *two, three = range(10)
```


```python
print("one is", one)
print("two is", two)
print("three is", three)
```

    one is 0
    two is [1, 2, 3, 4, 5, 6, 7, 8]
    three is 9

