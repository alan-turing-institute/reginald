# 2.2 Using Libraries

*Estimated time for this notebook: 5 minutes*

## 2.2.1 Import

Research programming is all about using libraries: tools other people have provided programs that do many cool things.
By combining them we can feel really powerful but doing minimum work ourselves.

The python syntax to import someone else's library is "import".
To use a function or type from a python library, rather than a **built-in** function or type, we have to import the library.


```python
math.sin(1.6)
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    Input In [1], in <cell line: 1>()
    ----> 1 math.sin(1.6)


    NameError: name 'math' is not defined



```python
import math
```


```python
math.sin(1.6)
```




    0.9995736030415051



We call these libraries **modules**:


```python
type(math)
```




    module



The tools supplied by a module are *attributes* of the module, and as such, are accessed with a dot.


```python
dir(math)
```




    ['__doc__',
     '__file__',
     '__loader__',
     '__name__',
     '__package__',
     '__spec__',
     'acos',
     'acosh',
     'asin',
     'asinh',
     'atan',
     'atan2',
     'atanh',
     'ceil',
     'comb',
     'copysign',
     'cos',
     'cosh',
     'degrees',
     'dist',
     'e',
     'erf',
     'erfc',
     'exp',
     'expm1',
     'fabs',
     'factorial',
     'floor',
     'fmod',
     'frexp',
     'fsum',
     'gamma',
     'gcd',
     'hypot',
     'inf',
     'isclose',
     'isfinite',
     'isinf',
     'isnan',
     'isqrt',
     'ldexp',
     'lgamma',
     'log',
     'log10',
     'log1p',
     'log2',
     'modf',
     'nan',
     'perm',
     'pi',
     'pow',
     'prod',
     'radians',
     'remainder',
     'sin',
     'sinh',
     'sqrt',
     'tan',
     'tanh',
     'tau',
     'trunc']



They include properties as well as functions:


```python
math.pi
```




    3.141592653589793



You can always find out where on your storage medium a library has been imported from:


```python
print(math.__file__[0:50])
print(math.__file__[50:])
```

    /usr/local/anaconda3/envs/rse_course/lib/python3.8
    /lib-dynload/math.cpython-38-darwin.so


Note that `import` does *not* install libraries. It just makes them available to your current notebook session, assuming they are already installed. Installing libraries is harder, and we'll cover it later.
So what libraries are available? Until you install more, you might have just the modules that come with Python, the *standard library*.

**Supplementary Materials**: Review the list of standard library modules: https://docs.python.org/library/

If you installed via Anaconda, then you also have access to a bunch of modules that are commonly used in research.

**Supplementary Materials**: Review the list of modules that are packaged with Anaconda by default on different architectures: https://docs.anaconda.com/anaconda/packages/pkg-docs/ (modules installed by default are shown with ticks)

We'll see later how to add more libraries to our setup.

### Why bother?

Why bother with modules? Why not just have everything available all the time?

The answer is that there are only so many names available! Without a module system, every time I made a variable whose name matched a function in a library, I'd lose access to it. In the olden days, people ended up having to make really long variable names, thinking their names would be unique, and they still ended up with "name clashes". The module mechanism avoids this.

## 2.2.2 Importing from modules

Still, it can be annoying to have to write `math.sin(math.pi)` instead of `sin(pi)`.
Things can be imported *from* modules to become part of the current module:


```python
import math

math.sin(math.pi)
```




    1.2246467991473532e-16




```python
from math import sin

sin(math.pi)
```




    1.2246467991473532e-16



Importing one-by-one like this is a nice compromise between typing and risk of name clashes.

It *is* possible to import **everything** from a module, but you risk name clashes.


```python
from math import *

sin(pi)
```




    1.2246467991473532e-16



###  Import and rename

You can rename things as you import them to avoid clashes or for typing convenience


```python
import math as m

m.cos(0)
```




    1.0




```python
pi = 3
from math import pi as realpi

print(sin(pi), sin(realpi))
```

    0.1411200080598672 1.2246467991473532e-16
