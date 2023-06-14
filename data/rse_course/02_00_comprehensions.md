# 2.0 Comprehensions

*Estimated time for this notebook: 10 minutes*

## 2.0.1 The list comprehension

If you write a for loop **inside** a pair of square brackets for a list, you magic up a list as defined.
This can make for concise but hard to read code, so be careful.


```python
[2**x for x in range(10)]
```




    [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]



Which is equivalent to the following code without using comprehensions:


```python
result = []
for x in range(10):
    result.append(2**x)

result
```




    [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]



You can do quite weird and cool things with comprehensions:


```python
[len(str(2**x)) for x in range(10)]
```




    [1, 1, 1, 1, 2, 2, 2, 3, 3, 3]



## 2.0.2 Selection in comprehensions

You can write an `if` statement in comprehensions too: 


```python
[2**x for x in range(30) if x % 3 == 0]
```




    [1, 8, 64, 512, 4096, 32768, 262144, 2097152, 16777216, 134217728]



Consider the following, and make sure you understand why it works:


```python
"".join([letter for letter in "James Hetherington" if letter.lower() not in "aeiou"])
```




    'Jms Hthrngtn'



## 2.0.3 Comprehensions versus building lists with `append`:

This code:


```python
result = []
for x in range(30):
    if x % 3 == 0:
        result.append(2**x)
result
```




    [1, 8, 64, 512, 4096, 32768, 262144, 2097152, 16777216, 134217728]



Does the same as the comprehension above. The comprehension is generally considered more readable.

Comprehensions are therefore an example of what we call 'syntactic sugar': they do not increase the capabilities of the language.

Instead, they make it possible to write the same thing in a more readable way. 

Almost everything we learn from now on will be either syntactic sugar or interaction with something other than idealised memory, such as a storage device or the internet. Once you have variables, conditionality, and branching, your language can do anything. (And this can be proved.)

## 2.0.4 Nested comprehensions

If you write two `for` statements in a comprehension, you get a single array generated over all the pairs:


```python
[x - y for x in range(4) for y in range(4)]
```




    [0, -1, -2, -3, 1, 0, -1, -2, 2, 1, 0, -1, 3, 2, 1, 0]



You can select on either, or on some combination:


```python
[x - y for x in range(4) for y in range(4) if x >= y]
```




    [0, 1, 0, 2, 1, 0, 3, 2, 1, 0]



If you want something more like a matrix, you need to do *two nested* comprehensions!


```python
[[x - y for x in range(4)] for y in range(4)]
```




    [[0, 1, 2, 3], [-1, 0, 1, 2], [-2, -1, 0, 1], [-3, -2, -1, 0]]



Note the subtly different square brackets.

Note that the list order for multiple or nested comprehensions can be confusing:


```python
[x + y for x in ["a", "b", "c"] for y in ["1", "2", "3"]]
```




    ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3']




```python
[[x + y for x in ["a", "b", "c"]] for y in ["1", "2", "3"]]
```




    [['a1', 'b1', 'c1'], ['a2', 'b2', 'c2'], ['a3', 'b3', 'c3']]



## 2.0.5 Dictionary Comprehensions

You can automatically build dictionaries, by using a list comprehension syntax, but with curly brackets and a colon:


```python
{(str(x)) * 3: x for x in range(3)}
```




    {'000': 0, '111': 1, '222': 2}



## 2.0.6 List-based thinking

Once you start to get comfortable with comprehensions, you find yourself working with containers, nested groups of lists 
and dictionaries, as the 'things' in your program, not individual variables. 

Given a way to analyse some dataset, we'll find ourselves writing stuff like:

    analysed_data = [analyze(datum) for datum in data]

There are lots of built-in methods that provide actions on lists as a whole:


```python
any([True, False, True])
```




    True




```python
all([True, False, True])
```




    False




```python
max([1, 2, 3])
```




    3




```python
sum([1, 2, 3])
```




    6



My favourite is `map`, which, similar to a list comprehension, applies one function to every member of a list:


```python
[str(x) for x in range(10)]
```




    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']




```python
list(map(str, range(10)))
```




    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']



So I can write:
    
    analysed_data = map(analyse, data)

We'll learn more about `map` and similar functions when we discuss functional programming later in the course.


```python

```
