# Module 2: Hands-on session (Solutions)

⚠️ **Warning** ⚠️ These are sample solutions to the exercises for the Module 2 hands-on session. We don't recommend looking here before you've attempted them!

## Notebook Setup

Import necessary packages for this work:


```python
import os

import pandas as pd

from handson_utils import (
    parse_country_values_2011,
    check_dataset_load,
    check_dataset_explored,
    check_column_mapping
)
```

Define path to data. This relies on the data being saved in the specified location below.


```python
DATA_ROOT_PATH = "../m4/data/UKDA-7724-csv" # should match the path you unzipped the data to

COMBINED_CSV_PATH = os.path.join(DATA_ROOT_PATH, "csv/eqls_2007and2011.csv")
MAPPING_CSV_PATH = os.path.join(DATA_ROOT_PATH, "mrdoc/excel/eqls_api_map.csv")

# consts for loading categorical data value maps
CATEGORICAL_VALUES_XLSX_PATH = os.path.join(DATA_ROOT_PATH, "mrdoc/excel/eqls_concordance_grid.xlsx")
CATEGORICAL_VALUES_XLSX_SHEET_NAME = "Values"
```

## Exploring the Downloaded Files

Take some time to familiarise yourself with the file structure of the downloaded files (in the `UKDA-7724-csv` directory), opening them in Excel/Numbers/relevant application of your choice initially. In particular:

- The table of files `mrdoc/excel/7724_file_information_csv.csv`
- The `csv` directory
   - What data does each file contain?
- The user guide `mrdoc/pdf/7724_eqls_2007-2011_user_guide_v2.pdf`
- The "Variables" and "Values" worksheet in `mrdoc/excel/eqls_concordance_grid.xlsx`
   - How many variables are there? Can they be grouped in any way?


**Answer:** There are 199 variables listed in `mrdoc/excel/eqls_concordance_grid.xlsx`. There are a number of "Variable Groups" (e.g., "Family and Social Life") and "Topic Classifications" (e.g., "Social stratification and groupings - Family life and marriage")

## Load and Explore

***Relevant sections:*** *2.1.4 (Data Sources and Formats), 2.2.1 (Data Consistency)*

Read the combined 2007 and 2011 data into a pandas `DataFrame`


```python
# ANSWER read in the file and display the head
####

df = pd.read_csv(COMBINED_CSV_PATH)
display(df.head())

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
      <th>Wave</th>
      <th>Y11_Country</th>
      <th>Y11_Q31</th>
      <th>Y11_Q32</th>
      <th>Y11_ISCEDsimple</th>
      <th>Y11_Q49</th>
      <th>Y11_Q67_1</th>
      <th>Y11_Q67_2</th>
      <th>Y11_Q67_3</th>
      <th>Y11_Q67_4</th>
      <th>...</th>
      <th>DV_Q54a</th>
      <th>DV_Q54b</th>
      <th>DV_Q55</th>
      <th>DV_Q56</th>
      <th>DV_Q8</th>
      <th>DV_Q10</th>
      <th>ISO3166_Country</th>
      <th>RowID</th>
      <th>URIRowID</th>
      <th>UniqueID</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2</td>
      <td>1</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>4.0</td>
      <td>4.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>https://www.iso.org/obp/ui/#iso:code:3166:AT</td>
      <td>1</td>
      <td>https://api.ukdataservice.ac.uk/V1/datasets/eq...</td>
      <td>AT9000083</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>4.0</td>
      <td>4.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>https://www.iso.org/obp/ui/#iso:code:3166:AT</td>
      <td>2</td>
      <td>https://api.ukdataservice.ac.uk/V1/datasets/eq...</td>
      <td>AT9000126</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>1</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>3.0</td>
      <td>2.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>https://www.iso.org/obp/ui/#iso:code:3166:AT</td>
      <td>3</td>
      <td>https://api.ukdataservice.ac.uk/V1/datasets/eq...</td>
      <td>AT9000267</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2</td>
      <td>1</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>1.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>https://www.iso.org/obp/ui/#iso:code:3166:AT</td>
      <td>4</td>
      <td>https://api.ukdataservice.ac.uk/V1/datasets/eq...</td>
      <td>AT9000268</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2</td>
      <td>1</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>4.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>https://www.iso.org/obp/ui/#iso:code:3166:AT</td>
      <td>5</td>
      <td>https://api.ukdataservice.ac.uk/V1/datasets/eq...</td>
      <td>AT9000427</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 199 columns</p>
</div>



```python
# checks - will produce an `AssertionError` until DataFrame loaded correctly
check_dataset_load(df)
```

    ✅ df loaded correctly


Take a look at some summary statistics and use these to assign the variables below correctly.

You can assign the variables manually from inspecting printed output or assign them results from methods/properties.


```python
# ANSWER - example functions to explore and answer questions below

df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 79270 entries, 0 to 79269
    Columns: 199 entries, Wave to UniqueID
    dtypes: float64(187), int64(9), object(3)
    memory usage: 120.4+ MB



