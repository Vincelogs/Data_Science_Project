from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Create a connection to the SQLite database
def connect_db():
    conn = sqlite3.connect('social_media_data.db')
    return conn

# Create a table to store survey responses
def create_table():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS survey_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            gender TEXT,
            location TEXT,
            occupation TEXT,
            preferred_content TEXT,
            device TEXT,
            time_spent TEXT,
            satisfaction TEXT,
            privacy_concern TEXT,
            suspicious_activity TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Home route to show the survey form
@app.route('/')
def survey_form():
    return render_template('survey_form.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_survey():
    if request.method == 'POST':
        age = request.form['age']
        gender = request.form['gender']
        location = request.form['location']
        occupation = request.form['occupation']
        preferred_content = request.form['preferred_content']
        device = request.form['device']
        time_spent = request.form['time_spent']
        satisfaction = request.form['satisfaction']
        privacy_concern = request.form['privacy_concern']
        suspicious_activity = request.form['suspicious_activity']

        # Insert survey data into database
        conn = connect_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO survey_responses 
            (age, gender, location, occupation, preferred_content, device, time_spent, satisfaction, privacy_concern, suspicious_activity) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (age, gender, location, occupation, preferred_content, device, time_spent, satisfaction, privacy_concern, suspicious_activity)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('survey_form'))

# Route to handle machine learning predictions (example for fraud detection)
@app.route('/predict_fraud', methods=['POST'])
def predict_fraud():
    # Load pre-trained fraud detection model
    model = joblib.load('models/fraud_detection_model.pkl')

    # Get form data (simulated here; in production, fetch data from the request)
    data = request.get_json()
    features = [data['login_frequency'], data['posts_per_day'], data['average_time_on_site'], data['likes_received'], data['friends_count']]

    # Predict whether the user is fraudulent
    prediction = model.predict([features])
    return jsonify({'is_fraudulent': bool(prediction[0])})

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
