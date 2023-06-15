# 1.6 Data structures

*Estimated time for this notebook: 5 minutes*

## 1.6.1 Nested Lists and Dictionaries

In research programming, one of our most common tasks is building an appropriate *structure* to model our complicated
data. Later in the course, we'll see how we can define our own types, with their own attributes, properties, and methods. But probably the most common approach is to use nested structures of lists, dictionaries, and sets to model our data. For example, an address might be modelled as a dictionary with appropriately named fields:


```python
UCL = {"City": "London", "Street": "Gower Street", "Postcode": "WC1E 6BT"}
```


```python
James = {"City": "London", "Street": "Waterson Street", "Postcode": "E2 8HH"}
```

A collection of people's addresses is then a list of dictionaries:


```python
addresses = [UCL, James]
```


```python
addresses
```




    [{'City': 'London', 'Street': 'Gower Street', 'Postcode': 'WC1E 6BT'},
     {'City': 'London', 'Street': 'Waterson Street', 'Postcode': 'E2 8HH'}]



A more complicated data structure, for example for a census database, might have a list of residents or employees at each address:


```python
UCL["people"] = ["Clare", "James", "Owain"]
```


```python
James["people"] = ["Sue", "James"]
```


```python
addresses
```




    [{'City': 'London',
      'Street': 'Gower Street',
      'Postcode': 'WC1E 6BT',
      'people': ['Clare', 'James', 'Owain']},
     {'City': 'London',
      'Street': 'Waterson Street',
      'Postcode': 'E2 8HH',
      'people': ['Sue', 'James']}]



Which is then a list of dictionaries, with keys which are strings or lists.

We can go further, e.g.:


```python
UCL["Residential"] = False
```

And we can write code against our structures:


```python
leaders = [place["people"][0] for place in addresses]
leaders
```




    ['Clare', 'Sue']



This was an example of a 'list comprehension', which have used to get data of this structure, and which we'll see more of in a moment...
