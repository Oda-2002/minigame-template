from flask import Blueprint, render_template
from flask_socketio import emit, SocketIO
import math
import queue
import struct
import sys
import numpy as np
import sounddevice as sd
from threading import Lock
from flask import request
import os

# Blueprint の作成
sustainability_of_voice_bp = Blueprint(
    'sustainability_of_voice', __name__,
    static_folder='../static',
    template_folder='../templates'
)

mic_stream = None
lock = Lock()

class MicrophoneStream:
    def __init__(self, rate, chunk):
        self.rate = rate
        self.chunk = chunk
        self.buff = queue.Queue()

    def open_stream(self):
        self.input_stream = sd.RawInputStream(
            samplerate=self.rate,
            blocksize=self.chunk,
            dtype="int16",
            channels=1,
            callback=self.callback,
        )
        self.input_stream.start()

    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.buff.put(bytes(indata))

    def compute_power(self, indata):
        audio = struct.unpack(f"{len(indata) // 2}h", indata)
        rms = math.sqrt(np.mean(np.square(audio)))
        return 20 * math.log10(rms) if rms > 0.0 else -math.inf
    
def monitor_audio(socketio):
    global mic_stream
    mic_stream = MicrophoneStream(rate=16000, chunk=1024)
    mic_stream.open_stream()

    threshold = 0
    is_above_threshold = False

    while True:
        data = mic_stream.buff.get()
        if data is None:
            break
        power = mic_stream.compute_power(data)

        if power > threshold:
            if not is_above_threshold:
                is_above_threshold = True
                socketio.emit('threshold_exceeded', {'power': power, 'state': 'start'})
        else:
            if is_above_threshold:
                is_above_threshold = False
                socketio.emit('threshold_exceeded', {'power': power, 'state': 'stop'})

# イベントを登録する関数
def register_socket_events(socketio):
    @socketio.on('start_monitoring')
    def handle_start_monitoring():
        print("Monitoring started")
        socketio.start_background_task(target=monitor_audio, socketio=socketio)

    @socketio.on('stop_monitoring')
    def handle_stop_monitoring():
        print("Monitoring stopped")
        global mic_stream
        if mic_stream:
            mic_stream.input_stream.stop()
            mic_stream = None
    
@sustainability_of_voice_bp.route('/')
def index():
    mode = request.args.get('mode', 'normal')
    if mode == 'hard':
        return render_template('hard.html')
    return render_template('normal.html')