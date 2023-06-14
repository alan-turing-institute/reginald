# 1.1 Variables

*Estimated time for this notebook: 10 minutes*

## 1.1.1 Variable Assignment

When we generate a result, the answer is displayed, but not kept anywhere.


```python
2 * 3
```




    6



If we want to get back to that result, we have to store it. We put it in a box, with a name on the box. This is a **variable**.


```python
six = 2 * 3
```


```python
print(six)
```

    6


If we look for a variable that hasn't ever been defined, we get an error. 


```python
print(seven)
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    Input In [4], in <cell line: 1>()
    ----> 1 print(seven)


    NameError: name 'seven' is not defined


That's **not** the same as an empty box, well labeled:


```python
nothing = None
```


```python
print(nothing)
```

    None



```python
type(None)
```




    NoneType



(None is the special python value for a no-value variable.)

*Supplementary Materials*: There's more on variables at http://swcarpentry.github.io/python-novice-inflammation/01-numpy/index.html 

Anywhere we could put a raw number, we can put a variable label, and that works fine:


```python
print(5 * six)
```

    30



```python
scary = six * six * six
```


```python
print(scary)
```

    216


## 1.1.2 Reassignment and multiple labels

But here's the real scary thing: it seems like we can put something else in that box:


```python
scary = 25
```


```python
print(scary)
```

    25


Note that **the data that was there before has been lost**. 

No labels refer to it any more - so it has been "Garbage Collected"! We might imagine something pulled out of the box, and thrown on the floor, to make way for the next occupant.

In fact, though, it is the **label** that has moved. We can see this because we have more than one label refering to the same box:


```python
name = "James"
```


```python
nom = name
```


```python
print(nom)
```

    James



```python
print(name)
```

    James


And we can move just one of those labels:


```python
nom = "Hetherington"
```


```python
print(name)
```

    James



```python
print(nom)
```

    Hetherington


So we can now develop a better understanding of our labels and boxes: each box is a piece of space (an *address*) in computer memory.
Each label (variable) is a reference to such a place.

When the number of labels on a box ("variables referencing an address") gets down to zero, then the data in the box cannot be found any more.

After a while, the language's "Garbage collector" will wander by, notice a box with no labels, and throw the data away, **making that box
available for more data**.

Old fashioned languages like C and Fortran don't have Garbage collectors. So a memory address with no references to it
still takes up memory, and the computer can more easily run out.

So when I write:


```python
name = "Jim"
```

The following things happen:

1. A new text **object** is created, and an address in memory is found for it.
1. The variable "name" is moved to refer to that address.
1. The old address, containing "James", now has no labels.
1. The garbage collector frees the memory at the old address.

**Supplementary materials**: There's an online python tutor which is great for visualising memory and references. Try the [scenario we just looked at](http://www.pythontutor.com/visualize.html#code=name+%3D+%22James%22%0Anom+%3D+name%0Aprint+nom%0Aprint+name%0Anom+%3D+%22Hetherington%22%0Aprint+nom%0Aprint+name%0Aname%3D+%22Jim%22%0Aprint+nom%0Aprint+name&mode=display&origin=opt-frontend.js&cumulative=false&heapPrimitives=true&textReferences=false&py=2&rawInputLstJSON=%5B%5D&curInstr=0)

Labels are contained in groups called "frames": our frame contains two labels, 'nom' and 'name'.

## 1.1.3 Objects and types

An object, like `name`, has a type. In the online python tutor example, we see that the objects have type "str".
`str` means a text object: Programmers call these 'strings'. 


```python
type(name)
```




    str



Depending on its type, an object can have different *properties*: data fields Inside the object.

Consider a Python complex number for example:


```python
z = 3 + 1j
```

We can see what properties and methods an object has available using the `dir` function:


```python
dir(z)
```




    ['__abs__',
     '__add__',
     '__bool__',
     '__class__',
     '__delattr__',
     '__dir__',
     '__divmod__',
     '__doc__',
     '__eq__',
     '__float__',
     '__floordiv__',
     '__format__',
     '__ge__',
     '__getattribute__',
     '__getnewargs__',
     '__gt__',
     '__hash__',
     '__init__',
     '__init_subclass__',
     '__int__',
     '__le__',
     '__lt__',
     '__mod__',
     '__mul__',
     '__ne__',
     '__neg__',
     '__new__',
     '__pos__',
     '__pow__',
     '__radd__',
     '__rdivmod__',
     '__reduce__',
     '__reduce_ex__',
     '__repr__',
     '__rfloordiv__',
     '__rmod__',
     '__rmul__',
     '__rpow__',
     '__rsub__',
     '__rtruediv__',
     '__setattr__',
     '__sizeof__',
     '__str__',
     '__sub__',
     '__subclasshook__',
     '__truediv__',
     'conjugate',
     'imag',
     'real']



You can see that there are several methods whose name starts and ends with `__` (e.g. `__init__`): these are special methods that Python uses internally, and we will discuss some of them later on in this course. The others (in this case, `conjugate`, `img` and `real`) are the methods and fields through which we can interact with this object.


```python
type(z)
```




    complex




```python
z.real
```




    3.0




```python
z.imag
```




    1.0



A property of an object is accessed with a dot.

The jargon is that the "dot operator" is used to obtain a property of an object.

When we try to access a property that doesn't exist, we get an error:


```python
z.wrong
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    Input In [27], in <cell line: 1>()
    ----> 1 z.wrong


    AttributeError: 'complex' object has no attribute 'wrong'


## 1.1.4 Reading error messages.

It's important, when learning to program, to develop an ability to read an error message and find, from in amongst
all the confusing noise, the bit of the error message which tells you what to change!

We don't yet know what is meant by `AttributeError`, or "Traceback".


```python
z2 = 5 - 6j
print("Gets to here")
print(z.wrong)
print("Didn't get to here")
```

    Gets to here



    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    Input In [28], in <cell line: 3>()
          1 z2 = 5 - 6j
          2 print("Gets to here")
    ----> 3 print(z.wrong)
          4 print("Didn't get to here")


    AttributeError: 'complex' object has no attribute 'wrong'


But in the above, we can see that the error happens on the **third** line of our code cell.

We can also see that the error message: 
> 'complex' object has no attribute 'wrong' 

...tells us something important. Even if we don't understand the rest, this is useful for debugging!

## 1.1.5 Variables and the notebook kernel

When I type code in the notebook, the objects live in memory between cells.


```python
number = 0
```


```python
print(number)
```

    0


If I change a variable:


```python
number = number + 1
```


```python
print(number)
```

    1


It keeps its new value for the next cell.

But cells are **not** always evaluated in order.

If I now go back to input cell reading `number = number + 1`, and run it again, with shift-enter. Number will change from 2 to 2, then from 2 to 3, then from 3 to 4... Try it!

So it's important to remember that if you move your cursor around in the notebook, it doesn't always run top to bottom.

**Supplementary material**: (1) https://jupyter-notebook.readthedocs.io/en/latest/ 

## 1.1.6 Comments

Code after a `#` symbol doesn't get run.


```python
print("This runs")  # print("This doesn't")
# print("This doesn't either")
```

    This runs

