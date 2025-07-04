"""
Конфигурация приложения Sendi
"""

import os
import json
from pathlib import Path

class Config:
    """Класс для управления конфигурацией приложения"""
    
    def __init__(self, config_file="sendi_config.json"):
        self.config_file = config_file
        self.default_config = {
            "voice": {
                "rate": 150,
                "volume": 0.8,
                "voice_id": None,
                "language": "ru-RU"
            },
            "recognition": {
                "timeout": 1,
                "phrase_time_limit": 5,
                "ambient_duration": 1,
                "language": "ru-RU"
            },
            "ui": {
                "window_width": 800,
                "window_height": 600,
                "theme": "dark",
                "accent_color": "#8e2de2",
                "background_color": "#121212"
            },
            "logging": {
                "log_file": "sendi.log",
                "max_log_entries": 1000,
                "auto_export": False,
                "export_interval": 24  # часы
            },
            "commands": {
                "wake_word": "sendi",
                "auto_start": False,
                "sound_feedback": True
            }
        }
        self.config = self.load_config()
    
    def load_config(self):
        """Загрузка конфигурации из файла"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Объединение с дефолтными настройками
                    return self.merge_configs(self.default_config, config)
            else:
                # Создание файла с дефолтными настройками
                self.save_config(self.default_config)
                return self.default_config
        except Exception as e:
            print(f"Ошибка загрузки конфигурации: {e}")
            return self.default_config
    
    def save_config(self, config=None):
        """Сохранение конфигурации в файл"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Ошибка сохранения конфигурации: {e}")
            return False
    
    def merge_configs(self, default, user):
        """Объединение дефолтной и пользовательской конфигурации"""
        result = default.copy()
        
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self.merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def get(self, key, default=None):
        """Получение значения конфигурации по ключу"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key, value):
        """Установка значения конфигурации по ключу"""
        keys = key.split('.')
        config = self.config
        
        # Навигация к нужному уровню
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Установка значения
        config[keys[-1]] = value
        
        # Сохранение
        return self.save_config()
    
    def reset_to_default(self):
        """Сброс к дефолтным настройкам"""
        self.config = self.default_config.copy()
        return self.save_config()
    
    def get_voice_settings(self):
        """Получение настроек голоса"""
        return self.get('voice', {})
    
    def get_recognition_settings(self):
        """Получение настроек распознавания"""
        return self.get('recognition', {})
    
    def get_ui_settings(self):
        """Получение настроек интерфейса"""
        return self.get('ui', {})
    
    def get_logging_settings(self):
        """Получение настроек логирования"""
        return self.get('logging', {})
    
    def get_command_settings(self):
        """Получение настроек команд"""
        return self.get('commands', {})

# Глобальный экземпляр конфигурации
config = Config()

# Функции для удобного доступа к настройкам
def get_voice_rate():
    """Получение скорости речи"""
    return config.get('voice.rate', 150)

def get_voice_volume():
    """Получение громкости речи"""
    return config.get('voice.volume', 0.8)

def get_recognition_timeout():
    """Получение таймаута распознавания"""
    return config.get('recognition.timeout', 1)

def get_wake_word():
    """Получение слова активации"""
    return config.get('commands.wake_word', 'sendi')

def get_window_size():
    """Получение размера окна"""
    return (
        config.get('ui.window_width', 800),
        config.get('ui.window_height', 600)
    )

def get_accent_color():
    """Получение цвета акцента"""
    return config.get('ui.accent_color', '#8e2de2')

def get_background_color():
    """Получение цвета фона"""
    return config.get('ui.background_color', '#121212') 