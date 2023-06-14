# 8.2 Iterators and Generators

*Estimated time for this notebook: 25 minutes*

In Python, anything which can be iterated over is called an iterable:


```python
bowl = {"apple": 5, "banana": 3, "orange": 7}

for fruit in bowl:
    print(fruit.upper())
```

    APPLE
    BANANA
    ORANGE


Surprisingly often, we want to iterate over something that takes a moderately
large amount of memory to store - for example, our map images in the
green-graph example.

Our green-graph example involved making an array of all the maps between London
and Birmingham. This kept them all in memory *at the same time*: first we
downloaded all the maps, then we counted the green pixels in each of them. 

This would NOT work if we used more points: eventually, we would run out of memory.
We need to use a **generator** instead. This chapter will look at iterators and generators in more detail:
how they work, when to use them, how to create our own.

## Iterators

Consider the basic python `range` function:


```python
range(10)
```




    range(0, 10)




```python
total = 0
for x in range(int(1e6)):
    total += x

total
```




    499999500000



In order to avoid allocating a million integers, `range` actually uses an **iterator**.

We don't actually need a million integers *at once*, just each
integer *in turn* up to a million.

Because we can get an iterator from it, we say that a range is an **iterable**.

So we can `for`-loop over it:


```python
for i in range(3):
    print(i)
```

    0
    1
    2


There are two important Python built-in functions for working with iterables.
First is `iter`, which lets us create an iterator from any iterable object.


```python
a = iter(range(3))
```

Once we have an iterator object, we can pass it to the `next` function. This
moves the iterator forward, and gives us its next element:


```python
next(a)
```




    0




```python
next(a)
```




    1




```python
next(a)
```




    2



When we are out of elements, a `StopIteration` exception is raised:


```python
next(a)
```


    ---------------------------------------------------------------------------

    StopIteration                             Traceback (most recent call last)

    /var/folders/xv/d5nvn2ps5r3fcf276w707n01qdmpqf/T/ipykernel_88854/1242322984.py in <module>
    ----> 1 next(a)
    

    StopIteration: 


This tells Python that the iteration is over. For example, if we are in a `for i in range(3)` loop, this lets us know when we should exit the loop.

We can turn an iterable or iterator into a list with the `list` constructor function:


```python
list(range(5))
```




    [0, 1, 2, 3, 4]



## Defining Our Own Iterable

When we write `next(a)`, under the hood Python tries to call the `__next__()` method of `a`. Similarly, `iter(a)` calls `a.__iter__()`.

We can make our own iterators by defining *classes* that can be used with the `next()` and `iter()` functions: this is the **iterator protocol**.

For each of the *concepts* in Python, like sequence, container, iterable, the language defines a *protocol*, a set of methods a class must implement, in order to be treated as a member of that concept.

To define an iterator, the methods that must be supported are `__next__()` and `__iter__()`.

`__next__()` must update the iterator.

We'll see why we need to define `__iter__` in a moment.

Here is an example of defining a custom iterator class:


```python
class fib_iterator:
    """An iterator over part of the Fibonacci sequence."""

    def __init__(self, limit, seed1=1, seed2=1):
        self.limit = limit
        self.previous = seed1
        self.current = seed2

    def __iter__(self):
        return self

    def __next__(self):
        (self.previous, self.current) = (self.current, self.previous + self.current)
        self.limit -= 1
        if self.limit < 0:
            raise StopIteration()
        return self.current
```


```python
x = fib_iterator(5)
```


```python
next(x)
```




    2




```python
next(x)
```




    3




```python
next(x)
```




    5




```python
next(x)
```




    8




```python
for x in fib_iterator(5):
    print(x)
```

    2
    3
    5
    8
    13



```python
sum(fib_iterator(1000))
```




    297924218508143360336882819981631900915673130543819759032778173440536722190488904520034508163846345539055096533885943242814978469042830417586260359446115245634668393210192357419233828310479227982326069668668250



## A shortcut to iterables: the `__iter__` method

In fact,  we don't always have to define both `__iter__` and `__next__`!

