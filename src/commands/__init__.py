"""
Модуль команд голосового помощника
"""

from .command_processor import CommandProcessor
from .base_command import BaseCommand
from .system_commands import SystemCommands
# from .browser_commands import BrowserCommands

__all__ = ['CommandProcessor', 'BaseCommand', 'SystemCommands', 'BrowserCommands'] 