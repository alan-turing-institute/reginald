# 7.3 Linting

*Estimated time for this notebook: 15 minutes*


There are automated tools which enforce coding conventions and check for common mistakes. These are called *linters*.


Do not blindly believe all these automated tools! Style guides are **guides** not **rules**.

## Linters Starter Pack

A good starting point for any Python project is to use `flake8`, `black`, and `isort`. All three should improve the style and consistency of your code whilst requiring minimal setup, and generally they are not opinionated about the way your code is designed, only the way it is formatted and syntax or convention errors.

### [flake8](https://flake8.pycqa.org/en/latest/index.html)

Combines two main tools:
- [PyFlakes](https://github.com/PyCQA/pyflakes) - checks Python code for syntax errors
- [pycodestyle](https://pycodestyle.pycqa.org/en/latest/) - checks whether Python code is compliant with PEP8 conventions

`flake8` only checks code and flags any syntax/style errors, it does not attempt to fix them.

For example, consider this piece of code:


```python
%%writefile flake8_example.py

from constants import e

def circumference(r):
    return 2 * pi * r
```

    Writing flake8_example.py


Running `flake8` on it gives the following warnings:


```python
! flake8 flake8_example.py
```

    [1mflake8_example.py[m[36m:[m2[36m:[m1[36m:[m [1m[31mF401[m 'constants.e' imported but unused
    [1mflake8_example.py[m[36m:[m4[36m:[m1[36m:[m [1m[31mE302[m expected 2 blank lines, found 1
    [1mflake8_example.py[m[36m:[m5[36m:[m16[36m:[m [1m[31mF821[m undefined name 'pi'


The first warning tells us we have imported a variable called `e` but not used it, and the last that we're trying to use a variable called `pi` but haven't defined it anywhere. The 2nd warning indicates that in the [PEP8](https://peps.python.org/pep-0008/#blank-lines) conventions there should be two blank lines before a function definition, but we only have 1.

```{admonition} Running on multiple files
All the examples here run a linter on a single file, but they can be run on all the files in a project at once as well (e.g. by just running `flake8` without a filename).
```

### [black](https://black.readthedocs.io/)

A highly opinionated code formatter, which enforces control of minutiae details of your code.
The name comes from a Henry Ford quote: "Any customer can have a car painted any color that he wants, so long as it is black."

For example, consider this piece of code:


```python
%%writefile black_example.py

import numpy as np

def my_complex_function(important_argument_1,important_argument_2,optional_argument_3 = 3,optional_argument_4 = 4):
    return np.random.random()*important_argument_1*important_argument_2*optional_argument_3*optional_argument_4

def hello(name,greet='Hello',end="!"):
    print(greet,    name,    end)
```

    Writing black_example.py



```python
! black black_example.py
```

    [1mreformatted black_example.py[0m
    
    [1mAll done! ✨ 🍰 ✨[0m
    [34m[1m1 file [0m[1mreformatted[0m.


After running `black` on the file its contents become:


```python
!cat black_example.py
```

    import numpy as np
    
    
    def my_complex_function(
        important_argument_1,
        important_argument_2,
        optional_argument_3=3,
        optional_argument_4=4,
    ):
        return (
            np.random.random()
            * important_argument_1
            * important_argument_2
            * optional_argument_3
            * optional_argument_4
        )
    
    
    def hello(name, greet="Hello", end="!"):
        print(greet, name, end)


Changes made by `black`:
- Ensured there are two blank lines before and after function definitions
- Wrapped long lines intelligently
- Removed excess whitespace (e.g. between the arguments in the print statement on the last line)
- Used double quotes `"` for all strings (rather than a mix of `'` and `"`)

Note that `black` will automatically fix most of the whitespace-related warnings picked up by `flake8` (but it would not fix the import or undefined name errors in the `flake8` example above).

```{admonition} Line length
`black` is not compliant with PEP8 in one way - by default it uses a maximum line length of 88 characters (PEP8 suggests 79 characters). [This is discussed in the black documentation](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html#line-length).
```

### [isort](https://pycqa.github.io/isort/)

"Sorts" imports alphabetically in groups in the following order:

1. standard library imports (_e.g._ `import os`).
1. third-party imports (_e.g._ `import pandas`).
1. local application/library specific imports (_e.g._ `from .my_python_file import MyClass`).

with a blank line between each group.

For example, consider the following code:


```python
%%writefile isort_example.py

import pandas as pd
import os
from matplotlib import pyplot as plt
import black_example
import numpy as np
import json
```

    Writing isort_example.py



```python
! isort isort_example.py
```

    Fixing /home/runner/work/rse-course/rse-course/module07_construction_and_design/isort_example.py
    [0m

If we run isort it becomes:


```python
!cat isort_example.py
```

    
    import json
    import os
    
    import numpy as np
    import pandas as pd
    from matplotlib import pyplot as plt
    
    import black_example


Note that `from` imports are placed at the bottom of each group.

## Other Linters

### [mypy](https://mypy.readthedocs.io/en/stable/)

If you use type annotations in your code, `mypy` can check it for errors that may result from variables being assigned the wrong type.
For example, consider the following code:


```python
%%writefile mypy_example.py

def hello(name: str, greet: str = "Hello", rep: int = 1) -> str:
    message: str = ""
    for _ in range(rep):
        message += f"{greet} {name}\n"
    return message


print(hello("Bob", 5))
```

    Writing mypy_example.py


If we run `mypy` on it:


```python
! mypy mypy_example.py
```

    mypy_example.py:9: [1m[31merror:[m Argument 2 to [m[1m"hello"[m has incompatible type [m[1m"int"[m; expected [m[1m"str"[m[m
    [1m[31mFound 1 error in 1 file (checked 1 source file)[m


The error tells us we have passed an `int` as the 2nd argument to `hello`, but in the function definition the second argument (`greet`) is defined to be a `str`. We probably meant to write `hello("Bob", rep=5)`.

### [pylint](https://www.pylint.org/)

`pylint` analyses your code for errors, coding standards, and makes suggestions around where code could be refactored. It checks for a much wider range of code quality issues than `flake8` but is also much more likely to pick up _false positives_, i.e. `pylint` is more likely to give you warnings about things you don't want to change.

Let's run it on the same code we used for our `flake8` example earlier:


```python
%%writefile pylint_example.py

from constants import e

def circumference(r):
    return 2 * pi * r
```

    Writing pylint_example.py



```python
! pylint pylint_example.py
```

    ************* Module pylint_example
    pylint_example.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    pylint_example.py:2:0: E0401: Unable to import 'constants' (import-error)
    pylint_example.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
    pylint_example.py:4:18: C0103: Argument name "r" doesn't conform to snake_case naming style (invalid-name)
    pylint_example.py:5:15: E0602: Undefined variable 'pi' (undefined-variable)
    pylint_example.py:2:0: W0611: Unused e imported from constants (unused-import)
    
    ------------------------------------------------------------------
    Your code has been rated at 0.00/10 (previous run: 0.00/10, +0.00)
    
    [0m

Compared to `flake8`, in this case `pylint` also warns us that:
- The `circumference` function doesn't have a docstring
- The `constants` library we try to import is not available on our system
- The variable name `r` doesn't follow conventions (single letter variables are discouraged by convention, we could use `radius` instead)

### [nbqa](https://nbqa.readthedocs.io/en/latest/index.html)

`nbqa` allows you to run many Python quality tools (including all the ones we've introduced here) on jupyter notebooks. For example:


```python
! nbqa flake8 07_02_coding_conventions.ipynb
```

    07_02_coding_conventions.ipynb:cell_5:1:1: F811 redefinition of unused 'ClassName' from line 10


### [pylama](https://klen.github.io/pylama/)

`pylama` wraps many code quality tools (including `isort`, `mypy`, `pylint` and much of `flake8`) in a single command.


```python
! pylama --linters isort,mccabe,mypy,pycodestyle,pydocstyle,pyflakes,pylint flake8_example.py
```

    ERROR: /home/runner/work/rse-course/rse-course/module07_construction_and_design/flake8_example.py Imports are incorrectly sorted and/or formatted.
    flake8_example.py:0:1  Incorrectly sorted imports. [isort]
    flake8_example.py:1:1 C0114 Missing module docstring [pylint]
    flake8_example.py:1:1 D100 Missing docstring in public module [pydocstyle]
    flake8_example.py:2:1  Cannot find implementation or library stub for module named "constants" [mypy]
    flake8_example.py:2:1  See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports [mypy]
    flake8_example.py:2:1 E0401 Unable to import 'constants' [pylint]
    flake8_example.py:2:1 W0611 Unused e imported from constants [pylint]
    flake8_example.py:4:1 C0116 Missing function or method docstring [pylint]
    flake8_example.py:4:19 C0103 Argument name "r" doesn't conform to snake_case naming style [pylint]
    flake8_example.py:4:1 D103 Missing docstring in public function [pydocstyle]
    flake8_example.py:4:1 E302 expected 2 blank lines, found 1 [pycodestyle]
    flake8_example.py:5:16 E0602 Undefined variable 'pi' [pylint]
    [0m

## Setup

### Compatibility between linters

If you're using multiple linters in your project you may need to configure them to be compatible with each other. For example, `flake8` warns about lines longer than 79 characters (the PEP8 convention) but `black` will allow lines up to 88 characters by default.

[This repository](https://github.com/alan-turing-institute/Python-quality-tools) has an example setup for using `black`, `isort`, and `flake8` together. The `.flake8` and `pyproject.toml` configuration files set `flake8` and `isort` to run in modes compatible with `black`.

### Ignoring lines of code or linting rules

There will be times where a linter warns you about something in your code but there's a valid reason it's structured that way and you don't want to change it. Most linters can be configured to ignore specific warnings, either by the type of warning, by file, or by individual code line. For example, adding a `# noqa` comment to a line will make `flake8` ignore it.

Each linter does this differently so check their documentation (e.g. [flake8](https://flake8.pycqa.org/en/3.1.1/user/ignoring-errors.html), [isort](https://pycqa.github.io/isort/docs/configuration/options.html), [mypy](https://mypy.readthedocs.io/en/stable/config_file.html), [pylint](https://pylint.pycqa.org/en/latest/user_guide/messages/message_control.html)).

### Running Linters

It's a good idea to run linters regularly, or even better to have them setup to run automatically so you don't have to remember. There are various tools to help with that:


#### IDE Integration

Many editors/IDEs have integrations with common linters or have their own built-in. This can include highlighting problems inline, or automatically running linters when files are saved, for example. Here is the [VS Code documentation for linting in Python](https://code.visualstudio.com/docs/python/linting).

There are also tools like [editorconfig](https://editorconfig.org/) to help sharing the conventions used within a project, where each contributor uses different IDEs and tools.

#### [pre-commit](https://pre-commit.com/) 

pre-commit is a manager for creating git "hooks" - scripts that run before making a commit. If a hook errors the commit won't be made, and you'll be prompted to fix the problems first. There are `pre-commit` plugins for all the linters discussed here, and it's a good way to ensure all code committed to your repo has had a level of quality control applied to it.

#### Continuous Integration

As well as automating unit tests on a CI system like GitHub Actions it's a good idea to configure them to run linters on your code too.

[Here is an example](https://github.com/alan-turing-institute/AIrsenal/blob/main/.github/workflows/main.yml) from a repo using `isort`, `flake8` and `black` in a GitHub Action. Note that in a CI setup tools that usually change your code, like `black` and `isort`, will be configured to only check whether there are changes that need to be made.
