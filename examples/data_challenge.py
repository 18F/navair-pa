"""
Requirements:
A virtualenv is highly recommended.

pip install xlrd
pip install pandas
pip install matplotlib
pip install scipy
pip install scikit-learn

Alterations to ei_file:
1. Removed extra rows above header
2. Removed "Duty Station" column, since it's all FRC SE
3. Removed "Duty Station Remarks" since there are none.
4. Assigned one retiree who was missing Years of Experience as "31+"
5. Dropped empty first row.

Other alterations are done from within pandas, outlined below.

I recommend opening a python shell and running each line of this individually
rather than running it as a script. I think it'll be much more meaningful like that.

"""

import pandas as pd
import numpy as np
import matplotlib
# this corrects for some weirdness in installed python versions, 
# matplotlib and a "not installed as a framework" error.
# This may not affect you, but if it does the command below resolves the backend.
# Note that it MUST be run before any further imports.
matplotlib.use('TkAgg')

# You may now continue importing
import matplotlib.pyplot as plt

# Open and read the excel file
ei_file = 'data_challenge/exit_interview_data.xlsx'
df = pd.read_excel(ei_file)

# df is the dataframe we'll be working with
# Does the dataframe look like the spreadsheet?
print(df.shape)    # output row and column numbers
print(df.describe) # output what the data (truncated) looks like

# Let's map experience ranges to numerics.
min_experience = {
    '0-5': 0, 
    '6-10': 6,
    '11-20': 11,
    '21-30': 21,
    '31+': 31,
    }
max_experience = {
    '0-5': 5, 
    '6-10': 10,
    '11-20': 20,
    '21-30': 30,
    '31+': 50,   # this may be an inaccurate assumption
}
# and add new columns for them.
df.insert(3, 'Min Years Experience', df['Years of NAVAIR experience'].map(min_experience))
df.insert(4, 'Max Years Experience', df['Years of NAVAIR experience'].map(max_experience))

# New columns can be confirmed with `df.columns`, by re-running print(df.shape)
# Or by selecting the subset of columns: `df.loc[ : , 'Years of NAVAIR experience':'Max Years Experience']`
# See https://medium.com/@msalmon00/helpful-python-code-snippets-for-data-exploration-in-pandas-b7c5aed5ecb9
# for lots of helpful pandas tips.

# Now that we've added those columns, let's play with those numbers a little...
# See https://pandas.pydata.org/pandas-docs/stable/api.html#api-dataframe-stats

df.loc[:,'Min Years Experience'].mean()
# 14.754639175257733
df.loc[:,'Min Years Experience'].median()
# 11.0
df.loc[:,'Min Years Experience'].std() #standard deviation
# 12.759035209083953

df.loc[:,'Max Years Experience'].mean()
# 25.20618556701031
df.loc[:,'Max Years Experience'].median()
# 20.0
df.loc[:,'Max Years Experience'].std()
#18.518439628862033


# In case we want to work with a subset of columns:
# subset = df.loc[ : , 'Years of NAVAIR experience':'Max Years Experience']

# PLOTTING
# for more on plotting in pandas, see 
# https://pandas.pydata.org/pandas-docs/stable/visualization.html
# and http://jonathansoma.com/lede/algorithms-2017/classes/fuzziness-matplotlib/understand-df-plot-in-pandas/

# Let's look at how years of experience relates to whether or not people would
# recommend NAVAIR as a good place to work with a scatter plot
df.plot(x='Min Years Experience', y="Recommend Employment at NAVAIR - 'Yes'", kind="scatter")
plt.show()

# we can also plot dropping into plt instead of from pandas
# plt.hist(df["Max Years Experience"])

# What about people who didn't retire
not_retired = df[df["Reason for Leaving - Retirement"] == 0] 
# Now who's likelier to recommend?
not_retired.plot(y='Max Years Experience', x="Recommend Employment at NAVAIR - 'Yes'", kind="hist")
plt.show()
# We see there's a valley. The retirees were likely to recommend, 
# and the people with relatively little experience are, 
# but people who have been there awhile and quit are less likely to.

# It would be *really* useful to have a granular "years of service" number
# rather than a range in order to drill into these sorts of correlations more.

# Let's roll it into scikit-learn and see what happens.
# See https://www.dataquest.io/blog/machine-learning-python/
# Because we added columns, make sure our indexes are ok.
df = df.reset_index()

