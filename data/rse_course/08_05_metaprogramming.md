# 8.5 Metaprogramming
⚠️ **Warning: Advanced Topic!** ⚠️

*Estimated time for this notebook: 15 minutes*

## Metaprogramming globals


Consider a bunch of variables, each of which need initialising and incrementing:





```python
bananas = 0
apples = 0
oranges = 0
bananas += 1
apples += 1
oranges += 1
```



The right hand side of these assignments doesn't respect the DRY principle. We
could of course define a variable for our initial value:





```python
initial_fruit_count = 0
bananas = initial_fruit_count
apples = initial_fruit_count
oranges = initial_fruit_count
```



However, this is still not as DRY as it could be: what if we wanted to replace
the assignment with, say, a class constructor and a buy operation:





```python
class Basket:
    def __init__(self):
        self.count = 0

    def buy(self):
        self.count += 1


bananas = Basket()
apples = Basket()
oranges = Basket()
bananas.buy()
apples.buy()
oranges.buy()
```



We had to make the change in three places. Whenever you see a situation where a
refactoring or change of design might require you to change the code in
multiple places, you have an opportunity to make the code DRYer.

In this case, metaprogramming for incrementing these variables would involve
just a loop over all the variables we want to initialise:





```python
baskets = [bananas, apples, oranges]
for basket in baskets:
    basket.buy()
```



However, this trick **doesn't** work for initialising a new variable:





```python
baskets = [bananas, apples, oranges, kiwis]
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    /var/folders/xv/d5nvn2ps5r3fcf276w707n01qdmpqf/T/ipykernel_48934/672045426.py in <module>
    ----> 1 baskets = [bananas, apples, oranges, kiwis]
    

    NameError: name 'kiwis' is not defined




So can we declare a new variable programmatically? Given a list of the
**names** of fruit baskets we want, initialise a variable with that name?







Every module or class in Python, is, under the hood, a special
dictionary storing the values in its **namespace**. `globals()` gives a reference to the attribute dictionary for the current module:





```python
print("globals() is a\n", type(globals()))
print("\nWith these keys:\n", globals().keys())
```

    globals() is a
     <class 'dict'>
    
    With these keys:
     dict_keys(['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__builtin__', '__builtins__', '_ih', '_oh', '_dh', 'In', 'Out', 'get_ipython', 'exit', 'quit', '_', '__', '___', '_i', '_ii', '_iii', '_i1', 'bananas', 'apples', 'oranges', '_i2', 'initial_fruit_count', '_i3', 'Basket', '_i4', 'baskets', 'basket', '_i5', '_i6'])


We can access variables via this dictionary:


```python
globals()["apples"]
```




    <__main__.Basket at 0x1092ea970>




```python
apples
```




    <__main__.Basket at 0x1092ea970>



And create new variables by assigning to this dictionary:


```python
basket_names = ["bananas", "apples", "oranges", "kiwis"]

for name in basket_names:
    globals()[name] = Basket()


kiwis.count
```




    0





This is **metaprogramming**.

I would NOT recommend using it for an example as trivial as the one above. 
A better, more Pythonic choice here would be to use a data structure to manage your set of fruit baskets:





```python
baskets = {}
for name in basket_names:
    baskets[name] = Basket()

baskets["kiwis"].count
```




    0





Or even, using a dictionary comprehension:





```python
baskets = {name: Basket() for name in baskets}
baskets["kiwis"].count
```




    0





Which is the nicest way to do this, I think. Code which feels like
metaprogramming is needed to make it less repetitive can often instead be DRYed
up using a refactored data structure, in a way which is cleaner and more easy
to understand. Nevertheless, metaprogramming is worth knowing. 


## Metaprogramming class attributes

We can metaprogram the attributes of a **module** using the globals() function.

We will also want to be able to metaprogram a class, by accessing its attribute dictionary.

This will allow us, for example, to programmatically add members to a class.


```python
class Boring:
    pass
```

If we are adding our own attributes, we can just do so directly:


```python
x = Boring()

x.name = "Michael"
```


```python
x.name
```




    'Michael'



And these turn up, as expected, in an attribute dictionary for the class:


```python
x.__dict__
```




    {'name': 'Michael'}



We can use `getattr` to access this special dictionary:


```python
getattr(x, "name")
```




    'Michael'



If we want to add an attribute given it's name as a string, we can use setattr:


```python
setattr(x, "age", 75)

x.age
```




    75



And we could do this in a loop to programmatically add many attributes.

The real power of accessing the attribute dictionary comes when we realise that
there is *very little difference* between member data and member functions.

Now that we know, from our functional programming, that **a function is just a
variable that can be *called* with `()`**, we can set an attribute to a function,
and
it becomes a member function!


```python
setattr(Boring, "describe", lambda self: f"{self.name} is {self.age}")
```


```python
x.describe()
```




    'Michael is 75'




```python
x.describe
```




    <bound method <lambda> of <__main__.Boring object at 0x10acb4880>>




```python
Boring.describe
```




    <function __main__.<lambda>(self)>



Note that we set this method as an attribute of the class, not the instance, so it is available to other instances of `Boring`:


```python
y = Boring()
y.name = "Terry"
y.age = 78
```


```python
y.describe()
```




    'Terry is 78'



We can define a standalone function, and then **bind** it to the class. Its first argument automagically becomes
`self`.


```python
import datetime


def broken_birth_year(b_instance):
    current = datetime.datetime.now().year
    return current - b_instance.age
```


```python
Boring.birth_year = broken_birth_year
```


```python
x.birth_year()
```




    1947




```python
x.birth_year
```




    <bound method broken_birth_year of <__main__.Boring object at 0x10acb4880>>




```python
x.birth_year.__name__
```




    'broken_birth_year'



## Metaprogramming function locals

We can access the attribute dictionary for the local namespace inside a
function with `locals()` but this *cannot be written to*.

Lack of safe
programmatic creation of function-local variables is a flaw in Python.


```python
class Person:
    def __init__(self, name, age, job, children_count):
        for var_name, value in locals().items():
            if var_name == "self":
                continue
            print(f"Setting self.{var_name} to {value}")
            setattr(self, var_name, value)
```


```python
terry = Person("Terry", 78, "Screenwriter", 0)
```

    Setting self.first_name to Terry
    Setting self.age to 78
    Setting self.job to Screenwriter
    Setting self.children_count to 0



```python
terry.first_name
```




    'Terry'



## Metaprogramming warning!


Use this stuff **sparingly**!

The above example worked, but it produced Python code which is not particularly understandable.
Remember, your objective when programming is to produce code which is **descriptive of what it does**.

The above code is **definitely** less readable, less maintainable and more error prone than:





```python
class Person:
    def __init__(self, name, age, job, children_count):
        self.name = name
        self.age = age
        self.job = job
        self.children_count = children_count
```




Sometimes, metaprogramming will be **really** helpful in making non-repetitive
code, and you should have it in your toolbox, which is why I'm teaching you it.
But doing it all the time overcomplicated matters. We've talked a lot about the
DRY principle, but there is another equally important principle:

> **KISS**: *Keep it simple, Stupid!*

Whenever you write code and you think, "Gosh, I'm really clever",you're
probably *doing it wrong*. Code should be about clarity, not showing off.

