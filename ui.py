from PyQt6.QtWidgets import (
    QMainWindow, QTextEdit, QPushButton,
    QVBoxLayout, QWidget, QComboBox, QLabel, QMessageBox, QProgressBar,
    QHBoxLayout, QCheckBox, QFileDialog, QLineEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
import sounddevice as sd
import torch
import queue
import os
from config import WHISPER_MODELS
from audio_recorder import AudioRecorder
from transcriber import Transcriber

class ModelLoaderThread(QThread):
    """Thread para carregar modelo sem bloquear a UI"""
    finished = pyqtSignal()
    
    def __init__(self, transcriber, model_name):
        super().__init__()
        self.transcriber = transcriber
        self.model_name = model_name
        
    def run(self):
        self.transcriber.start(self.model_name)
        self.finished.emit()

class TranscriptionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RealTimeTranscription")
        self.setMinimumSize(600, 500)  # Aumentado para acomodar novos controles

        self.audio_queue = queue.Queue()
        self.transcriber = None
        self.recorder = None
        self.audio_save_path = os.path.expanduser("~/Gravações")
        
        # Layout e componentes
        self._setup_ui()
        
        # Signals
        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)
        self.browse_button.clicked.connect(self.browse_save_location)

        # Popula lista de dispositivos
        self.populate_devices()
        
    def _setup_ui(self):
        # Widgets de configuração
        self.device_label = QLabel("💻 Selecione o dispositivo:")
        self.device_choice = QComboBox()
        self.device_choice.addItem("CPU", "cpu")
        if torch.cuda.is_available():
            self.device_choice.addItem("GPU (CUDA)", "cuda")

        self.model_label = QLabel("📦 Selecione o modelo Whisper:")
        self.model_selector = QComboBox()
        for model in WHISPER_MODELS:
            self.model_selector.addItem(model)

        self.mic_label = QLabel("🎤 Selecione o microfone:")
        self.device_selector = QComboBox()

        # Opções para salvar áudio
        self.save_audio_checkbox = QCheckBox("Salvar áudio gravado")
        self.save_audio_checkbox.setChecked(True)
        
        # Layout para pasta de salvamento
        save_path_layout = QHBoxLayout()
        self.save_path_label = QLabel("📂 Local para salvar:")
        self.save_path_edit = QLineEdit(self.audio_save_path)
        self.browse_button = QPushButton("Procurar...")
        save_path_layout.addWidget(self.save_path_label)
        save_path_layout.addWidget(self.save_path_edit, 1)  # 1 = stretch factor
        save_path_layout.addWidget(self.browse_button)

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        
        # Barra de progresso para carregamento do modelo
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        self.start_button = QPushButton("Iniciar")
        self.stop_button = QPushButton("Parar")
        self.stop_button.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.device_label)
        layout.addWidget(self.device_choice)
        layout.addWidget(self.model_label)
        layout.addWidget(self.model_selector)
        layout.addWidget(self.mic_label)
        layout.addWidget(self.device_selector)
        layout.addWidget(self.save_audio_checkbox)
        layout.addLayout(save_path_layout)
        layout.addWidget(self.text_area)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def populate_devices(self):
        devices = sd.query_devices()
        input_devices = [
            (i, d['name']) for i, d in enumerate(devices)
            if d['max_input_channels'] > 0
        ]
        for idx, name in input_devices:
            self.device_selector.addItem(f"{name}", idx)

    def browse_save_location(self):
        folder = QFileDialog.getExistingDirectory(
            self, 
            "Selecionar pasta para salvar gravações",
            self.save_path_edit.text()
        )
        if folder:
            self.save_path_edit.setText(folder)
            self.audio_save_path = folder

    def start_recording(self):
        # Desativa botões durante inicialização
        self.start_button.setEnabled(False)
        self.model_selector.setEnabled(False)
        self.device_choice.setEnabled(False)
        self.device_selector.setEnabled(False)
        self.save_audio_checkbox.setEnabled(False)
        self.save_path_edit.setEnabled(False)
        self.browse_button.setEnabled(False)
        
        # Mostra barra de progresso
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_progress)
        self.timer.start(100)
        
        self.text_area.append("🔄 Carregando modelo, aguarde...")
        
        device_index = self.device_selector.currentData()
        device_type = self.device_choice.currentData()
        model_name = self.model_selector.currentText()
        save_audio = self.save_audio_checkbox.isChecked()
        save_path = self.save_path_edit.text() if save_audio else None

        # Inicializa componentes
        self.transcriber = Transcriber(self.audio_queue, self.display_result, device_type)
        self.recorder = AudioRecorder(
            self.audio_queue, 
            device=device_index,
            save_audio=save_audio,
            save_path=save_path
        )
        
        # Carrega modelo em thread separada
        self.loader_thread = ModelLoaderThread(self.transcriber, model_name)
        self.loader_thread.finished.connect(self._on_model_loaded)
        self.loader_thread.start()

    def _update_progress(self):
        current = self.progress_bar.value()
        if current < 95:  # Limita a 95% até que o modelo realmente carregue
            self.progress_bar.setValue(current + 5)
    
    def _on_model_loaded(self):
        self.timer.stop()
        self.progress_bar.setValue(100)
        self.progress_bar.setVisible(False)
        
        # Inicia gravação
        self.recorder.start()
        
        # Indica ao usuário se está salvando áudio
        if self.save_audio_checkbox.isChecked():
            self.text_area.append(f"🎙️ Modelo carregado. Gravação iniciada (salvando áudio em {self.save_path_edit.text()})...\n")
        else:
            self.text_area.append("🎙️ Modelo carregado. Gravação iniciada (sem salvar áudio)...\n")
        
        self.stop_button.setEnabled(True)

    def stop_recording(self):
        # Para componentes
        if self.recorder:
            self.recorder.stop()
        if self.transcriber:
            self.transcriber.stop()
            
        # Reseta UI
        self.text_area.append("⏹️ Gravação finalizada.\n")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.model_selector.setEnabled(True)
        self.device_choice.setEnabled(True)
        self.device_selector.setEnabled(True)
        self.save_audio_checkbox.setEnabled(True)
        self.save_path_edit.setEnabled(True)
        self.browse_button.setEnabled(True)

    def display_result(self, text):
        if text.strip():  # Evita adicionar texto vazio
            self.text_area.append(f"> {text}")
