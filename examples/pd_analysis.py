"""
Requirements:
A virtualenv is highly recommended.

pip install xlrd
pip install pandas
pip install matplotlib
pip install scipy
pip install scikit-learn

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
xl_file = 'spreadsheets/Industrial material analyst PD word frequencies.xlsx'
df = pd.read_excel(xl_file)

# df is the dataframe we'll be working with
# Does the dataframe look like the spreadsheet?
print(df.shape)    # output row and column numbers
print(df.describe) # output what the data (truncated) looks like

# throw out the "sum" column
df = df.loc[ : , '0058-18':'1101-09']
df.corr()

"""
          0058-18   0059-18   1101-11   1101-09
0058-18  1.000000  0.666738  0.761357  0.290801
0059-18  0.666738  1.000000  0.484970  0.129880
1101-11  0.761357  0.484970  1.000000  0.552023
1101-09  0.290801  0.129880  0.552023  1.000000
"""
