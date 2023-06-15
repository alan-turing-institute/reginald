# Module 2: Hands-on session

In this hands-on notebook we'll be getting familiar with working with the [European Quality of Life data](https://beta.ukdataservice.ac.uk/datacatalogue/studies/study?id=7724#!/access-data) in pandas by:

- Creating a Local Python Environment
- Downloading the data
- Loading and exploring the data
- Understanding the different data types present
- Making the data more readable
- Considering how missing data is represented
- Exploring some differences between the 2007 and 2011 data
- Comparing data from UK and Spain respondees with respect to data missingness

We have marked the exercise parts of this notebook as `# TODO` with some comments as guidance. You can refer back to the taught material, or external documentation, for further information.

## Running the notebook

### Prerequisites

To setup and run the commands in this notebook you will need a (preferably bash/similar) shell with these installed:
- Python 3.7 or later
   - Check by running `python --version` or `python3 --version` in your shell
- Git (optional)
   - Check by running `git --version` in your shell
- Curl (optional)
   - Check by running `curl --version` in your shell

If you don't have these we have instructions in our [Research Software Engineering course](https://alan-turing-institute.github.io/rse-course/html/course_prerequisites/index.html).

### Clone the Course Repository

In order to work locally with this notebook, you should clone the course repository.

1. Go to the GitHub repository in a web browser: https://github.com/alan-turing-institute/rds-course
2. Click on the green "Code" button and copy the address under "Clone - HTTPS".
3. In your shell, run the following command from a sensible location (this will create a new dir for the course in current dir):
   ```bash
   git clone https://github.com/alan-turing-institute/rds-course.git
   ```
4. Change directory to the repository root
   ```bash
   cd rds-course
   ```
5. We're currently using the `develop` branch, so check that out
   ```bash
   git checkout develop
   ```

**Troubleshooting:**

- **If you don't have `git`:** We recommend using git, but if you don't have it installed you can download a zip of the code by clicking on "Download Zip" in step 2 above instead, and unpack it locally.
- **If you previously cloned/downloaded the repo:** Please run `git checkout develop` and then `git pull` from the `rds-course` directory to ensure you have the latest version of the material.

### Create a Local Python Environment

We need to install third-party packages necessary for the course, with the same package versions as it was developed with to ensure compatibility and reproducibility.

### Managing Python Versions

