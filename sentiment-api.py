import pickle
import numpy as np
import re
import string
from flask import Flask,request,jsonify
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

app = Flask(__name__)

def clean_text(text):
    text= ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", text).split())
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    lemmatizer = WordNetLemmatizer() 
    words = [lemmatizer.lemmatize(word) for word in words]
    text = ' '.join(word for word in words)
    return text

@app.route('/')
def index():
  return 'Server Works!'
  
@app.route('/process_text',methods=['POST'])
def processing_text():
  text = request.form.get('text')
  text = clean_text(text)
  tfidf = pickle.load(open('tfidf.pickle','rb'))
  lr = pickle.load(open('logistic_regression.pickle','rb'))
  testing = tfidf.transform([text])
  prediction = lr.predict(testing)
  prediction = 'positive' if prediction == 1 else 'negative'
  neg_value = round(float(lr.predict_proba(testing).T[0]),2)
  pos_value = round(float(lr.predict_proba(testing).T[1]),2)
  items = jsonify({'prediction':prediction,'pos_value':pos_value,'neg_value':neg_value})
  return (items)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='80')
