import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

def transform_text(text):
    text=text.lower()
    text=nltk.word_tokenize(text)
    f=[]
    for i in text:
        if(i.isalnum()):
            f.append(i)
    text=f.copy()
    f.clear()

    for i in text:
        if(i not in string.punctuation and i not in stopwords.words("english")):
            f.append(i)

    text=f.copy()
    f.clear()

    for i in text:
        f.append(ps.stem(i))
    return " ".join(f)

st.title("SMS Spam Classifier")
input_sms = st.text_area("Enter the message")

if st.button('Predict'):

    # Preprocess the input
    transformed_sms=transform_text(input_sms)

    # Vectorize the transformed text
    vector_input=vectorizer.transform([transformed_sms])

    # Make prediction
    result = model.predict(vector_input)[0]

    if result==0:
        st.header("Not Scam")
    else:
        st.header("Spam")