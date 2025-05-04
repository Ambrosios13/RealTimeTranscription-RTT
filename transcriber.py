import threading
import whisper
import torch
import queue
import traceback

class Transcriber:
    def __init__(self, audio_queue, result_callback, device_type="cpu", model_name="base"):
        self.audio_queue = audio_queue
        self.result_callback = result_callback
        self.device = device_type
        self.running = True
        self.thread = None
        # Carregamento do modelo movido para um método separado
        self.model = None
        
    def load_model(self, model_name):
        return whisper.load_model(model_name, device=self.device)
        
    def start(self, model_name="base"):
        # Inicializa o modelo em thread separada para não bloquear a interface
        loading_thread = threading.Thread(target=self._load_model_thread, args=(model_name,), daemon=True)
        loading_thread.start()
    
    def _load_model_thread(self, model_name):
        self.model = self.load_model(model_name)
        self.running = True
        # Inicia a thread de transcrição só depois que o modelo foi carregado
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        
    def _run(self):
        while self.running:
            try:
                # Tenta obter dados da fila com timeout de 1 segundo
                try:
                    chunk = self.audio_queue.get(timeout=1)
                except queue.Empty:
                    # Se não há dados na fila, simplesmente continua o loop
                    continue
                
                # Processa o áudio e realiza a transcrição
                try:
                    audio = whisper.pad_or_trim(chunk)
                    mel = whisper.log_mel_spectrogram(audio).to(self.device)
                    result = self.model.decode(mel, language="pt", fp16=(self.device == "cuda"))
                    self.result_callback(result.text)
                except Exception as e:
                    if self.running:  # Ignora erros se estiver parando
                        print(f"Erro na transcrição do áudio: {e}")
                        # Imprime stack trace para facilitar debug
                        traceback.print_exc()
                    
            except Exception as e:
                if self.running:  # Ignora erros se estiver parando
                    print(f"Erro inesperado no loop de transcrição: {e}")
                    traceback.print_exc()
                    
    def stop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)
