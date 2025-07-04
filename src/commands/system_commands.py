"""
Системные команды голосового помощника
"""

import datetime
import webbrowser
from typing import Tuple
import sys
import os

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .base_command import BaseCommand
from utils.system_utils import SystemUtils


class TimeCommand(BaseCommand):
    """Команда для получения времени"""
    
    def __init__(self):
        super().__init__(
            name="Время",
            description="Показывает текущее время",
            keywords=["время", "который час", "сколько времени"]
        )
    
    def execute(self, command_text: str) -> Tuple[bool, str]:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return True, f"Текущее время: {current_time}"


class DateCommand(BaseCommand):
    """Команда для получения даты"""
    
    def __init__(self):
        super().__init__(
            name="Дата",
            description="Показывает текущую дату",
            keywords=["дата", "какое число", "сегодня"]
        )
    
    def execute(self, command_text: str) -> Tuple[bool, str]:
        current_date = datetime.datetime.now().strftime("%d.%m.%Y")
        return True, f"Сегодня: {current_date}"


class SystemInfoCommand(BaseCommand):
    """Команда для получения информации о системе"""
    
    def __init__(self):
        super().__init__(
            name="Система",
            description="Показывает информацию о системе",
            keywords=["система", "информация о системе", "системная информация"]
        )
    
    def execute(self, command_text: str) -> Tuple[bool, str]:
        info = SystemUtils.get_system_info()
        return True, f"ОС: {info['os']}, Процессор: {info['processor']}"


class CreateFolderCommand(BaseCommand):
    """Команда для создания папки"""
    
    def __init__(self):
        super().__init__(
            name="Создать папку",
            description="Создает папку на рабочем столе",
            keywords=["создай папку", "создать папку", "новая папка"]
        )
    
    def execute(self, command_text: str) -> Tuple[bool, str]:
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


class OpenBrowserCommand(BaseCommand):
    """Команда для открытия браузера"""
    
    def __init__(self):
        super().__init__(
            name="Открыть браузер",
            description="Открывает веб-браузер",
            keywords=["открой браузер", "открыть браузер", "браузер"]
        )
    
    def execute(self, command_text: str) -> Tuple[bool, str]:
        try:
            webbrowser.open("https://www.google.com")
            return True, "Браузер открыт"
        except Exception as e:
            return False, f"Ошибка при открытии браузера: {str(e)}"


class ProcessesCommand(BaseCommand):
    """Команда для получения списка процессов"""
    
    def __init__(self):
        super().__init__(
            name="Процессы",
            description="Показывает активные процессы",
            keywords=["процессы", "активные процессы", "задачи"]
        )
    
    def execute(self, command_text: str) -> Tuple[bool, str]:
        try:
            import psutil
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


class SystemCommands:
    """Коллекция системных команд"""
    
    def __init__(self):
        self.commands = [
            TimeCommand(),
            DateCommand(),
            SystemInfoCommand(),
            CreateFolderCommand(),
            OpenBrowserCommand(),
            ProcessesCommand()
        ]
    
    def get_all_commands(self):
        """Получение всех команд"""
        return self.commands
    
    def find_command(self, command_text: str):
        """Поиск подходящей команды"""
        for command in self.commands:
            if command.matches(command_text):
                return command
        return None 