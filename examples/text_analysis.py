"""
Requirements:
A virtualenv is highly recommended.

You must `pip install PyPDF2`, `pip install nltk` 
and either `pip install matpotlib` or comment out the imports
if you don't intend to use plotting.

PyPDF2 is to read the PDFs and extract text.
nltk is the Natural Language Toolkit, used for the textual analysis.

Be sure to set the `pd_file` variable with the name of the PDF you're reading from
and, if necessary, set `pd_directory` to the directory holding the PDFs, 
relative to where you're running this script from.

This script will work for PDF or TXT files.

"""
import operator
import PyPDF2

from pprint import pprint

import nltk
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize

import matplotlib
# In some cases you may run into some weirdness in installed 
# python versions, matplotlib and a "not installed as a framework" error.
# If so, the command below resolves the backend.
# Note that it MUST be run before any further imports.
matplotlib.use('TkAgg')
# You may now continue importing
import matplotlib.pyplot as plt

# Point to where the PDF you're reading from lives
pd_file = '0059-18 Industrial Material Analyst.pdf'

pd_directory = 'pd_files/'

pd_file_path = pd_directory + pd_file

# make sure NLTK modules are loaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def get_keyword_frequency():
    try:
        suffix = pd_file_path.rsplit('.', 1)[1].lower()
    except IndexError:
        print("No suffix: We don't know what the file type is.")
        return
    if suffix == 'pdf':
        # Open and read the file into pyPDF2
        pd_file = open(pd_file_path,'rb')
        pd = PyPDF2.PdfFileReader(pd_file)

        #Iterate through PDF pages and extract
        pd_text = ''
        for page in pd.pages:
            pd_text += page.extractText()
    elif suffix == "txt":
        pd_file = open(pd_file_path,'r')
        pd_text = pd_file.read()
    else:
        print("Unknown file type. Please use PDF or TXT files")
        return

    # Strip newlines cause we just don't care about them for
    # word counts, and cast to lowercase for consistency
    pd_text = pd_text.replace('\n', '').lower()

    # we see lots of / in PDs, so let's split those and
    # extract the words from either side of the slash:
    pd_text = pd_text.replace('/', " ")

    # extract the word tokens with NLTK
    tokens = word_tokenize(pd_text)

    # what do we not want?
    # Note: there's probably a regex that would strip punctuation more cleanly
    punctuation = ['(', ')', ';', ':', '[', ']', ',', '.', '#', '%', "'s"]
    stop_words = stopwords.words('english')

    # quick list comprehension to strip out unwanted punctuation and stopwords
    words = [word for word in tokens if not word in stop_words and not word in punctuation]

    # for a quick primer on more great stuff we can do with NLTK, see
    # https://likegeeks.com/nlp-tutorial-using-python-nltk/
    # for now, we're going to just run our words lemmatization
    # to boil down to root words. See:
    # https://textminingonline.com/dive-into-nltk-part-iv-stemming-and-lemmatization

    

    # first lemmatize for common words
    lemmatizer = WordNetLemmatizer()
    lem_words = [lemmatizer.lemmatize(word) for word in words]
    # and now a second pass to pick up any verbs remaining
    keywords = [lemmatizer.lemmatize(word, pos='v') for word in lem_words]

    # we may not have to get into stemming, but we could.
    # If we did, we'd probably want to build a data structure with both the
    # stem and the words in the PD that stem from it, or one representative
    # word at least, because the stems themselves aren't always clearly related.
    # For example, the stem of "provision" may be "provid".
    #stems = [stemmer.stem(word) for word in keywords]

    # And now get the frequency of our keywords
    freq = nltk.FreqDist(keywords)
    common_words = freq.most_common(50)

    # We can show a plot of the words, if we want...
    # freq.plot(20, cumulative=False)

    # Rather than formatting with spaces, it may be better
    # to just output the words as comma-delimited text.
    # we could also, if we wanted, just skip printing them and just 
    # output csv or xls.
    for k, v in common_words:
        print(f'{k:<20} {v}')

    #alphabetized = sorted([w[0] for w in common_words])
    #print("here's the same list, alphabetized, so we can look for dupes...")
    #print(alphabetized)

if __name__ == "__main__":
    # execute only if run as a script
    get_keyword_frequency()