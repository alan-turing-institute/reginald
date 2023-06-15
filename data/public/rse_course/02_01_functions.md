# 2.1 Functions

*Estimated time for this notebook: 15 minutes*

Defining **functions** which put together code to make a more complex task seem simple from the outside is the most important thing in programming.
We can wrap code up in a **function**, so that we can repeatedly get just the information we want.


## 2.1.1 Definition

We use `def` to define a function, and `return` to pass back a value:
The input comes in in brackets after the function name:



```python
def double(x):
    return x * 2


print(double(5), double([5]), double("five"))
```

    10 [5, 5] fivefive


## 2.1.2 Default Parameters

We can specify default values for parameters:


```python
def jeeves(name="Sir"):
    return f"Very good, {name}"
```


```python
jeeves()
```




    'Very good, Sir'




```python
jeeves("James")
```




    'Very good, James'



If you have some parameters with defaults, and some without, those with defaults **must** go later.

If you have multiple default arguments, you can specify neither, one or both:


```python
def jeeves(greeting="Very good", name="Sir"):
    return f"{greeting}, {name}"
```


```python
jeeves()
```




    'Very good, Sir'




```python
jeeves("Hello")
```




    'Hello, Sir'




```python
jeeves(name="James")
```




    'Very good, James'




```python
jeeves(greeting="Suits you")
```




    'Suits you, Sir'




```python
jeeves("Hello", "Sailor")
```




    'Hello, Sailor'



## 2.1.3 Early Return


Return without arguments can be used to exit early from a function




Here's a slightly convoluted example of a function which will return early under specific conditions. In this case if a list contains the string 'cat'.


```python
def are_there_cats(my_input_list):

    if "cat" in my_input_list:  # If the string "cat" is in the list
        print("There is a cat in here")  # print a statement to screen
        return

    print("Nothing to see here")
```


```python
first_list = ["cat", "dog", "hamster", 42]

second_list = ["duck", 17, "elk"]
```


```python
are_there_cats(first_list)
```

    There is a cat in here



```python
are_there_cats(second_list)
```

    Nothing to see here


## 2.1.4 Scoping

There are differences in how variables and names are accessed by your code based on where they are defined.

Within this notebook any variables that have been defined outside of a function will be available to the rest of the notebook. At this point in the notebook, x has not been defined.


```python
x
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-15-6fcf9dfbd479> in <module>
    ----> 1 x


    NameError: name 'x' is not defined


If we now define x and write and call a function in which uses it; the function can still access x, even if x isn't given as an argument.


```python
x = 5  # Define x now


def can_we_see_x():
    print(f"x = {x}")


can_we_see_x()
```

    x = 5


However if we define y locally - in a function - we can access it from within that function:


```python
def can_we_see_y():
    y = 7  # Define y in the function
    print(f"x = {x}")
    print(f"y = {y}")


can_we_see_y()
```

    x = 5
    y = 7


However y isn't accessible globally - that is it isn't available outside of the function in which it was defined


```python
y
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-18-9063a9f0e032> in <module>
    ----> 1 y


    NameError: name 'y' is not defined


*Note for the two functions above we used syntax for building strings that contain the values of variables. You can read more about it [here](https://realpython.com/python-string-formatting/#3-string-interpolation-f-strings-python-36) or in the official documentation for formatted string literals; [f-strings](https://docs.python.org/3/tutorial/inputoutput.html#tut-f-strings).*

## 2.1.5 Side effects

Functions can do things to change their **mutable** arguments,
so `return` is optional.

This is pretty awful style, in general, functions should normally be side-effect free.

Here is a contrived example of a function that makes plausible use of a side-effect


```python
def double_inplace(vec):
    vec[:] = [element * 2 for element in vec]


z = list(range(4))
double_inplace(z)
print(z)
```

    [0, 2, 4, 6]



```python
letters = ["a", "b", "c", "d", "e", "f", "g"]
letters[:] = []
```

In this example, we're using `[:]` to access into the same list, and write its data.

    vec = [element*2 for element in vec]

would just move a local label, not change the input.

See Module 1.5 - Memory and Containers for a refresher

But I'd usually just write this as a function which **returned** the output:


```python
def double(vec):
    return [element * 2 for element in vec]
```

Let's remind ourselves of the behaviour for modifying lists in-place using `[:]` with a simple array:


```python
x = 5
x = 7
x = ["a", "b", "c"]
y = x
```


```python
x
```




    ['a', 'b', 'c']




```python
x[:] = ["Hooray!", "Yippee"]
```


```python
y
```




    ['Hooray!', 'Yippee']



## 2.1.6 Unpacking arguments


```python
def arrow(before, after):
    return str(before) + " -> " + str(after)


arrow(1, 3)
```




    '1 -> 3'




If a function that takes multiple arguments is given an iterable object prepended with '*',
each element of that object is taken in turn and used to fill the function's arguments one-by-one.





```python
x = [1, -1]
arrow(*x)
```




    '1 -> -1'






This can be quite powerful:





```python
charges = {"neutron": 0, "proton": 1, "electron": -1}
for particle in charges.items():
    print(arrow(*particle))
```

    neutron -> 0
    proton -> 1
    electron -> -1


## 2.1.7 Sequence Arguments

Similiarly, if a `*` is used in the **definition** of a function, multiple
arguments are absorbed into a list **inside** the function:


```python
def doubler(*sequence):
    return [x * 2 for x in sequence]
```


```python
doubler(1, 2, 3)
```




    [2, 4, 6]




```python
doubler(5, 2, "Wow!")
```




    [10, 4, 'Wow!Wow!']



## 2.1.8 Keyword Arguments

If two asterisks are used, named arguments are supplied inside the function as a dictionary:


```python
def arrowify(**args):
    for key, value in args.items():
        print(key + " -> " + value)


arrowify(neutron="n", proton="p", electron="e")
```

    neutron -> n
    proton -> p
    electron -> e


These different approaches can be mixed:


```python
def somefunc(a, b, *args, **kwargs):
    print("A:", a)
    print("B:", b)
    print("args:", args)
    print("keyword args", kwargs)
```


```python
somefunc(1, 2, 3, 4, 5, fish="Haddock")
```

    A: 1
    B: 2
    args: (3, 4, 5)
    keyword args {'fish': 'Haddock'}