```python
df.describe()
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
      <th>Wave</th>
      <th>Y11_Country</th>
      <th>Y11_Q31</th>
      <th>Y11_Q32</th>
      <th>Y11_ISCEDsimple</th>
      <th>Y11_Q49</th>
      <th>Y11_Q67_1</th>
      <th>Y11_Q67_2</th>
      <th>Y11_Q67_3</th>
      <th>Y11_Q67_4</th>
      <th>...</th>
      <th>DV_Q7</th>
      <th>DV_Q67</th>
      <th>DV_Q43Q44</th>
      <th>DV_Q54a</th>
      <th>DV_Q54b</th>
      <th>DV_Q55</th>
      <th>DV_Q56</th>
      <th>DV_Q8</th>
      <th>DV_Q10</th>
      <th>RowID</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>79270.000000</td>
      <td>79270.000000</td>
      <td>78756.000000</td>
      <td>78769.000000</td>
      <td>78556.000000</td>
      <td>79082.000000</td>
      <td>43636.000000</td>
      <td>43636.000000</td>
      <td>43636.000000</td>
      <td>43636.000000</td>
      <td>...</td>
      <td>2225.000000</td>
      <td>43636.000000</td>
      <td>78312.000000</td>
      <td>43636.000000</td>
      <td>43636.000000</td>
      <td>43636.000000</td>
      <td>43636.000000</td>
      <td>43636.000000</td>
      <td>43636.000000</td>
      <td>79270.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>2.550473</td>
      <td>16.841138</td>
      <td>1.856049</td>
      <td>1.598141</td>
      <td>4.019146</td>
      <td>2.640955</td>
      <td>1.959368</td>
      <td>1.023673</td>
      <td>1.019204</td>
      <td>1.001971</td>
      <td>...</td>
      <td>52.612135</td>
      <td>1.086465</td>
      <td>2.485992</td>
      <td>2.815565</td>
      <td>2.925635</td>
      <td>0.303442</td>
      <td>0.231437</td>
      <td>3.931708</td>
      <td>3.283482</td>
      <td>39635.500000</td>
    </tr>
    <tr>
      <th>std</th>
      <td>0.497449</td>
      <td>9.358320</td>
      <td>1.186271</td>
      <td>1.276425</td>
      <td>1.368993</td>
      <td>0.987352</td>
      <td>0.197437</td>
      <td>0.152030</td>
      <td>0.137244</td>
      <td>0.044351</td>
      <td>...</td>
      <td>15.696943</td>
      <td>0.460388</td>
      <td>0.838558</td>
      <td>0.721642</td>
      <td>0.568403</td>
      <td>0.881979</td>
      <td>0.827727</td>
      <td>0.436254</td>
      <td>1.130667</td>
      <td>22883.422256</td>
    </tr>
    <tr>
      <th>min</th>
      <td>2.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>...</td>
      <td>5.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>2.000000</td>
      <td>9.000000</td>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>3.000000</td>
      <td>2.000000</td>
      <td>2.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>...</td>
      <td>43.000000</td>
      <td>1.000000</td>
      <td>2.000000</td>
      <td>3.000000</td>
      <td>3.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>4.000000</td>
      <td>2.000000</td>
      <td>19818.250000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>3.000000</td>
      <td>16.000000</td>
      <td>1.000000</td>
      <td>2.000000</td>
      <td>4.000000</td>
      <td>3.000000</td>
      <td>2.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>...</td>
      <td>50.000000</td>
      <td>1.000000</td>
      <td>3.000000</td>
      <td>3.000000</td>
      <td>3.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>4.000000</td>
      <td>4.000000</td>
      <td>39635.500000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>3.000000</td>
      <td>25.000000</td>
      <td>3.000000</td>
      <td>2.000000</td>
      <td>5.000000</td>
      <td>4.000000</td>
      <td>2.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>...</td>
      <td>61.000000</td>
      <td>1.000000</td>
      <td>3.000000</td>
      <td>3.000000</td>
      <td>3.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>4.000000</td>
      <td>4.000000</td>
      <td>59452.750000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>3.000000</td>
      <td>35.000000</td>
      <td>4.000000</td>
      <td>5.000000</td>
      <td>8.000000</td>
      <td>4.000000</td>
      <td>2.000000</td>
      <td>2.000000</td>
      <td>2.000000</td>
      <td>2.000000</td>
      <td>...</td>
      <td>80.000000</td>
      <td>6.000000</td>
      <td>3.000000</td>
      <td>6.000000</td>
      <td>6.000000</td>
      <td>4.000000</td>
      <td>4.000000</td>
      <td>4.000000</td>
      <td>4.000000</td>
      <td>79270.000000</td>
    </tr>
  </tbody>
</table>
<p>8 rows × 196 columns</p>
</div>




```python
df["Y11_Country"].nunique()
```




    35




```python
# ANSWER
n_columns = 199 # how many columns are there in the DataFrame? This matches the number expected from the documentation.
n_float64_columns = 187 # how many columns are of dtype float64?
Y11_Q31_mean_value = 1.856049 #  what is the mean of the values in the Y11_Q31 column?
Y11_Country_n_unique = 35 # how many unique values in the Y11_Country column?