As well as the versions of packages your codebase should specify which version(s) of Python itself that it's compatible with. The code for this course should run with Python 3.7 or above. We don't cover it here to speedup setup, but if you need to use multiple versions of Python on your system we recommend [Pyenv](https://github.com/pyenv/pyenv) and [Conda](https://conda.io/projects/conda/en/latest/index.html#).

### Creating a Virtual Environment with `Poetry`

The Python ecosystem has many different ways of managing packaging and installing dependencies ([this page](https://packaging.python.org/key_projects/#pipenv) lists somem). The most well-known is `pip` with dependencies listed in a `requirements.txt` file.

In this course we use the tool [Poetry](https://python-poetry.org/), which can help manage [multiple environments](https://python-poetry.org/docs/managing-environments/), in particular [switching between environments ](https://python-poetry.org/docs/managing-environments/#switching-between-environments).

Dependencies are listed in `pyproject.toml` and have versions fixed in `poetry.lock`. `Poetry` will pick these files up and install the required packages in a predictable manner, and into a virtual environment isolated from other projects on your system.



1. Install `Poetry` by following their instructions [here](https://python-poetry.org/docs/#installation).

2. Change to the `rds-course` directory (the directory of the git repository cloned above), if you're  not there already:
   cd /path/to/rds-course

3. Set the relevant Python executable for Poetry to use:
   - If `python --version` returns a version number of 3.7 or above:
      - Skip to step 4
   - If `python --version` is less than 3.7 (e.g., 2.7), but `python3 --version` gives 3.7 or above:
      - Run `poetry env use python3`
   - If you have a Python 3.7+ environment available somewhere else:
      -  Run `poetry env use /full/path/to/python`
   - If you don't have Python 3.7+ installed or don't know where to find it:
      - Refer back to the instructions in the prerequisites and/or ask for help.

4. Run the following command to create the virtual environment and install the third-party packages necessary for the course:
   ```bash
   poetry install
   ```

5. Check the details of the virtual environment that's been created:
   ```bash
   poetry env info
   ```

6. Initialise the environment:
   ```bash
   poetry shell
   ```

The last step creates a new shell setup to use the Python virtual environment we just created (e.g., `which python`, should now show the path returned earlier by `poetry env info` above, rather the path to your global Python executable). If you want to stop using the virtual environment `exit` the shell.

**Troubleshooting:**

- **If you don't have `curl`**:
   - `curl` is used to download a Python script (currently [this script](https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py) but check the [Poetry documentation](https://python-poetry.org/docs/#installation) for the latest URL). Save this script as `get-poetry.py` and then run `python get-poetry.py` to install Poetry.
- **If you don't want to use `Poetry`**:
   - You can install the course dependencies by running `pip install .` from the `rds-course` directory, but we recommend doing this in an alternative virtual environment of your choice (not in your global Python installation).

### Jupyter

We recommend use of [JupyterLab](https://jupyter.org/) for running through the hands-on notebooks in this course.

JuypyterLab was installed into your Poetry environment in the previous step. We can launch a local instance, from the poetry environment terminal, with:

```bash
jupyter lab # from the root of the cloned github repository! "rds-course" directory
```

We recommend following the rest of the notebook via the JupyterLab instance that should spawn!

Click through the file explorer in the left-hand pane to bring up this notebook.

The notebook should be present at: `rds-course/coursebook/modules/m2/2-hands-on.ipynb`

If you've not used `Jupyter` before you might find their [Notebook basics](https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Notebook%20Basics.html) and [Running code](https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Running%20Code.html) documentation helpful.

## Download Data

1. As described in module 1, we can find the data available for download from the UK Data Service [here](https://beta.ukdataservice.ac.uk/datacatalogue/studies/study?id=7724#!/access-data)
2. Observe the licence and take this opportunity to check your obligations
3. Download the CSV data
4. Unzip the data to `$PROJECT_ROOT/data` this should give us `$PROJECT_ROOT/data/UKDA-7724-csv`

`$PROJECT_ROOT` is the root of the cloned github repository for this course. If you change the directory that you hold this data in, you'll need to make appropriate changes to the `DATA_ROOT_PATH` variable below.

## Notebook Setup

Import necessary packages for this work:


```python
import os

import pandas as pd

# these are utility functions to check some answers in the notebook
from handson_utils import (
    parse_country_values_2011,
    check_dataset_load,
    check_dataset_explored,
    check_column_mapping,
    set_column_mapping
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



```python
# TODO
```

## Pandas Help

You'll be using pandas for most of the hands-on session. In each question there's a list of sections from the teaching material that may give you hints for how to approach them.

You might also like to refer to the Pandas documentation:

- [User Guide](https://pandas.pydata.org/docs/user_guide)
- [Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
- [API Reference](https://pandas.pydata.org/docs/reference)

Or you can get a function's documentation in the notebook by:

- Hitting SHIFT + TAB in a code cell with your text cursor on a function name.
- Running `help(<function_name>)` in a code cell (e.g. `help(pd.read_csv)`


## Load and Explore

***Relevant sections:*** *2.1.4 (Data Sources and Formats), 2.2.1 (Data Consistency)*

Read the combined 2007 and 2011 data into a pandas `DataFrame`


```python
# TODO read in the file and display the head

# your code here
df = None
```


```python
# checks - will produce an `AssertionError` until DataFrame loaded correctly
check_dataset_load(df)
```

Take a look at some summary statistics and use these to assign the variables below correctly.

You can assign the variables manually from inspecting printed output or assign them results from methods/properties.


```python
# TODO - code to explore dataframe can go here

```


```python
# TODO - fill in the below with the correct values
n_columns = 0 # how many columns are there in the DataFrame? Does this match number of variables you expected?
n_float64_columns = 0 # how many columns are of dtype float64?
Y11_Q31_mean_value = 0 #  what is the mean of the values in the Y11_Q31 column?
Y11_Country_n_unique = 0 # how many unique values in the Y11_Country column?


# function to check your answers (run this cell)
check_dataset_explored(
    n_columns,
    n_float64_columns,
    Y11_Q31_mean_value,
    Y11_Country_n_unique
)
```

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


```python
# TODO
```

For one example of each type, what are the possible values the data can take, according to the documentation? What does each value mean? Is each possible value present in the dataset?


```python
# TODO
```

What is the minimum, maximum and mean value in each of your example columns? Taking into consideration the type of data in the column, are all of these values meaningful?


```python
# TODO
```

For one of the categorical columns, replace the numerical encodings with their actual meaning (category title). You can do this by manually creating a Python dictionary with the values to replace (we'll look at extracting them with code later). What is the most common value?


```python
# TODO
```

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

⚠️ **Note:** ⚠️ This is a reasonably tricky regex question. If you prefer to move on to the following questions there is a code cell you can run below to set the updated column names.


```python
# TODO
column_mapping = {}


# TODO
# Apply your column mapping to df

```


```python
# check your answer
check_column_mapping(column_mapping, df)
```

If you would like to skip this question, uncomment the code and run this cell:


```python
### THIS CODE MODIFIES df TO THE EXPECTED RESULT AFTER THE MAKING THINGS MORE READABLE EXERCISE

# !!! uncomment the line below and run the cell to set the answer !!!
# df = set_column_mapping(df, eqls_api_map_df)

df.head()
```

## Self-Reported Health

***Relevant Sections:*** *2.2.1 (Data Consistency), 2.2.3 (Feature Engineering), 2.2.4.3 (Categorical Data)*

The research question we defined in Module 1 and will explore in more detail in Modules 3 and 4 aims to explore the contribution of various factors on self-reported health.

Which column in the dataset contains self-reported health values? How many people had "Very good" self-reported health?


```python
# TODO
```

For the models we develop in Module 4 we'll convert self-reported health into a binary variable. What might be a sensible way to group the categories into only two possible values? Create a new column with your proposed binary encoding for self-reported health.


```python
# TODO
```

## Missing Values

***Relevant Sections:*** *2.2.1 (Data Consistency), 2.2.7 (Missing Data)*

There are at least three different ways missing data and unknown information are represented in this dataset.

Look at one row of the data. What value does Pandas use to represent missing data? How many missing values are there in the row you picked?


```python
# TODO
```

Looking at the possible values for each column in the dataset documentation, find two different columns and at least two different values that are also used to represent missing or unknown information.


```python
# TODO
```

For the columns you picked:
- How many missing values does Pandas say the column has?
- How many values match the numeric representation of missing data you found from the documentation (e.g., if the documentation says -99 means unknown, how many -99 values are there in the column)?
- Does Pandas include the numeric representation in its count of missing values?


```python
# TODO
```

Replace the numbers representing missing values in the columns you picked with the `NaN` type from `numpy`. What is the Pandas count of missing values now?


```python
# TODO
```

Are there different types of missing data in the dataset (different reasons values can be unknown)? Does this have any implications for the way you would analyse the data?


```python
# TODO
```

## 2007 vs 2011

***Relevant Sections:*** *2.2.1 (Data Consistency), 2.2.7 (Missing Data)*

- Which column should be used to distinguish between the collection years? (2007 and 2011)
- How many rows do we have for each year?
- For each collection year, what % of null values do we have for each column?
    - Why is this?
    - Display these %s in descending  order sorted by: 2007 then 2011


```python
# TODO
```

## UK vs Spain

Further to the missing data we saw above, grouped by wave/year, how do missing values look for each country of collection?

Compare the UK with Spain:
- are there columns that have all values for one country but some are missing for the other?
- are there columns that don't have any values for one country but at least some are present for the other?

What implications are there from your answers to the above questions?

For simplicity, just look at 2011 data.


```python
df_2011 = None # TODO
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

You can write your own function to extract the data you need from the `cat_vals_df` dataframe, input it manually, or use our prewritten function


```python
country_mapping_2011 = None # TODO


# uncomment beow if you want to use our pre-written function to parse the data for country mappings
#country_mapping_2011 = parse_country_values_2011(categorical_values_df=cat_vals_df)

# display
country_mapping_2011
```


```python
# TODO - Null values in UK vs Spain
```

## Your Turn!

We now leave it to you to learn something interesting from the dataset, using any of the techniques we've learned. You could attempt to explore questions like the ones below, for example, but pick anything that appeals to you. Always take care to consider whether the values you've calculated are likely to be representative.

- Which age group is most optimistic about the future?
- Which country has the most trust in the police? And the least?
- Are there differences between genders for the highest level of education completed? Does this vary by country and/or age group?

If you prefer, you could also do this with one of the example datasets we used during teaching:
- World Bank percentage of people living in urban environments ([Section 2.1.4 Data Sources and Formats](2-01-04-DataSourcesAndFormats))
- Palmer Penguins dataset ([Section 2.2.1 Data Consistency](2-02-01-DataConsistency))
- Anthropometric Survey of US Army Personnel ([Section 2.2.3 Feature Engineering](2-02-03-FeatureEngineering))
- New York Patient Characteristics Survey ([Section 2.2.4.3 Categorical Data](2-02-04-03-CategoricalData))

These datasets are stored in the `coursebook/modules/m2/data` directory, but you may prefer to download the original versions as we made modifications for teaching.


```python
# TODO
```
