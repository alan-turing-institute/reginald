# 9.1 Optimising with pure Python

*Estimated time for this notebook: 5 minutes*

First, we look at changes we can make to our function that don't rely on any external libraries or tools.

We start by copying our `mandel()` function into this notebook and producing a list of input values for the function.


```python
def mandel(constant, max_iterations=50):
    """Computes the values of the series for up to a maximum number of iterations.

    The function stops when the absolute value of the series surpasses 2 or when it reaches the maximum
    number of iterations.

    Returns the number of iterations.
    """

    value = 0

    counter = 0
    while counter < max_iterations:
        if abs(value) > 2:
            break

        value = (value**2) + constant

        counter = counter + 1

    return counter


assert mandel(0) == 50
assert mandel(3) == 1
assert mandel(0.5) == 5
```


```python
xmin = -1.5
ymin = -1.0
xmax = 0.5
ymax = 1.0
resolution = 300
xstep = (xmax - xmin) / resolution
ystep = (ymax - ymin) / resolution
xs = [(xmin + xstep * i) for i in range(resolution)]
ys = [(ymin + ystep * i) for i in range(resolution)]
```

## 9.1.1 Attempt 1: For-loop vs. list comprehension

We want to run our `mandel` function on a range of complex input values. We can do that by either looping over all the values in the (nested) list, or by using a list comprehension as we did in the previous notebook. We know that list comprehensions are supposed to be more "pythonic", but are they also faster? Let's find out!


```python
def listcomp_mandel(xs, ys):
    return [[mandel(x + 1j * y) for x in xs] for y in ys]
```


```python
def for_loop_mandel(xs, ys):
    result = []

    for y in ys:
        result_inner = []
        for x in xs:
            result_inner.append(mandel(x + 1j * y))
        result.append(result_inner)
    return result


assert for_loop_mandel([1], [0]) == [[3]]
```


```python
%%timeit
listcomp_mandel(xs, ys)
```

    432 ms ± 9.38 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)



```python
%%timeit
for_loop_mandel(xs, ys)
```

    438 ms ± 6.66 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


The results are very close. A bit disappointing, but at least the list comprehensions look more elegant.

## 9.1.2 Profiling

It looks like we don't gain much by changing the way we call the function. Maybe we should instead focus on the function itself. 
There are useful tools out there that we can use to gain more insight into which part of a function takes up most computation time. In this module we use `line_profiler`.

`line_profiler` is a Python module that we need to install into our virtual environment before we can use it.
This tool breaks down the computation time of our function line by line. 


