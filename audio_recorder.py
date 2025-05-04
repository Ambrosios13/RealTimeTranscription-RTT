import numpy as np
import sounddevice as sd
import wave
import os
from datetime import datetime

class AudioRecorder:
    def __init__(self, audio_queue, device=None, save_audio=False, save_path=None):
        self.audio_queue = audio_queue
        self.device = device
        self.stream = None
        self.buffer = np.zeros((0,), dtype=np.float32)
        self.audio_rate = 16000
        self.chunk_duration = 5
        self.chunk_samples = self.audio_rate * self.chunk_duration

        # Opções para salvar o áudio
        self.save_audio = save_audio
        self.save_path = save_path
        self.full_audio_buffer = None
        self.wave_file = None

    def _callback(self, indata, frames, time, status):
        if status:
            print("⚠️", status)
        
        # Adiciona dados ao buffer de processamento
        self.buffer = np.concatenate((self.buffer, indata[:, 0]))
        
        # Salva áudio completo se necessário
        if self.save_audio and self.full_audio_buffer is not None:
            self.full_audio_buffer = np.concatenate((self.full_audio_buffer, indata[:, 0]))
        
        # Processa chunks para a transcrição
        while len(self.buffer) >= self.chunk_samples:
            chunk, self.buffer = self.buffer[:self.chunk_samples], self.buffer[self.chunk_samples:]
            self.audio_queue.put(chunk.copy())

    def start(self):
        # Inicializa buffer para gravação completa se ativado
        if self.save_audio:
            self.full_audio_buffer = np.zeros((0,), dtype=np.float32)
            
            # Cria pasta de destino se não existir
            if self.save_path and not os.path.exists(self.save_path):
                os.makedirs(self.save_path)

        # Inicia o stream de áudio
        self.stream = sd.InputStream(
            samplerate=self.audio_rate,
            channels=1,
            dtype='float32',
            callback=self._callback,
            device=self.device
        )
        self.stream.start()

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
        
        # Salva o arquivo de áudio se a opção estiver ativada
        if self.save_audio and self.full_audio_buffer is not None:
            self._save_audio_file()
    
    def _save_audio_file(self):
        try:
            # Gera nome do arquivo com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"
            
            # Define caminho completo
            if self.save_path:
                filepath = os.path.join(self.save_path, filename)
            else:
                filepath = filename
            
            # Converte para int16 (formato padrão para WAV)
            audio_data = (self.full_audio_buffer * 32767).astype(np.int16)
            
            # Salva como arquivo WAV
            with wave.open(filepath, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)  # 2 bytes para int16
                wf.setframerate(self.audio_rate)
                wf.writeframes(audio_data.tobytes())
            
            print(f"Áudio salvo em: {filepath}")
            return filepath
        except Exception as e:
            print(f"Erro ao salvar áudio: {e}")
            return None