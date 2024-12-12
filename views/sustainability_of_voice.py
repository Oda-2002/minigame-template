from flask import Blueprint, render_template
from flask_socketio import emit
import math
import queue
import struct
import sys
from threading import Lock
import numpy as np
from flask import request

# Blueprintの作成
sustainability_of_voice_bp = Blueprint('sustainability_of_voice', __name__, static_folder='../static', template_folder='../templates')

def register_socket_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    @socketio.on('audio_data')
    def handle_audio_data(data):
        """クライアントから送信された音声データを処理"""
        power = data.get('power', 0)  # デフォルト値を0に変更
        # 負の値を0に制限
        power = max(0, power)
        print(f"Received audio power: {power}")
        emit('audio_data', {'power': power})

@sustainability_of_voice_bp.route('/')
def index():
    mode = request.args.get('mode', 'normal')  # パラメータが指定されていない場合は 'normal' をデフォルトに
    if mode == 'hard':
        return render_template('hard.html')
    else:
        return render_template('normal.html')