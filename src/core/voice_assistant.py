"""
Голосовой помощник - основной класс для распознавания речи
"""

import speech_recognition as sr
from PyQt5.QtCore import QThread, pyqtSignal


class VoiceAssistant(QThread):
    """Поток для работы с голосовым помощником"""
    command_received = pyqtSignal(str)
    status_changed = pyqtSignal(str)
    speech_recognized = pyqtSignal(str)
    
    def __init__(self, config=None):
        super().__init__()
        self.running = True
        self.config = config or {}
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Настройка параметров распознавания
        self.timeout = self.config.get('timeout', 1)
        self.phrase_time_limit = self.config.get('phrase_time_limit', 5)
        self.ambient_duration = self.config.get('ambient_duration', 1)
        self.language = self.config.get('language', 'ru-RU')
        
        # Настройка микрофона
        self._setup_microphone()
    
    def _setup_microphone(self):
        """Настройка микрофона"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(
                    source, 
                    duration=self.ambient_duration
                )
        except Exception as e:
            print(f"Ошибка настройки микрофона: {e}")
    
    def run(self):
        """Основной цикл распознавания речи"""
        self.status_changed.emit("Ожидание команды...")
        
        while self.running:
            try:
                with self.microphone as source:
                    self.status_changed.emit("Слушаю...")
                    audio = self.recognizer.listen(
                        source, 
                        timeout=self.timeout, 
                        phrase_time_limit=self.phrase_time_limit
                    )
                
                try:
                    text = self.recognizer.recognize_google(
                        audio, 
                        language=self.language
                    ).lower()
                    
                    self.status_changed.emit(f"Распознано: {text}")
                    self.speech_recognized.emit(text)
                    
                    # Обрабатываем команду в любом случае
                    self.command_received.emit(text)
                    if "sendi" in text:
                        self.status_changed.emit("Команда получена")
                    else:
                        self.status_changed.emit("Команда обработана")
                        
                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    self.status_changed.emit("Ошибка распознавания")
                    
            except sr.WaitTimeoutError:
                pass
            except Exception as e:
                self.status_changed.emit(f"Ошибка: {str(e)}")
    
    def stop(self):
        """Остановка потока"""
        self.running = False
    
    def update_config(self, new_config):
        """Обновление конфигурации"""
        self.config.update(new_config)
        self.timeout = self.config.get('timeout', 1)
        self.phrase_time_limit = self.config.get('phrase_time_limit', 5)
        self.ambient_duration = self.config.get('ambient_duration', 1)
        self.language = self.config.get('language', 'ru-RU') 