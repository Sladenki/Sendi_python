"""
Модуль команд голосового помощника
"""

from .command_processor import CommandProcessor
from .base_command import BaseCommand
from .system_commands import SystemCommands
from .web_commands import WebCommands

__all__ = ['CommandProcessor', 'BaseCommand', 'SystemCommands', 'WebCommands'] 