# function to check your answers (run this cell)
check_dataset_explored(
    n_columns,
    n_float64_columns,
    Y11_Q31_mean_value,
    Y11_Country_n_unique
)
```

    n_columns answer ✅ correct
    n_float64_columns answer ✅ correct
    Y11_Q31_mean_value answer ✅ correct
    Y11_Country_n_unique answer ✅ correct


## Different Data Types

***Relevant Sections:*** *2.2.1 (Data Consistency)*

Are there columns containing the following types of data? If so give examples.

- Numeric data (without a set of pre-defined categories)
- Binary data
- Categorical data, unordered
- Categorical data, ordered
- Text data
- Time or date data

**Note:**

- The dataset contains at least 4 of these, try to have another look if you found fewer.
- You'll need to refer to the dataset documentation to fully understand which columns contain which types (`mrdoc/excel/eqls_concordance_grid.xlsx` may be helpful, in particlar).

**Answer**:

A few examples:

- Numeric data
   - `Y11_Q8` (How many hours would you prefer to work)
   - `Y11_Q52` (How much time spent on travelling to work/study)

- Binary data
  - `Y11_Q67_1` (I am a citizen of the country)
  - `Y11_HH2a` (Gender - discussion point re inclusivity)

- Categorical data, unordered
  - `Country`
  - `Y11_EmploymentStatus` (e.g., no clear ordering between retired, unable to work, homemaker and unemployed)

- Categorical data, ordered
  - Majority of the data can be treated as ordered categories.
  - `Y11_Agecategory` (Age)
  - `Y11_Q53a` (Quality of Health services)

- Text data
  - There are no free text fields, but there are a couple of columns with strings (IDs/URLs mostly), e.g., `ISO3166_Country`, `UniqueID`.

- Time or date data
  - None in this dataset (could claim that `Wave` is perhaps as it represents a year)

For one example of each type, what are the possible values the data can take, according to the documentation? What does each value mean? Is each possible value present in the dataset?


```python
# Numeric example:
# Note the question of "what are the possible values" only really makes sense for categorical data,
# but we could talk about the range of values in the data.

df["Y11_Q8"].describe()
# units are hours
```




    count    37958.000000
    mean        29.658043
    std         16.476718
    min          0.000000
    25%         20.000000
    50%         36.000000
    75%         40.000000
    max        120.000000
    Name: Y11_Q8, dtype: float64




```python
# Binary example:

df["Y11_Q67_1"].value_counts()
# 1 means No and 2 means Yes
```




    2.0    41863
    1.0     1773
    Name: Y11_Q67_1, dtype: int64




```python
# Unordered categorical example:
df["Y11_EmploymentStatus"].value_counts()

# Values represent employment status: 1 = Employed (includes on leave), 2 = Unemployed, 3 = Unable to work - disability/illness,
# 4 = Retired, 5 = Homemaker, 6 = Student, 7 = Other"
# There are rows with all 7 values present.

```




    1    36381
    4    22925
    5     7372
    2     5375
    6     4259
    3     1720
    7     1238
    Name: Y11_EmploymentStatus, dtype: int64




```python
# Ordered categorical example:
df["Y11_Q53a"].value_counts().sort_index()

# Values are respondent's rating of the quality of health services, from 1 (very poor) to 10 (very high).
# There are rows with all 10 values present.
```




    1.0      3481
    2.0      2876
    3.0      5041
    4.0      5963
    5.0     12780
    6.0      9705
    7.0     13805
    8.0     13970
    9.0      5672
    10.0     4715
    Name: Y11_Q53a, dtype: int64



What is the minimum, maximum and mean value in each of your example columns? Taking into consideration the type of data in the column, are all of these values meaningful?


```python
# Can use "describe" or the "min", "max" and "mean" functions

df["Y11_Q8"].describe()  # Numeric
```




    count    37958.000000
    mean        29.658043
    std         16.476718
    min          0.000000
    25%         20.000000
    50%         36.000000
    75%         40.000000
    max        120.000000
    Name: Y11_Q8, dtype: float64




```python
df["Y11_Q67_1"].describe()  # Binary

# The mean represents the proportion of people that answered "Yes" here (1.96  means 96% of
# people answered Yes (2), and 4% no (1). Would be clearer if no was 0 and yes was 1.
```




    count    43636.000000
    mean         1.959368
    std          0.197437
    min          1.000000
    25%          2.000000
    50%          2.000000
    75%          2.000000
    max          2.000000
    Name: Y11_Q67_1, dtype: float64




```python
df["Y11_EmploymentStatus"].describe() # Unordered category

# Note: The mean of an unordered category is not meaningful!
# E.g. if we had 2 people, one with a value of 4 (retired), and one with 5 (homemaker), we'd compute
# a mean of 4.5 - does that mean they're part-time retired, part-time homemaker?!
```




    count    79270.000000
    mean         2.713145
    std          1.793318
    min          1.000000
    25%          1.000000
    50%          2.000000
    75%          4.000000
    max          7.000000
    Name: Y11_EmploymentStatus, dtype: float64




```python
df["Y11_Q53a"].describe()  # Ordered  category

# Need to be careful about interpreting the mean for ordered categories. For this column the
# categories are ratings from 1 to 10, and the mean rating represents what you'd expect. Others may
# be more nuanced, e.g. the age category column has categories with different sized bins (18-24
# covers 7 years, 35-49 covers 15 years, 65+ covers N years).
```




    count    78008.000000
    mean         6.113873
    std          2.293152
    min          1.000000
    25%          5.000000
    50%          6.000000
    75%          8.000000
    max         10.000000
    Name: Y11_Q53a, dtype: float64



For one of the categorical columns, replace the numerical encodings with their actual meaning (category title). You can do this by manually creating a Python dictionary with the values to replace (we'll look at extracting them with code later). What is the most common value?


```python
status_encoding = {
    1: "Employed (includes on leave)",
    2: "Unemployed",
    3: "Unable to work - disability/illness",
    4: "Retired",
    5: "Homemaker",
    6: "Student",
    7: "Other"
}

