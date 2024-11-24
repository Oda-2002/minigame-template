from flask import Flask
from flask import Flask, request, jsonify, send_from_directory, render_template
import requests
import os
from views.sample_audio import sample_audio_bp
from views.sustainability_of_voice import sustainability_of_voice_bp
from views.utterance_check import utterance_check_bp
from views.voice_jump import voice_jump_bp

app = Flask(__name__)

app.register_blueprint(sample_audio_bp, url_prefix='/sample_audio')
app.register_blueprint(sustainability_of_voice_bp, url_prefix='/sustainability_of_voice')
app.register_blueprint(utterance_check_bp, url_prefix='/utterance_check')
app.register_blueprint(voice_jump_bp, url_prefix='/voice_jump')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)