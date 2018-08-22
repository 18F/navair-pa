"""
Requirements:
A virtualenv is highly recommended.

You must `pip install PyPDF2` and `pip install nltk`

The former is to read the PDFs and extract text.
The latter is for the textual analysis.

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

# Point to where the PDF you're reading from lives
pd_file = 'BUSINESS OPERATIONS DIRECTOR GS-15.pdf'
pd_directory = 'pd_files/'
pd_file_path = pd_directory + pd_file

# make sure NLTK modules are loaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def get_keyword_frequency():
    # Open and read the file into pyPDF2
    pd_file = open(pd_file_path,'rb')
    pd = PyPDF2.PdfFileReader(pd_file)

    #Iterate through PDF pages and extract
    pd_text = ''
    for page in pd.pages:
        pd_text += page.extractText()

    # Strip newlines cause we just don't care,
    # and cast to lowercase for consistency
    pd_text = pd_text.replace('\n', '').lower()

    # we see lots of / in PDs, so let's split those words:
    pd_text = pd_text.replace('/', " ")

    # extract the word tokens with NLTK
    tokens = word_tokenize(pd_text)

    # what do we not want?
    # Note: there's probably a regex that would strip punctuation more cleanly
    punctuation = ['(', ')', ';', ':', '[', ']', ',', '.']
    stop_words = stopwords.words('english')

    # quick list comprehension to strip out unwanted punctuation and stopwords
    words = [word for word in tokens if not word in stop_words and not word in punctuation]

    # for a quick primer on more great stuff we can do with NLTK, see
    # https://likegeeks.com/nlp-tutorial-using-python-nltk/
    # for now, we're going to just run our words lemmatization
    # to boil down to root words. See:
    # https://textminingonline.com/dive-into-nltk-part-iv-stemming-and-lemmatization

    # we may not have to get into stemming.
    #stems = [stemmer.stem(word) for word in words]

    # first lemmatize for common words
    lemmatizer = WordNetLemmatizer()
    lem_words = [lemmatizer.lemmatize(word) for word in words]
    # and now a second pass to pick up any verbs remaining
    keywords = [lemmatizer.lemmatize(word, pos='v') for word in lem_words]

    # And now get the frequency of our keywords
    freq = nltk.FreqDist(keywords)
    common_words = freq.most_common(50)

    # could plot, if matplotlib is installed
    # freq.plot(20, cumulative=False)

    for k, v in common_words:
        print(f'{k:<20} {v}')

    #alphabetized = sorted([w[0] for w in common_words])
    #print("here's the same list, alphabetized, so we can look for dupes...")
    #print(alphabetized)

if __name__ == "__main__":
    # execute only if run as a script
    get_keyword_frequency()