employment_status = df["Y11_EmploymentStatus"].replace(status_encoding)
employment_status.value_counts()
```




    Employed (includes on leave)           36381
    Retired                                22925
    Homemaker                               7372
    Unemployed                              5375
    Student                                 4259
    Unable to work - disability/illness     1720
    Other                                   1238
    Name: Y11_EmploymentStatus, dtype: int64



## Making Things More Readable

***Relevant Sections:*** *2.2.2 (Modifying Columns and Indices), 2.2.4.2 (Text Data)*

At the moment, we've got column headings such as `'Y11_Country'`, `'Y11_Q31'` and `'Y11_Q32'` in our data. These aren't particularly helpful at a glance and we'd need to do some cross-referencing with `eqls_api_map.csv` to make sense of them.

To make things more readable, let's rename our columns according to the `'VariableLabel'` column in `mrdoc/excel/eqls_api_map.csv`.

However, because it can make `.` access a bit tricky, we'd like to make sure we don't have any spaces or non-word characters in our new column names! For consistency, we'd like everything to be lower case.


```python
# we have to explicitly use latin1 encoding as the file is not saved in utf-8 (our platform default)
eqls_api_map_df = pd.read_csv(MAPPING_CSV_PATH, encoding='latin1')
eqls_api_map_df.head()
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
      <th>VariableName</th>
      <th>VariableLabel</th>
      <th>Question</th>
      <th>TopicValue</th>
      <th>KeywordValue</th>
      <th>VariableGroupValue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Wave</td>
      <td>EQLS Wave</td>
      <td>EQLS Wave</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Administrative Variables</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Y11_Country</td>
      <td>Country</td>
      <td>Country</td>
      <td>Geographies</td>
      <td>NaN</td>
      <td>Household Grid and Country</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Y11_Q31</td>
      <td>Marital status</td>
      <td>Marital status</td>
      <td>Social stratification and groupings - Family l...</td>
      <td>Marital status</td>
      <td>Family and Social Life</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Y11_Q32</td>
      <td>No. of children</td>
      <td>Number of children of your own</td>
      <td>Social stratification and groupings - Family l...</td>
      <td>Children</td>
      <td>Family and Social Life</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Y11_ISCEDsimple</td>
      <td>Education completed</td>
      <td>Highest level of education completed</td>
      <td>Education - Higher and further</td>
      <td>Education levels</td>
      <td>Education</td>
    </tr>
  </tbody>
</table>
</div>



TODO:
- replace column names in `df` with corresponding entry in `'VariableLabel'` column from `eqls_api_map_df`
- ensure all column names are entirely lowercase
- ensure only characters [a-zA-Z0-9_] are present in column names
    - remove apostrophes (`"'"`)
    - replace otherwise non-matching (e.g., whitespace or `'/'`) character with `'_'`
    - we don't want consecutive `'_'` characters (e.g., `no_of_children` rather than `no__of_children`)
- keep a map (python `dict`) that shows the old -> new column mapping in case we ever want to invert this transformation.

Example manual mapping (you should produce this with a general code solution!):

```json
{
    ...,
    'Y11_Q32' -> 'no_of_children'
    ...,
    'Y11_Q67_4' -> 'citizenship_dont_know',
    ...,
}
```

