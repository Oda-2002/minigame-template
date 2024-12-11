from dotenv import load_dotenv
from flask import Flask, render_template
from flask_socketio import SocketIO
from views.sample_audio import sample_audio_bp
from views.sustainability_of_voice import sustainability_of_voice_bp, register_socket_events
from views.utterance_check import utterance_check_bp
from views.voice_jump import voice_jump_bp
import requests
from flask_cors import CORS
import os
import eventlet  # 必須: eventlet をインポート
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()  # .envファイルを読み込む

# Flask アプリと Socket.IO の初期化
app = Flask(__name__)

# リバースプロキシ対応を追加
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

socketio = SocketIO(
    app, 
    cors_allowed_origins="*",  # "*" を指定して全てのオリジンを許可（一時的に）
    async_mode='eventlet', # WebSocket サポートのために eventlet を使用
    logger=True, # ログを有効化
    engineio_logger=True # Engine.IO のログを有効化
)

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
    port = int(os.environ.get("PORT", 8080))
    socketio.run(app, host='0.0.0.0', port=port)