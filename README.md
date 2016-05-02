

# Python 3.x notebooks about real-world data cleaning and visualization

A set of iPython notebooks on data wrangling and visualization for Stanford Computational Journalism, using the standard lib as well as pandas and matplotlib.

(in progress)


# Contents


## Data extraction

Recipes for extracting (but _not_ cleaning/wrangling) machine-readable data from raw sources.

The results can be found in the __extracted__ subdirectories in [data](data).

- [NASA plaintext data files](Data-Extraction--NASA-Text.ipynb)
- [California Dept. of Education Excel spreadsheets](Data-Extraction--CDE-XLS.ipynb) - extracting SAT scores and student poverty data from workbooks of various design.
- [California Dept. of Education fixed-width fields](Data-Extraction--CDE-API-fixed-width.ipynb) - scraping a HTML table to get the field-boundaries for the CDE's legacy data format for school performance.
- [Texas Dept. of Justice; Death row inmates - HTML scraping with lxml](Data-Extraction--Texas-Death-Row-Executions.ipynb)
- [Texas Dept. of Justice; Executions - HTML crawling with Beautiful Soup](Data-Extraction--Texas-Death-Row-Executions.ipynb) (in progress)

## Visualization

- [Visualizing the relationship between SAT performance and percentage of students eligible for free-or-reduced-price lunch](Visualization--School-Scores-and-Poverty.ipynb).




# Resources

## Matplotlib

- [Matplotlib homepage](http://matplotlib.org/)
  + [Examples index](http://matplotlib.org/examples/index.html)
- [How to make beautiful data visualizations in Python with matplotlib](http://www.randalolson.com/2014/06/28/how-to-make-beautiful-data-visualizations-in-python-with-matplotlib/)


## Pandas

- [10 Minutes to pandas](http://pandas.pydata.org/pandas-docs/stable/10min.html)
- [Pandas cookbook](http://pandas.pydata.org/pandas-docs/stable/cookbook.html#cookbook)
- [An Introduction to Pandas, via Michael Hansen](http://synesthesiam.com/posts/an-introduction-to-pandas.html)
- [12 Useful Pandas Techniques in Python for Data Manipulation](http://www.analyticsvidhya.com/blog/2016/01/12-pandas-techniques-python-data-manipulation/)
- [Things in Pandas I Wish I'd Known Earlier](http://nbviewer.jupyter.org/github/rasbt/python_reference/blob/master/tutorials/things_in_pandas.ipynb)
- [Useful Pandas Snippets gist cheatsheet](https://gist.github.com/bsweger/e5817488d161f37dcbd2)
- [Intro to pandas data structures](http://www.gregreda.com/2013/10/26/intro-to-pandas-data-structures/)
  - [Part 2: Working with DataFrames](http://www.gregreda.com/2013/10/26/working-with-pandas-dataframes/)
  - [Part 3: Using pandas with the MovieLens dataset](http://www.gregreda.com/2013/10/26/using-pandas-on-the-movielens-dataset/)
- [Quandl's Numpy/Scipy/Pandas cheat sheet](https://s3.amazonaws.com/quandl-static-content/Documents/Quandl+-+Pandas,+SciPy,+NumPy+Cheat+Sheet.pdf)
- [Dataconomy's 14 best Python Pandas features](http://dataconomy.com/14-best-python-pandas-features/)
- [Brandon Rhodes - Pandas From The Ground Up - PyCon 2015 (Video)](https://www.youtube.com/watch?v=5JnMutdy6Fw)
