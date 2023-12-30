import nltk
import streamlit as st
import streamlit as st
import preprocessor, staticAnalysis
import seaborn as sns
import numpy as np
from pydub import AudioSegment
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd
import re

st.title("Malicious Link")
# Streamlit title and layout config
st.title('News Authenticator')
st.write('Enter a news title and author to check if it is Real or Fake.')

# Check if stopwords are downloaded, otherwise download
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Load and preprocess data
news_dataset = pd.read_csv('train.csv')
news_dataset = news_dataset.fillna('')
news_dataset['content'] = news_dataset['author'] + ' ' + news_dataset['title']

port_stem = PorterStemmer()

def stemming(content):
    stemmed_content = re.sub('[^a-zA-Z]', ' ', content)
    stemmed_content = stemmed_content.lower()
    stemmed_content = stemmed_content.split()
    stemmed_content = [port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
    stemmed_content = ' '.join(stemmed_content)
    return stemmed_content

news_dataset['content'] = news_dataset['content'].apply(stemming)
x = news_dataset['content'].values
y = news_dataset['label'].values

vectorizer = TfidfVectorizer()
vectorizer.fit(x)
x = vectorizer.transform(x)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y, random_state=2)

model = LogisticRegression()
model.fit(x_train, y_train)

# Streamlit input and prediction
author = st.text_input("Author")
title = st.text_input("Title")
if st.button("Predict"):
    content = author + ' ' + title
    content = stemming(content)
    content_vectorized = vectorizer.transform([content])
    prediction = model.predict(content_vectorized)

    if prediction[0] == 0:
        st.write('The news is Real')
    else:
        st.write('The news is Fake')

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Load the dataset
urls_data = pd.read_csv("urldata.csv")

def makeTokens(f):
    tkns_BySlash = str(f.encode('utf-8')).split('/')
    total_Tokens =[]
    for i in tkns_BySlash:
        tokens = str(i).split('-')
        tkns_ByDot =[]
        for j in range(0,len(tokens)):
            temp_Tokens = str(tokens[j]).split('.')
            tkns_ByDot = tkns_ByDot + temp_Tokens
        total_Tokens = total_Tokens +tokens +tkns_ByDot
    total_Tokens = list(set(total_Tokens))
    if 'com' in total_Tokens:
        total_Tokens.remove('com')
    return total_Tokens

y = urls_data["label"]
url_list = urls_data["url"]

# Vectorize the URL data
vectorizer = TfidfVectorizer(tokenizer=makeTokens)
X = vectorizer.fit_transform(url_list)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a logistic regression model
logit = LogisticRegression()
logit.fit(X_train, y_train)

# Streamlit app
st.title("Phishing URL Detector")

# Input for user to enter a URL
user_input = st.text_input("Enter a URL:")

if user_input:
    X_predict = [user_input]
    X_predict = vectorizer.transform(X_predict)
    prediction = logit.predict(X_predict)

    st.write("Prediction:", prediction[0])