If, to be iterated over, a class just wants to behave as if it were some other iterable, you can just implement `__iter__` and return `iter(some_other_iterable)`, without implementing `next`.  For example, an image class might want to implement some metadata, but behave just as if it were just a 1-d pixel array when being iterated:


```python
from matplotlib import pyplot as plt
from numpy import array


class MyImage:
    def __init__(self, pixels):
        self.pixels = array(pixels, dtype="uint8")
        self.channels = self.pixels.shape[2]

    def __iter__(self):
        # return an iterator over just the pixel values
        return iter(self.pixels.reshape(-1, self.channels))

    def show(self):
        plt.imshow(self.pixels, interpolation="None")


x = [[[255, 255, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 255]]]
image = MyImage(x)
```


```python
%matplotlib inline
image.show()
```


    
![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module08_advanced_programming_techniques/08_02_iterators_and_generators_37_0.png)
    



```python
image.channels
```




    3




```python
from webcolors import rgb_to_name

for pixel in image:
    print(rgb_to_name(pixel))
```

    yellow
    lime
    blue
    white


See how we used `image` in a `for` loop, even though it doesn't satisfy the iterator protocol (we didn't define both `__iter__` and `__next__` for it)?

The key here is that we can use any *iterable* object (like `image`) in a `for` expression,
not just iterators! Internally, Python will create an iterator from the iterable (by calling its `__iter__` method), but this means we don't need to define a `__next__` method explicitly.

The *iterator* protocol is to implement both `__iter__` and
`__next__`, while the *iterable* protocol is to implement `__iter__` and return
an iterator.

## Generators

There's a fair amount of "boiler-plate" in the above class-based definition of
an iterable.

Python provides another way to specify something
which meets the iterator protocol: **generators**.


```python
def my_generator():
    yield 5
    yield 10


x = my_generator()
```


```python
next(x)
```




    5




```python
next(x)
```




    10




```python
next(x)
```


    ---------------------------------------------------------------------------

    StopIteration                             Traceback (most recent call last)

    /var/folders/xv/d5nvn2ps5r3fcf276w707n01qdmpqf/T/ipykernel_88854/3485793935.py in <module>
    ----> 1 next(x)
    

    StopIteration: 



```python
for a in my_generator():
    print(a)
```

    5
    10



```python
sum(my_generator())
```




    15



A function which has `yield` statements instead of a `return` statement returns
**temporarily**: it automagically becomes something which implements `__next__`.

Each call of `next()` returns control to the function where it
left off.

 Control passes back-and-forth between the generator and the caller.
Our Fibonacci example therefore becomes a function rather than a class.


```python
def yield_fibs(limit, seed1=1, seed2=1):
    current = seed1
    previous = seed2

    while limit > 0:
        limit -= 1
        current, previous = current + previous, current
        yield current
```

We can now use the output of the function like a normal iterable:


```python
sum(yield_fibs(5))
```




    31




```python
for a in yield_fibs(10):
    if a % 2 == 0:
        print(a)
```

    2
    8
    34
    144


Sometimes we may need to gather all values from a generator into a list, such as before passing them to a function that expects a list:


```python
list(yield_fibs(10))
```




    [2, 3, 5, 8, 13, 21, 34, 55, 89, 144]




```python
plt.plot(list(yield_fibs(20)))
```




    [<matplotlib.lines.Line2D at 0x10e30d130>]




    
![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module08_advanced_programming_techniques/08_02_iterators_and_generators_59_1.png)
    


# Related Concepts

Iterables and generators can be used to achieve complex behaviour, especially when combined with functional programming. In fact, Python itself contains some very useful language features that make use of these practices: context managers and decorators. We have already seen these in this class, but here we discuss them in more detail.

## Context managers

