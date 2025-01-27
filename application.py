import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
        
import re
import nltk
from nltk.util import pr
stemmer = nltk.SnowballStemmer("english")
from nltk.corpus import stopwords
import string
stopword = set(stopwords.words("english"))

file_path = r'c:\study material\projects\hate speech det 3rd sem\Hate_Speech_Detection\twitter_dataset.csv'
df = pd.read_csv(file_path)
#print(df.head())

df['labels'] = df['class'].map({0:"Hate Speech Detected.", 1:"Offensive Language Detected.", 2:"No Hate or Offensive Speech."})
#print(df.head())

df = df[['tweet', 'labels']]
df.head()

def clean(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = [word for word in text.split(' ') if word not in stopword]
    text = " ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text = " ".join(text)
    return text
df["tweet"] = df["tweet"].apply(clean)
#print(df.head())

x = np.array(df["tweet"])
y = np.array(df["labels"])

cv = CountVectorizer()
x = cv.fit_transform(x)
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.33, random_state = 42)
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)
# Make predictions on the test set
y_pred = clf.predict(X_test)

# Calculate the accuracy score
accuracy = accuracy_score(y_test, y_pred)

# Print or display the accuracy score
print(f"Accuracy: {accuracy}")

def hate_speech_detection():
    import streamlit as st
    st.title("Hate Speech Detection")
    user = st.text_area("Enter any Tweet: ")
    if len(user) < 1:
        st.write("  ")
    else:
        sample = user
        data = cv.transform([sample]).toarray()
        a = clf.predict(data)
        st.title(a)
hate_speech_detection()