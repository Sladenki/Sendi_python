"""
Системные утилиты для работы с ОС
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
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'hostname': platform.node()
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
    
    @staticmethod
    def get_memory_info():
        """Получение информации о памяти"""
        try:
            memory = psutil.virtual_memory()
            return {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'percent': memory.percent
            }
        except Exception:
            return None
    
    @staticmethod
    def get_cpu_info():
        """Получение информации о процессоре"""
        try:
            return {
                'count': psutil.cpu_count(),
                'percent': psutil.cpu_percent(interval=1),
                'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
            }
        except Exception:
            return None
    
    @staticmethod
    def get_disk_info():
        """Получение информации о дисках"""
        try:
            disk = psutil.disk_usage('/')
            return {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent
            }
        except Exception:
            return None 