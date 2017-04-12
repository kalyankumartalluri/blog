from django.shortcuts import render
from .models import Test
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
import os

import re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer

def review_to_words(raw_review):
    # Function to convert a raw review to a string of words
    # The input is a single string (a raw movie review), and
    # the output is a single string (a preprocessed movie review)
    #
    # 1. Remove HTML
    if raw_review:
        review_text = BeautifulSoup(raw_review).get_text()
        #
        # 2. Remove non-letters
        letters_only = re.sub("[^a-zA-Z]", " ", review_text)
        #
        # 3. Convert to lower case, split into individual words
        words = letters_only.lower().split()
        #
        # 4. In Python, searching a set is much faster than searching
        #   a list, so convert the stop words to a set
        stops = set(stopwords.words("english"))
        #
        # 5. Remove stop words
        meaningful_words = [w for w in words if not w in stops]
        #
        # 6. Join the words back into one string separated by space,
        # and return the result.
        return (" ".join(meaningful_words))
    else:
        return raw_review



# Create your views here.
def test_list(request):
    tests = Test.objects.order_by('name')
    return render(request, 'cqtest/test_list.html', {'tests': tests})

# Create your views here.
def test_testimport(request):
    # train = pd.read_excel('C:\\Kalyan\\ProdDev\\AdvancedRevEngg\\MySite\\mysite\\cqtest\\testdata\\Parabank Manual tests ATR v1.xls', header=0)
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'testdata\\Parabank Manual tests ATR v1.xls')
    train = pd.read_excel(file_path,header=0)

    # Initialize the "CountVectorizer" object, which is scikit-learn's
    # bag of words tool.
    vectorizer = CountVectorizer(analyzer="word",
                                 tokenizer=None,
                                 preprocessor=None,
                                 stop_words=None,
                                 max_features=5000)
    prevtestname = ""
    for i in train.index:
        clean_stepdescs = []
        testname = train['Test Case Name'][i]
        # print('%f',testname)
        if not pd.isnull(train['Test Case Name'][i]) :
            prevtestname = testname
        else:
            testname = prevtestname

        test = Test()
        test.name = testname
        test.author = request.user
        if not pd.isnull(train['Description'][i]) :
            test.desc = train['Description'][i]

        if not pd.isnull(train['Test Step Description'][i]):
            test.stepdesc = review_to_words(train['Test Step Description'][i])

        if not pd.isnull(train['Expected Result'][i]):
            test.stepexpresult = review_to_words(train['Expected Result'][i])
        # if r == 'Test Step Description' or r == 'Expected Result':
        #    for i in train.index:
        clean_stepdescs.append(test.stepdesc)  # ( " ".join(words)))
        clean_stepdescs.append(test.stepexpresult)  # ( " ".join(words)))

        # fit_transform() does two functions: First, it fits the model
        # and learns the vocabulary; second, it transforms our training data
        # into feature vectors. The input to fit_transform should be a list of
        # strings.
        train_data_features = vectorizer.fit_transform(clean_stepdescs)

        # Numpy arrays are easy to work with, so convert the result to an
        # array
        train_data_features = train_data_features.toarray()
        # Take a look at the words in the vocabulary
        vocab = vectorizer.get_feature_names()
        # Sum up the counts of each vocabulary word
        dist = np.sum(train_data_features, axis=0)

        # For each, print the vocabulary word and the number of times it
        # appears in the training set
        temptoken = []
        for tag, count in zip(vocab, dist):
            temptoken.append("%s:%d" % (tag, count))

        test.tokenised = temptoken
        print(test.tokenised)
        test.publish()
    tests = Test.objects.order_by('name')
    return render(request, 'cqtest/test_list.html', {'tests': tests})


def test_detail(request, pk):
    test = get_object_or_404(Test, pk=pk)
    return render(request, 'cqtest/test_detail.html', {'test': test})

def test_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.author = request.user
            test.publish()
            #return redirect('test_detail', pk=test.pk)
            return test_list(request)
    else:
        form = PostForm()
    return render(request, 'cqtest/test_edit.html', {'form': form})

def test_edit(request, pk):
    test = get_object_or_404(Test, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=test)
        if form.is_valid():
            test = form.save(commit=False)
            test.author = request.user
            test.publish()
            return redirect('test_detail', pk=test.pk)
    else:
        form = PostForm(instance=test)
    return render(request, 'cqtest/test_edit.html', {'form': form})