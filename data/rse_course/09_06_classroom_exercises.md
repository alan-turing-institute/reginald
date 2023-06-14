# 9.6 Classroom Exercises

**List of exercises**


[9a - Timing](#Exercise-9a-Timing) 

[9b -  Multiplication vs. power](#Exercise-9b-Multiplication-vs.-power) 

[9c - Binary Mandelbrot](#Exercise-9c-Binary-Mandelbrot) 

[9d - Parallelisation with Multiprocessing](#Exercise-9d-Parallelisation-with-Multiprocessing)

[9e - Performance Scaling](#Exercise-9e-Performance-Scaling)

## Exercise 9a Timing

*Relevant sections: 9.0.1 - 9.0.4*

Which is faster

```python
complex(a,b)
```

or 

```python
a + b*1j
```
with a = 5 and b = 6?

## Exercise 9b Multiplication vs. power

*Relevant sections: 9.1.1, 9.1.2.*

- Write another function that does the same, but squares a value by multiplying it with itself.
- Compare the performance of the two functions. Which one is faster?

## Exercise 9c Binary Mandelbrot

*Relevant sections: 9.2.1, 9.2.2*

Can you use this techinque to stop our values going to infinity? 
- Modify the function accordingly using the hint below.
- Time the performance of the modified function.
- Plot the result.

**Hint:** Look at what this code is doing.
```python
a = np.linspace(1,10,10)
b = a > 5
a[b] = 5
a
```

## Exercise 9d Parallelisation with Multiprocessing

*Relevant sections: 9.4.1, 9.4.2*

- Remove the call to `sleep()`
- Reload the `sleeping` module 
- Run the `list(map(...))` vs `pool.map(...)` comparison again

Which is faster, and by how much? Why?

## Exercise 9e Performance Scaling

*Relevant sections: Notebook 9.5*

In a previous notebook, we found that doing `a * a` was quicker than `a ** 2`. Is this true for all exponents, even very large ones?
If not, at what point do they cross over?
Can you plot it?


```python
def time_pow_multiply(power):

    the_string = "2"

    for _ in range(power - 1):
        # ToDo Complete this loop
        pass

    return repeat(the_string, number=100)
```


```python
def time_pow_expo(power):

    # ToDo Complete this string
    the_string = ""

    return repeat(the_string, number=100)
```
