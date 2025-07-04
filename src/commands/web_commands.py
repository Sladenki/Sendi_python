"""
Веб-команды и команды для приложений
"""

import webbrowser
import os
import subprocess
from typing import Tuple
from .base_command import BaseCommand


class CheckEmailCommand(BaseCommand):
    """Команда для проверки почты"""
    
    def __init__(self):
        super().__init__(
            name="Проверь почту",
            description="Открывает почту Mail.ru",
            keywords=["проверь почту", "почта", "майл", "email", "письма"]
        )
    
    def execute(self, command_text: str) -> Tuple[bool, str]:
        try:
            url = "https://e.mail.ru/inbox/?back=1&afterReload=1"
            webbrowser.open(url)
            return True, "Почта Mail.ru открыта"
        except Exception as e:
            return False, f"Ошибка при открытии почты: {str(e)}"


class OpenTelegramCommand(BaseCommand):
    """Команда для открытия Telegram"""
    
    def __init__(self):
        super().__init__(
            name="Открой Телеграм",
            description="Открывает Telegram Desktop",
            keywords=["открой телеграм", "телеграм", "telegram"]
        )
    
    def execute(self, command_text: str) -> Tuple[bool, str]:
        try:
            # Попытка найти Telegram в стандартных путях
            telegram_paths = [
                os.path.expanduser("~/AppData/Roaming/Telegram Desktop/Telegram.exe"),
                "C:/Users/Public/Desktop/Telegram Desktop.lnk",
                "C:/Program Files/Telegram Desktop/Telegram.exe",
                "C:/Program Files (x86)/Telegram Desktop/Telegram.exe"
            ]
            
            for path in telegram_paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    return True, "Telegram Desktop открыт"
            
            # Если не найден в стандартных путях, попробуем через браузер
            webbrowser.open("https://web.telegram.org")
            return True, "Telegram Web открыт в браузере"
            
        except Exception as e:
            return False, f"Ошибка при открытии Telegram: {str(e)}"


class PlayMusicCommand(BaseCommand):
    """Команда для включения музыки"""
    
    def __init__(self):
        super().__init__(
            name="Включи музыку",
            description="Открывает OperaGX и Spotify",
            keywords=["включи музыку", "музыка", "спотифай", "spotify", "опера"]
        )
    
    def execute(self, command_text: str) -> Tuple[bool, str]:
        try:
            results = []
            
            # Открытие OperaGX
            opera_paths = [
                os.path.expanduser("~/AppData/Local/Programs/Opera GX/launcher.exe"),
                "C:/Program Files/Opera GX/launcher.exe",
                "C:/Program Files (x86)/Opera GX/launcher.exe"
            ]
            
            opera_opened = False
            for path in opera_paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    results.append("OperaGX")
                    opera_opened = True
                    break
            
            if not opera_opened:
                # Если OperaGX не найден, откроем обычный браузер
                webbrowser.open("https://www.opera.com/gx")
                results.append("OperaGX в браузере")
            
            # Открытие Spotify
            spotify_paths = [
                os.path.expanduser("~/AppData/Roaming/Spotify/Spotify.exe"),
                "C:/Users/Public/Desktop/Spotify.lnk",
                "C:/Program Files/WindowsApps/SpotifyAB.SpotifyMusic_*/Spotify.exe"
            ]
            
            spotify_opened = False
            for path in spotify_paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    results.append("Spotify")
                    spotify_opened = True
                    break
            
            if not spotify_opened:
                # Если Spotify не найден, откроем в браузере
                webbrowser.open("https://open.spotify.com")
                results.append("Spotify в браузере")
            
            return True, f"Открыто: {' и '.join(results)}"
            
        except Exception as e:
            return False, f"Ошибка при открытии музыки: {str(e)}"


class EnableVPNCommand(BaseCommand):
    """Команда для включения VPN"""
    
    def __init__(self):
        super().__init__(
            name="Включи VPN",
            description="Запускает Psiphon VPN",
            keywords=["включи vpn", "vpn", "псифон", "psiphon"]
        )
    
    def execute(self, command_text: str) -> Tuple[bool, str]:
        try:
            vpn_path = "D:/psiphon-184-20241217.exe"
            
            if os.path.exists(vpn_path):
                subprocess.Popen([vpn_path])
                return True, "Psiphon VPN запущен"
            else:
                return False, f"Файл VPN не найден по пути: {vpn_path}"
                
        except Exception as e:
            return False, f"Ошибка при запуске VPN: {str(e)}"


class WebCommands:
    """Коллекция веб-команд и команд приложений"""
    
    def __init__(self):
        self.commands = [
            CheckEmailCommand(),
            OpenTelegramCommand(),
            PlayMusicCommand(),
            EnableVPNCommand()
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