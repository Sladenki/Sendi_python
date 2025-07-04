"""
Голосовой помощник - основной класс для распознавания речи
"""

import speech_recognition as sr
from PyQt5.QtCore import QThread, pyqtSignal
import sys
import os

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from commands.command_processor import CommandProcessor
from core.tts_engine import TTSEngine


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
        
        # Обработчик команд
        self.command_processor = CommandProcessor()
        
        # TTS движок
        self.tts_engine = None
        
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
    
    def speak(self, text):
        """Произнести текст"""
        try:
            if self.tts_engine and self.tts_engine.isRunning():
                self.tts_engine.stop()
            
            self.tts_engine = TTSEngine(text, self.config)
            self.tts_engine.start()
        except Exception as e:
            print(f"Ошибка TTS: {e}")
    
    def process_command(self, text):
        """Обработать команду"""
        try:
            success, response = self.command_processor.process_command(text)
            
            if success:
                self.speak(response)
                self.status_changed.emit(f"Выполнено: {response}")
            else:
                self.speak("Команда не найдена")
                self.status_changed.emit(f"Ошибка: {response}")
                
        except Exception as e:
            error_msg = f"Ошибка обработки команды: {str(e)}"
            self.speak("Произошла ошибка")
            self.status_changed.emit(error_msg)
    
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
                    
                    # Обрабатываем команду
                    self.command_received.emit(text)
                    self.process_command(text)
                        
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
        if self.tts_engine and self.tts_engine.isRunning():
            self.tts_engine.stop()
    
    def update_config(self, new_config):
        """Обновление конфигурации"""
        self.config.update(new_config)
        self.timeout = self.config.get('timeout', 1)
        self.phrase_time_limit = self.config.get('phrase_time_limit', 5)
        self.ambient_duration = self.config.get('ambient_duration', 1)
        self.language = self.config.get('language', 'ru-RU') 