import nltk
from flask import Flask, request, render_template, url_for, jsonify
import pickle
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
import db  # our new database module

app = Flask(__name__, static_folder='static')

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
    # Keep in-memory history as fallback when database is not available
    if not hasattr(app, 'history'):
        app.history = []
    
    if request.method == 'POST':
        message = request.form['message']
        transformed = transform_message(message)
        vector_input = vectorizer.transform([transformed]).toarray()
        result = model.predict(vector_input)[0]
        prediction = 'Spam' if result == 1 else 'Not Spam'
        
        # Try to save to database, fall back to in-memory if that fails
        saved = db.insert_message(message, prediction)
        if not saved:
            app.history.insert(0, {'message': message, 'prediction': prediction})
            if len(app.history) > 20:
                app.history = app.history[:20]

    # Try to get history from database, fall back to in-memory if that fails
    history = db.get_history(20)
    if not history:
        history = getattr(app, 'history', [])

    return render_template('index.html', prediction=prediction, history=history)

@app.route('/delete_message/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    success = db.delete_message(message_id)
    return jsonify({'success': success})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
