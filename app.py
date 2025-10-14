from flask import Flask, request, render_template
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
ps = PorterStemmer()

def transform_message(message):
    message = message.lower()
    message = nltk.word_tokenize(message)

    y = []
    for i in message:
        if i.isalnum():
            y.append(i)

    message = y[:]
    y.clear()

    for i in message:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    message = y[:]
    y.clear()

    for i in message:
        y.append(ps.stem(i))

    return " ".join(y)




@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    if request.method == 'POST':
        message = request.form['message']
        transformed = transform_message(message)
        vector_input = vectorizer.transform([transformed]).toarray()
        result = model.predict(vector_input)[0]
        prediction = 'Spam' if result == 1 else 'Not Spam'

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)

