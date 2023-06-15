# 8.7 Exercises

### Exercise 1: Iterators and generators

Write your own version of the `range` iterator. If we call it `range2`, then `range2(10)` should return an iterator such that repeatedly calling `next` on it yields the numbers from 0 to 9, and then terminates. Do this both
1. as a class with `__iter__` and `__next__` methods.
2. as a generator, using the `yield` statement.

### Exercise 2: Operator overloading

Often in research code, we might want to construct a data "pipeline", where different bits of code perform different operations on our data.   For example, there might be a "Data Loader" module, a "Data Cleaner" module, one or more "Data Processor" modules, and a "Data Output" module.

We could potentially use Operator Overloading to compose this pipeline.  In particular, the `__iadd__` function will overload `+=`, so we could for example do:

```
mypipeline = Pipeline()
mypipeline += DataLoader()
mypipeline += DataCleaner()
```

Here are some basic classes we could use:


```python
class Pipeline:
    def __init__(self):
        self.modules = []

    def process(self):
        print("I'm a pipeline, don't do anything much by myself")
        for module in self.modules:
            module.process()
```


```python
class DataLoader:
    def __init__(self):
        pass

    def process(self):
        print("I am loading some data")


class DataCleaner:
    def __init__(self):
        pass

    def process(self):
        print("I am cleaning some data")
```

Have a go at overloading the '+=' operator such that we can add modules to the pipeline, and the following code would work:


```python
p = Pipeline()
p += DataLoader()
p += DataCleaner()
p.process()
```
