class VolumeProcessor extends AudioWorkletProcessor {
    process(inputs) {
      const input = inputs[0];
      if (input.length > 0) {
        const channelData = input[0];
        const rms = Math.sqrt(channelData.reduce((sum, val) => sum + val ** 2, 0) / channelData.length);
        const volume = Math.min(1, rms); // 0.0 ～ 1.0 の範囲で正規化
        this.port.postMessage({ volume });
      }
      return true;
    }
  }
  
  registerProcessor('volume-processor', VolumeProcessor);