```python
# you can also run this in your terminal (without the '!')
!pip install line_profiler
```

    Requirement already satisfied: line_profiler in /Users/pwochner/Projects/rse-course-2022/rse-course/.venv/lib/python3.7/site-packages (3.5.1)
    
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m A new release of pip available: [0m[31;49m22.3[0m[39;49m -> [0m[32;49m22.3.1[0m
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m To update, run: [0m[32;49mpip install --upgrade pip[0m



```python
%load_ext line_profiler
```


```python
%lprun?
```


```python
%lprun -f mandel mandel(xs[0] + 1j*ys[0])
```

## 9.1.3 Attempt 2: Multiplication vs. power

Looking at the `line_profiler` output, it seems like the line where we compute the value of the series for the current iteration takes quite long. The operations that are performed are squaring the value (using power 2) and adding a constant. Maybe we can speed up the code by replacing the power operation by multiplying the value with itself. 

Before we re-write the `mandel()` function, we will write new functions that repeatedly squares a value for a given number of iterations.


```python
def square_power(value, iterations):
    """Repeatedly square a value using **."""

    for _ in range(iterations):
        value = value**2

    return value


assert square_power(2, 1) == 4
assert square_power(2, 0) == 2
```

Go to notebook **9.6 Classroom Exercises** and do exercise 9b. 

 ...
 

 ...
 
 
 ...
 
 ...
 

 ...
 
 
 ...

We now have another function to square a value, this time by multiplying the value with itself. This function could look like this.


```python
def square_multiply(value, iterations):
    """Repeatedly square a value using *."""

    for _ in range(iterations):
        value = value * value

    return value


assert square_multiply(2, 1) == 4
assert square_multiply(2, 0) == 2
```

The computational cost for `square_power` and `square_multiply` are quite different. 
Conclusion: `**` is not simply a wrapper around `*`.

Can we find out more about this?

The `dis` module supports analysis of CPython code by disassembling it.


```python
import dis
```


```python
dis.dis(square_power)
```

      4           0 SETUP_LOOP              24 (to 26)
                  2 LOAD_GLOBAL              0 (range)
                  4 LOAD_FAST                1 (iterations)
                  6 CALL_FUNCTION            1
                  8 GET_ITER
            >>   10 FOR_ITER                12 (to 24)
                 12 STORE_FAST               2 (_)
    
      5          14 LOAD_FAST                0 (value)
                 16 LOAD_CONST               1 (2)
                 18 BINARY_POWER
                 20 STORE_FAST               0 (value)
                 22 JUMP_ABSOLUTE           10
            >>   24 POP_BLOCK
    
      7     >>   26 LOAD_FAST                0 (value)
                 28 RETURN_VALUE



```python
dis.dis(square_multiply)
```

      4           0 SETUP_LOOP              24 (to 26)
                  2 LOAD_GLOBAL              0 (range)
                  4 LOAD_FAST                1 (iterations)
                  6 CALL_FUNCTION            1
                  8 GET_ITER
            >>   10 FOR_ITER                12 (to 24)
                 12 STORE_FAST               2 (_)
    
      5          14 LOAD_FAST                0 (value)
                 16 LOAD_FAST                0 (value)
                 18 BINARY_MULTIPLY
                 20 STORE_FAST               0 (value)
                 22 JUMP_ABSOLUTE           10
            >>   24 POP_BLOCK
    
      7     >>   26 LOAD_FAST                0 (value)
                 28 RETURN_VALUE


We can see that the two methods of squaring are translated into different bite code. The Python interpreter is not optimising (whereas a compiler in a compiled language might be able to do that).

## 9.1.4 Attempt 3: In-place multiplication

Python has an operator for inplace multiplication: `*=`. Is that faster?


```python
def square_inplace_multiply(value, iterations):
    """Repeatedly square a value using *."""

    for _ in range(iterations):
        value *= value

    return value


assert square_multiply(2, 1) == 4
assert square_multiply(2, 0) == 2
```


```python
%%timeit
square_inplace_multiply(1.9, 10)
```

    553 ns ± 18.9 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)


This is the slowest way of squaring a value that we've tried.


```python
dis.dis(square_inplace_multiply)
```

      4           0 SETUP_LOOP              24 (to 26)
                  2 LOAD_GLOBAL              0 (range)
                  4 LOAD_FAST                1 (iterations)
                  6 CALL_FUNCTION            1
                  8 GET_ITER
            >>   10 FOR_ITER                12 (to 24)
                 12 STORE_FAST               2 (_)
    
      5          14 LOAD_FAST                0 (value)
                 16 LOAD_FAST                0 (value)
                 18 INPLACE_MULTIPLY
                 20 STORE_FAST               0 (value)
                 22 JUMP_ABSOLUTE           10
            >>   24 POP_BLOCK
    
      7     >>   26 LOAD_FAST                0 (value)
                 28 RETURN_VALUE


## 9.1.4 Rewrite Mandelbrot: "square-by-multiply"

Let's rewrite the `mandel()` function and time its performance, using what we've learnt in this notebook:
- Square the value by multiplication with itself (but not inplace).
- Run the function over a range of values by using list comprehension (instead of for-loop).


```python
def mandel(constant, max_iterations=50):
    """Computes the values of the series for up to a maximum number of iterations.

    The function stops when the absolute value of the series surpasses 2 or when it reaches the maximum
    number of iterations.

    Returns the number of iterations.
    """

    value = 0

    counter = 0
    while counter < max_iterations:
        if abs(value) > 2:
            break

        value = (value * value) + constant

        counter = counter + 1

    return counter


assert mandel(0) == 50
assert mandel(3) == 1
assert mandel(0.5) == 5
```


```python
%%timeit
[[mandel(x + 1j * y) for x in xs] for y in ys]
```

    385 ms ± 6.21 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


## Things to be aware of

- Try to understand _why_ one method is faster than the other.
- Is it worth the speed up? 
- Do you get the same answers for all possible inputs?
- We're using CPython. Would the optimisations still hold for other implementations of Python?

