"""
Утилиты для голосового помощника Sendi
"""

import os
import platform
import subprocess
import psutil
import datetime
from pathlib import Path

class SystemUtils:
    """Утилиты для работы с системой"""
    
    @staticmethod
    def get_system_info():
        """Получение информации о системе"""
        return {
            'os': platform.system(),
            'version': platform.version(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor()
        }
    
    @staticmethod
    def get_desktop_path():
        """Получение пути к рабочему столу"""
        if platform.system() == "Windows":
            return os.path.join(os.path.expanduser("~"), "Desktop")
        elif platform.system() == "Darwin":  # macOS
            return os.path.join(os.path.expanduser("~"), "Desktop")
        else:  # Linux
            return os.path.join(os.path.expanduser("~"), "Desktop")
    
    @staticmethod
    def create_folder(path, name):
        """Создание папки"""
        try:
            full_path = os.path.join(path, name)
            os.makedirs(full_path, exist_ok=True)
            return True, full_path
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def open_file(path):
        """Открытие файла в системе по умолчанию"""
        try:
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", path])
            else:  # Linux
                subprocess.run(["xdg-open", path])
            return True, "Файл открыт"
        except Exception as e:
            return False, str(e)

class CommandProcessor:
    """Обработчик команд"""
    
    def __init__(self):
        self.commands = {
            'открой браузер': self.open_browser,
            'создай папку': self.create_folder,
            'создай папку на рабочем столе': self.create_desktop_folder,
            'время': self.get_time,
            'дата': self.get_date,
            'система': self.get_system_info,
            'процессы': self.get_processes
        }
    
    def process_command(self, command_text):
        """Обработка команды"""
        command_text = command_text.lower().strip()
        
        for key, func in self.commands.items():
            if key in command_text:
                return func(command_text)
        
        return False, "Команда не распознана"
    
    def open_browser(self, command):
        """Открытие браузера"""
        try:
            import webbrowser
            webbrowser.open("https://www.google.com")
            return True, "Браузер открыт"
        except Exception as e:
            return False, f"Ошибка при открытии браузера: {str(e)}"
    
    def create_folder(self, command):
        """Создание папки"""
        try:
            desktop_path = SystemUtils.get_desktop_path()
            folder_name = f"Sendi_Folder_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            success, result = SystemUtils.create_folder(desktop_path, folder_name)
            
            if success:
                return True, f"Папка {folder_name} создана на рабочем столе"
            else:
                return False, f"Ошибка при создании папки: {result}"
        except Exception as e:
            return False, f"Ошибка при создании папки: {str(e)}"
    
    def create_desktop_folder(self, command):
        """Создание папки на рабочем столе (алиас)"""
        return self.create_folder(command)
    
    def get_time(self, command):
        """Получение текущего времени"""
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return True, f"Текущее время: {current_time}"
    
    def get_date(self, command):
        """Получение текущей даты"""
        current_date = datetime.datetime.now().strftime("%d.%m.%Y")
        return True, f"Сегодня: {current_date}"
    
    def get_system_info(self, command):
        """Получение информации о системе"""
        info = SystemUtils.get_system_info()
        return True, f"ОС: {info['os']}, Процессор: {info['processor']}"
    
    def get_processes(self, command):
        """Получение списка процессов"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    if proc.info['cpu_percent'] > 5.0:  # Только активные процессы
                        processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Сортировка по использованию CPU
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            
            if processes:
                top_processes = processes[:5]  # Топ-5 процессов
                result = "Активные процессы:\n"
                for proc in top_processes:
                    result += f"- {proc['name']}: {proc['cpu_percent']:.1f}% CPU\n"
                return True, result
            else:
                return True, "Нет активных процессов"
        except Exception as e:
            return False, f"Ошибка при получении процессов: {str(e)}"

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
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'russian' in voice.name.lower() or 'ru' in voice.id.lower():
                return voice.id
        return voices[0].id if voices else None

class Logger:
    """Система логирования"""
    
    def __init__(self, log_file=None):
        self.log_file = log_file or "sendi.log"
        self.log_entries = []
    
    def log(self, level, source, message):
        """Добавление записи в лог"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{level}] {source}: {message}"
        
        # Добавление в память
        self.log_entries.append(entry)
        
        # Запись в файл
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(entry + '\n')
        except Exception as e:
            print(f"Ошибка записи в лог: {e}")
        
        return entry
    
    def get_recent_logs(self, count=50):
        """Получение последних записей"""
        return self.log_entries[-count:] if self.log_entries else []
    
    def clear_logs(self):
        """Очистка логов"""
        self.log_entries.clear()
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("")
        except Exception as e:
            print(f"Ошибка очистки лога: {e}")
    
    def export_logs(self, filename=None):
        """Экспорт логов в файл"""
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sendi_logs_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for entry in self.log_entries:
                    f.write(entry + '\n')
            return True, f"Логи экспортированы в {filename}"
        except Exception as e:
            return False, f"Ошибка экспорта: {str(e)}" 