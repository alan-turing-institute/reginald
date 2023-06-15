*Estimated time for this notebook: 20 minutes*

Cython can be viewed as an extension of Python where variables and functions are annotated with extra information, in particular types. The resulting Cython source code will be compiled into optimized C or C++ code, which can potentially speed up slow Python code. In other words, Cython provides a way of writing Python with comparable performance to that of C/C++.

## 9.3.0 How to Build Cython Code

Cython code must, unlike Python, be compiled. This happens in the following stages:

* The cython code in `.pyx` file will be translated to a `C` file.
* The `C` file will be compiled by a C compiler into a shared library, which will be directly loaded into Python.

If you're writing `.py` files, you use the `cythonize` command in your terminal.
In a Jupyter notebook, everything is a lot easier. One needs only to load the Cython extension (`%load_ext Cython`) at the beginning and use `%%cython` cell magic. Cells starting with `%%cython` will be treated as a `.pyx` code and, consequently, compiled.

For details, please see [Building Cython Code](http://docs.cython.org/src/quickstart/build.html).

## 9.3.1 Compiling a Pure Python Function

We'll copy our pure Python `mandel()` function from the earlier notebook and redefine our real and imaginary inputs.


```python
xmin = -1.5
ymin = -1.0
xmax = 0.5
ymax = 1.0
resolution = 300
xstep = (xmax - xmin) / resolution
ystep = (ymax - ymin) / resolution
xs = [(xmin + (xmax - xmin) * i / resolution) for i in range(resolution)]
ys = [(ymin + (ymax - ymin) * i / resolution) for i in range(resolution)]
```


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

We will cythonise our function without adding any type hints.


```python
%load_ext Cython
```


```cython
%%cython

def mandel_cython():
    value = 0
```


```python
mandel_cython()
```


```cython
%%cython

def mandel_cython(constant, max_iterations=50):
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


assert mandel_cython(0) == 50
assert mandel_cython(3) == 1
assert mandel_cython(0.5) == 5
```

Let's verify the result


```python
data_python = [[mandel(x + 1j * y) for x in xs] for y in ys]
data_cython = [[mandel_cython(x + 1j * y) for x in xs] for y in ys]
```


```python
from matplotlib import pyplot as plt

plt.set_cmap("cividis")  # use a CVD-friendly palette

f, axarr = plt.subplots(1, 2)
axarr[0].imshow(data_python, interpolation="none", extent=[xmin, xmax, ymin, ymax])
axarr[0].set_title("Pure Python")
axarr[0].set_ylabel("Imaginary")
axarr[0].set_xlabel("Real")
axarr[1].imshow(data_cython, interpolation="none", extent=[xmin, xmax, ymin, ymax])
axarr[1].set_title("Cython")
axarr[1].set_ylabel("Imaginary")
axarr[1].set_xlabel("Real")
f.tight_layout()
```


    <Figure size 432x288 with 0 Axes>




![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module09_programming_for_speed/09_03_optimising_with_cython_15_1.png)




```python
%%timeit
[[mandel(x + 1j * y) for x in xs] for y in ys]  # pure python
```

    410 ms ± 7.08 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)



```python
%%timeit
[[mandel_cython(x + 1j * y) for x in xs] for y in ys]  # cython
```

    230 ms ± 9.05 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


We have improved the performance of a factor of 1.5 by just using the Cython compiler, **without changing the code**!

## 9.3.2 Cython with C Types

But we can do better by telling Cython what C data types we would use in the code. Note we're not actually writing C, we're writing Python with C types.

### The --annotate Option

If we pass the `--annotate`/`-a` option to `%%cython` then it will output information about the line-by-line cost of running your function. You can use this to target the most costly operations first or to estimate how much more optimising there is to do.


```cython
%%cython --annotate

def mandel_cython(constant, max_iterations=50):
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
```




<!DOCTYPE html>
<!-- Generated by Cython 0.29.24 -->
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Cython: _cython_magic_ef6ffd3d158c0ef85d8a6a569a8a1a20.pyx</title>
    <style type="text/css">

body.cython { font-family: courier; font-size: 12; }

