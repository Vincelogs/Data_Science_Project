from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import joblib

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
            gender TEXT,
            following_rate INTEGER,
            followers_avg_age INTEGER,
            following_avg_age INTEGER,
            max_repetitive_punc INTEGER,
            num_of_hashtags_per_action INTEGER,
            emoji_count_per_action INTEGER,
            punctuations_per_action INTEGER,
            number_of_words_per_action INTEGER,
            avgCompletion INTEGER,
            avgTimeSpent INTEGER,
            avgDuration INTEGER,
            avgComments INTEGER,
            creations INTEGER,
            content_views INTEGER,
            num_of_comments INTEGER,
            age_group INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Home route to show the survey form
@app.route('/', methods=['GET', 'POST'])
def user_form():
    if request.method == 'POST':
        # Load the model
        model = joblib.load('models/fraud_detection_model.pkl')

        # Get form data
        gender = int(request.form['gender'])
        following_rate = float(request.form['following_rate'])
        followers_avg_age = float(request.form['followers_avg_age'])
        following_avg_age = float(request.form['following_avg_age'])
        max_repetitive_punc = int(request.form['max_repetitive_punc'])
        num_of_hashtags_per_action = int(request.form['num_of_hashtags_per_action'])
        emoji_count_per_action = int(request.form['emoji_count_per_action'])
        punctuations_per_action = int(request.form['punctuations_per_action'])
        number_of_words_per_action = int(request.form['number_of_words_per_action'])
        avgCompletion = float(request.form['avgCompletion'])
        avgTimeSpent = float(request.form['avgTimeSpent'])
        avgDuration = float(request.form['avgDuration'])
        creations = int(request.form['creations'])

        # Prepare features
        features = [
            gender, following_rate, followers_avg_age, following_avg_age, 
            max_repetitive_punc, num_of_hashtags_per_action, emoji_count_per_action, 
            punctuations_per_action, number_of_words_per_action, avgCompletion, 
            avgTimeSpent, avgDuration, creations
        ]

        # Predict
        prediction = model.predict([features])[0]  # Assuming binary classification
        result = "Fraudulent" if prediction == 1 else "Not Fraudulent"

        # Render the form with the result
        return render_template('user_form.html', result=result)

    # GET request: Render the form without result
    return render_template('user_form.html', result=None)

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        gender = request.form['gender']
        following_rate = request.form['following_rate']
        followers_avg_age = request.form['followers_avg_age']
        following_avg_age = request.form['following_avg_age']
        max_repetitive_punc = request.form['max_repetitive_punc']
        num_of_hashtags_per_action = request.form['num_of_hashtags_per_action']
        emoji_count_per_action = request.form['emoji_count_per_action']
        punctuations_per_action = request.form['punctuations_per_action']
        number_of_words_per_action = request.form['number_of_words_per_action']
        avgCompletion = request.form['avgCompletion']
        avgTimeSpent = request.form['avgTimeSpent']
        avgDuration = request.form['avgDuration']
        avgComments = request.form['avgComments']
        creations = request.form['creations']
        content_views = request.form['content_views']
        num_of_comments = request.form['num_of_comments']
        age_group = request.form['age_group']


        # Insert survey data into database
        conn = connect_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO survey_responses 
            (gender, following_rate, followers_avg_age, following_avg_age, max_repetitive_punc, num_of_hashtags_per_action, emoji_count_per_action, punctuations_per_action, number_of_words_per_action, avgCompletion, avgTimeSpent,avgDuration, avgComments, creations, content_views, num_of_comments, age_group) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (gender, following_rate, followers_avg_age, following_avg_age, max_repetitive_punc, num_of_hashtags_per_action, emoji_count_per_action, punctuations_per_action, number_of_words_per_action, avgCompletion, avgTimeSpent, avgDuration, avgComments, creations, content_views, num_of_comments, age_group)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('user_form'))

# Route to handle machine learning predictions (example for fraud detection)
@app.route('/predict_fraud', methods=['POST'])
def predict_fraud():
    # Load pre-trained fraud detection model
    model = joblib.load('models/fraud_detection_model.pkl')

    # Get form data (simulated here; in production, fetch data from the request)
    data = request.get_json()
    features = [data['gender'], data['following_rate'], data['followers_avg_age'], data['following_avg_age'], data['max_repetitive_punc'], data['num_of_hashtags_per_action'], data['emoji_count_per_action'], data['punctuations_per_action'], data['number_of_words_per_action'], data['avgCompletion'], data['avgTimeSpent'], data['avgDuration'], data['creations']]

    # Predict whether the user is fraudulent
    prediction = model.predict([features])
    return jsonify({'is_fraudulent': bool(prediction[0])})

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
