# 1.8 Iteration

*Estimated time for this notebook: 10 minutes*

Our other aspect of control is looping back on ourselves.

We use `for` ... `in` to "iterate" over lists:


```python
mylist = [3, 7, 15, 2]
```


```python
for whatever in mylist:
    print(whatever**2)
```

    9
    49
    225
    4


Each time through the loop, the variable in the `value` slot is updated to the **next** element of the sequence.

## 1.8.1 Iterables


Any sequence type is iterable:





```python
vowels = "aeiou"
sarcasm = []

for letter in "Okay":
    if letter.lower() in vowels:
        repetition = 3
    else:
        repetition = 1

    sarcasm.append(letter * repetition)

"".join(sarcasm)
```




    'OOOkaaay'



The above is a little puzzle, work through it to understand why it does what it does.

###  Dictionaries are Iterables

All sequences are iterables. Some iterables (things you can `for` loop over) are not sequences (things with you can do `x[5]` to), for example sets and dictionaries.


```python
current_year = 2022
founded = {"Barack Obama": 1961, "UCL": 1826, "The Alan Turing Institute": 2015}

for thing in founded:
    print(f"In {current_year} {thing} is {current_year - founded[thing]} years old.")
```

    In 2022 Barack Obama is 61 years old.
    In 2022 UCL is 195 years old.
    In 2022 The Alan Turing Institute is 7 years old.


## 1.8.2 Unpacking and Iteration


Unpacking can be useful with iteration:





```python
triples = [[4, 11, 15], [39, 4, 18]]
```


```python
for whatever in triples:
    print(whatever)
```

    [4, 11, 15]
    [39, 4, 18]



```python
for first, middle, last in triples:
    print(middle)
```

    11
    4



```python
# A reminder that the words you use for variable names are arbitrary:
for hedgehog, badger, fox in triples:
    print(badger)
```

    11
    4





for example, to iterate over the items in a dictionary as pairs:





```python
things = {
    "James": [1976, "Kendal"],
    "UCL": [1826, "Bloomsbury"],
    "Cambridge": [1209, "Cambridge"],
}

print(things.items())
```

    dict_items([('James', [1976, 'Kendal']), ('UCL', [1826, 'Bloomsbury']), ('Cambridge', [1209, 'Cambridge'])])



```python
for name, year in founded.items():
    print(name, "is", current_year - year, "years old.")
```

    James is 45 years old.
    UCL is 195 years old.
    Cambridge is 812 years old.


## 1.8.3 Break, Continue


* Continue skips to the next turn of a loop
* Break stops the loop early





```python
for n in range(50):
    if n == 20:
        break
    if n % 2 == 0:
        continue
    print(n)
```

    1
    3
    5
    7
    9
    11
    13
    15
    17
    19


These aren't useful that often, but are worth knowing about. There's also an optional `else` clause on loops, executed only if you don't `break`, but I've never found that useful.


```python

```
