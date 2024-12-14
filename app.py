from dotenv import load_dotenv
from flask import Flask, render_template
from flask_socketio import SocketIO
from views.sustainability_of_voice import sustainability_of_voice_bp, register_socket_events
from views.sample_audio import sample_audio_bp
from views.utterance_check import utterance_check_bp
from views.voice_jump import voice_jump_bp
import os
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()

# Flask アプリと Socket.IO の初期化
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent', logger=True, engineio_logger=True)

# CORS 設定
CORS(app)

# Blueprint 登録
app.register_blueprint(sample_audio_bp, url_prefix='/sample_audio')
app.register_blueprint(sustainability_of_voice_bp, url_prefix='/sustainability_of_voice')
app.register_blueprint(utterance_check_bp, url_prefix='/utterance_check')
app.register_blueprint(voice_jump_bp, url_prefix='/voice_jump')

# Socket.IO イベントを登録
register_socket_events(socketio)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    socketio.run(app, host='0.0.0.0', port=port)