var threshold = 0;
var timer;
var elapsedTime = 0;

function setThreshold() {
  const dBValue = parseInt(document.getElementById('threshold').value, 10);
  threshold = dBValue;
  resetTimer();
}

socket.on('threshold_exceeded', function(data) {
  if (data.state === 'start') {
    startTimer();
  } else if (data.state === 'stop') {
    stopTimer();
  }
});

function startTimer() {
  if (!timer) {
    timer = setInterval(() => {
      elapsedTime += 0.01;
      document.getElementById('elapsedTime').innerText =
        '経過時間: ' + elapsedTime.toFixed(2) + '秒';
    }, 10);
  }
}

function stopTimer() {
  clearInterval(timer);
  timer = null;
}

function resetTimer() {
  stopTimer();
  elapsedTime = 0;
  document.getElementById('elapsedTime').innerText = '経過時間: 0秒';
}