# RealTimeTranscription-RTT

# RealTimeTranscription-RTT 🎙️➡️📝

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Whisper](https://img.shields.io/badge/OpenAI-Whisper-green.svg)](https://github.com/openai/whisper)

Uma aplicação desktop para transcrição de áudio em tempo real usando modelos Whisper da OpenAI, com interface gráfica intuitiva desenvolvida em PyQt6.

![RTT Screenshot](https://via.placeholder.com/800x450.png?text=RealTimeTranscription+Screenshot)

## 🌟 Características

- ⚡ **Transcrição em tempo real** - Converte fala em texto enquanto você fala
- 🔄 **Processamento em chunks** - Processa o áudio em segmentos de 5 segundos
- 🧠 **Múltiplos modelos Whisper** - Suporte para tiny, base, small, medium e large
- 💻 **Seleção de dispositivo** - Escolha entre CPU ou GPU (CUDA) para processamento
- 🎤 **Seleção de microfone** - Compatível com múltiplos dispositivos de entrada
- 💾 **Gravação de áudio** - Opção para salvar o áudio em formato WAV
- 🌙 **Tema escuro** - Interface com tema dark mode para reduzir fadiga visual
- 🇧🇷 **Suporte ao português** - Otimizado para transcrição em português

## 📋 Requisitos

- Python 3.8 ou superior
- PyQt6
- sounddevice
- numpy
- PyTorch
- OpenAI Whisper
- qdarkstyle

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Ambrosios13/RealTimeTranscription-RTT.git
cd RealTimeTranscription-RTT
```

2. Crie e ative um ambiente virtual (recomendado):
```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute a aplicação:
```bash
python main.py
```

## ⚙️ Configuração

### Modelos Disponíveis
O tamanho do modelo afeta diretamente a qualidade da transcrição e o consumo de recursos:

| Modelo  | Qualidade | RAM | Velocidade |
|---------|-----------|-----|------------|
| tiny    | Básica    | ~1GB  | Rápido     |
| base    | Boa       | ~1GB  | Moderado   |
| small   | Melhor    | ~2GB  | Mais lento |
| medium  | Excelente | ~5GB  | Lento      |
| large   | Superior  | ~10GB | Muito lenta|

### Opções de Processamento
- **CPU**: Funciona em qualquer computador, mas pode ser mais lento
- **GPU (CUDA)**: Requer uma placa NVIDIA compatível, mas oferece velocidade significativamente superior

## 📱 Como Usar

1. **Selecione o hardware**: Escolha entre CPU ou GPU para processamento
2. **Escolha o modelo**: Selecione o tamanho do modelo Whisper
3. **Selecione o microfone**: Escolha o dispositivo de entrada de áudio
4. **Configure a gravação**: Marque a opção para salvar áudio, se desejado
5. **Inicie a transcrição**: Clique em "Iniciar" e comece a falar
6. **Visualize o texto**: Veja a transcrição aparecendo em tempo real
7. **Finalize**: Clique em "Parar" quando terminar

## 🛠️ Estrutura do Projeto

```
RealTimeTranscription-RTT/
├── main.py              # Ponto de entrada da aplicação
├── ui.py                # Interface gráfica do usuário
├── transcriber.py       # Motor de transcrição com Whisper
├── audio_recorder.py    # Captura e processamento de áudio
├── config.py            # Configurações globais
├── .gitignore           # Arquivos ignorados pelo Git
├── LICENSE              # Arquivo de licença MIT
└── README.md            # Este arquivo
```

## 🔍 Detalhes Técnicos

A aplicação funciona dividindo o fluxo de áudio em chunks de 5 segundos, que são processados pelo modelo Whisper para gerar transcrições de texto. A interface gráfica PyQt6 permite uma experiência de usuário fluida enquanto os processos intensivos são executados em threads separadas para evitar o congelamento da interface.

### Processamento de Áudio
- Taxa de amostragem: 16kHz (formato padrão para Whisper)
- Duração do chunk: 5 segundos
- Formato de gravação: WAV mono 16-bit

## 📈 Roadmap de Desenvolvimento

- [ ] Adicionar suporte para mais idiomas
- [ ] Implementar exportação de texto para diversos formatos
- [ ] Adicionar reconhecimento de pontuação automática
- [ ] Implementar identificação de falantes
- [ ] Adicionar opção de tradução em tempo real

## 🤔 Solução de Problemas

**Problema**: Não detecta meu microfone.
**Solução**: Verifique se o microfone está conectado e funcionando. Talvez seja necessário reiniciar a aplicação.

**Problema**: Erro ao carregar modelo Whisper.
**Solução**: Verifique sua conexão com a internet e se há espaço disponível no disco. Os modelos maiores requerem download e espaço substancial.

**Problema**: Transcrição muito lenta.
**Solução**: Tente usar um modelo menor (tiny ou base) ou ative o processamento por GPU se disponível.

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [OpenAI Whisper](https://github.com/openai/whisper) pelo incrível modelo de reconhecimento de fala
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) pela biblioteca de interface gráfica
- [sounddevice](https://python-sounddevice.readthedocs.io/) pela captura de áudio
- [QDarkStyle](https://github.com/ColinDuquesnoy/QDarkStyleSheet) pelo tema escuro
