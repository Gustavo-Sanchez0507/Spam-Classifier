# Spam Classifier Web Application

A production-ready machine learning web application that detects and filters spam messages in real time. Built with Flask, PostgreSQL, and Docker, and deployed on AWS EC2 for scalable cloud access.

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-336791.svg)](https://www.postgresql.org/)

---

## 🌟 Features

- **Real-time Spam Detection**: Classify messages instantly using machine learning
- **Message History**: PostgreSQL database stores all predictions with timestamps
- **Interactive UI**: Bootstrap-based responsive design with dynamic feedback
- **Delete Functionality**: Remove messages from history (click trash icon)
- **Dockerized Deployment**: Fully containerized with Docker Compose
- **Cloud Deployed**: Running on AWS EC2 for public access
- **Persistent Storage**: Docker volumes ensure data persistence across restarts

---

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Dataset](#dataset)
- [Machine Learning Pipeline](#machine-learning-pipeline)
- [Web Application](#web-application)
- [Docker Deployment](#docker-deployment)
- [AWS EC2 Deployment](#aws-ec2-deployment)
- [Installation](#installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Security Considerations](#security-considerations)

---

## 🎯 Project Overview

This project implements a **full-stack spam detection system** using:
- **Machine Learning**: Ensemble model (Multinomial NB + SVC + Extra Trees)
- **Backend**: Flask web framework with PostgreSQL database
- **Frontend**: Bootstrap 5 with async JavaScript
- **Infrastructure**: Docker containers orchestrated with Docker Compose
- **Cloud**: Deployed on AWS EC2 with proper security groups

---

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Browser   │ ───> │ Flask App    │ ───> │ PostgreSQL  │
│  (Port 80)  │ <─── │ (Port 5000)  │ <─── │ (Port 5432) │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                     ┌──────┴──────┐
                     │  ML Model   │
                     │  (Pickle)   │
                     └─────────────┘
```

**Components:**
- **Web Layer**: Bootstrap UI with JavaScript for async requests
- **Application Layer**: Flask REST API with message processing
- **ML Layer**: Pre-trained ensemble model with TF-IDF vectorization
- **Data Layer**: PostgreSQL for persistent message storage
- **Deployment**: Docker Compose with separate web and db services

---

## 📊 Dataset

- **Source**: `spamhamdata.csv`
- **Structure**: 
  - `label` – Spam or Ham classification
  - `message` – Text content
- **Statistics**: ~88% Ham, ~12% Spam (5,572 messages after deduplication)

---

## 🤖 Machine Learning Pipeline

### 1. Data Preprocessing
- Text normalization (lowercase, tokenization)
- Stopword removal using NLTK
- Porter Stemmer for word reduction
- Special character and punctuation removal

### 2. Feature Engineering
- **TF-IDF Vectorization**: `max_features=3000`, `ngram_range=(1,3)`
- Numeric features: character count, word count, sentence count

### 3. Model Training
**Models Evaluated:**
- Logistic Regression, SVM, Decision Tree, KNN
- Random Forest, AdaBoost, Bagging, Extra Trees
- Gradient Boosting, XGBoost
- Naive Bayes (Multinomial, Gaussian, Bernoulli)

**Final Model**: Voting Classifier combining:
- Multinomial Naive Bayes
- Support Vector Classifier (SVC)
- Extra Trees Classifier

**Performance**: High accuracy and precision in spam detection

**Artifacts**:
- `model.pkl` – Trained ensemble model
- `vectorizer.pkl` – TF-IDF vectorizer

---

## 🌐 Web Application

### Features
- **Dynamic UI**: Button state changes based on input
- **Real-time Classification**: Instant spam/ham prediction
- **Message History**: View last 20 classified messages
- **Delete Messages**: Remove entries from database
- **Loading Indicators**: Progress bar during classification
- **Responsive Design**: Bootstrap 5 mobile-friendly layout
- **Custom Scrollbar**: Styled message history container

### Technology Stack
- **Backend**: Flask 3.0, Python 3.10
- **Database**: PostgreSQL 13 with psycopg2
- **Frontend**: Bootstrap 5, Vanilla JavaScript (ES6+)
- **NLP**: NLTK (punkt, punkt_tab, stopwords)
- **ML**: scikit-learn, pickle

---

## 🐳 Docker Deployment

### Docker Compose Setup
```yaml
services:
  web:
    - Flask application
    - Exposes port 5000
    - Reads credentials from .env
  
  db:
    - PostgreSQL 13
    - Persistent volume for data
    - Environment variables from .env
```

### Build and Run Locally

```bash
# Clone repository
git clone https://github.com/SiDeRaLBeBa/Spam-Classifier.git
cd Spam-Classifier

# Create .env file from template
cp .env.example .env
# Edit .env with your credentials

# Build Docker image
docker build -t spam-app .

# Start services
docker-compose up -d

# View logs
docker-compose logs -f web

# Access application
# Open browser: http://localhost:5000
```

### Stop Services
```bash
docker-compose down          # Stop containers
docker-compose down -v       # Stop and remove volumes
```

### Check Database
```bash
# Connect to PostgreSQL
docker-compose exec db psql -U postgres -d spam_classifier

# View messages
SELECT * FROM messages ORDER BY created_at DESC LIMIT 10;

# Exit
\q
```

---

## ☁️ AWS EC2 Deployment

### Prerequisites
- AWS Account
- EC2 instance (t2.small or larger recommended)
- Security Group configured with ports: 22 (SSH), 80 (HTTP), 443 (HTTPS), 5000 (Flask)

### Deployment Steps

**1. Launch EC2 Instance**
```bash
AMI: Ubuntu Server 22.04 LTS or Amazon Linux 2023
Instance Type: t2.small (2GB RAM)
Key Pair: Your .pem file
Security Group: Allow ports 22, 80, 443, 5000
Storage: 20GB
```

**2. Connect to EC2**
```bash
ssh -i your-key.pem ec2-user@<EC2-PUBLIC-IP>
```

**3. Install Docker & Docker Compose**
```bash
# Update system
sudo yum update -y

# Install Docker
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Git
sudo yum install git -y

# Refresh group membership
newgrp docker
```

**4. Deploy Application**
```bash
# Clone repository
git clone https://github.com/SiDeRaLBeBa/Spam-Classifier.git
cd Spam-Classifier

# Create .env file
nano .env
# Add your environment variables (see below)

# Build and run
docker build -t spam-app .
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs -f web
```

**5. Access Application**
```
http://<EC2-PUBLIC-IP>:5000
```

---

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```bash
# PostgreSQL Database
DATABASE_URL=postgresql://postgres:your_password@db:5432/spam_classifier
PGHOST=db
PGPORT=5432
PGUSER=postgres
PGPASSWORD=your_secure_password
PGDATABASE=spam_classifier

# Flask Configuration
SECRET_KEY=your_random_secret_key_here

# Optional: AWS Credentials (if using AWS services)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-west-2
```

**⚠️ Important**: 
- Never commit `.env` to Git (already in `.gitignore`)
- Use `.env.example` as a template
- Rotate credentials regularly

---

## 🔌 API Endpoints

### `GET /`
Returns the main HTML page with classification form and message history.

### `POST /`
Classifies a message as spam or not spam.

**Request**:
```
Content-Type: application/x-www-form-urlencoded
message=Your message text here
```

**Response**: HTML with prediction result and updated history

### `DELETE /delete_message/<int:message_id>`
Deletes a message from the database.

**Response**:
```json
{
  "success": true
}
```

---

## 🔒 Security Considerations

### Current Implementation
- ✅ Environment variables for credentials
- ✅ `.gitignore` prevents credential commits
- ✅ PostgreSQL not exposed to internet (internal Docker network)
- ✅ SSH restricted to specific IP addresses

### Known Issues & Recommendations
- ⚠️ **Delete endpoint has no authentication** – anyone can delete messages
- ⚠️ **Hardcoded credentials in .env.example** should be rotated
- 🔧 **Recommendation**: Add admin authentication for delete functionality
- 🔧 **Recommendation**: Use AWS Secrets Manager or Parameter Store
- 🔧 **Recommendation**: Set up HTTPS with Let's Encrypt SSL
- 🔧 **Recommendation**: Use AWS RDS instead of containerized PostgreSQL for production

### For Production
```bash
# Set up Nginx reverse proxy
sudo yum install nginx -y

# Configure SSL with Let's Encrypt
sudo yum install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com

# Update docker-compose.yml to use port 80
```

---

## 📦 Installation

### Local Development

```bash
# Clone repository
git clone https://github.com/SiDeRaLBeBa/Spam-Classifier.git
cd Spam-Classifier

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords')"

# Run locally (without Docker)
python app.py
```

---

## 🚀 Usage

### Testing the Application

1. **Access the web interface**: `http://localhost:5000` or `http://<EC2-IP>:5000`

2. **Classify a message**:
   - Enter text in the input field
   - Click "Classify" button
   - View prediction (Spam/Not Spam badge)

3. **View message history**:
   - Scroll through recent predictions
   - Messages are stored with timestamps

4. **Delete messages**:
   - Click trash icon next to any message
   - Message is removed from database

### Example Messages to Test

**Spam Examples**:
```
WINNER!! You have been selected to receive $1000. Click here now!
Congratulations! You've won a free iPhone. Claim now!
```

**Ham Examples**:
```
Hey, what's your plan for today?
Can we meet tomorrow at 3 PM?
```

---

## 📁 Project Structure

```
Spam-Classifier/
├── app.py                 # Flask application
├── db.py                  # Database operations
├── model.pkl              # Trained ML model
├── vectorizer.pkl         # TF-IDF vectorizer
├── dockerfile             # Docker image definition
├── docker-compose.yml     # Multi-container orchestration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── spamhamdata.csv       # Training dataset
├── main.ipynb            # Jupyter notebook (ML training)
├── templates/
│   └── index.html        # Web interface
├── static/
│   └── js/
│       └── classifier.js # Client-side JavaScript
└── README.md             # This file
```

---

## 🛠️ Technologies Used

| Category | Technology |
|----------|-----------|
| **Language** | Python 3.10 |
| **Web Framework** | Flask 3.0 |
| **Database** | PostgreSQL 13 |
| **ML Libraries** | scikit-learn, NLTK |
| **Frontend** | Bootstrap 5, JavaScript ES6 |
| **Containerization** | Docker, Docker Compose |
| **Cloud** | AWS EC2 |
| **Version Control** | Git, GitHub |

---

## 📝 License

This project is open source and available under the MIT License.

