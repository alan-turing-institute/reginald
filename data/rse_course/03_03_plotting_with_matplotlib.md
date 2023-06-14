# 3.3 Plotting with Matplotlib

*Estimated time to complete this notebook: 25 minutes*

## 3.3.1 Importing Matplotlib

We import the `pyplot` object from Matplotlib, which provides us with an interface for making figures.
We usually abbreviate it.


```python
from matplotlib import pyplot as plt
```

## 3.3.2 Notebook magics

When we write:


```python
%matplotlib inline
```

We tell the Jupyter notebook to show figures we generate alongside the code that created it, rather than in a separate window.
Lines beginning with a single percent are not python code: they control how the notebook deals with python code.

Lines beginning with two percent signs are "cell magics", that tell Jupyter notebook how to interpret the particular cell;
we've seen `%%writefile` and `%%bash` for example.

## 3.3.3 A basic plot

When we write:


```python
from math import cos, pi, sin

myfig = plt.plot([sin(pi * x / 100.0) for x in range(100)])
```


    
![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module03_research_data_in_python/03_03_plotting_with_matplotlib_12_0.png)
    


The plot command *returns* a figure, just like the return value of any function.
The notebook then displays this.

To add a title, axis labels etc, we need to get that figure object, and manipulate it.
For convenience, matplotlib allows us to do this just by issuing commands to change the "current figure":


```python
plt.plot([sin(pi * x / 100.0) for x in range(100)])
plt.title("Hello")
```




    Text(0.5, 1.0, 'Hello')




    
![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module03_research_data_in_python/03_03_plotting_with_matplotlib_15_1.png)
    


But this requires us to keep all our commands together in a single cell, and makes use of a "global" single "current plot", which, while convenient for quick exploratory sketches, is a bit cumbersome.
If we want to produce publication-quality plots from our notebook, `matplotlib`, defines some types we can use to treat individual figures as variables, and manipulate these.

## 3.3.4 Figures and Axes

We often want multiple graphs in a single figure (e.g. for figures which display a matrix of graphs of different variables for comparison).

So Matplotlib divides a `figure` object up into axes: each pair of axes is one 'subplot'.
To make a boring figure with just one pair of axes, however, we can just ask for a default new figure, with
brand new axes.
The relevant function returns a (figure, axis) pair, which we can deal out with parallel assignment.


```python
sine_graph, sine_graph_axes = plt.subplots()
```


    
![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module03_research_data_in_python/03_03_plotting_with_matplotlib_20_0.png)
    


Once we have some axes, we can plot a graph on them:


```python
sine_graph_axes.plot([sin(pi * x / 100.0) for x in range(100)], label="sin(x)")
```




    [<matplotlib.lines.Line2D at 0x7fb1700bfe50>]



We can add a title to a pair of axes:


```python
sine_graph_axes.set_title("My graph")
```




    Text(0.5, 1.0, 'My graph')




```python
sine_graph_axes.set_ylabel("f(x)")
```




    Text(3.200000000000003, 0.5, 'f(x)')




```python
sine_graph_axes.set_xlabel("100 x")
```




    Text(0.5, 3.1999999999999993, '100 x')



Now we need to actually display the figure.
As always with the notebook, if we make a variable be returned by the last line of a code cell, it gets displayed:


```python
sine_graph
```




    
![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module03_research_data_in_python/03_03_plotting_with_matplotlib_28_0.png)
    



We can add another curve:


```python
sine_graph_axes.plot([cos(pi * x / 100.0) for x in range(100)], label="cos(x)")
```




    [<matplotlib.lines.Line2D at 0x7fb1700de760>]




```python
sine_graph
```




    
![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module03_research_data_in_python/03_03_plotting_with_matplotlib_31_0.png)
    



A legend will help us distinguish the curves:


```python
sine_graph_axes.legend()
```




    <matplotlib.legend.Legend at 0x7fb1700de070>




```python
sine_graph
```




    
![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module03_research_data_in_python/03_03_plotting_with_matplotlib_34_0.png)
    



## 3.3.5 Saving figures

We must be able to save figures to disk, in order to use them in papers.
This is really easy:


```python
sine_graph.savefig("my_graph.png")
```

In order to be able to check that it worked, we need to know how to display an arbitrary image in the notebook.

The programmatic way is like this:


```python
# Use the notebook's own library for manipulating itself.
from IPython.display import Image

Image(filename="my_graph.png")
```




    
![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module03_research_data_in_python/03_03_plotting_with_matplotlib_40_0.png)
    



## 3.3.6 Subplots

We might have wanted the $\sin$ and $\cos$ graphs on separate axes:


```python
double_graph = plt.figure()
```


    <Figure size 432x288 with 0 Axes>



```python
sin_axes = double_graph.add_subplot(2, 1, 1)  # 2 rows, 1 column, 1st subplot
```


```python
cos_axes = double_graph.add_subplot(2, 1, 2)
```


```python
double_graph
```




    
![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module03_research_data_in_python/03_03_plotting_with_matplotlib_46_0.png)
    