[We have seen before](../module02_intermediate_python/02_04_working_with_files.html#Closing-files) [[notebook](../module02_intermediate_python/02_04_working_with_files.ipynb#Closing-files)] that, instead of separately `open`ing and `close`ing a file, we can have
the file be automatically closed using a context manager:


```python
%%writefile example.yaml
modelname: brilliant
```

    Overwriting example.yaml



```python
import yaml

with open("example.yaml") as foo:
    print(yaml.safe_load(foo))
```

    {'modelname': 'brilliant'}


In addition to more convenient syntax, this takes care of any clean-up that has to be done after the file is closed, even if any errors occur while we are working on the file.




How could we define our own one of these, if we too have clean-up code we
always want to run after a calling function has done its work, or set-up code
we want to do first?

We can define a class that meets an appropriate protocol:





```python
class verbose_context:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print("Get ready, ", self.name)

    def __exit__(self, exc_type, exc_value, traceback):
        print("OK, done")


with verbose_context("Monty"):
    print("Doing it!")
```

    Get ready,  Monty
    Doing it!
    OK, done




However, this is pretty verbose! Again, a generator with `yield` makes for an easier syntax:





```python
from contextlib import contextmanager


@contextmanager
def verbose_context(name):
    print("Get ready for action, ", name)
    yield name.upper()
    print("You did it")


with verbose_context("Monty") as shouty:
    print(f"Doing it, {shouty}")
```

    Get ready for action,  Monty
    Doing it, MONTY
    You did it




Again, we use `yield` to temporarily return from a function.


## Decorators


When doing functional programming, we may often want to define mutator
functions which take in one function and return a new function, such as our
derivative example earlier.





```python
def repeat(func):
    def _repeated(x):
        return func(func(x))

    return _repeated


def hello(name):
    return f"Hello, {name}"


print(hello("Cleese"))
print(repeat(hello)("Cleese"))
```

    Hello, Cleese
    Hello, Hello, Cleese


Any function which accepts a function as its first argument and returns a function can be used as a **decorator** like this:


```python
@repeat
def hello(name):
    return f"Hello, {name}"


hello("Cleese")
```




    'Hello, Hello, Cleese'



We could also modify this to create a decorator that takes an argument specifying how many times the function should be repeated: 


```python
def repeater(count):
    def wrap_function_in_repeat(func):
        def _repeated(x):
            counter = count
            while counter > 0:
                counter -= 1
                x = func(x)
            return x

        return _repeated

    return wrap_function_in_repeat
```


```python
from math import sqrt

fiftytimes = repeater(50)
fiftyroots = fiftytimes(sqrt)

fiftyroots(100)
```




    1.000000000000004




```python
@repeater(3)
def hello(name):
    return f"Hello, {name}"


hello("Cleese")
```




    'Hello, Hello, Hello, Cleese'



It turns out that, quite often, we want to apply one of these to a function as we're defining a class.
For example, we may want to specify that after certain methods are called, data should always be stored.

Much of Python's standard functionality is implemented as decorators: we've
seen `@contextmanager`, `@classmethod` and `@attribute`. The `@contextmanager`
metafunction, for example, takes in an iterator, and yields a class conforming
to the context manager protocol.



# Supplementary material

The remainder of this page contains an example of the flexibility of the features discussed above. Specifically, it shows how generators and context managers can be combined to create a testing framework like the one previously seen in the course.

## Test generators

Earlier in the course we saw a test which loaded its test cases from a YAML file and asserted each input with each output.
This was nice and concise, but had one flaw: we had just one test, covering all the fixtures, so we got just one `.` in the test output when we ran the tests, and if any test failed, the rest were not run.
We can do a nicer job with a test **generator**:


```python
import os


def assert_exemplar(**fixture):
    answer = fixture.pop("answer")
    assert_equal(greet(**fixture), answer)


def test_greeter():
    with open(
        os.path.join(os.path.dirname(__file__), "fixtures", "samples.yaml")
    ) as fixtures_file:
        fixtures = yaml.safe_load(fixtures_file)

        for fixture in fixtures:
            yield assert_exemplar(**fixture)
```

Each time a function beginning with `test_` does a `yield` it results in another test.

## Negative test contexts managers

We have seen this:


```python
from pytest import raises

with raises(AttributeError):
    x = 2
    x.foo()
```

We can now see how `pytest` might have implemented this:


```python
@contextmanager
def reimplement_raises(exception):
    try:
        yield
    except exception:
        pass
    else:
        raise Exception("Expected,", exception, " to be raised, nothing was.")
```


```python
with reimplement_raises(AttributeError):
    x = 2
    x.foo()
```

## Skip test decorators

Some frameworks also implement decorators for skipping tests or dealing with tests that are known to raise exceptions (due to known bugs or limitations). For example:


```python
%%writefile test_skipped.py
import pytest
import sys


@pytest.mark.skipif(sys.version_info < (4, 0), reason="requires python 4")
def test_python_4():
    raise RuntimeError("something went wrong")
```

    Writing test_skipped.py



```python
! pytest test_skipped.py
```

    [1m============================= test session starts ==============================[0m
    platform darwin -- Python 3.8.12, pytest-7.1.3, pluggy-1.0.0
    rootdir: /Users/jrobinson/projects/applied-skills/rse-course/module08_advanced_programming_techniques
    plugins: anyio-3.6.1, cov-4.0.0, pylama-8.4.1
    collected 1 item                                                               [0m
    
    test_skipped.py [33ms[0m[33m                                                        [100%][0m
    
    [33m============================== [33m[1m1 skipped[0m[33m in 0.05s[0m[33m ==============================[0m
    [0m


```python
%%writefile test_not_skipped.py
import pytest
import sys


@pytest.mark.skipif(sys.version_info < (3, 0), reason="requires python 3")
def test_python_3():
    raise RuntimeError("something went wrong")
```

    Writing test_not_skipped.py



```python
! pytest test_not_skipped.py
```

    [1m============================= test session starts ==============================[0m
    platform darwin -- Python 3.8.12, pytest-7.1.3, pluggy-1.0.0
    rootdir: /Users/jrobinson/projects/applied-skills/rse-course/module08_advanced_programming_techniques
    plugins: anyio-3.6.1, cov-4.0.0, pylama-8.4.1
    collected 1 item                                                               [0m
    
    test_not_skipped.py [31mF[0m[31m                                                    [100%][0m
    
    =================================== FAILURES ===================================
    [31m[1m________________________________ test_python_3 _________________________________[0m
    
        [37m@pytest[39;49;00m.mark.skipif(sys.version_info < ([94m3[39;49;00m, [94m0[39;49;00m), reason=[33m"[39;49;00m[33mrequires python 3[39;49;00m[33m"[39;49;00m)
        [94mdef[39;49;00m [92mtest_python_3[39;49;00m():
    >       [94mraise[39;49;00m [96mRuntimeError[39;49;00m([33m"[39;49;00m[33msomething went wrong[39;49;00m[33m"[39;49;00m)
    [1m[31mE       RuntimeError: something went wrong[0m
    
    [1m[31mtest_not_skipped.py[0m:7: RuntimeError
    =========================== short test summary info ============================
    FAILED test_not_skipped.py::test_python_3 - RuntimeError: something went wrong
    [31m============================== [31m[1m1 failed[0m[31m in 0.18s[0m[31m ===============================[0m
    [0m

We could reimplement this ourselves now too:


```python
def homemade_skip_decorator(skip):
    def wrap_function(func):
        if skip:
            # if the test should be skipped, return a function
            # that just prints a message
            def do_nothing(*args):
                print("test was skipped")

            return do_nothing
        # otherwise use the original function as normal
        return func

    return wrap_function
```


```python
@homemade_skip_decorator(3.9 < 4.0)
def test_skipped():
    raise RuntimeError("This test is skipped")


test_skipped()
```

    test was skipped



```python
@homemade_skip_decorator(3.9 < 3.0)
def test_runs():
    raise RuntimeError("This test is run")


test_runs()
```


    ---------------------------------------------------------------------------

    RuntimeError                              Traceback (most recent call last)

    Input In [130], in <cell line: 6>()
          1 @homemade_skip_decorator(3.9 < 3.0)
          2 def test_runs():
          3     raise RuntimeError("This test is run")
    ----> 6 test_runs()


    Input In [130], in test_runs()
          1 @homemade_skip_decorator(3.9 < 3.0)
          2 def test_runs():
    ----> 3     raise RuntimeError("This test is run")


    RuntimeError: This test is run

