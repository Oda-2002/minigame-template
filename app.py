from dotenv import load_dotenv
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_socketio import SocketIO
from views.sample_audio import sample_audio_bp
from views.sustainability_of_voice import sustainability_of_voice_bp, register_socket_events
from views.utterance_check import utterance_check_bp
from views.voice_jump import voice_jump_bp
import requests
from flask_cors import CORS

load_dotenv()  # .envファイルを読み込む

# Flask アプリと Socket.IO の初期化
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# アプリの初期化部分に追加
CORS(app)

# Blueprint の登録
app.register_blueprint(sample_audio_bp, url_prefix='/sample_audio')
app.register_blueprint(sustainability_of_voice_bp, url_prefix='/sustainability_of_voice')
app.register_blueprint(utterance_check_bp, url_prefix='/utterance_check')
app.register_blueprint(voice_jump_bp, url_prefix='/voice_jump')

# Socket.IO イベントを登録
def register_global_events(socketio):
    """Socket.IO のグローバルイベントを登録"""
    @socketio.on('message')
    def handle_message(msg):
        print(f'Received message: {msg}')
        socketio.send(f'You sent: {msg}')

    @socketio.on('custom_event')
    def handle_custom_event(data):
        print(f'Received custom event with data: {data}')
        socketio.emit('response', {'status': 'success', 'data': data})

# 各 Blueprint の Socket.IO イベントを登録
register_global_events(socketio)
register_socket_events(socketio)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Flask アプリ全体を Socket.IO サーバーとして動作させる
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)