"""
Обработчик команд голосового помощника
"""

from typing import Tuple
from .system_commands import SystemCommands
from .web_commands import WebCommands


class CommandProcessor:
    """Обработчик команд"""
    
    def __init__(self):
        self.system_commands = SystemCommands()
        self.web_commands = WebCommands()
        self.all_commands = (
            self.system_commands.get_all_commands() + 
            self.web_commands.get_all_commands()
        )
    
    def process_command(self, command_text: str) -> Tuple[bool, str]:
        """
        Обработка команды
        
        Args:
            command_text: Текст команды
            
        Returns:
            Tuple[bool, str]: (успех, результат)
        """
        command_text = command_text.lower().strip()
        
        # Поиск подходящей команды
        for command in self.all_commands:
            if command.matches(command_text):
                return command.execute(command_text)
        
        return False, "Команда не распознана"
    
    def get_available_commands(self) -> list:
        """
        Получение списка доступных команд
        
        Returns:
            list: Список команд с описанием
        """
        return [command.get_help() for command in self.all_commands]
    
    def add_command(self, command):
        """
        Добавление новой команды
        
        Args:
            command: Экземпляр команды
        """
        self.all_commands.append(command)
    
    def remove_command(self, command_name: str):
        """
        Удаление команды
        
        Args:
            command_name: Название команды
        """
        self.all_commands = [
            cmd for cmd in self.all_commands 
            if cmd.name.lower() != command_name.lower()
        ]
    
    def get_command_help(self, command_name: str) -> str:
        """
        Получение справки по конкретной команде
        
        Args:
            command_name: Название команды
            
        Returns:
            str: Справка по команде
        """
        for command in self.all_commands:
            if command.name.lower() == command_name.lower():
                return command.get_help()
        return "Команда не найдена" 