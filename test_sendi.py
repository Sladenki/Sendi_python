"""
Тестирование приложения Sendi
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread

# Добавляем текущую директорию в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import CommandProcessor, SystemUtils, VoiceUtils, Logger

class TestSendiUtils(unittest.TestCase):
    """Тесты для утилит Sendi"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.command_processor = CommandProcessor()
        self.logger = Logger("test_log.txt")
    
    def test_system_info(self):
        """Тест получения информации о системе"""
        info = SystemUtils.get_system_info()
        self.assertIsInstance(info, dict)
        self.assertIn('os', info)
        self.assertIn('processor', info)
    
    def test_desktop_path(self):
        """Тест получения пути к рабочему столу"""
        path = SystemUtils.get_desktop_path()
        self.assertIsInstance(path, str)
        self.assertTrue(len(path) > 0)
    
    def test_create_folder(self):
        """Тест создания папки"""
        test_path = os.path.join(os.getcwd(), "test_folder")
        success, result = SystemUtils.create_folder(os.getcwd(), "test_folder")
        
        if success:
            self.assertTrue(os.path.exists(test_path))
            # Очистка
            os.rmdir(test_path)
        else:
            self.fail(f"Не удалось создать папку: {result}")
    
    def test_command_processor(self):
        """Тест обработчика команд"""
        # Тест команды времени
        success, result = self.command_processor.process_command("время")
        self.assertTrue(success)
        self.assertIn("время", result.lower())
        
        # Тест неизвестной команды
        success, result = self.command_processor.process_command("неизвестная команда")
        self.assertFalse(success)
        self.assertIn("не распознана", result)
    
    def test_voice_utils(self):
        """Тест утилит голоса"""
        # Тест форматирования текста
        test_text = "Это\nтестовый\nтекст  с  лишними  пробелами"
        formatted = VoiceUtils.format_response(test_text)
        self.assertNotIn('\n', formatted)
        self.assertNotIn('  ', formatted)
        
        # Тест настроек голоса
        settings = VoiceUtils.get_voice_settings()
        self.assertIn('rate', settings)
        self.assertIn('volume', settings)
    
    def test_logger(self):
        """Тест системы логирования"""
        # Тест записи лога
        entry = self.logger.log("TEST", "TestSource", "Test message")
        self.assertIn("TestSource", entry)
        self.assertIn("Test message", entry)
        
        # Тест получения последних логов
        recent_logs = self.logger.get_recent_logs(5)
        self.assertIsInstance(recent_logs, list)
        
        # Очистка
        self.logger.clear_logs()

class TestSendiApp(unittest.TestCase):
    """Тесты для главного приложения"""
    
    @classmethod
    def setUpClass(cls):
        """Настройка для всех тестов"""
        cls.app = QApplication(sys.argv)
    
    def test_app_creation(self):
        """Тест создания приложения"""
        from main import SendiApp
        
        # Создание приложения
        window = SendiApp()
        self.assertIsNotNone(window)
        
        # Проверка основных компонентов
        self.assertIsNotNone(window.command_processor)
        self.assertIsNotNone(window.logger)
        self.assertIsNotNone(window.status_label)
        self.assertIsNotNone(window.log_display)
        
        # Закрытие окна
        window.close()

if __name__ == "__main__":
    # Запуск тестов
    unittest.main(verbosity=2) 