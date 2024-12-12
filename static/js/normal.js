var socket = io.connect('wss://minigame-template-571979192050.asia-northeast1.run.app', {
  transports: ['websocket', 'polling'],  // WebSocket と polling を明示的に指定
  upgrade: true                          // WebSocket にアップグレードを許可
});
var threshold = 0;
var timer;
var elapsedTime = 0;
var isDetecting = false; 
var isDetecting = false;
var hasExceededThreshold = false;

// 音声入力を取得してサーバーに送信
navigator.mediaDevices.getUserMedia({ audio: true })
  .then(function(stream) {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const source = audioContext.createMediaStreamSource(stream);
    const processor = audioContext.createScriptProcessor(1024, 1, 1);

    source.connect(processor);
    processor.connect(audioContext.destination);

    processor.onaudioprocess = function(event) {
      const input = event.inputBuffer.getChannelData(0);
      const rms = Math.sqrt(input.reduce((sum, value) => sum + value * value, 0) / input.length);
      // dB値を計算し、正の値に変換（基準値を調整）
      const dB = 20 * Math.log10(rms) + 100; // +100 を加えて正の値にシフト

      // 値が0未満の場合は0にする
      const normalizedDB = Math.max(0, dB);
      
      // サーバーに音声データを送信
      socket.emit('audio_data', { power: normalizedDB });
    };
  })
  .catch(function(err) {
    console.error('マイクへのアクセスに失敗しました:', err);
  });

// サーバーからのデータを受信
socket.on('audio_data', function(data) {
  console.log('Received audio data:', data);
  var dB = data.power;
  document.getElementById('volume').style.width = (dB / 100 * 100) + '%';
});

socket.on('disconnect', function() {
  console.log('Disconnected from server');
  socket.emit('stop_monitoring');
});

function dBToLinear(dB) {
  return Math.pow(10, dB / 20);
}

function setThreshold() {
  const dBValue = parseFloat(document.getElementById('threshold').value);
  threshold = dBValue;
  resetTimer();

  //しきい値が設定されたら音声認識を開始
  if(threshold > 0){
    socket.emit('start_monitoring');
  }
}

function startTimer() {
  timer = setInterval(() => {
    elapsedTime += 0.01; // 0.01秒ずつ増加
    const elapsedTimeElement = document.getElementById('elapsedTime');
    if (elapsedTimeElement) {
      elapsedTimeElement.innerText = '経過時間: ' + elapsedTime.toFixed(2) + '秒'; // 小数第2位まで表示
    }
  }, 10); // 10ミリ秒ごとに更新
}

function stopTimer() {
  clearInterval(timer);
  timer = null;
}

function resetTimer() {
  stopTimer();
  elapsedTime = 0;
  const elapsedTimeElement = document.getElementById('elapsedTime');
  if (elapsedTimeElement) {
    elapsedTimeElement.innerText = '経過時間: 0秒';
  }
}

function beginDetect() {
  if (threshold > 0) {
    isDetecting = true; // 開始ボタンが押されたら動作を開始
    hasExceededThreshold = false; // フラグをリセット
    socket.emit('start_monitoring');
  } else {
    alert('しきい値を設定してください。');
  }
}

function goBack() {
  window.location.href = "../../index.html";
}