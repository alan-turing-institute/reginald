# 1.7 Control and Flow

*Estimated time for this notebook: 15 minutes*

## 1.7.1 Turing completeness

Now that we understand how we can use objects to store and model our data, we only need to be able to control the flow of our
program in order to have a program that can, in principle, do anything!

Specifically we need to be able to:

* Control whether a program statement should be executed or not, based on a variable. "Conditionality"
* Jump back to an earlier point in the program, and run some statements again. "Branching"

Once we have these, we can write computer programs to process information in arbitrary ways: we are *Turing Complete*!

## 1.7.2 Conditionality

Conditionality is achieved through Python's `if` statement:


```python
x = 5

if x < 0:
    print(x, " is negative")
```

The absence of output here means the if clause prevented the print statement from running.


```python
x = -10

if x < 0:
    print(x, " is negative")
```

    -10  is negative


The first time through, the print statement never happened.

The **controlled** statements are indented. Once we remove the indent, the statements will once again happen regardless.

### Else and Elif

Python's if statement has optional elif (else-if) and else clauses:


```python
x = 5
if x < 0:
    print("x is negative")
else:
    print("x is positive")
```

    x is positive



```python
x = 5
if x < 0:
    print("x is negative")
elif x == 0:
    print("x is zero")
else:
    print("x is positive")
```

    x is positive


Try editing the value of x here, and note that other sections are found.


```python
choice = "high"

if choice == "high":
    print(1)
elif choice == "medium":
    print(2)
else:
    print(3)
```

    1


## 1.7.3 Comparison

`True` and `False` are used to represent **boolean** (true or false) values.


```python
1 > 2
```




    False



Comparison on strings is alphabetical.


```python
"UCL" > "KCL"
```




    True



But case sensitive:


```python
"UCL" > "kcl"
```




    False



There's no automatic conversion of the **string** True to true:


```python
True == "True"
```




    False



And you cannot compare a string of a number to a number.


```python
"1" < 2
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    /var/folders/q7/nl3w6z854711jwsdy0hj7sxhwypcgh/T/ipykernel_64389/4031537418.py in <module>
    ----> 1 "1" < 2


    TypeError: '<' not supported between instances of 'str' and 'int'



```python
"5" < 2
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    /var/folders/q7/nl3w6z854711jwsdy0hj7sxhwypcgh/T/ipykernel_64389/1549792606.py in <module>
    ----> 1 "5" < 2


    TypeError: '<' not supported between instances of 'str' and 'int'



```python
"1" > 2
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    /var/folders/q7/nl3w6z854711jwsdy0hj7sxhwypcgh/T/ipykernel_64389/1687267052.py in <module>
    ----> 1 "1" > 2


    TypeError: '>' not supported between instances of 'str' and 'int'


Any statement that evaluates to `True` or `False` can be used to control an `if` Statement.

### Automatic Falsehood

Various other things automatically count as true or false, which can make life easier when coding:


```python
mytext = "Hello"
```


```python
if mytext:
    print("Mytext is not empty")
```

    Mytext is not empty



```python
mytext2 = ""
```


```python
if mytext2:
    print("Mytext2 is not empty")
```

We can use logical not and logical and to combine true and false:


```python
x = 3.2
if not (x > 0 and type(x) == int):
    print(x, "is not a positive integer")
```

    3.2 is not a positive integer


`not` also understands magic conversion from false-like things to True or False.


```python
not not "Who's there!"
```




    True




```python
bool("")
```




    False




```python
bool("James")
```




    True




```python
bool([])
```




    False




```python
bool(["a"])
```




    True




```python
bool({})
```




    False




```python
bool({"name": "James"})
```




    True




```python
bool(0)
```




    False




```python
bool(1)
```




    True



But subtly, although these quantities evaluate True or False in an if statement, they're not themselves actually True or False under ==:


```python
[] == False
```




    False




```python
bool([]) == False
```




    True



## 1.7.4 Indentation

In Python, indentation is semantically significant.
You can choose how much indentation to use, so long as you
are consistent, but four spaces is
conventional. Please do not use tabs.

In the notebook, and most good editors, when you press `<tab>`, you get four spaces.

No indentation when it is expected, results in an error:


```python
x = 2
```


```python
if x > 0:
print(x)
```


      File "/var/folders/q7/nl3w6z854711jwsdy0hj7sxhwypcgh/T/ipykernel_64389/1979913910.py", line 2
        print(x)
            ^
    IndentationError: expected an indented block



but:


```python
if x > 0:
    print(x)
```

    2


## 1.7.5 Pass


A statement expecting identation must have some indented code.
This can be annoying when commenting things out. (With `#`)





```python
if x > 0:
    # print x

print("Hello")
```


      File "/var/folders/q7/nl3w6z854711jwsdy0hj7sxhwypcgh/T/ipykernel_64389/2248443618.py", line 4
        print("Hello")
            ^
    IndentationError: expected an indented block






So the `pass` statement is used to do nothing.





```python
if x > 0:
    # print x
    pass

print("Hello")
```

    Hello