You may find it helpful to use a site like [regex101](https://regex101.com/) to experiment with creating a
suitable regex expression.


```python
# Answer
old_cols = eqls_api_map_df["VariableName"]

# The 4 .str calls below:
#  convert to lowercase
#  remove apostrophes
#  replace whitespace with _
#  rremove consecutive underscores
new_cols = eqls_api_map_df["VariableLabel"].str.lower()\
                                        .str.replace("'",'')\
                                        .str.replace('[^\w]','_')\
                                        .str.replace("_+", "_")

column_mapping = dict(zip(old_cols, new_cols))


# Apply your column mapping to df
df = df.rename(columns=column_mapping)

display(df.head())
```

    /var/folders/xv/d5nvn2ps5r3fcf276w707n01qdmpqf/T/ipykernel_77880/3644821443.py:9: FutureWarning: The default value of regex will change from True to False in a future version.
      new_cols = eqls_api_map_df["VariableLabel"].str.lower()\



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
      <th>eqls_wave</th>
      <th>country</th>
      <th>marital_status</th>
      <th>no_of_children</th>
      <th>education_completed</th>
      <th>rural_urban_living</th>
      <th>citizenship_country</th>
      <th>citizenship_another_eu_member</th>
      <th>citizenship_a_non_eu_country</th>
      <th>citizenship_dont_know</th>
      <th>...</th>
      <th>dv_anyone_used_would_have_like_to_use_child_care_last_12_months_</th>
      <th>dv_anyone_used_would_have_like_to_use_long_term_care_last_12_months_</th>
      <th>dv_no_of_factors_which_made_it_difficult_to_use_child_care_</th>
      <th>dv_no_of_factors_which_made_it_difficult_to_use_long_term_care_</th>
      <th>dv_preferred_working_hours_3_groups_</th>
      <th>dv_preferred_working_hours_of_respondents_partner_3_groups_</th>
      <th>iso3166_country_url</th>
      <th>rowid_for_the_uk_data_service_public_api</th>
      <th>root_uri_for_a_row_respondent_that_displays_all_data_values_for_a_single_row_via_the_uk_data_service_public_api</th>
      <th>unique_respondent_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2</td>
      <td>1</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>4.0</td>
      <td>4.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>https://www.iso.org/obp/ui/#iso:code:3166:AT</td>
      <td>1</td>
      <td>https://api.ukdataservice.ac.uk/V1/datasets/eq...</td>
      <td>AT9000083</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>4.0</td>
      <td>4.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>https://www.iso.org/obp/ui/#iso:code:3166:AT</td>
      <td>2</td>
      <td>https://api.ukdataservice.ac.uk/V1/datasets/eq...</td>
      <td>AT9000126</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>1</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>3.0</td>
      <td>2.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>https://www.iso.org/obp/ui/#iso:code:3166:AT</td>
      <td>3</td>
      <td>https://api.ukdataservice.ac.uk/V1/datasets/eq...</td>
      <td>AT9000267</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2</td>
      <td>1</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>1.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>https://www.iso.org/obp/ui/#iso:code:3166:AT</td>
      <td>4</td>
      <td>https://api.ukdataservice.ac.uk/V1/datasets/eq...</td>
      <td>AT9000268</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2</td>
      <td>1</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>4.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>https://www.iso.org/obp/ui/#iso:code:3166:AT</td>
      <td>5</td>
      <td>https://api.ukdataservice.ac.uk/V1/datasets/eq...</td>
      <td>AT9000427</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 199 columns</p>
</div>



```python
# check your answer
check_column_mapping(column_mapping, df)
```

    Checking each column...
    ✅ Column mapping correct... Checking df columns set correctly...
    ✅ Success!


## Self-Reported Health

***Relevant Sections:*** *2.2.1 (Data Consistency), 2.2.3 (Feature Engineering), 2.2.4.3 (Categorical Data)*

The research question we defined in Module 1 and will explore in more detail in Modules 3 and 4 aims to explore the contribution of various factors on self-reported health.

Which column in the dataset contains self-reported health values? How many people had "Very good" self-reported health?


```python
# The relevant column is "health_condition" (Y11_Q42 before renaming)
df["health_condition"].value_counts().sort_index()

# 16898 people reported "very good" health (value of 1 below)
```




    1.0    16898
    2.0    31248
    3.0    22265
    4.0     6916
    5.0     1802
    Name: health_condition, dtype: int64



For the models we develop in Module 4 we'll convert self-reported health into a binary variable. What might be a sensible way to group the categories into only two possible values? Create a new column with your proposed binary encoding for self-reported health.


```python
# Could assign 1, 2, 3 (very good, good, fair) as "good health", and 4, 5 (bad, very bad) as "bad health".
df["bad_health"] = (df["health_condition"] > 3).astype(int)

display(df[["health_condition", "bad_health"]].sample(5))

# Note this creates very imbalanced classes.
df["bad_health"].value_counts()
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
      <th>health_condition</th>
      <th>bad_health</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>28292</th>
      <td>2.0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>43984</th>
      <td>2.0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>37485</th>
      <td>3.0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>76012</th>
      <td>1.0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>49608</th>
      <td>1.0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>





    0    70552
    1     8718
    Name: bad_health, dtype: int64



## Missing Values

***Relevant Sections:*** *2.2.1 (Data Consistency), 2.2.7 (Missing Data)*

There are at least three different ways missing data and unknown information are represented in this dataset.

Look at one row of the data. What value does Pandas use to represent missing data? How many missing values are there in the row you picked?


```python
df.iloc[0].values
# missing values represented by "nan"
```




    array([2, 1, 4.0, 0.0, 4.0, 4.0, nan, nan, nan, nan, nan, 1, 1, 4, nan, 5,
           2.0, 6, nan, 2.0, nan, 2, nan, nan, nan, nan, nan, nan, nan, nan,
           nan, nan, nan, nan, nan, 1.0, 2.0, nan, 4.0, 3.0, 1.0, 2.0, 2.0,
           2.0, 2.0, 1.0, 4.0, nan, nan, nan, nan, nan, nan, 2.0, nan, nan,
           nan, nan, nan, nan, nan, nan, nan, nan, nan, 7.0, 6.0, 8.0, 7.0,
           nan, nan, 6.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan,
           nan, nan, nan, nan, nan, nan, nan, nan, 6.0, 2.0, 2.0, 2.0, 2.0,
           2.0, 2.0, nan, 7.0, 6.0, 7.0, 8.0, 8.0, nan, nan, nan, nan, nan,
           nan, nan, nan, nan, nan, 2.0, nan, nan, 2.0, 3.0, 1.0, 2.0, 4.0,
           nan, 3.5, nan, nan, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0,
           nan, nan, nan, nan, 0.0, 2.0, nan, nan, nan, 3.0, 9.0, nan, 9.0,
           7.0, 8.0, 10.0, 10.0, nan, 7.0, 3.0, 2.0, 2.0, 1.0, 2.0, nan, nan,
           nan, 80.0, 3.6421, 1.80451061034635, 1.80982660081538, nan, nan,
           nan, nan, nan, nan, nan, nan, nan, nan, nan, 2.0, 5.0, 2.0, nan,
           nan, nan, nan, nan, nan, nan, nan, nan, 3.0, nan, nan, nan, nan,
           nan, nan, 'https://www.iso.org/obp/ui/#iso:code:3166:AT', 1,
           'https://api.ukdataservice.ac.uk/V1/datasets/eqls/rows/1',
           'AT9000083', 0], dtype=object)




```python
df.iloc[0].isna().sum()
# no. of missing values in this row
```




    113



Looking at the possible values for each column in the dataset documentation, find two different columns and at least two different values that are also used to represent missing or unknown information.

**Answer:** Examples include:
- `education_3_groups` (`Y11_Education` before renaming)
   - 5 = "Don't know", 6 = "Refused to Answer".
   - 4 = "Educated abroad": Could also be considered missing (as we don't know whether it was primary/secondary/tertiary education)

- `direct_contact_with_children` (`Y11_Q33a` before renaming)
   - 6 = "NA"

For the columns you picked:
- How many missing values does Pandas say the column has?
- How many values match the numeric representation of missing data you found from the documentation (e.g., if the documentation says -99 means unknown, how many -99 values are there in the column)?
- Does Pandas include the numeric representation in its count of missing values?


```python
column = "education_3_groups"
print(column, ":", df[column].isna().sum(), "Pandas missing values")
print(column, ":", (df[column] > 3).sum(), "Numeric representation of missing values\n")

column = "direct_contact_with_children"
print(column, ":", df[column].isna().sum(), "Pandas missing values")
print(column, ":", (df[column] == 6).sum(), "Numeric representation of missing values")

# In both cases Pandas does NOT know to include the numeric values in its count of missing data
```

    education_3_groups : 623 Pandas missing values
    education_3_groups : 276 Numeric representation of missing values

    direct_contact_with_children : 47519 Pandas missing values
    direct_contact_with_children : 6860 Numeric representation of missing values


Replace the numbers representing missing values in the columns you picked with the `NaN` type from `numpy`. What is the Pandas count of missing values now?


```python
import numpy as np

column = "education_3_groups"
df[column] = df[column].replace([4,5,6], np.nan)
print(column, ":", df[column].isna().sum(), "Pandas missing values")

column = "direct_contact_with_children"
df[column] = df[column].replace(6, np.nan)
print(column, ":", df[column].isna().sum(), "Pandas missing values")

```

    education_3_groups : 899 Pandas missing values
    direct_contact_with_children : 54379 Pandas missing values


Are there different types of missing data in the dataset (different reasons values can be unknown)? Does this have any implications for the way you would analyse the data?

**Answer:** Yes, as described above in the `education_3_groups` values could be unknown becuase they're missing, the person refused to anwer, or the person was educated abroad. Being educated abroad, for example, is quite a different reason for not knowing what level of education they received (and perhaps could be correlated with having more opportunities or wealth).

## 2007 vs 2011

***Relevant Sections:*** *2.2.1 (Data Consistency), 2.2.7 (Missing Data)*

- Which column should be used to distinguish between the collection years? (2007 and 2011)
- How many rows do we have for each year?
- For each collection year, what % of null values do we have for each column?
    - Why is this?
    - Display these %s in descending  order sorted by: 2007 then 2011


```python
# Column to use is "eqls_wave"
# 2 is 2007, and 3 is 2011
df["eqls_wave"].value_counts()
```




    3    43636
    2    35634
    Name: eqls_wave, dtype: int64




```python
missing = df.groupby("eqls_wave").apply(lambda g: g.isna().mean() * 100).round(3).transpose()
missing.sort_values(by=[2,3], ascending=False)
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
      <th>eqls_wave</th>
      <th>2</th>
      <th>3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>difficult_to_use_long_term_care_because_of_quality_of_care_</th>
      <td>100.0</td>
      <td>89.603</td>
    </tr>
    <tr>
      <th>difficult_to_use_long_term_care_because_of_cost_</th>
      <td>100.0</td>
      <td>89.534</td>
    </tr>
    <tr>
      <th>difficult_to_use_long_term_care_because_of_access_</th>
      <td>100.0</td>
      <td>89.495</td>
    </tr>
    <tr>
      <th>difficult_to_use_long_term_care_because_of_availability_</th>
      <td>100.0</td>
      <td>89.433</td>
    </tr>
    <tr>
      <th>difficult_to_use_child_care_because_of_quality_of_care_</th>
      <td>100.0</td>
      <td>83.401</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>iso3166_country_url</th>
      <td>0.0</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>rowid_for_the_uk_data_service_public_api</th>
      <td>0.0</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>root_uri_for_a_row_respondent_that_displays_all_data_values_for_a_single_row_via_the_uk_data_service_public_api</th>
      <td>0.0</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>unique_respondent_id</th>
      <td>0.0</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>bad_health</th>
      <td>0.0</td>
      <td>0.000</td>
    </tr>
  </tbody>
</table>
<p>200 rows × 2 columns</p>
</div>



Why? In `UKDA-7724-csv/mrdoc/excel/eqls_concordance_grid.xlsx` we can see some variables not collected for given year.

## UK vs Spain

Further to the missing data we saw above, grouped by wave/year, how do missing values look for each country of collection?

Compare the UK with Spain:
- are there columns that have all values for one country but some are missing for the other?
- are there columns that don't have any values for one country but at least some are present for the other?

What implications are there from your answers to the above questions?

For simplicity, just look at 2011 data.


```python
# Select 2011 data
df_2011 = df[df["eqls_wave"] == 3]
```


```python
# Some code for parsing the data in mrdoc/excel/eqls_concordance_grid.xlsx"
# E.g. country data is categorically encoded in our DataFrame but not human readable
# We can get the human readable categories from this file


# load the categorical value data from excel workbook, specifying the appropriate sheet
cat_vals_df = pd.read_excel(CATEGORICAL_VALUES_XLSX_PATH, sheet_name=CATEGORICAL_VALUES_XLSX_SHEET_NAME)

# display head
cat_vals_df.head()
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
      <th>Variable name</th>
      <th>Variable label</th>
      <th>Variable question text</th>
      <th>Topic Classifications</th>
      <th>Keywords</th>
      <th>Variable Groups</th>
      <th>Values if present - 2007</th>
      <th>Values if present - 2011</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Wave</td>
      <td>EQLS Wave</td>
      <td>EQLS Wave</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Administrative Variables</td>
      <td>2 = 2007\n3 = 2011</td>
      <td>2 = 2007\n3 = 2011</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Y11_Country</td>
      <td>Country</td>
      <td>Country</td>
      <td>Geographies</td>
      <td>NaN</td>
      <td>Household Grid and Country</td>
      <td>1 = Austria\n2 = Belgium\n3 = Bulgaria\n4 = Cy...</td>
      <td>1 = Austria\n2 = Belgium\n3 = Bulgaria\n4 = Cy...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Y11_Q31</td>
      <td>Marital status</td>
      <td>Marital status</td>
      <td>Social stratification and groupings - Family l...</td>
      <td>Marital status</td>
      <td>Family and Social Life</td>
      <td>1 = Married or living with partner\n2 = Separa...</td>
      <td>1 = Married or living with partner\n2 = Separa...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Y11_Q32</td>
      <td>No. of children</td>
      <td>Number of children of your own</td>
      <td>Social stratification and groupings - Family l...</td>
      <td>Children</td>
      <td>Family and Social Life</td>
      <td>5 = 5 or more children</td>
      <td>5 = 5 or more children</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Y11_ISCEDsimple</td>
      <td>Education completed</td>
      <td>Highest level of education completed</td>
      <td>Education - Higher and further</td>
      <td>Education levels</td>
      <td>Education</td>
      <td>1 = No education completed (ISCED 0)\n2 = Prim...</td>
      <td>1 = No education completed (ISCED 0)\n2 = Prim...</td>
    </tr>
  </tbody>
</table>
</div>



You can write your own function to extract the data you need from the `cat_vals_df` dataframe, input it manually, or use our prewritten function


```python
country_mapping_2011 = parse_country_values_2011(categorical_values_df=cat_vals_df)

# display
country_mapping_2011
```




    {1: 'Austria',
     2: 'Belgium',
     3: 'Bulgaria',
     4: 'Cyprus',
     5: 'Czech Republic',
     6: 'Germany',
     7: 'Denmark',
     8: 'Estonia',
     9: 'Greece',
     10: 'Spain',
     11: 'Finland',
     12: 'France',
     13: 'Hungary',
     14: 'Ireland',
     15: 'Italy',
     16: 'Lithuania',
     17: 'Luxembourg',
     18: 'Latvia',
     19: 'Malta',
     20: 'Netherlands',
     21: 'Poland',
     22: 'Portugal',
     23: 'Romania',
     24: 'Sweden',
     25: 'Slovenia',
     26: 'Slovakia',
     27: 'UK',
     28: 'Turkey',
     29: 'Croatia',
     30: 'Macedonia (FYROM)',
     31: 'Kosovo',
     32: 'Serbia',
     33: 'Montenegro',
     34: 'Iceland',
     35: 'Norway'}




```python
# add country_human column with mapped value
df_2011["country_human"] = df_2011["country"].map(country_mapping_2011) # ignore set with copy warning

# % missing values in each column for each country
by_country = df_2011.groupby("country_human").apply(lambda g: g.isna().mean() * 100).round(3).transpose()

# extract UK and Spain
uk_vs_spain = by_country[["UK", "Spain"]]
```

    /var/folders/xv/d5nvn2ps5r3fcf276w707n01qdmpqf/T/ipykernel_77880/1548146086.py:2: SettingWithCopyWarning:
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead

    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      df_2011["country_human"] = df_2011["country"].map(country_mapping_2011) # ignore set with copy warning



```python
# one 0% NA but not the other
uk_vs_spain[(uk_vs_spain == 0.0).apply(sum, axis=1) == 1]
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
      <th>country_human</th>
      <th>UK</th>
      <th>Spain</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>rural_urban_living</th>
      <td>0.577</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>dv_rural_urban_living</th>
      <td>0.577</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>degree_of_urbanisation</th>
      <td>5.595</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>health_condition</th>
      <td>0.044</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>how_frequently_take_part_in_sports_or_exercise_</th>
      <td>0.089</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>how_frequently_participate_in_social_activities_</th>
      <td>0.089</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>how_often_worked_unpaid_for_community_services_last_12_months_</th>
      <td>0.000</td>
      <td>0.794</td>
    </tr>
    <tr>
      <th>how_often_worked_unpaid_for_education_cultural_etc_organisation_last_12_months_</th>
      <td>0.000</td>
      <td>0.794</td>
    </tr>
    <tr>
      <th>how_satisfied_with_present_standard_of_living_</th>
      <td>0.044</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>how_satisfied_with_accommodation_</th>
      <td>0.044</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>how_satisfied_with_family_life_</th>
      <td>0.755</td>
      <td>0.000</td>
    </tr>
  </tbody>
</table>
</div>



## Your Turn!

We now leave it to you to learn something interesting from the dataset, using any of the techniques we've learned. You could attempt to explore questions like the ones below, for example, but pick anything that appeals to you. Always take care to consider whether the values you've calculated are likely to be representative.

- Which age group is most optimistic about the future?
- Which country has the most trust in the police? And the least?
- Are there differences between genders for the highest level of education completed? Does this vary by country and/or age group?

If you prefer, you could also do this with one of the example datasets we used during teaching:
- World Bank percentage of people living in urban environments (Section 2.1.4 Data Sources and Formats)
- Palmer Penguins dataset (Section 2.2.1 Data Consistency)
- Anthropometric Survey of US Army Personnel (Section 2.2.3 Feature Engineering)
- New York Patient Characteristics Survey (Section 2.2.4.3 Categorical Data)

These datasets are stored in the `coursebook/modules/m2/data` directory, but you may prefer to download the original versions as we made modifications for teaching.


```python
# Which age group is most optimistic about the future?

df.groupby("age")["i_am_optimistic_about_the_future"].mean()
# younger people seem to be more optimistic on average
```




    age
    1    2.163824
    2    2.346278
    3    2.548597
    4    2.679574
    5    2.752320
    Name: i_am_optimistic_about_the_future, dtype: float64




```python
# Which country has the most trust in the police? And the least?

df_2011.groupby("country_human")["how_much_trust_the_police_"].mean().sort_values()
# Bulgaria have the least trust, Finland the most

# Caveat for all of this: ~1000 respondents per country (and check user guide for details on data collection)!
```




    country_human
    Bulgaria             4.168737
    Serbia               4.331643
    Montenegro           4.531773
    Romania              4.583611
    Macedonia (FYROM)    4.660144
    Croatia              4.662614
    Slovakia             4.718782
    Cyprus               4.771574
    Greece               4.876754
    Latvia               4.958420
    Slovenia             4.971660
    Hungary              5.078764
    Czech Republic       5.098802
    Poland               5.243012
    Lithuania            5.260073
    Kosovo               5.314096
    Portugal             5.587649
    Italy                5.750224
    France               5.783880
    Belgium              5.892430
    Spain                6.129593
    Malta                6.338809
    Estonia              6.411224
    Netherlands          6.498004
    UK                   6.529096
    Luxembourg           6.575605
    Ireland              6.644359
    Turkey               6.708880
    Sweden               6.716000
    Germany              6.842923
    Austria              6.927734
    Denmark              7.830059
    Iceland              7.952953
    Finland              8.138643
    Name: how_much_trust_the_police_, dtype: float64




```python
# Are there differences between genders for the highest level of education completed? Does this vary
# by country and/or age group?

df.groupby("gender")["education_completed"].mean()
# Males seem to reach (are given the opportunity to reach) a slightly higher education level
# on average, but we'd need to check the significance of this.
```




    gender
    1    4.106716
    2    3.952754
    Name: education_completed, dtype: float64




```python
edu_age_m = df[df["gender"] == 1].groupby("age")["education_completed"].mean()
edu_age_f = df[df["gender"] == 2].groupby("age")["education_completed"].mean()

edu_age_m - edu_age_f
# The difference appears to be larger in older people and disappears (maybe even reverts)
# in younger people.
```




    age
    1   -0.049220
    2   -0.007889
    3    0.043056
    4    0.145832
    5    0.453163
    Name: education_completed, dtype: float64




```python
edu_cntry_m = df_2011[df_2011["gender"] == 1].groupby("country_human")["education_completed"].mean()
edu_cntry_f = df_2011[df_2011["gender"] == 2].groupby("country_human")["education_completed"].mean()

(edu_cntry_m - edu_cntry_f).sort_values()
# Ireland, Estonia, Latvia : Top 3 countries with higher female education than male
# Turkey, Romania, Malta : Top 3 countries with  higher male education than female
```




    country_human
    Ireland             -0.375420
    Estonia             -0.181662
    Latvia              -0.171925
    Finland             -0.126074
    Lithuania           -0.087181
    Bulgaria            -0.032975
    Iceland             -0.017156
    Slovenia             0.004494
    Hungary              0.026447
    Denmark              0.030770
    Sweden               0.047772
    France               0.060102
    Austria              0.072093
    Italy                0.097751
    Portugal             0.098896
    Poland               0.107906
    Cyprus               0.113697
    UK                   0.127559
    Czech Republic       0.131751
    Montenegro           0.138855
    Belgium              0.150959
    Serbia               0.166398
    Spain                0.185198
    Macedonia (FYROM)    0.185369
    Netherlands          0.187195
    Slovakia             0.194347
    Croatia              0.258897
    Greece               0.294329
    Germany              0.297801
    Kosovo               0.333768
    Luxembourg           0.385009
    Malta                0.387355
    Romania              0.486371
    Turkey               0.562414
    Name: education_completed, dtype: float64



**CAVEAT!** The dataset includes weighting factors that should be used when computing some stats and comparing countries. We've simplified and not included that here. See the user guide for details if needed.
