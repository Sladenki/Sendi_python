"""
Главный файл приложения Sendi
"""

import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.voice_assistant import VoiceAssistant
from core.tts_engine import TTSEngine
from commands.command_processor import CommandProcessor
from logging_module.logger import Logger
from utils.voice_utils import VoiceUtils
from config.config_manager import ConfigManager


class ModernButton(QPushButton):
    """Кастомная кнопка с современным дизайном"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(40)
        self.setFont(QFont("Segoe UI", 10))
        self.setCursor(Qt.PointingHandCursor)
        
        # Стили
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #8e2de2, stop:1 #4a00e0);
                border: none;
                border-radius: 20px;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #9e3df2, stop:1 #5a10f0);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7e1dd2, stop:1 #3a00d0);
            }
        """)


class StatusLabel(QLabel):
    """Кастомная метка статуса"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.setStyleSheet("""
            QLabel {
                color: #8e2de2;
                background: rgba(142, 45, 226, 0.1);
                border: 2px solid #8e2de2;
                border-radius: 15px;
                padding: 10px;
                margin: 5px;
            }
        """)


class LogDisplay(QTextEdit):
    """Кастомное поле для логов"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setFont(QFont("Consolas", 10))
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #e0e0e0;
                border: 2px solid #333;
                border-radius: 10px;
                padding: 10px;
            }
        """)


class SendiApp(QMainWindow):
    """Главное окно приложения Sendi"""
    
    def __init__(self):
        super().__init__()
        
        # Инициализация компонентов
        self.config_manager = ConfigManager()
        self.command_processor = CommandProcessor()
        self.logger = Logger()
        
        # Голосовые компоненты
        self.voice_assistant = None
        self.tts_engine = None
        
        # Инициализация UI
        self.init_ui()
        self.init_voice_assistant()
        self.speak_welcome()
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle("Sendi - Голосовой помощник")
        self.setFixedSize(800, 600)
        
        # Установка стилей
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #121212, stop:1 #1a1a1a);
            }
        """)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Главный layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Заголовок
        title_label = QLabel("Sendi")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 32, QFont.Bold))
        title_label.setStyleSheet("""
            QLabel {
                color: #8e2de2;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #8e2de2, stop:1 #4a00e0);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 20px;
            }
        """)
        main_layout.addWidget(title_label)
        
        # Подзаголовок
        subtitle_label = QLabel("Ваш голосовой помощник")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont("Segoe UI", 14))
        subtitle_label.setStyleSheet("color: #888; margin-bottom: 20px;")
        main_layout.addWidget(subtitle_label)
        
        # Статус
        self.status_label = StatusLabel("Инициализация...")
        main_layout.addWidget(self.status_label)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        
        self.start_button = ModernButton("Запустить помощника")
        self.start_button.clicked.connect(self.start_voice_assistant)
        button_layout.addWidget(self.start_button)
        
        self.stop_button = ModernButton("Остановить")
        self.stop_button.clicked.connect(self.stop_voice_assistant)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)
        
        self.clear_button = ModernButton("Очистить логи")
        self.clear_button.clicked.connect(self.clear_logs)
        button_layout.addWidget(self.clear_button)
        
        self.export_button = ModernButton("Экспорт логов")
        self.export_button.clicked.connect(self.export_logs)
        button_layout.addWidget(self.export_button)
        
        main_layout.addLayout(button_layout)
        
        # Область логов
        log_label = QLabel("История команд:")
        log_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        log_label.setStyleSheet("color: #e0e0e0; margin-top: 20px;")
        main_layout.addWidget(log_label)
        
        self.log_display = LogDisplay()
        main_layout.addWidget(self.log_display)
        
        # Информация о командах
        commands_info = " | ".join([
            "'открой браузер'", "'создай папку'", "'время'", 
            "'дата'", "'система'", "'процессы'"
        ])
        info_label = QLabel(f"Доступные команды: {commands_info}")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setFont(QFont("Segoe UI", 10))
        info_label.setStyleSheet("color: #666; margin-top: 10px;")
        main_layout.addWidget(info_label)
    
    def init_voice_assistant(self):
        """Инициализация голосового помощника"""
        voice_config = self.config_manager.get_recognition_settings()
        self.voice_assistant = VoiceAssistant(voice_config)
        self.voice_assistant.command_received.connect(self.process_command)
        self.voice_assistant.status_changed.connect(self.update_status)
        self.voice_assistant.speech_recognized.connect(self.show_recognized_text)
    
    def speak_welcome(self):
        """Приветственное сообщение"""
        welcome_text = "Привет! Я Sendi, ваш голосовой помощник. Готов к работе!"
        self.speak(welcome_text)
        self.log_action("Система", f"Приветствие: {welcome_text}")
    
    def speak(self, text):
        """Синтез речи"""
        if self.tts_engine and self.tts_engine.isRunning():
            self.tts_engine.stop()
        
        tts_config = self.config_manager.get_voice_settings()
        self.tts_engine = TTSEngine(text, tts_config)
        self.tts_engine.start()
    
    def start_voice_assistant(self):
        """Запуск голосового помощника"""
        if self.voice_assistant and not self.voice_assistant.isRunning():
            self.voice_assistant.start()
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.log_action("Система", "Голосовой помощник запущен")
    
    def stop_voice_assistant(self):
        """Остановка голосового помощника"""
        if self.voice_assistant and self.voice_assistant.isRunning():
            self.voice_assistant.stop()
            self.voice_assistant.wait()
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.update_status("Остановлен")
            self.log_action("Система", "Голосовой помощник остановлен")
    
    def process_command(self, command_text):
        """Обработка голосовых команд"""
        self.log_action("Пользователь", f"Команда: {command_text}")
        
        # Использование обработчика команд
        success, result = self.command_processor.process_command(command_text)
        
        if success:
            self.speak(result)
            self.log_action("Система", f"Выполнено: {result}")
        else:
            response = "Команда не распознана. Попробуйте еще раз."
            self.speak(response)
            self.log_action("Система", f"Ответ: {response}")
    
    def show_recognized_text(self, text):
        """Показать распознанный текст пользователя в логах"""
        self.log_action("Микрофон", f"Вы сказали: {text}")
    
    def update_status(self, status):
        """Обновление статуса"""
        self.status_label.setText(status)
    
    def log_action(self, source, message):
        """Логирование действий"""
        # Логирование в файл
        self.logger.log("INFO", source, message)
        
        # Отображение в интерфейсе
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {source}: {message}"
        
        # Добавление в лог
        self.log_display.append(log_entry)
        
        # Прокрутка к последней записи
        scrollbar = self.log_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear_logs(self):
        """Очистка логов"""
        self.log_display.clear()
        self.logger.clear_logs()
        self.log_action("Система", "Логи очищены")
    
    def export_logs(self):
        """Экспорт логов в файл"""
        success, result = self.logger.export_logs()
        if success:
            self.log_action("Система", result)
        else:
            self.log_action("Ошибка", result)
    
    def closeEvent(self, event):
        """Обработка закрытия приложения"""
        self.stop_voice_assistant()
        if self.tts_engine and self.tts_engine.isRunning():
            self.tts_engine.stop()
        event.accept()


def main():
    """Главная функция"""
    app = QApplication(sys.argv)
    
    # Установка стилей приложения
    app.setStyle('Fusion')
    
    # Создание и отображение главного окна
    window = SendiApp()
    window.show()
    
    # Запуск приложения
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 