import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

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

st.markdown("""
    <style>
        .centered {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding-top: 50px;
        }
        input[type="text"] {
            width: 300px;
            padding: 10px;
            font-size: 16px;
        }
        .result {
            font-size: 24px;
            margin-top: 20px;
            color: #333;
        }
    </style>
    <div class="centered">
        <h2>Spam Classifier</h2>
    </div>
""", unsafe_allow_html=True)

# Load model and vectorizer
model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

# Streamlit UI
st.title('Spam and Ham Classifier')

input_sms = st.text_area("", placeholder="Type your message here...")

if st.button("Predict"):
    if input_sms:
        # 1. Preprocess
        transformed_sms = transform_message(input_sms)

        # 2. Vectorize
        vector_input = vectorizer.transform([transformed_sms]).toarray()

        # 3. Predict
        result = model.predict(vector_input)[0]

        label = "Spam" if result else "Not Spam"
        color = "red" if label == "Spam" else "green"
        st.markdown(f"<div class='result' style='color:{color}; text-align:center;'>{label}</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter a message before classifying.")