.cython.tag  {  }
.cython.line { margin: 0em }
.cython.code { font-size: 9; color: #444444; display: none; margin: 0px 0px 0px 8px; border-left: 8px none; }

.cython.line .run { background-color: #B0FFB0; }
.cython.line .mis { background-color: #FFB0B0; }
.cython.code.run  { border-left: 8px solid #B0FFB0; }
.cython.code.mis  { border-left: 8px solid #FFB0B0; }

.cython.code .py_c_api  { color: red; }
.cython.code .py_macro_api  { color: #FF7000; }
.cython.code .pyx_c_api  { color: #FF3000; }
.cython.code .pyx_macro_api  { color: #FF7000; }
.cython.code .refnanny  { color: #FFA000; }
.cython.code .trace  { color: #FFA000; }
.cython.code .error_goto  { color: #FFA000; }

.cython.code .coerce  { color: #008000; border: 1px dotted #008000 }
.cython.code .py_attr { color: #FF0000; font-weight: bold; }
.cython.code .c_attr  { color: #0000FF; }
.cython.code .py_call { color: #FF0000; font-weight: bold; }
.cython.code .c_call  { color: #0000FF; }

.cython.score-0 {background-color: #FFFFff;}
.cython.score-1 {background-color: #FFFFe7;}
.cython.score-2 {background-color: #FFFFd4;}
.cython.score-3 {background-color: #FFFFc4;}
.cython.score-4 {background-color: #FFFFb6;}
.cython.score-5 {background-color: #FFFFaa;}
.cython.score-6 {background-color: #FFFF9f;}
.cython.score-7 {background-color: #FFFF96;}
.cython.score-8 {background-color: #FFFF8d;}
.cython.score-9 {background-color: #FFFF86;}
.cython.score-10 {background-color: #FFFF7f;}
.cython.score-11 {background-color: #FFFF79;}
.cython.score-12 {background-color: #FFFF73;}
.cython.score-13 {background-color: #FFFF6e;}
.cython.score-14 {background-color: #FFFF6a;}
.cython.score-15 {background-color: #FFFF66;}
.cython.score-16 {background-color: #FFFF62;}
.cython.score-17 {background-color: #FFFF5e;}
.cython.score-18 {background-color: #FFFF5b;}
.cython.score-19 {background-color: #FFFF57;}
.cython.score-20 {background-color: #FFFF55;}
.cython.score-21 {background-color: #FFFF52;}
.cython.score-22 {background-color: #FFFF4f;}
.cython.score-23 {background-color: #FFFF4d;}
.cython.score-24 {background-color: #FFFF4b;}
.cython.score-25 {background-color: #FFFF48;}
.cython.score-26 {background-color: #FFFF46;}
.cython.score-27 {background-color: #FFFF44;}
.cython.score-28 {background-color: #FFFF43;}
.cython.score-29 {background-color: #FFFF41;}
.cython.score-30 {background-color: #FFFF3f;}
.cython.score-31 {background-color: #FFFF3e;}
.cython.score-32 {background-color: #FFFF3c;}
.cython.score-33 {background-color: #FFFF3b;}
.cython.score-34 {background-color: #FFFF39;}
.cython.score-35 {background-color: #FFFF38;}
.cython.score-36 {background-color: #FFFF37;}
.cython.score-37 {background-color: #FFFF36;}
.cython.score-38 {background-color: #FFFF35;}
.cython.score-39 {background-color: #FFFF34;}
.cython.score-40 {background-color: #FFFF33;}
.cython.score-41 {background-color: #FFFF32;}
.cython.score-42 {background-color: #FFFF31;}
.cython.score-43 {background-color: #FFFF30;}
.cython.score-44 {background-color: #FFFF2f;}
.cython.score-45 {background-color: #FFFF2e;}
.cython.score-46 {background-color: #FFFF2d;}
.cython.score-47 {background-color: #FFFF2c;}
.cython.score-48 {background-color: #FFFF2b;}
.cython.score-49 {background-color: #FFFF2b;}
.cython.score-50 {background-color: #FFFF2a;}
.cython.score-51 {background-color: #FFFF29;}
.cython.score-52 {background-color: #FFFF29;}
.cython.score-53 {background-color: #FFFF28;}
.cython.score-54 {background-color: #FFFF27;}
.cython.score-55 {background-color: #FFFF27;}
.cython.score-56 {background-color: #FFFF26;}
.cython.score-57 {background-color: #FFFF26;}
.cython.score-58 {background-color: #FFFF25;}
.cython.score-59 {background-color: #FFFF24;}
.cython.score-60 {background-color: #FFFF24;}
.cython.score-61 {background-color: #FFFF23;}
.cython.score-62 {background-color: #FFFF23;}
.cython.score-63 {background-color: #FFFF22;}
.cython.score-64 {background-color: #FFFF22;}
.cython.score-65 {background-color: #FFFF22;}
.cython.score-66 {background-color: #FFFF21;}
.cython.score-67 {background-color: #FFFF21;}
.cython.score-68 {background-color: #FFFF20;}
.cython.score-69 {background-color: #FFFF20;}
.cython.score-70 {background-color: #FFFF1f;}
.cython.score-71 {background-color: #FFFF1f;}
.cython.score-72 {background-color: #FFFF1f;}
.cython.score-73 {background-color: #FFFF1e;}
.cython.score-74 {background-color: #FFFF1e;}
.cython.score-75 {background-color: #FFFF1e;}
.cython.score-76 {background-color: #FFFF1d;}
.cython.score-77 {background-color: #FFFF1d;}
.cython.score-78 {background-color: #FFFF1c;}
.cython.score-79 {background-color: #FFFF1c;}
.cython.score-80 {background-color: #FFFF1c;}
.cython.score-81 {background-color: #FFFF1c;}
.cython.score-82 {background-color: #FFFF1b;}
.cython.score-83 {background-color: #FFFF1b;}
.cython.score-84 {background-color: #FFFF1b;}
.cython.score-85 {background-color: #FFFF1a;}
.cython.score-86 {background-color: #FFFF1a;}
.cython.score-87 {background-color: #FFFF1a;}
.cython.score-88 {background-color: #FFFF1a;}
.cython.score-89 {background-color: #FFFF19;}
.cython.score-90 {background-color: #FFFF19;}
.cython.score-91 {background-color: #FFFF19;}
.cython.score-92 {background-color: #FFFF19;}
.cython.score-93 {background-color: #FFFF18;}
.cython.score-94 {background-color: #FFFF18;}
.cython.score-95 {background-color: #FFFF18;}
.cython.score-96 {background-color: #FFFF18;}
.cython.score-97 {background-color: #FFFF17;}
.cython.score-98 {background-color: #FFFF17;}
.cython.score-99 {background-color: #FFFF17;}
.cython.score-100 {background-color: #FFFF17;}
.cython.score-101 {background-color: #FFFF16;}
.cython.score-102 {background-color: #FFFF16;}
.cython.score-103 {background-color: #FFFF16;}
.cython.score-104 {background-color: #FFFF16;}
.cython.score-105 {background-color: #FFFF16;}
.cython.score-106 {background-color: #FFFF15;}
.cython.score-107 {background-color: #FFFF15;}
.cython.score-108 {background-color: #FFFF15;}
.cython.score-109 {background-color: #FFFF15;}
.cython.score-110 {background-color: #FFFF15;}
.cython.score-111 {background-color: #FFFF15;}
.cython.score-112 {background-color: #FFFF14;}
.cython.score-113 {background-color: #FFFF14;}
.cython.score-114 {background-color: #FFFF14;}
.cython.score-115 {background-color: #FFFF14;}
.cython.score-116 {background-color: #FFFF14;}
.cython.score-117 {background-color: #FFFF14;}
.cython.score-118 {background-color: #FFFF13;}
.cython.score-119 {background-color: #FFFF13;}
.cython.score-120 {background-color: #FFFF13;}
.cython.score-121 {background-color: #FFFF13;}
.cython.score-122 {background-color: #FFFF13;}
.cython.score-123 {background-color: #FFFF13;}
.cython.score-124 {background-color: #FFFF13;}
.cython.score-125 {background-color: #FFFF12;}
.cython.score-126 {background-color: #FFFF12;}
.cython.score-127 {background-color: #FFFF12;}
.cython.score-128 {background-color: #FFFF12;}
.cython.score-129 {background-color: #FFFF12;}
.cython.score-130 {background-color: #FFFF12;}
.cython.score-131 {background-color: #FFFF12;}
.cython.score-132 {background-color: #FFFF11;}
.cython.score-133 {background-color: #FFFF11;}
.cython.score-134 {background-color: #FFFF11;}
.cython.score-135 {background-color: #FFFF11;}
.cython.score-136 {background-color: #FFFF11;}
.cython.score-137 {background-color: #FFFF11;}
.cython.score-138 {background-color: #FFFF11;}
.cython.score-139 {background-color: #FFFF11;}
.cython.score-140 {background-color: #FFFF11;}
.cython.score-141 {background-color: #FFFF10;}
.cython.score-142 {background-color: #FFFF10;}
.cython.score-143 {background-color: #FFFF10;}
.cython.score-144 {background-color: #FFFF10;}
.cython.score-145 {background-color: #FFFF10;}
.cython.score-146 {background-color: #FFFF10;}
.cython.score-147 {background-color: #FFFF10;}
.cython.score-148 {background-color: #FFFF10;}
.cython.score-149 {background-color: #FFFF10;}
.cython.score-150 {background-color: #FFFF0f;}
.cython.score-151 {background-color: #FFFF0f;}
.cython.score-152 {background-color: #FFFF0f;}
.cython.score-153 {background-color: #FFFF0f;}
.cython.score-154 {background-color: #FFFF0f;}
.cython.score-155 {background-color: #FFFF0f;}
.cython.score-156 {background-color: #FFFF0f;}
.cython.score-157 {background-color: #FFFF0f;}
.cython.score-158 {background-color: #FFFF0f;}
.cython.score-159 {background-color: #FFFF0f;}
.cython.score-160 {background-color: #FFFF0f;}
.cython.score-161 {background-color: #FFFF0e;}
.cython.score-162 {background-color: #FFFF0e;}
.cython.score-163 {background-color: #FFFF0e;}
.cython.score-164 {background-color: #FFFF0e;}
.cython.score-165 {background-color: #FFFF0e;}
.cython.score-166 {background-color: #FFFF0e;}
.cython.score-167 {background-color: #FFFF0e;}
.cython.score-168 {background-color: #FFFF0e;}
.cython.score-169 {background-color: #FFFF0e;}
.cython.score-170 {background-color: #FFFF0e;}
.cython.score-171 {background-color: #FFFF0e;}
.cython.score-172 {background-color: #FFFF0e;}
.cython.score-173 {background-color: #FFFF0d;}
.cython.score-174 {background-color: #FFFF0d;}
.cython.score-175 {background-color: #FFFF0d;}
.cython.score-176 {background-color: #FFFF0d;}
.cython.score-177 {background-color: #FFFF0d;}
.cython.score-178 {background-color: #FFFF0d;}
.cython.score-179 {background-color: #FFFF0d;}
.cython.score-180 {background-color: #FFFF0d;}
.cython.score-181 {background-color: #FFFF0d;}
.cython.score-182 {background-color: #FFFF0d;}
.cython.score-183 {background-color: #FFFF0d;}
.cython.score-184 {background-color: #FFFF0d;}
.cython.score-185 {background-color: #FFFF0d;}
.cython.score-186 {background-color: #FFFF0d;}
.cython.score-187 {background-color: #FFFF0c;}
.cython.score-188 {background-color: #FFFF0c;}
.cython.score-189 {background-color: #FFFF0c;}
.cython.score-190 {background-color: #FFFF0c;}
.cython.score-191 {background-color: #FFFF0c;}
.cython.score-192 {background-color: #FFFF0c;}
.cython.score-193 {background-color: #FFFF0c;}
.cython.score-194 {background-color: #FFFF0c;}
.cython.score-195 {background-color: #FFFF0c;}
.cython.score-196 {background-color: #FFFF0c;}
.cython.score-197 {background-color: #FFFF0c;}
.cython.score-198 {background-color: #FFFF0c;}
.cython.score-199 {background-color: #FFFF0c;}
.cython.score-200 {background-color: #FFFF0c;}
.cython.score-201 {background-color: #FFFF0c;}
.cython.score-202 {background-color: #FFFF0c;}
.cython.score-203 {background-color: #FFFF0b;}
.cython.score-204 {background-color: #FFFF0b;}
.cython.score-205 {background-color: #FFFF0b;}
.cython.score-206 {background-color: #FFFF0b;}
.cython.score-207 {background-color: #FFFF0b;}
.cython.score-208 {background-color: #FFFF0b;}
.cython.score-209 {background-color: #FFFF0b;}
.cython.score-210 {background-color: #FFFF0b;}
.cython.score-211 {background-color: #FFFF0b;}
.cython.score-212 {background-color: #FFFF0b;}
.cython.score-213 {background-color: #FFFF0b;}
.cython.score-214 {background-color: #FFFF0b;}
.cython.score-215 {background-color: #FFFF0b;}
.cython.score-216 {background-color: #FFFF0b;}
.cython.score-217 {background-color: #FFFF0b;}
.cython.score-218 {background-color: #FFFF0b;}
.cython.score-219 {background-color: #FFFF0b;}
.cython.score-220 {background-color: #FFFF0b;}
.cython.score-221 {background-color: #FFFF0b;}
.cython.score-222 {background-color: #FFFF0a;}
.cython.score-223 {background-color: #FFFF0a;}
.cython.score-224 {background-color: #FFFF0a;}
.cython.score-225 {background-color: #FFFF0a;}
.cython.score-226 {background-color: #FFFF0a;}
.cython.score-227 {background-color: #FFFF0a;}
.cython.score-228 {background-color: #FFFF0a;}
.cython.score-229 {background-color: #FFFF0a;}
.cython.score-230 {background-color: #FFFF0a;}
.cython.score-231 {background-color: #FFFF0a;}
.cython.score-232 {background-color: #FFFF0a;}
.cython.score-233 {background-color: #FFFF0a;}
.cython.score-234 {background-color: #FFFF0a;}
.cython.score-235 {background-color: #FFFF0a;}
.cython.score-236 {background-color: #FFFF0a;}
.cython.score-237 {background-color: #FFFF0a;}
.cython.score-238 {background-color: #FFFF0a;}
.cython.score-239 {background-color: #FFFF0a;}
.cython.score-240 {background-color: #FFFF0a;}
.cython.score-241 {background-color: #FFFF0a;}
.cython.score-242 {background-color: #FFFF0a;}
.cython.score-243 {background-color: #FFFF0a;}
.cython.score-244 {background-color: #FFFF0a;}
.cython.score-245 {background-color: #FFFF0a;}
.cython.score-246 {background-color: #FFFF09;}
.cython.score-247 {background-color: #FFFF09;}
.cython.score-248 {background-color: #FFFF09;}
.cython.score-249 {background-color: #FFFF09;}
.cython.score-250 {background-color: #FFFF09;}
.cython.score-251 {background-color: #FFFF09;}
.cython.score-252 {background-color: #FFFF09;}
.cython.score-253 {background-color: #FFFF09;}
.cython.score-254 {background-color: #FFFF09;}
pre { line-height: 125%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.cython .hll { background-color: #ffffcc }
.cython { background: #f8f8f8; }
.cython .c { color: #3D7B7B; font-style: italic } /* Comment */
.cython .err { border: 1px solid #FF0000 } /* Error */
.cython .k { color: #008000; font-weight: bold } /* Keyword */
.cython .o { color: #666666 } /* Operator */
.cython .ch { color: #3D7B7B; font-style: italic } /* Comment.Hashbang */
.cython .cm { color: #3D7B7B; font-style: italic } /* Comment.Multiline */
.cython .cp { color: #9C6500 } /* Comment.Preproc */
.cython .cpf { color: #3D7B7B; font-style: italic } /* Comment.PreprocFile */
.cython .c1 { color: #3D7B7B; font-style: italic } /* Comment.Single */
.cython .cs { color: #3D7B7B; font-style: italic } /* Comment.Special */
.cython .gd { color: #A00000 } /* Generic.Deleted */
.cython .ge { font-style: italic } /* Generic.Emph */
.cython .gr { color: #E40000 } /* Generic.Error */
.cython .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.cython .gi { color: #008400 } /* Generic.Inserted */
.cython .go { color: #717171 } /* Generic.Output */
.cython .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.cython .gs { font-weight: bold } /* Generic.Strong */
.cython .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.cython .gt { color: #0044DD } /* Generic.Traceback */
.cython .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.cython .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.cython .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.cython .kp { color: #008000 } /* Keyword.Pseudo */
.cython .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.cython .kt { color: #B00040 } /* Keyword.Type */
.cython .m { color: #666666 } /* Literal.Number */
.cython .s { color: #BA2121 } /* Literal.String */
.cython .na { color: #687822 } /* Name.Attribute */
.cython .nb { color: #008000 } /* Name.Builtin */
.cython .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.cython .no { color: #880000 } /* Name.Constant */
.cython .nd { color: #AA22FF } /* Name.Decorator */
.cython .ni { color: #717171; font-weight: bold } /* Name.Entity */
.cython .ne { color: #CB3F38; font-weight: bold } /* Name.Exception */
.cython .nf { color: #0000FF } /* Name.Function */
.cython .nl { color: #767600 } /* Name.Label */
.cython .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.cython .nt { color: #008000; font-weight: bold } /* Name.Tag */
.cython .nv { color: #19177C } /* Name.Variable */
.cython .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.cython .w { color: #bbbbbb } /* Text.Whitespace */
.cython .mb { color: #666666 } /* Literal.Number.Bin */
.cython .mf { color: #666666 } /* Literal.Number.Float */
.cython .mh { color: #666666 } /* Literal.Number.Hex */
.cython .mi { color: #666666 } /* Literal.Number.Integer */
.cython .mo { color: #666666 } /* Literal.Number.Oct */
.cython .sa { color: #BA2121 } /* Literal.String.Affix */
.cython .sb { color: #BA2121 } /* Literal.String.Backtick */
.cython .sc { color: #BA2121 } /* Literal.String.Char */
.cython .dl { color: #BA2121 } /* Literal.String.Delimiter */
.cython .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.cython .s2 { color: #BA2121 } /* Literal.String.Double */
.cython .se { color: #AA5D1F; font-weight: bold } /* Literal.String.Escape */
.cython .sh { color: #BA2121 } /* Literal.String.Heredoc */
.cython .si { color: #A45A77; font-weight: bold } /* Literal.String.Interpol */
.cython .sx { color: #008000 } /* Literal.String.Other */
.cython .sr { color: #A45A77 } /* Literal.String.Regex */
.cython .s1 { color: #BA2121 } /* Literal.String.Single */
.cython .ss { color: #19177C } /* Literal.String.Symbol */
.cython .bp { color: #008000 } /* Name.Builtin.Pseudo */
.cython .fm { color: #0000FF } /* Name.Function.Magic */
.cython .vc { color: #19177C } /* Name.Variable.Class */
.cython .vg { color: #19177C } /* Name.Variable.Global */
.cython .vi { color: #19177C } /* Name.Variable.Instance */
.cython .vm { color: #19177C } /* Name.Variable.Magic */
.cython .il { color: #666666 } /* Literal.Number.Integer.Long */
    </style>
</head>
<body class="cython">
<p><span style="border-bottom: solid 1px grey;">Generated by Cython 0.29.24</span></p>
<p>
    <span style="background-color: #FFFF00">Yellow lines</span> hint at Python interaction.<br />
    Click on a line that starts with a "<code>+</code>" to see the C code that Cython generated for it.
</p>
<div class="cython"><pre class="cython line score-39" onclick="(function(s){s.display=s.display==='block'?'none':'block'})(this.nextElementSibling.style)">+<span class="">01</span>: <span class="k">def</span> <span class="nf">mandel_cython</span><span class="p">(</span><span class="n">constant</span><span class="p">,</span> <span class="n">max_iterations</span><span class="o">=</span><span class="mf">50</span><span class="p">):</span></pre>
<pre class='cython code score-39 '>/* Python wrapper */
static PyObject *__pyx_pw_46_cython_magic_ef6ffd3d158c0ef85d8a6a569a8a1a20_1mandel_cython(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static char __pyx_doc_46_cython_magic_ef6ffd3d158c0ef85d8a6a569a8a1a20_mandel_cython[] = "Computes the values of the series for up to a maximum number of iterations. \n    \n    The function stops when the absolute value of the series surpasses 2 or when it reaches the maximum \n    number of iterations.\n    \n    Returns the number of iterations.\n    ";
static PyMethodDef __pyx_mdef_46_cython_magic_ef6ffd3d158c0ef85d8a6a569a8a1a20_1mandel_cython = {"mandel_cython", (PyCFunction)(void*)(PyCFunctionWithKeywords)__pyx_pw_46_cython_magic_ef6ffd3d158c0ef85d8a6a569a8a1a20_1mandel_cython, METH_VARARGS|METH_KEYWORDS, __pyx_doc_46_cython_magic_ef6ffd3d158c0ef85d8a6a569a8a1a20_mandel_cython};
static PyObject *__pyx_pw_46_cython_magic_ef6ffd3d158c0ef85d8a6a569a8a1a20_1mandel_cython(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_v_constant = 0;
  PyObject *__pyx_v_max_iterations = 0;
  PyObject *__pyx_r = 0;
  <span class='refnanny'>__Pyx_RefNannyDeclarations</span>
  <span class='refnanny'>__Pyx_RefNannySetupContext</span>("mandel_cython (wrapper)", 0);
  {
    static PyObject **__pyx_pyargnames[] = {&amp;__pyx_n_s_constant,&amp;__pyx_n_s_max_iterations,0};
    PyObject* values[2] = {0,0};
    values[1] = ((PyObject *)__pyx_int_50);
    if (unlikely(__pyx_kwds)) {
      Py_ssize_t kw_args;
      const Py_ssize_t pos_args = <span class='py_macro_api'>PyTuple_GET_SIZE</span>(__pyx_args);
      switch (pos_args) {
        case  2: values[1] = <span class='py_macro_api'>PyTuple_GET_ITEM</span>(__pyx_args, 1);
        CYTHON_FALLTHROUGH;
        case  1: values[0] = <span class='py_macro_api'>PyTuple_GET_ITEM</span>(__pyx_args, 0);
        CYTHON_FALLTHROUGH;
        case  0: break;
        default: goto __pyx_L5_argtuple_error;
      }
      kw_args = <span class='py_c_api'>PyDict_Size</span>(__pyx_kwds);
      switch (pos_args) {
        case  0:
        if (likely((values[0] = <span class='pyx_c_api'>__Pyx_PyDict_GetItemStr</span>(__pyx_kwds, __pyx_n_s_constant)) != 0)) kw_args--;
        else goto __pyx_L5_argtuple_error;
        CYTHON_FALLTHROUGH;
        case  1:
        if (kw_args &gt; 0) {
          PyObject* value = <span class='pyx_c_api'>__Pyx_PyDict_GetItemStr</span>(__pyx_kwds, __pyx_n_s_max_iterations);
          if (value) { values[1] = value; kw_args--; }
        }
      }
      if (unlikely(kw_args &gt; 0)) {
        if (unlikely(<span class='pyx_c_api'>__Pyx_ParseOptionalKeywords</span>(__pyx_kwds, __pyx_pyargnames, 0, values, pos_args, "mandel_cython") &lt; 0)) <span class='error_goto'>__PYX_ERR(0, 1, __pyx_L3_error)</span>
      }
    } else {
      switch (<span class='py_macro_api'>PyTuple_GET_SIZE</span>(__pyx_args)) {
        case  2: values[1] = <span class='py_macro_api'>PyTuple_GET_ITEM</span>(__pyx_args, 1);
        CYTHON_FALLTHROUGH;
        case  1: values[0] = <span class='py_macro_api'>PyTuple_GET_ITEM</span>(__pyx_args, 0);
        break;
        default: goto __pyx_L5_argtuple_error;
      }
    }
    __pyx_v_constant = values[0];
    __pyx_v_max_iterations = values[1];
  }
  goto __pyx_L4_argument_unpacking_done;
  __pyx_L5_argtuple_error:;
  <span class='pyx_c_api'>__Pyx_RaiseArgtupleInvalid</span>("mandel_cython", 0, 1, 2, <span class='py_macro_api'>PyTuple_GET_SIZE</span>(__pyx_args)); <span class='error_goto'>__PYX_ERR(0, 1, __pyx_L3_error)</span>
  __pyx_L3_error:;
  <span class='pyx_c_api'>__Pyx_AddTraceback</span>("_cython_magic_ef6ffd3d158c0ef85d8a6a569a8a1a20.mandel_cython", __pyx_clineno, __pyx_lineno, __pyx_filename);
  <span class='refnanny'>__Pyx_RefNannyFinishContext</span>();
  return NULL;
  __pyx_L4_argument_unpacking_done:;
  __pyx_r = __pyx_pf_46_cython_magic_ef6ffd3d158c0ef85d8a6a569a8a1a20_mandel_cython(__pyx_self, __pyx_v_constant, __pyx_v_max_iterations);
  int __pyx_lineno = 0;
  const char *__pyx_filename = NULL;
  int __pyx_clineno = 0;

  /* function exit code */
  <span class='refnanny'>__Pyx_RefNannyFinishContext</span>();
  return __pyx_r;
}

static PyObject *__pyx_pf_46_cython_magic_ef6ffd3d158c0ef85d8a6a569a8a1a20_mandel_cython(CYTHON_UNUSED PyObject *__pyx_self, PyObject *__pyx_v_constant, PyObject *__pyx_v_max_iterations) {
  PyObject *__pyx_v_value = NULL;
  PyObject *__pyx_v_counter = NULL;
  PyObject *__pyx_r = NULL;
  <span class='refnanny'>__Pyx_RefNannyDeclarations</span>
  <span class='refnanny'>__Pyx_RefNannySetupContext</span>("mandel_cython", 0);
/* … */
  /* function exit code */
  __pyx_L1_error:;
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_t_1);
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_t_3);
  <span class='pyx_c_api'>__Pyx_AddTraceback</span>("_cython_magic_ef6ffd3d158c0ef85d8a6a569a8a1a20.mandel_cython", __pyx_clineno, __pyx_lineno, __pyx_filename);
  __pyx_r = NULL;
  __pyx_L0:;
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_v_value);
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_v_counter);
  <span class='refnanny'>__Pyx_XGIVEREF</span>(__pyx_r);
  <span class='refnanny'>__Pyx_RefNannyFinishContext</span>();
  return __pyx_r;
}
/* … */
  __pyx_tuple_ = <span class='py_c_api'>PyTuple_Pack</span>(4, __pyx_n_s_constant, __pyx_n_s_max_iterations, __pyx_n_s_value, __pyx_n_s_counter);<span class='error_goto'> if (unlikely(!__pyx_tuple_)) __PYX_ERR(0, 1, __pyx_L1_error)</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_tuple_);
  <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_tuple_);
/* … */
  __pyx_t_1 = PyCFunction_NewEx(&amp;__pyx_mdef_46_cython_magic_ef6ffd3d158c0ef85d8a6a569a8a1a20_1mandel_cython, NULL, __pyx_n_s_cython_magic_ef6ffd3d158c0ef85d);<span class='error_goto'> if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 1, __pyx_L1_error)</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
  if (<span class='py_c_api'>PyDict_SetItem</span>(__pyx_d, __pyx_n_s_mandel_cython, __pyx_t_1) &lt; 0) <span class='error_goto'>__PYX_ERR(0, 1, __pyx_L1_error)</span>
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
</pre><pre class="cython line score-0">&#xA0;<span class="">02</span>:     <span class="sd">&quot;&quot;&quot;Computes the values of the series for up to a maximum number of iterations. </span></pre>
<pre class="cython line score-0">&#xA0;<span class="">03</span>: <span class="sd">    </span></pre>
<pre class="cython line score-0">&#xA0;<span class="">04</span>: <span class="sd">    The function stops when the absolute value of the series surpasses 2 or when it reaches the maximum </span></pre>
<pre class="cython line score-0">&#xA0;<span class="">05</span>: <span class="sd">    number of iterations.</span></pre>
<pre class="cython line score-0">&#xA0;<span class="">06</span>: <span class="sd">    </span></pre>
<pre class="cython line score-0">&#xA0;<span class="">07</span>: <span class="sd">    Returns the number of iterations.</span></pre>
<pre class="cython line score-0">&#xA0;<span class="">08</span>: <span class="sd">    &quot;&quot;&quot;</span></pre>
<pre class="cython line score-0">&#xA0;<span class="">09</span>: </pre>
<pre class="cython line score-1" onclick="(function(s){s.display=s.display==='block'?'none':'block'})(this.nextElementSibling.style)">+<span class="">10</span>:     <span class="n">value</span> <span class="o">=</span> <span class="mf">0</span></pre>
<pre class='cython code score-1 '>  <span class='pyx_macro_api'>__Pyx_INCREF</span>(__pyx_int_0);
  __pyx_v_value = __pyx_int_0;
</pre><pre class="cython line score-0">&#xA0;<span class="">11</span>: </pre>
<pre class="cython line score-1" onclick="(function(s){s.display=s.display==='block'?'none':'block'})(this.nextElementSibling.style)">+<span class="">12</span>:     <span class="n">counter</span> <span class="o">=</span> <span class="mf">0</span></pre>
<pre class='cython code score-1 '>  <span class='pyx_macro_api'>__Pyx_INCREF</span>(__pyx_int_0);
  __pyx_v_counter = __pyx_int_0;
</pre><pre class="cython line score-8" onclick="(function(s){s.display=s.display==='block'?'none':'block'})(this.nextElementSibling.style)">+<span class="">13</span>:     <span class="k">while</span> <span class="n">counter</span> <span class="o">&lt;</span> <span class="n">max_iterations</span><span class="p">:</span></pre>
<pre class='cython code score-8 '>  while (1) {
    __pyx_t_1 = <span class='py_c_api'>PyObject_RichCompare</span>(__pyx_v_counter, __pyx_v_max_iterations, Py_LT); <span class='refnanny'>__Pyx_XGOTREF</span>(__pyx_t_1);<span class='error_goto'> if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 13, __pyx_L1_error)</span>
    __pyx_t_2 = <span class='pyx_c_api'>__Pyx_PyObject_IsTrue</span>(__pyx_t_1); if (unlikely(__pyx_t_2 &lt; 0)) <span class='error_goto'>__PYX_ERR(0, 13, __pyx_L1_error)</span>
    <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
    if (!__pyx_t_2) break;
</pre><pre class="cython line score-11" onclick="(function(s){s.display=s.display==='block'?'none':'block'})(this.nextElementSibling.style)">+<span class="">14</span>:         <span class="k">if</span> <span class="nb">abs</span><span class="p">(</span><span class="n">value</span><span class="p">)</span> <span class="o">&gt;</span> <span class="mf">2</span><span class="p">:</span></pre>
<pre class='cython code score-11 '>    __pyx_t_1 = <span class='pyx_c_api'>__Pyx_PyNumber_Absolute</span>(__pyx_v_value);<span class='error_goto'> if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 14, __pyx_L1_error)</span>
    <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
    __pyx_t_3 = <span class='py_c_api'>PyObject_RichCompare</span>(__pyx_t_1, __pyx_int_2, Py_GT); <span class='refnanny'>__Pyx_XGOTREF</span>(__pyx_t_3);<span class='error_goto'> if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 14, __pyx_L1_error)</span>
    <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
    __pyx_t_2 = <span class='pyx_c_api'>__Pyx_PyObject_IsTrue</span>(__pyx_t_3); if (unlikely(__pyx_t_2 &lt; 0)) <span class='error_goto'>__PYX_ERR(0, 14, __pyx_L1_error)</span>
    <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_3); __pyx_t_3 = 0;
    if (__pyx_t_2) {
/* … */
    }
</pre><pre class="cython line score-0" onclick="(function(s){s.display=s.display==='block'?'none':'block'})(this.nextElementSibling.style)">+<span class="">15</span>:             <span class="k">break</span></pre>
<pre class='cython code score-0 '>      goto __pyx_L4_break;
</pre><pre class="cython line score-0">&#xA0;<span class="">16</span>: </pre>
<pre class="cython line score-12" onclick="(function(s){s.display=s.display==='block'?'none':'block'})(this.nextElementSibling.style)">+<span class="">17</span>:         <span class="n">value</span> <span class="o">=</span> <span class="p">(</span><span class="n">value</span> <span class="o">*</span> <span class="n">value</span><span class="p">)</span> <span class="o">+</span> <span class="n">constant</span></pre>
<pre class='cython code score-12 '>    __pyx_t_3 = <span class='py_c_api'>PyNumber_Multiply</span>(__pyx_v_value, __pyx_v_value);<span class='error_goto'> if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 17, __pyx_L1_error)</span>
    <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_3);
    __pyx_t_1 = <span class='py_c_api'>PyNumber_Add</span>(__pyx_t_3, __pyx_v_constant);<span class='error_goto'> if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 17, __pyx_L1_error)</span>
    <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
    <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_3); __pyx_t_3 = 0;
    <span class='pyx_macro_api'>__Pyx_DECREF_SET</span>(__pyx_v_value, __pyx_t_1);
    __pyx_t_1 = 0;
</pre><pre class="cython line score-0">&#xA0;<span class="">18</span>: </pre>
<pre class="cython line score-3" onclick="(function(s){s.display=s.display==='block'?'none':'block'})(this.nextElementSibling.style)">+<span class="">19</span>:         <span class="n">counter</span> <span class="o">=</span> <span class="n">counter</span> <span class="o">+</span> <span class="mf">1</span></pre>
<pre class='cython code score-3 '>    __pyx_t_1 = <span class='pyx_c_api'>__Pyx_PyInt_AddObjC</span>(__pyx_v_counter, __pyx_int_1, 1, 0, 0);<span class='error_goto'> if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 19, __pyx_L1_error)</span>
    <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
    <span class='pyx_macro_api'>__Pyx_DECREF_SET</span>(__pyx_v_counter, __pyx_t_1);
    __pyx_t_1 = 0;
  }
  __pyx_L4_break:;
</pre><pre class="cython line score-0">&#xA0;<span class="">20</span>: </pre>
<pre class="cython line score-2" onclick="(function(s){s.display=s.display==='block'?'none':'block'})(this.nextElementSibling.style)">+<span class="">21</span>:     <span class="k">return</span> <span class="n">counter</span></pre>
<pre class='cython code score-2 '>  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_r);
  <span class='pyx_macro_api'>__Pyx_INCREF</span>(__pyx_v_counter);
  __pyx_r = __pyx_v_counter;
  goto __pyx_L0;
</pre></div></body></html>



### Typing Variables


```cython
%%cython

def mandel_cython_var_typed(constant, max_iterations=50):
    """Computes the values of the series for up to a maximum number of iterations.

    The function stops when the absolute value of the series surpasses 2 or when it reaches the maximum
    number of iterations.

    Returns the number of iterations.
    """
    cdef double complex value # typed variable
    value = 0

    counter = 0
    while counter < max_iterations:
        if abs(value) > 2:
            break

        value = (value * value) + constant

        counter = counter + 1

    return counter


assert mandel_cython_var_typed(0) == 50
assert mandel_cython_var_typed(3) == 1
assert mandel_cython_var_typed(0.5) == 5
```


```python
%%timeit
[[mandel_cython_var_typed(x + 1j * y) for x in xs] for y in ys]
```

    133 ms ± 1.81 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


### Typing Function Parameters and Return Values


```cython
%%cython

cpdef int mandel_cython_func_typed(double complex constant, int max_iterations=50):
    """Computes the values of the series for up to a maximum number of iterations.

    The function stops when the absolute value of the series surpasses 2 or when it reaches the maximum
    number of iterations.

    Returns the number of iterations.
    """
    cdef double complex value # typed variable
    value = 0

    cdef int counter = 0
    while counter < max_iterations:
        if abs(value) > 2:
            break

        value = (value * value) + constant

        counter = counter + 1

    return counter


assert mandel_cython_func_typed(0) == 50
assert mandel_cython_func_typed(3) == 1
assert mandel_cython_func_typed(0.5) == 5
```


```python
%%timeit
[[mandel_cython_func_typed(x + 1j * y) for x in xs] for y in ys]
```

    24.3 ms ± 81.9 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)


### Cython with numpy ndarray

You can use NumPy from Cython exactly the same as in regular Python, but by doing so you are losing potentially high speedups because Cython has support for fast access to NumPy arrays.


```python
import numpy as np

cs_listcomp = [[(x + 1j * y) for x in xs] for y in ys]
cs = np.asarray(cs_listcomp)
```


```cython
%%cython

import numpy as np
cimport numpy as np

cpdef int mandel_cython_numpy(np.ndarray[double complex, ndim=2] constants, int max_iterations=50):
    cdef np.ndarray[long,ndim=2] diverged_at_count
    cdef np.ndarray[double complex, ndim=2] value
    cdef int counter

    diverged_at_count = np.ones((constants.shape[0], constants.shape[1]), dtype=int)*max_iterations
    value = np.zeros((constants.shape[0], constants.shape[1]), dtype=complex)
    counter = 0
    while counter < max_iterations:
        value = value*value + constants
        diverging = abs(value) > 2

        # Any positions which are:
        # - diverging
        # - haven't diverged before
        # are diverging for the first time
        first_diverged_this_time = np.logical_and(
            diverging,
            diverged_at_count == max_iterations
        )

        # Update diverged_at_count for all positions which first diverged at this step
        diverged_at_count[first_diverged_this_time] = counter
        # Reset any divergent values to exactly 2
        value[diverging] = 2
        counter = counter + 1

    return diverged_at_count

assert mandel_cython_numpy(np.asarray([[0 + 1j*0]])) == np.asarray([[50]])
assert mandel_cython_numpy(np.asarray([[4 + 1j*0]])) == np.asarray([[0]])
```

Note the double import of numpy:

- the standard numpy module
- the Cython-enabled version of numpy that ensures fast indexing of and other operations on arrays.

**Both import statements are necessary** in code that uses numpy arrays. The new thing in the code above is declaration of arrays by np.ndarray.


```python
%%timeit
mandel_cython_numpy(cs)
```

    51.3 ms ± 4.96 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