```python
sin_axes.plot([sin(pi * x / 100.0) for x in range(100)])
```




    [<matplotlib.lines.Line2D at 0x7fb1701709d0>]




```python
sin_axes.set_ylabel("sin(x)")
```




    Text(3.200000000000003, 0.5, 'sin(x)')




```python
cos_axes.plot([cos(pi * x / 100.0) for x in range(100)])
```




    [<matplotlib.lines.Line2D at 0x7fb1700bf0d0>]




```python
cos_axes.set_ylabel("cos(x)")
```




    Text(3.200000000000003, 0.5, 'cos(x)')




```python
cos_axes.set_xlabel("100 x")
```




    Text(0.5, 3.200000000000003, '100 x')




```python
double_graph
```




    
![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module03_research_data_in_python/03_03_plotting_with_matplotlib_52_0.png)
    



## 3.3.7 Versus plots

When we specify a single `list` to `plot`, the x-values are just the array index number.
We usually want to plot something more meaningful:


```python
double_graph = plt.figure()
sin_axes = double_graph.add_subplot(2, 1, 1)
cos_axes = double_graph.add_subplot(2, 1, 2)
cos_axes.set_ylabel("cos(x)")
sin_axes.set_ylabel("sin(x)")
cos_axes.set_xlabel("x")
```




    Text(0.5, 0, 'x')




    
![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module03_research_data_in_python/03_03_plotting_with_matplotlib_55_1.png)
    



```python
sin_axes.plot(
    [x / 100.0 for x in range(100)], [sin(pi * x / 100.0) for x in range(100)]
)
cos_axes.plot(
    [x / 100.0 for x in range(100)], [cos(pi * x / 100.0) for x in range(100)]
)
```




    [<matplotlib.lines.Line2D at 0x7fb18054d100>]




```python
double_graph
```




    
![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module03_research_data_in_python/03_03_plotting_with_matplotlib_57_0.png)
    



## 3.3.8 Sunspot Data

We can incorporate what we have learned in the sunspots example to produce graphs of the data.


```python
import pandas as pd

df = pd.read_csv(
    "http://www.sidc.be/silso/INFO/snmtotcsv.php",
    sep=";",
    header=None,
    names=["year", "month", "date", "mean", "deviation", "observations", "definitive"],
)
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



We can plot all the data in the dataframe separately, but that isn't always useful!


```python
df.plot(subplots=True)
```


    
![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module03_research_data_in_python/03_03_plotting_with_matplotlib_62_0.png)
    


Let's produce some more meaningful and useful visualisations by accessing the dataframe directly.

We start by discarding any rows with an invalid (negative) standard deviation.


```python
df = df[df["deviation"] > 0]
```

Next we use the dataframe to construct some useful lists.


```python
deviation = df["deviation"].tolist()  # Get the dataframe column (series) as a list
observations = df["observations"].tolist()
mean = df["mean"].tolist()
date = df["date"].tolist()
```


```python
fig = plt.figure(
    figsize=(15, 10)
)  # Set the width of the figure to be 15 inches, and the height to be 5 inches

ax1 = fig.add_subplot(2, 2, 1)  # 2 rows, 2 columns, 1st subplot
ax1.errorbar(
    df["date"],  # Date on the x axis
    df["mean"],  # Mean on the y axis
    yerr=df["deviation"],  # Use the deviation for the error bars
    color="orange",  # Plot the sunspot (mean) data in orange
    ecolor="black",
)  # Show the error bars in black
ax1.set_xlabel("Date")
ax1.set_ylabel("Mean")
ax1.set_title("From Dataframe")

ax2 = fig.add_subplot(2, 2, 2)  # 2 rows, 2 columns, 2nd subplot
ax2.scatter(df["date"], df["observations"], color="grey", marker="+")
ax2.set_xlabel("Date")
ax2.set_ylabel("Number of Observations")
ax2.set_title("From Dataframe")

ax3 = fig.add_subplot(2, 2, 3)  # 2 rows, 2 columns, 3rd subplot
ax3.errorbar(date, mean, yerr=deviation, color="pink", ecolor="black")
ax3.set_xlabel("Date")
ax3.set_ylabel("Mean")
ax3.set_title("From List")

ax4 = fig.add_subplot(2, 2, 4)  # 2 rows, 2 columns, 4th subplot
ax4.scatter(date, observations, color="red", marker="o")
ax4.set_xlabel("Date")
ax4.set_ylabel("Number of Observations")
ax4.set_title("From List")
```




    Text(0.5, 1.0, 'From List')




    
![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module03_research_data_in_python/03_03_plotting_with_matplotlib_67_1.png)
    


In this example we are plotting columns from the `pandas` `DataFrame` (series), and from lists to show this method works for both.
`numpy` arrays can also be used.

## 3.3.9 Learning More

There's so much more to learn about `matplotlib`: pie charts, bar charts, heat maps, 3-d plotting, animated plots, and so on.
You can learn all this via the [Matplotlib Website](https://matplotlib.org/stable/).
You should try to get comfortable with all this, so please use some time in class, or at home, to work your way through a bunch of the [examples](https://matplotlib.org/stable/gallery/index.html).
