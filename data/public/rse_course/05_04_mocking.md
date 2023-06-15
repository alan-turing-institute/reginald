# 5.4 Mocking

*Estimated time for this notebook: 15 minutes*

## Definition

**Mock**: *verb*,

1. to tease or laugh at in a scornful or contemptuous manner
2. to make a replica or imitation of something

**Mocking**

- Replace a real object with a pretend object, which records how it is called, and can assert if it is called wrong

## Mocking frameworks

* C: [CMocka](http://www.cmocka.org/)
* C++: [googlemock](https://google.github.io/googletest/reference/mocking.html)
* Python: [unittest.mock](http://docs.python.org/dev/library/unittest.mock)

## Recording calls with mock

Mock objects record the calls made to them:


```python
from unittest.mock import Mock

function = Mock(name="myroutine", return_value=2)
```


```python
function(1)
```




    2




```python
function(5, "hello", a=True)
```




    2




```python
function.mock_calls
```




    [call(1), call(5, 'hello', a=True)]



The arguments of each call can be recovered


```python
name, args, kwargs = function.mock_calls[1]
args, kwargs
```




    ((5, 'hello'), {'a': True})



Mock objects can return different values for each call


```python
function = Mock(name="myroutine", side_effect=[2, "xyz"])
```


```python
function(1)
```




    2




```python
function(1, "hello", {"a": True})
```




    'xyz'



We expect an error if there are no return values left in the list:


```python
function()
```


    ---------------------------------------------------------------------------

    StopIteration                             Traceback (most recent call last)

    Input In [18], in <cell line: 1>()
    ----> 1 function()


    File ~/opt/anaconda3/envs/rse-course/lib/python3.9/unittest/mock.py:1092, in CallableMixin.__call__(self, *args, **kwargs)
       1090 self._mock_check_sig(*args, **kwargs)
       1091 self._increment_mock_call(*args, **kwargs)
    -> 1092 return self._mock_call(*args, **kwargs)


    File ~/opt/anaconda3/envs/rse-course/lib/python3.9/unittest/mock.py:1096, in CallableMixin._mock_call(self, *args, **kwargs)
       1095 def _mock_call(self, /, *args, **kwargs):
    -> 1096     return self._execute_mock_call(*args, **kwargs)


    File ~/opt/anaconda3/envs/rse-course/lib/python3.9/unittest/mock.py:1153, in CallableMixin._execute_mock_call(self, *args, **kwargs)
       1151     raise effect
       1152 elif not _callable(effect):
    -> 1153     result = next(effect)
       1154     if _is_exception(result):
       1155         raise result


    StopIteration:


## Using mocks to model test resources

Often we want to write tests for code which interacts with remote resources. (E.g. databases, the internet, or data files.)

We don't want to have our tests *actually* interact with the remote resource, as this would mean our tests failed
due to lost internet connections, for example.

Instead, we can use mocks to assert that our code does the right thing in terms of the *messages it sends*: the parameters of the
function calls it makes to the remote resource.

For example, consider the following code that downloads a map from the internet:


```python
import requests


def map_at(lat, long, satellite=False, zoom=12, size=(400, 400)):
    base = "https://static-maps.yandex.ru/1.x/?"
    params = dict(
        z=zoom,
        size=str(size[0]) + "," + str(size[1]),
        ll=str(long) + "," + str(lat),
        l="sat" if satellite else "map",
        lang="en_US",
    )
    return requests.get(base, params=params, timeout=60)
```


```python
london_map = map_at(51.5073509, -0.1277583)
```


```python
%matplotlib inline
import IPython

IPython.core.display.Image(london_map.content)
```





![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module05_testing_your_code/05_04_mocking_25_0.png)




We would like to test that it is building the parameters correctly. We can do this by **mocking** the requests object. We need to temporarily replace a method in the library with a mock. We can use "patch" to do this:


```python
from unittest.mock import patch

with patch.object(requests, "get") as mock_get:
    london_map = map_at(51.5073509, -0.1277583)
    print(mock_get.mock_calls)
```

    [call('https://static-maps.yandex.ru/1.x/?', params={'z': 12, 'size': '400,400', 'll': '-0.1277583,51.5073509', 'l': 'map', 'lang': 'en_US'})]


Our tests then look like:


```python
def test_build_default_params():
    with patch.object(requests, "get") as mock_get:
        map_at(51.0, 0.0)
        mock_get.assert_called_with(
            "https://static-maps.yandex.ru/1.x/?",
            params={
                "z": 12,
                "size": "400,400",
                "ll": "0.0,51.0",
                "l": "map",
                "lang": "en_US",
            },
            timeout=60,
        )


test_build_default_params()
```

That was quiet, so it passed. When I'm writing tests, I usually modify one of the expectations, to something 'wrong', just to check it's not
passing "by accident", run the tests, then change it back!

## Testing functions that call other functions


```python
def partial_derivative(function, at, direction, delta=1.0):
    f_x = function(at)
    x_plus_delta = at[:]
    x_plus_delta[direction] += delta
    f_x_plus_delta = function(x_plus_delta)
    return (f_x_plus_delta - f_x) / delta
```

We want to test that the above function does the right thing. It is supposed to compute the derivative of a function
of a vector in a particular direction.

E.g.:


```python
partial_derivative(sum, [0, 0, 0], 1)
```




    1.0



How do we assert that it is doing the right thing? With tests like this:


```python
from unittest.mock import MagicMock


def test_derivative_2d_y_direction():
    func = MagicMock()
    partial_derivative(func, [0, 0], 1)
    func.assert_any_call([0, 1.0])
    func.assert_any_call([0, 0])


test_derivative_2d_y_direction()
```

We made our mock a "Magic Mock" because otherwise, the mock results `f_x_plus_delta` and `f_x` can't be subtracted:


```python
MagicMock() - MagicMock()
```




    <MagicMock name='mock.__sub__()' id='4662499600'>




```python
Mock() - Mock()
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    /var/folders/q7/nl3w6z854711jwsdy0hj7sxhwypcgh/T/ipykernel_66984/881210313.py in <module>
    ----> 1 Mock() - Mock()


    TypeError: unsupported operand type(s) for -: 'Mock' and 'Mock'
