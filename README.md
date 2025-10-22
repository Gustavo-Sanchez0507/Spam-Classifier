# Spam Classifier Web Application

A machine learning–based application that detects and filters spam messages from legitimate ones in real time. The app uses natural language processing (NLP) techniques to preprocess text data and a trained classification model to predict whether an incoming message is spam or not.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Data Preprocessing](#data-preprocessing)
- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
- [Feature Engineering](#feature-engineering)
- [Modeling](#modeling)
- [Model Evaluation](#model-evaluation)
- [Web Application](#web-application)
- [Docker and Deployment](#docker-and-deployment)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

---

## Project Overview
This project implements a **spam detection system** using supervised machine learning techniques. Messages are classified as **Spam** or **Not Spam (Ham)** using a combination of text preprocessing, vectorization, and model training.

---

## Dataset
- The dataset `spamhamdata.csv` contains two columns:  
  - `label` – indicates spam or ham  
  - `message` – the text content of the message  
- The dataset was cleaned and deduplicated, resulting in a balanced representation of messages (approx. 88% ham, 12% spam).

---

## Data Preprocessing
- **Null handling**: Replaced missing values with empty strings.  
- **Text cleaning**: Converted text to lowercase, tokenized sentences, removed punctuation and stopwords.  
- **Stemming**: Applied Porter Stemmer to reduce words to their root form.  

---

## Exploratory Data Analysis (EDA)
- Visualized distribution of message lengths, number of words, and number of sentences.  
- Created **histograms** and **pairplots** to compare spam vs. ham messages.  
- Generated **word clouds** to identify common words in spam and ham messages.

---

## Feature Engineering
- Used **TF-IDF Vectorization** to convert text into numerical features with `max_features=3000` and `ngram_range=(1,3)`.  
- Additional numeric features: number of characters, words, and sentences.

---

## Modeling
- Trained multiple machine learning models:
  - Logistic Regression, SVM, Decision Tree, KNN, Random Forest, AdaBoost, Bagging, Extra Trees, Gradient Boosting, XGBoost  
  - Naive Bayes variants: Multinomial, Gaussian, Bernoulli  
- Evaluated models using **accuracy** and **precision**.  
- Selected **Multinomial Naive Bayes + SVC + Extra Trees Voting Classifier** as the final model.

---

## Model Evaluation
- Created bar plots to compare model performance.  
- Achieved high **accuracy** and **precision** in spam detection.  
- Saved the final model and TF-IDF vectorizer using **pickle**:
  - `model.pkl`
  - `vectorizer.pkl`

---

## Web Application
- Developed a **Flask web app** for real-time message classification.  
- Features:
  - Input field for user messages
  - Predict button with **dynamic color and disabled state**
  - Display of spam/not spam prediction using **Bootstrap badges**
  - Loading indicator for user feedback

---

## Docker and Deployment
- Containerized the app with **Docker** for consistent environment and portability.  
- Steps:
  1. Built Docker image: `docker build -t spam-app .`  
  2. Ran container locally: `docker run -p 5000:5000 spam-app`  
  3. Deployed container to **AWS ECR** and optionally **ECS** or **Elastic Beanstalk** for public access.

---

## Installation
```bash
# Clone repository
git clone <repo_url>
cd spam-classifier

# Install dependencies
pip install -r requirements.txt

# Run the app locally
python app.py
