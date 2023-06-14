# 1.4 Containers

*Estimated time for this notebook: 10 minutes*

## 1.4.1 Checking for containment.

The `list` we saw is a container type: its purpose is to hold other objects. We can ask python whether or not a
container contains a particular item:


```python
"Dog" in ["Cat", "Dog", "Horse"]
```




    True




```python
"Bird" in ["Cat", "Dog", "Horse"]
```




    False




```python
2 in range(5)
```




    True




```python
99 in range(5)
```




    False



## 1.4.2 Mutability

A list can be modified: (is mutable)


```python
name = "James Philip John Hetherington".split(" ")
print(name)
```

    ['James', 'Philip', 'John', 'Hetherington']



```python
name[0] = "Dr"
name[1:3] = ["Griffiths-"]
name.append("PhD")

print(" ".join(name))
```

    Dr Griffiths- Hetherington PhD


## 1.4.3 Tuples

A `tuple` is an immutable sequence. It is like a list, except it cannot be changed. It is defined with round brackets.


```python
x = (0,)
type(x)
```




    tuple




```python
my_tuple = ("Hello", "World")
my_tuple[0] = "Goodbye"
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    /var/folders/q7/nl3w6z854711jwsdy0hj7sxhwypcgh/T/ipykernel_63992/1208414676.py in <module>
          1 my_tuple = ("Hello", "World")
    ----> 2 my_tuple[0] = "Goodbye"
    

    TypeError: 'tuple' object does not support item assignment



```python
type(my_tuple)
```




    tuple



`str` is immutable too:


```python
fish = "Hake"
fish[0] = "R"
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    /var/folders/q7/nl3w6z854711jwsdy0hj7sxhwypcgh/T/ipykernel_63992/2286101535.py in <module>
          1 fish = "Hake"
    ----> 2 fish[0] = "R"
    

    TypeError: 'str' object does not support item assignment


But note that container reassignment is moving a label, **not** changing an element:


```python
fish = "Rake"  # OK!
```

*Supplementary material*: Try the [online memory visualiser](http://www.pythontutor.com/visualize.html#code=name+%3D++%22James+Philip+John+Hetherington%22.split%28%22+%22%29%0A%0Aname%5B0%5D+%3D+%22Dr%22%0Aname%5B1%3A3%5D+%3D+%5B%22Griffiths-%22%5D%0Aname.append%28%22PhD%22%29%0A%0Aname+%3D+%22Bilbo+Baggins%22&mode=display&origin=opt-frontend.js&cumulative=false&heapPrimitives=true&textReferences=false&py=2&rawInputLstJSON=%5B%5D&curInstr=0) for this one.

## 1.4.4 Memory and containers


The way memory works with containers can be important:





```python
x = list(range(3))
x
```




    [0, 1, 2]




```python
y = x
y
```




    [0, 1, 2]




```python
z = x[0:3]
y[1] = "Gotcha!"
```


```python
x
```




    [0, 'Gotcha!', 2]




```python
y
```




    [0, 'Gotcha!', 2]




```python
z
```




    [0, 1, 2]




```python
z[2] = "Really?"
```


```python
x
```




    [0, 'Gotcha!', 2]




```python
y
```




    [0, 'Gotcha!', 2]




```python
z
```




    [0, 1, 'Really?']



*Supplementary material*: This one works well at the [memory visualiser](http://www.pythontutor.com/visualize.html#code=x+%3D+%5B%22What's%22,+%22Going%22,+%22On%3F%22%5D%0Ay+%3D+x%0Az+%3D+x%5B0%3A3%5D%0A%0Ay%5B1%5D+%3D+%22Gotcha!%22%0Az%5B2%5D+%3D+%22Really%3F%22&mode=display&origin=opt-frontend.js&cumulative=false&heapPrimitives=true&textReferences=false&py=2&rawInputLstJSON=%5B%5D&curInstr=0).

The explanation: While `y` is a second label on the *same object*, `z` is a separate object with the same data. Writing `x[:]` creates a new list containing all the elements of `x` (remember: `[:]` is equivalent to `[0:<last>]`). This is the case whenever we take a slice from a list, not just when taking all the elements with `[:]`.

The difference between `y=x` and `z=x[:]` is important!

Nested objects make it even more complicated:


```python
x = [["a", "b"], "c"]
y = x
z = x[0:2]
```


```python
x[0][1] = "d"
z[1] = "e"
```


```python
x
```




    [['a', 'd'], 'c']




```python
y
```




    [['a', 'd'], 'c']




```python
z
```




    [['a', 'd'], 'e']



Try the [visualiser](http://www.pythontutor.com/visualize.html#code=x%3D%5B%5B'a','b'%5D,'c'%5D%0Ay%3Dx%0Az%3Dx%5B0%3A2%5D%0A%0Ax%5B0%5D%5B1%5D%3D'd'%0Az%5B1%5D%3D'e'&mode=display&origin=opt-frontend.js&cumulative=false&heapPrimitives=true&textReferences=false&py=2&rawInputLstJSON=%5B%5D&curInstr=0) again.

*Supplementary material*: The copies that we make through slicing are called *shallow copies*: we don't copy all the objects they contain, only the references to them. This is why the nested list in `x[0]` is not copied, so `z[0]` still refers to it. It is possible to actually create copies of all the contents, however deeply nested they are - this is called a *deep copy*. Python provides methods for that in its standard library, in the `copy` module. You can read more about that, as well as about shallow and deep copies, in the [library reference](https://docs.python.org/3/library/copy.html).

## 1.4.5 Identity vs Equality

Having the same data is different from being the same actual object
in memory:


```python
[1, 2] == [1, 2]
```




    True




```python
[1, 2] is [1, 2]
```




    False



The == operator checks, element by element, that two containers have the same data. 
The `is` operator checks that they are actually the same object.

But, and this point is really subtle, for immutables, the python language might save memory by reusing a single instantiated copy. This will always be safe.


```python
"Hello" == "Hello"
```




    True




```python
"Hello" is "Hello"
```




    True



This can be useful in understanding problems like the one above:


```python
x = range(3)
y = x
z = x[:]
```


```python
x == y
```




    True




```python
x is y
```




    True




```python
x == z
```




    True




```python
x is z
```




    False


