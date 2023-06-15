# 6.3 Python outside the notebook

*Estimated time for this notebook: 15 minutes*

We will often want to save our Python functions and classes, for use in multiple Notebooks or to interact with them via a terminal.

## Writing Python in Text Files

If you create your own Python files ending in `.py`, then you can import them with `import` just like external libraries.

It's best to use an editor like [VS Code](https://code.visualstudio.com/) or [PyCharm](https://www.jetbrains.com/pycharm/) to do this. Here we use the `%%writefile` Jupyter "magic" to create files from the notebook.

Let's create a file `greeter.py` with a function `greet` that prints a welcome message in multiple colours (using the [`colorama`](https://pypi.org/project/colorama/) package):


```python
%%writefile greeter.py
import colorama  # used for creating coloured text


def greet(personal, family, title="", polite=False):
    greeting = "How do you do, " if polite else "Hey, "
    greeting = colorama.Back.BLACK + colorama.Fore.YELLOW + greeting
    if title:
        greeting += colorama.Back.BLUE + colorama.Fore.WHITE + title + " "

    greeting += (
        colorama.Back.WHITE
        + colorama.Style.BRIGHT
        + colorama.Fore.RED
        + personal
        + " "
        + family
    )
    return greeting
```

    Overwriting greeter.py


## Loading Our Function

We just wrote the file, there is no `greet` function in this notebook yet:


```python
greet("James", "Hetherington")
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    Input In [2], in <cell line: 1>()
    ----> 1 greet("James", "Hetherington")


    NameError: name 'greet' is not defined


But we can import the functionality from `greeter.py` file that we created:


```python
import greeter  # note that you don't include the .py extension

print(greeter.greet("James", "Hetherington"))
```

    [40m[33mHey, [47m[1m[31mJames Hetherington


Or import the function from the file directly:


```python
from greeter import greet

print(greet("James", "Hetherington"))
```

    [40m[33mHey, [47m[1m[31mJames Hetherington


Note the file we created is in the same directory as this notebook:


```python
# glob is a library for finding files that match given patterns
from glob import glob

# all files with a .py or .ipynb extension in the current directory
glob("*.py") + glob("*.ipynb")
```




    ['command.py',
     'greeter.py',
     '06_04_packaging.ipynb',
     '06_06_software_development.ipynb',
     '06_09_exercise.ipynb',
     '06_08_software_issues.ipynb',
     '06_01_pypi_packages.ipynb',
     '06_07_software_licensing.ipynb',
     '06_02_managing_dependencies.ipynb',
     '06_03_non_notebook_python.ipynb',
     '06_05_documentation.ipynb',
     '06_00_libraries.ipynb']



Currently we're relying on all the module source code being in our current working directory. We'll want to `import` our modules from notebooks elsewhere on our computer: it would be a bad idea to keep all our Python work in one folder.

The best way to do this is to learn how to make our code into a proper module that we can install. We'll see more on that in the next notebook.

## Command-line Interfaces

[argparse](https://docs.python.org/3/library/argparse.html) is the standard Python library for building programs with a command-line interface (another popular library is [click](https://click.palletsprojects.com/en/8.1.x/)).

Here's an example that creates a command-line interface to our `greet` function (in a file named `command.py`):


```python
%%writefile command.py
from argparse import ArgumentParser

from greeter import greet


def process():
    parser = ArgumentParser(description="Generate appropriate greetings")

    # required (positional) arguments
    parser.add_argument("personal")
    parser.add_argument("family")

    # optional (keyword) arguments
    parser.add_argument("--title", "-t")
    parser.add_argument("--polite", "-p", action="store_true")
    #   polite will be false unless "--polite" or "-p" given at command-line

    args = parser.parse_args()

    print(greet(args.personal, args.family, args.title, args.polite))


if __name__ == "__main__":
    process()

```

    Overwriting command.py


We can now run our saved interface with `python command.py` + the arguments we want to specify.

`argparse` generates some documentation to help us understand how to use it:


```bash
%%bash
python command.py --help
```

    usage: command.py [-h] [--title TITLE] [--polite] personal family

    Generate appropriate greetings

    positional arguments:
      personal
      family

    optional arguments:
      -h, --help            show this help message and exit
      --title TITLE, -t TITLE
      --polite, -p


A few examples:


```bash
%%bash
python command.py James Hetherington
```

    [40m[33mHey, [47m[1m[31mJames Hetherington



```bash
%%bash
python command.py --polite James Hetherington
```

    [40m[33mHow do you do, [47m[1m[31mJames Hetherington



```bash
%%bash
python command.py James Hetherington --title Dr
```

    [40m[33mHey, [44m[37mDr [47m[1m[31mJames Hetherington


Having to type `python command.py ...` is not very intuitive, and we're still relying on our files being in the same directory. In the next notebook we'll see a better way to include command-line interfaces as part of a package.

## `if __name__ == "__main__"`

In the `command.py` script above you may have noticed the strange `if __name__ == "__main__"` line. This is generally used when you have a file that can be used both as a script and as a module in a package.

Let's create a simplified version of `greeter.py` that prints the name of the special `__name__` variable when it is called:


```python
%%writefile greeter.py
print("executing greeter.py, __name__ is", __name__)


def greet(personal, family):
    return "Hey, " + personal + " " + family


if __name__ == "__main__":
    print(greet("Laura", "Greeter"))

```

    Overwriting greeter.py


If we invoke `greeter.py` directly, Python sets the value of `__name__` to `"__main__"` and the code in the if block runs:


```bash
%%bash
python greeter.py
```

    executing greeter.py, __name__ is __main__
    Hey, Laura Greeter


Now let's create a simplified `command.py` that also prints `__name__`, and imports the `greet` function from `greeter.py` as before:


```python
%%writefile command.py
print("executing command.py, __name__ is", __name__)

from argparse import ArgumentParser
from greeter import greet


def process():
    parser = ArgumentParser(description="Generate appropriate greetings")
    parser.add_argument("personal")
    parser.add_argument("family")
    args = parser.parse_args()
    print(greet(args.personal, args.family))


if __name__ == "__main__":
    process()

```

    Overwriting command.py


And run the command script:


```bash
%%bash
python command.py Sarah Command
```

    executing command.py, __name__ is __main__
    executing greeter.py, __name__ is greeter
    Hey, Sarah Command


Note that when we import `greeter.greet` the contents of the whole `greeter.py` file are executed, so the code to print the value of `__name__` still runs. However, `__name__` is now given the value `greeter`. This means when the if statement is executed `__name__ == "__main__"` returns `False`, and we don't see the "Hey, Laura Greeter" output.

Without that if statement we would get

```bash
Hey, Laura Greeter
Hey, Sarah Command
```

which is unlikely to be what we wanted when running `python command.py Sarah Command`.


```python

```
