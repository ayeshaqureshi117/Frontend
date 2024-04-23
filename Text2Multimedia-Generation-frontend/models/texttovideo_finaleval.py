"""Libraries"""

import torch
import nltk
import imageio
import numpy as np
from IPython.display import Audio, display
from flask import send_file
import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
import imageio
import numpy as np
import soundfile as sf
import os
import re
import time
import secrets
from pyngrok import ngrok
from collections import Counter
from flask import Flask, request, jsonify, send_file, redirect, url_for, session
from moviepy.editor import VideoFileClip, AudioFileClip
nltk.download('punkt')
from emotion import get_emotion
from video import text_to_video
from audio import emotional_TTS
from Render_template import render_html_template
from validate import validateFormData
import soundfile as sf

# Set your ngrok authtoken
ngrok.set_auth_token("2dENAXj0qJ1dMExir66eXh0ql6i_5qw8XNcN7nt2kk3Gmv39i")
public_url = ngrok.connect(8000)
print(public_url)

app = Flask(__name__,static_folder = '/content/drive/MyDrive/FYP/static')

# Generate a secure random secret key
secret_key = secrets.token_hex(16)
app.secret_key = secret_key

# Set the static and template folders
app.template_folder = '/content/drive/MyDrive/FYP/templates'

client = pymongo.MongoClient("mongodb+srv://alishbalaeeq:admin@cluster0.8gizr.mongodb.net/")
db = client.get_database('FYP')
collection = db.register

# Create unique indexes for username and email fields
collection.create_index([('username', pymongo.ASCENDING)], unique=True)
collection.create_index([('email', pymongo.ASCENDING)], unique=True)

@app.route('/static/convert.mp4')
def get_convert_video():
    return send_file('/content/drive/MyDrive/FYP/static/convert.mp4', mimetype='video/mp4')


@app.route('/static/Background.mp4')
def get_background_video():
    return send_file('/content/drive/MyDrive/FYP/static/Background.mp4', mimetype='video/mp4')
    
@app.route('/')
def landing_page():
    if 'logged_in' in session:
        username = session['username']

    # Determine login status
    login_status = 'Sign Out' if 'logged_in' in session else 'Sign In'
    register_text = f'Welcome {username}' if 'logged_in' in session else 'Register Now!'

    # Read the contents of the HTML file
    with open('/content/drive/MyDrive/FYP/templates/index.html', 'r') as file:
        html_content = file.read()

    # Replace placeholders for login_status and register_text
    html_content = html_content.replace('{{ login_status }}', login_status)
    html_content = html_content.replace('{{ register_text }}', register_text)

    # Render HTML template with login status
    return html_content

@app.route('/home')
def home_page():
    if 'logged_in' in session:
        username = session['username']

    # Determine login status
    login_status = 'Sign Out' if 'logged_in' in session else 'Sign In'
    register_text = f'Welcome {username}' if 'logged_in' in session else 'Register Now!'

    # Read the contents of the HTML file
    with open('/content/drive/MyDrive/FYP/templates/index.html', 'r') as file:
        html_content = file.read()

    # Replace placeholders for login_status and register_text
    html_content = html_content.replace('{{ login_status }}', login_status)
    html_content = html_content.replace('{{ register_text }}', register_text)

    # Render HTML template with login status
    return html_content

@app.route('/about')
def about_page():
    # Determine login status
    login_status = 'Sign Out' if 'logged_in' in session else 'Sign In'

    return render_html_template('/content/drive/MyDrive/FYP/templates/about.html',login_status=login_status)

# Route for handling login form submission
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # Get the login credentials from the form
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if email_or_username exists in the database
        user = collection.find_one({'$or': [{'email': email}, {'username': password}]})
        username = user.get('username', '')

        if user:
            # User found, check password
            if user['password'] == password:
                session['logged_in'] = True
                session['user_id'] = str(user['_id'])
                session['username'] = username
                return jsonify({'success': True, 'message': 'Login successful!', 'redirect': '/home'})  # Successful login
            else:
                # Incorrect password
                return jsonify({'success': False, 'error': 'Incorrect password'})
        else:
            # User not found
            return jsonify({'success': False, 'error': 'User not found'})
    else:
        # Return login page for GET request
        return send_file('/content/drive/MyDrive/FYP/templates/login.html')

# Route for user logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    return redirect('/home')

# Route to check login status
@app.route('/check_login_status')
def check_login_status():
    if 'logged_in' in session:
        return jsonify({'logged_in': True})
    else:
        return jsonify({'logged_in': False})


# Route to check login status
@app.route('/check_username')
def add_username():

    if 'logged_in' in session:
        username = session['username']

        username = f'Welcome {username}' if 'logged_in' in session else 'Register Now!'

        return jsonify({'username': username})
    else:
        return jsonify({'username': None})

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        formData = request.json

        # Perform server-side validation
        errorMsg = validateFormData(formData)

        if errorMsg:
            return jsonify({'error': errorMsg}), 400

        try:
            # Insert data into MongoDB
            collection.insert_one(formData)
            return jsonify({'success': True, 'message': 'Signup Successful!!', 'redirect': '/login'})
        except pymongo.errors.DuplicateKeyError:
            # Handle case where username or email already exists
            return jsonify({'error': 'Username or email already exists'})
    else:
        # Render the registration form
        return send_file('/content/drive/MyDrive/FYP/templates/register.html')
    
@app.route('/text', methods=['GET', 'POST'])
def video_gen_page():
    # Determine login status
    login_status = 'Sign Out' if 'logged_in' in session else 'Sign In'

    video_path = "/content/drive/MyDrive/FYP/static/output_video1.mp4"

    if request.method == 'POST':
        text = request.form.get('prompt')
        sentences = nltk.sent_tokenize(text)

        audio = []
        emotions = ['anger','approval','calm','disapproval','disgust','fear','gratitude','joy','neutral','optimism','sadness','surprise']
        vote_emotions = []

        for sent in sentences:
            emotion = get_emotion(sent)
            if emotion not in emotions:
                emotion = 'neutral'
            vote_emotions.append(emotion)

        word_counts = Counter(vote_emotions)
        most_common_emotion = word_counts.most_common(1)[0][0]

        for sent in sentences:
            audio.append(emotional_TTS(sent, most_common_emotion, f"/content/drive/MyDrive/FYP/static/audio/{emotion}.wav"))

        concatenated_audio=audio[0]
        for aud in audio[1:]:
            concatenated_audio = np.concatenate((concatenated_audio, aud))
        fps = 3
        vid = text_to_video(sentences, audio, fps = fps, num_inference_steps=4)
        imageio.mimsave("/content/drive/MyDrive/FYP/static/video/gen_content.mp4", vid, fps=fps)
        sf.write("/content/drive/MyDrive/FYP/static/audio/aud.wav", concatenated_audio, 22050)

        video_clip = VideoFileClip("/content/drive/MyDrive/FYP/static/video/gen_content.mp4")
        audio_clip = AudioFileClip("/content/drive/MyDrive/FYP/static/audio/aud.wav")

        video = video_clip.set_audio(audio_clip)
        video.write_videofile("/content/drive/MyDrive/FYP/static/output_video1.mp4")

        # Wait until the video is generated
        while not os.path.exists(video_path):
            time.sleep(1)

        return jsonify({'video_path':  '/static/output_video1.mp4'})
    else:
        return render_html_template('/content/drive/MyDrive/FYP/templates/text.html',login_status=login_status)

if __name__ == '__main__':
    app.run(port=8000,debug=False)