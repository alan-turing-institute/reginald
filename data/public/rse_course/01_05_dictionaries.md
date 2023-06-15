# 1.5 Dictionaries

*Estimated time for this notebook: 10 minutes*

## 1.5.1 The Python Dictionary

Python supports a container type called a dictionary.

This is also known as an "associative array", "map" or "hash" in other languages.

In a list, we use a number to look up an element:


```python
names = "Martin Luther King".split(" ")
```


```python
names[1]
```




    'Luther'



In a dictionary, we look up an element using **another object of our choice**:


```python
me = {"name": "James", "age": 39, "Jobs": ["Programmer", "Teacher"]}
```


```python
me
```




    {'name': 'James', 'age': 39, 'Jobs': ['Programmer', 'Teacher']}




```python
me["Jobs"]
```




    ['Programmer', 'Teacher']




```python
me["age"]
```




    39




```python
type(me)
```




    dict



### Keys and Values

The things we can use to look up with are called **keys**:


```python
me.keys()
```




    dict_keys(['name', 'age', 'Jobs'])



The things we can look up are called **values**:


```python
me.values()
```




    dict_values(['James', 39, ['Programmer', 'Teacher']])



When we test for containment on a `dict` we test on the **keys**:


```python
"Jobs" in me
```




    True




```python
"James" in me
```




    False




```python
"James" in me.values()
```




    True



### Immutable Keys Only

The way in which dictionaries work is one of the coolest things in computer science:
the "hash table". The details of this are beyond the scope of this course, but we will consider some aspects in the section on performance programming.

One consequence of this implementation is that you can only use **immutable** things as keys.


```python
good_match = {("Lamb", "Mint"): True, ("Bacon", "Chocolate"): False}
```

but:


```python
illegal = {["Lamb", "Mint"]: True, ["Bacon", "Chocolate"]: False}
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    Cell In [14], line 1
    ----> 1 illegal = {
          2     ["Lamb", "Mint"]: True,
          3     ["Bacon", "Chocolate"]: False
          4 }


    TypeError: unhashable type: 'list'


Remember -- square brackets denote lists, round brackets denote `tuple`s.

### Dictionary Order

Dictionaries will retain the order of the elements as they are defined (in Python versions >= 3.7).


```python
my_dict = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4}
print(my_dict)
print(my_dict.values())
```

    {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4}
    dict_values([0, 1, 2, 3, 4])



```python
rev_dict = {"4": 4, "3": 3, "2": 2, "1": 1, "0": 0}
print(rev_dict)
print(rev_dict.values())
```

    {'4': 4, '3': 3, '2': 2, '1': 1, '0': 0}
    dict_values([4, 3, 2, 1, 0])


Python does not consider the order of the elements relevant to equality:


```python
my_dict == rev_dict
```




    True



## 1.5.2 Sets

A set is a `list` which cannot contain the same element twice.
We make one by calling `set()` on any sequence, e.g. a list or string.


```python
name = "James Hetherington"
unique_letters = set(name)
```


```python
unique_letters
```




    {' ', 'H', 'J', 'a', 'e', 'g', 'h', 'i', 'm', 'n', 'o', 'r', 's', 't'}



Or by defining a literal like a dictionary, but without the colons:


```python
primes_below_ten = {2, 3, 5, 7}
```


```python
type(unique_letters)
```




    set




```python
type(primes_below_ten)
```




    set




```python
unique_letters
```




    {' ', 'H', 'J', 'a', 'e', 'g', 'h', 'i', 'm', 'n', 'o', 'r', 's', 't'}



This will be easier to read if we turn the set of letters back into a string, with `join`:


```python
"".join(unique_letters)
```




    'es mgtanorHiJh'



A set has no particular order, but is really useful for checking or storing **unique** values.

Set operations work as in mathematics:


```python
x = set("Hello")
y = set("Goodbye")
```


```python
x & y  # Intersection
```




    {'e', 'o'}




```python
x | y  # Union
```




    {'G', 'H', 'b', 'd', 'e', 'l', 'o', 'y'}




```python
y - x  # y intersection with complement of x: letters in Goodbye but not in Hello
```




    {'G', 'b', 'd', 'y'}



Your programs will be faster and more readable if you use the appropriate container type for your data's meaning.
Always use a set for lists which can't in principle contain the same data twice, always use a dictionary for anything
which feels like a mapping from keys to values.
