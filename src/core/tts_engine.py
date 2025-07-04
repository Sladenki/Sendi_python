"""
Движок синтеза речи (Text-to-Speech)
"""

import pyttsx3
from PyQt5.QtCore import QThread
import sys
import os

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.voice_utils import VoiceUtils


class TTSEngine(QThread):
    """Поток для синтеза речи"""
    
    def __init__(self, text, config=None):
        super().__init__()
        self.text = text
        self.config = config or {}
        self.engine = None
    
    def run(self):
        """Синтез речи"""
        try:
            self.engine = pyttsx3.init()
            
            # Получение настроек голоса
            settings = VoiceUtils.get_voice_settings()
            if self.config:
                settings.update(self.config)
            
            self.engine.setProperty('rate', settings.get('rate', 150))
            self.engine.setProperty('volume', settings.get('volume', 0.8))
            
            # Поиск русского голоса
            voice_id = VoiceUtils.find_russian_voice(self.engine)
            if voice_id:
                self.engine.setProperty('voice', voice_id)
            
            # Форматирование текста
            formatted_text = VoiceUtils.format_response(self.text)
            
            self.engine.say(formatted_text)
            self.engine.runAndWait()
            
        except Exception as e:
            print(f"Ошибка TTS: {e}")
        finally:
            if self.engine:
                self.engine.stop()
    
    def stop(self):
        """Остановка синтеза"""
        if self.engine:
            self.engine.stop()
        self.terminate()
        self.wait() 