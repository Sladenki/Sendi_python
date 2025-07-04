"""
Базовый класс для команд голосового помощника
"""

from abc import ABC, abstractmethod
from typing import Tuple, Any


class BaseCommand(ABC):
    """Базовый класс для всех команд"""
    
    def __init__(self, name: str, description: str, keywords: list):
        self.name = name
        self.description = description
        self.keywords = keywords
    
    @abstractmethod
    def execute(self, command_text: str) -> Tuple[bool, str]:
        """
        Выполнение команды
        
        Args:
            command_text: Текст команды
            
        Returns:
            Tuple[bool, str]: (успех, результат)
        """
        pass
    
    def matches(self, command_text: str) -> bool:
        """
        Проверка, подходит ли команда к тексту
        
        Args:
            command_text: Текст команды
            
        Returns:
            bool: True если команда подходит
        """
        command_lower = command_text.lower()
        return any(keyword in command_lower for keyword in self.keywords)
    
    def get_help(self) -> str:
        """
        Получение справки по команде
        
        Returns:
            str: Описание команды
        """
        return f"{self.name}: {self.description}" 