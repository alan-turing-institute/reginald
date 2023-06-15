# 3.1 Field and Record Data

*Estimated time to complete this notebook: 20 minutes*

## 3.1.1 Separated Value Files

Let's go back to the sunspots example [from the previous module](../module02_intermediate_python/02_04_getting_data_from_the_internet.ipynb).
We had downloaded some semicolon separated data and decided it was better to use a library than to write our own parser.


```python
import requests

spots = requests.get("http://www.sidc.be/silso/INFO/snmtotcsv.php", timeout=60)
spots.text.split("\n")[0]
```




    '1749;01;1749.042;  96.7; -1.0;   -1;1'



We want to work programmatically with *Separated Value* files.

These are files which have:

* Each *record* on a line
* Each record has multiple *fields*
* Fields are separated by some *separator*

Typical separators are the `space`, `tab`, `comma`, and `semicolon` separated values files, e.g.:

* Space separated value (e.g. `field1 "field two" field3` )
* Comma separated value (e.g. `field1, another field, "wow, another field"`)

Comma-separated-value is abbreviated CSV, and tab separated value TSV.

CSV is also used to refer to all the different sub-kinds of separated value files, i.e. some people use CSV to refer to tab, space and semicolon separated files.

CSV is not a particularly great data format, because it forces your data model to be a list of lists.
Richer file formats describe "serialisations" for dictionaries and for deeper-than-two nested list structures as well.

Nevertheless, CSV files are very popular because you can always export *spreadsheets* as CSV files, (each cell is a field, each row is a record)

## 3.1.2 CSV variants

Some CSV formats define a comment character, so that rows beginning with, e.g., a #, are not treated as data, but give a human comment.

Some CSV formats define a three-deep list structure, where a double-newline separates records into blocks.

Some CSV formats assume that the first line defines the names of the fields, e.g.:

```
name, age
James, 39
Will, 2
```

## 3.1.3 Python CSV readers

