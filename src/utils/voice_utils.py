"""
Утилиты для работы с голосом
"""

import pyttsx3


class VoiceUtils:
    """Утилиты для работы с голосом"""
    
    @staticmethod
    def format_response(text):
        """Форматирование ответа для голосового вывода"""
        # Убираем лишние символы и форматируем текст
        text = text.replace('\n', ' ')
        text = text.replace('  ', ' ')
        return text.strip()
    
    @staticmethod
    def get_voice_settings():
        """Получение настроек голоса"""
        return {
            'rate': 150,      # Скорость речи
            'volume': 0.8,    # Громкость
            'voice_id': None  # ID голоса (будет установлен автоматически)
        }
    
    @staticmethod
    def find_russian_voice(engine):
        """Поиск русского голоса"""
        try:
            voices = engine.getProperty('voices')
            for voice in voices:
                if 'russian' in voice.name.lower() or 'ru' in voice.id.lower():
                    return voice.id
            return voices[0].id if voices else None
        except Exception:
            return None
    
    @staticmethod
    def get_available_voices():
        """Получение списка доступных голосов"""
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            voice_list = []
            
            for voice in voices:
                voice_list.append({
                    'id': voice.id,
                    'name': voice.name,
                    'languages': voice.languages if hasattr(voice, 'languages') else [],
                    'gender': voice.gender if hasattr(voice, 'gender') else 'Unknown'
                })
            
            return voice_list
        except Exception as e:
            print(f"Ошибка получения голосов: {e}")
            return []
    
    @staticmethod
    def test_voice(text="Тест голоса", voice_id=None, rate=150, volume=0.8):
        """Тестирование голоса"""
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', rate)
            engine.setProperty('volume', volume)
            
            if voice_id:
                engine.setProperty('voice', voice_id)
            
            engine.say(text)
            engine.runAndWait()
            return True
        except Exception as e:
            print(f"Ошибка тестирования голоса: {e}")
            return False 