# Get only the numeric columns from our dataframe. 
# We may need to convert more data to numeric values
# For example, we could index Race against a numeric value in order to chart or ML against it.
good_columns = df._get_numeric_data()
# There are 5 or 6 cells under "Years of NAVAIR experience" with "Choose One..." values
# which means our created columns have some NaN values where they couldn't map. 
# We're gonna drop those.
good_columns.dropna(inplace=True)

# Kmeans is interesting as a learning experiment, but did not immediately tease out useful info.
# from sklearn.cluster import KMeans

# Initialize the model with 2 parameters -- number of clusters and random state.
# kmeans_model = KMeans(n_clusters=4, random_state=1)
# kmeans_model.fit(good_columns) # Fit the model using the good columns.
# Get the cluster assignments.
# labels = kmeans_model.labels_

# From https://www.dataquest.io/blog/machine-learning-python/ and applicable here...
# Our data has many columns -- it's outside of the realm of human understanding and physics to be 
# able to visualize things in more than 3 dimensions. 
# So we'll have to reduce the dimensionality of our data, without losing too much information. 
# One way to do this is a technique called principal component analysis, or PCA. 
# PCA takes multiple columns, and turns them into fewer columns while trying to preserve the 
# unique information in each column. 
from sklearn.decomposition import PCA
# Create a PCA model.
pca_2 = PCA(2)
# Fit the PCA model on the numeric columns from earlier.
plot_columns = pca_2.fit_transform(good_columns)
# Make a scatter plot of each game, shaded according to cluster assignment.
plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=labels)
# This is not a particularly useful or interesting plot, so we'll skip showing it.
#plt.show()

# Let's look at correlations
# What columns correlate to a recommendation?
# note that the result of corr() is a pandas Series (not dataframe)
good_cols_correlation = good_columns.corr()["Recommend Employment at NAVAIR - 'Yes'"]
# let's see that correlation:
print(good_cols_correlation)

#let's sort that Series for better visibility
sorted_corr = good_cols_correlation.sort_values(ascending=False)
print(sorted_corr)

# What about in the larger data set?
df_correlation = df.corr()["Recommend Employment at NAVAIR - 'Yes'"]

# Let's take another look with reasons for leaving.
reasons = good_columns.ix[:, "Recommend NAVAIR Change - Increase Pay, Better Benefits":"Recommend NAVAIR Change - Allowed to work independently with little supervision"]
reasons.shape
reasons.describe
#drop the non-numerics:
reasons.dropna(inplace=True)

# create another axis to compare against reasons for leaving
y = good_columns.loc[:,'Min Years Experience']
y.dropna(inplace=True)

# Now, can we create a regression?
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
logreg.fit(reasons, y)

# logreg is now a training set. if we had a second set of data to test against, 
# we should be able to compare the two
# new_df = logreg.predict(test_df)

# skikit's "unsupervised learning" feels particularly useful for NAVAIR purposes. 
# It's a way to build machine learning and AI when one does not necessarily know which 
# inputs may be important. 
# http://scikit-learn.org/stable/unsupervised_learning.html

# Perform hierarchical clustering on reasons using the
# linkage() function with the method='complete' keyword argument.
from scipy.cluster.hierarchy import linkage, dendrogram
mergings = linkage(reasons, method='complete')

# Plot a dendrogram using the dendrogram() function on mergings,
# specifying the keyword arguments labels=varieties, leaf_rotation=90,
# and leaf_font_size=6.
dendrogram(mergings,
    leaf_rotation=90,
    leaf_font_size=6,
)
# that data set is too large and/or poorly labelled to be useful,
# but gives some idea of what could be done with more controlled data sets.



# FINDINGS:
# Guard against missing data. It just kills the ML engines. Can it be interprolated? Removed?
# Have numeric values for textual inputs whenever possible. Possibly via lookup tables, if it's not keyed in the DB.
# - Example: Race = "White, non-Hispanic" is difficult to work with, 
#   but if race = 5 and 5 = White, non-Hispanic, then you can chart and learn against the number.
#   There is a conversion example above for "years of service"



# See also: 
# http://scikit-learn.org/stable/tutorial/basic/tutorial.html
# https://machinelearningmastery.com/make-predictions-scikit-learn/
# https://www.ritchieng.com/pandas-scikit-learn/
# https://towardsdatascience.com/logistic-regression-using-python-sklearn-numpy-mnist-handwriting-recognition-matplotlib-a6b31e2b166a
# https://towardsdatascience.com/unsupervised-learning-with-python-173c51dc7f03