The Python standard library has a `csv` module.
However, it's less powerful than the CSV capabilities in other libraries such as [`numpy`](https://numpy.org/).
Here we will use [`pandas`](https://pandas.pydata.org/) which is built on top of `numpy`.


```python
import pandas as pd
```


```python
df = pd.read_csv("http://www.sidc.be/silso/INFO/snmtotcsv.php", sep=";", header=None)
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1749</td>
      <td>1</td>
      <td>1749.042</td>
      <td>96.7</td>
      <td>-1.0</td>
      <td>-1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1749</td>
      <td>2</td>
      <td>1749.123</td>
      <td>104.3</td>
      <td>-1.0</td>
      <td>-1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1749</td>
      <td>3</td>
      <td>1749.204</td>
      <td>116.7</td>
      <td>-1.0</td>
      <td>-1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1749</td>
      <td>4</td>
      <td>1749.288</td>
      <td>92.8</td>
      <td>-1.0</td>
      <td>-1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1749</td>
      <td>5</td>
      <td>1749.371</td>
      <td>141.7</td>
      <td>-1.0</td>
      <td>-1</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



Pandas `read_csv` is a powerful CSV reader tool.
A path to the data is given, this can be something on a local machine, or in this case the path is a url.


We used the `sep` optional argument to specify the delimeter.
The optional argument `header` specifies if the data contains headers, and if so; the row numbers to use as column names.


The data is loaded into a DataFrame.
The `head` method shows us the first 5 entries in the dataframe.
The `tail` method shows us the last 5 entries.


```python
df.tail()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>3278</th>
      <td>2022</td>
      <td>3</td>
      <td>2022.204</td>
      <td>78.6</td>
      <td>14.0</td>
      <td>1413</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3279</th>
      <td>2022</td>
      <td>4</td>
      <td>2022.286</td>
      <td>84.1</td>
      <td>15.2</td>
      <td>1237</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3280</th>
      <td>2022</td>
      <td>5</td>
      <td>2022.371</td>
      <td>96.5</td>
      <td>16.0</td>
      <td>1250</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3281</th>
      <td>2022</td>
      <td>6</td>
      <td>2022.453</td>
      <td>70.5</td>
      <td>12.9</td>
      <td>1219</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3282</th>
      <td>2022</td>
      <td>7</td>
      <td>2022.538</td>
      <td>91.4</td>
      <td>12.2</td>
      <td>1304</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>




```python
df[3][0]
```




    96.7



We can now plot the "Sunspot cycle":


```python
df.plot(x=2, y=3)
```




    <AxesSubplot:xlabel='2'>





![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module03_research_data_in_python/03_01_fields_and_records_24_1.png)



The plot command accepted an series of 'X' values and an series of 'Y' values, identified by their column number in this case, as the dataframe does not have (useful) column headers yet.

## 3.1.4 Naming Columns

As it happens, the columns definitions can be found on the source website (http://www.sidc.be/silso/infosnmtot)

> CSV
>
> Filename: SN_m_tot_V2.0.csv
> Format: Comma Separated values (adapted for import in spreadsheets)
> The separator is the semicolon ';'.
>
> Contents:
> - Column 1-2: Gregorian calendar date
>   - Year
>   - Month
> - Column 3: Date in fraction of year.
> - Column 4: Monthly mean total sunspot number.
> - Column 5: Monthly mean standard deviation of the input sunspot numbers.
> - Column 6: Number of observations used to compute the monthly mean total sunspot number.
> - Column 7: Definitive/provisional marker. '1' indicates that the value is definitive. '0' indicates that the value is still provisional.

We can actually specify this to the formatter:


```python
df_w_names = pd.read_csv(
    "http://www.sidc.be/silso/INFO/snmtotcsv.php",
    sep=";",
    header=None,
    names=["year", "month", "date", "mean", "deviation", "observations", "definitive"],
)
df_w_names.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>year</th>
      <th>month</th>
      <th>date</th>
      <th>mean</th>
      <th>deviation</th>
      <th>observations</th>
      <th>definitive</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1749</td>
      <td>1</td>
      <td>1749.042</td>
      <td>96.7</td>
      <td>-1.0</td>
      <td>-1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1749</td>
      <td>2</td>
      <td>1749.123</td>
      <td>104.3</td>
      <td>-1.0</td>
      <td>-1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1749</td>
      <td>3</td>
      <td>1749.204</td>
      <td>116.7</td>
      <td>-1.0</td>
      <td>-1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1749</td>
      <td>4</td>
      <td>1749.288</td>
      <td>92.8</td>
      <td>-1.0</td>
      <td>-1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1749</td>
      <td>5</td>
      <td>1749.371</td>
      <td>141.7</td>
      <td>-1.0</td>
      <td>-1</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_w_names.plot(x="date", y="mean")
```




    <AxesSubplot:xlabel='date'>





![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module03_research_data_in_python/03_01_fields_and_records_31_1.png)



Note: The plot method used for the `DataFrame` is just a wrapper around the `matplotlib` function `plt.plot()`:

## 3.1.5 Typed Fields

It's also often useful to check, and if necessary specify, the datatype of each field.


```python
df_w_names.dtypes  # Check the data types of all columns in the DataFrame
```




    year              int64
    month             int64
    date            float64
    mean            float64
    deviation       float64
    observations      int64
    definitive        int64
    dtype: object



In this case the data types seem sensible, however if we wanted to convert the year into a floating point number instead, we could via:


```python
df_w_names["year"] = df_w_names["year"].astype("float64")
df_w_names.dtypes
```




    year            float64
    month             int64
    date            float64
    mean            float64
    deviation       float64
    observations      int64
    definitive        int64
    dtype: object




```python
df_w_names.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>year</th>
      <th>month</th>
      <th>date</th>
      <th>mean</th>
      <th>deviation</th>
      <th>observations</th>
      <th>definitive</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1749.0</td>
      <td>1</td>
      <td>1749.042</td>
      <td>96.7</td>
      <td>-1.0</td>
      <td>-1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1749.0</td>
      <td>2</td>
      <td>1749.123</td>
      <td>104.3</td>
      <td>-1.0</td>
      <td>-1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1749.0</td>
      <td>3</td>
      <td>1749.204</td>
      <td>116.7</td>
      <td>-1.0</td>
      <td>-1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1749.0</td>
      <td>4</td>
      <td>1749.288</td>
      <td>92.8</td>
      <td>-1.0</td>
      <td>-1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1749.0</td>
      <td>5</td>
      <td>1749.371</td>
      <td>141.7</td>
      <td>-1.0</td>
      <td>-1</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



## 3.1.6 Filtering data

Sometimes it is necessary to filter data, for example to only see the sunspots for the year 2018 you would use:


```python
df_twenty_eighteen = df_w_names[(df_w_names["year"] == 2018)]
df_twenty_eighteen.head(20)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>year</th>
      <th>month</th>
      <th>date</th>
      <th>mean</th>
      <th>deviation</th>
      <th>observations</th>
      <th>definitive</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>3228</th>
      <td>2018.0</td>
      <td>1</td>
      <td>2018.042</td>
      <td>6.8</td>
      <td>1.5</td>
      <td>701</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3229</th>
      <td>2018.0</td>
      <td>2</td>
      <td>2018.122</td>
      <td>10.7</td>
      <td>1.1</td>
      <td>917</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3230</th>
      <td>2018.0</td>
      <td>3</td>
      <td>2018.204</td>
      <td>2.5</td>
      <td>0.4</td>
      <td>1081</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3231</th>
      <td>2018.0</td>
      <td>4</td>
      <td>2018.286</td>
      <td>8.9</td>
      <td>1.3</td>
      <td>996</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3232</th>
      <td>2018.0</td>
      <td>5</td>
      <td>2018.371</td>
      <td>13.1</td>
      <td>1.6</td>
      <td>1234</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3233</th>
      <td>2018.0</td>
      <td>6</td>
      <td>2018.453</td>
      <td>15.6</td>
      <td>1.6</td>
      <td>1070</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3234</th>
      <td>2018.0</td>
      <td>7</td>
      <td>2018.538</td>
      <td>1.6</td>
      <td>0.6</td>
      <td>1438</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3235</th>
      <td>2018.0</td>
      <td>8</td>
      <td>2018.623</td>
      <td>8.7</td>
      <td>1.0</td>
      <td>1297</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3236</th>
      <td>2018.0</td>
      <td>9</td>
      <td>2018.705</td>
      <td>3.3</td>
      <td>0.6</td>
      <td>1223</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3237</th>
      <td>2018.0</td>
      <td>10</td>
      <td>2018.790</td>
      <td>4.9</td>
      <td>1.2</td>
      <td>1097</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3238</th>
      <td>2018.0</td>
      <td>11</td>
      <td>2018.873</td>
      <td>4.9</td>
      <td>0.6</td>
      <td>771</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3239</th>
      <td>2018.0</td>
      <td>12</td>
      <td>2018.958</td>
      <td>3.1</td>
      <td>0.5</td>
      <td>786</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



Even though we used
```bash
df_twenty_eighteen.head(20)
```
to show us the first 20 results from the dataframe, only 12 are shown as there are only 12 months in a year

If we wanted all data from 1997 to 1999 we could via:


```python
df_nineties = df_w_names[(df_w_names["year"] >= 1997) & (df_w_names["year"] < 2000)]
```


```python
df_nineties.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>year</th>
      <th>month</th>
      <th>date</th>
      <th>mean</th>
      <th>deviation</th>
      <th>observations</th>
      <th>definitive</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2976</th>
      <td>1997.0</td>
      <td>1</td>
      <td>1997.042</td>
      <td>7.4</td>
      <td>3.2</td>
      <td>497</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2977</th>
      <td>1997.0</td>
      <td>2</td>
      <td>1997.123</td>
      <td>11.0</td>
      <td>2.9</td>
      <td>545</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2978</th>
      <td>1997.0</td>
      <td>3</td>
      <td>1997.204</td>
      <td>12.1</td>
      <td>2.4</td>
      <td>627</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2979</th>
      <td>1997.0</td>
      <td>4</td>
      <td>1997.288</td>
      <td>23.0</td>
      <td>3.3</td>
      <td>663</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2980</th>
      <td>1997.0</td>
      <td>5</td>
      <td>1997.371</td>
      <td>25.4</td>
      <td>2.8</td>
      <td>716</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_nineties.tail()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>year</th>
      <th>month</th>
      <th>date</th>
      <th>mean</th>
      <th>deviation</th>
      <th>observations</th>
      <th>definitive</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>3007</th>
      <td>1999.0</td>
      <td>8</td>
      <td>1999.623</td>
      <td>142.3</td>
      <td>12.9</td>
      <td>649</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3008</th>
      <td>1999.0</td>
      <td>9</td>
      <td>1999.707</td>
      <td>106.3</td>
      <td>6.5</td>
      <td>624</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3009</th>
      <td>1999.0</td>
      <td>10</td>
      <td>1999.790</td>
      <td>168.7</td>
      <td>10.4</td>
      <td>531</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3010</th>
      <td>1999.0</td>
      <td>11</td>
      <td>1999.874</td>
      <td>188.3</td>
      <td>12.3</td>
      <td>406</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3011</th>
      <td>1999.0</td>
      <td>12</td>
      <td>1999.958</td>
      <td>116.8</td>
      <td>9.3</td>
      <td>404</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>
