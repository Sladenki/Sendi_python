"""
Главный модуль голосового помощника Sendi
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLabel, QTabWidget, QScrollArea,
    QFrame, QGridLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPalette, QColor, QLinearGradient

from core.voice_assistant import VoiceAssistant


class ModernMainWindow(QMainWindow):
    """Современное главное окно с вкладками"""
    
    def __init__(self):
        super().__init__()
        self.voice_assistant = VoiceAssistant()
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        self.setWindowTitle("Sendi - Голосовой помощник")
        self.setMinimumSize(900, 700)
        self.setStyleSheet(self.get_modern_stylesheet())
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Главный layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Заголовок
        self.create_header(main_layout)
        
        # Вкладки
        self.create_tabs(main_layout)
        
        # Статус бар
        self.create_status_bar()
        
    def create_header(self, layout):
        """Создание заголовка"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        
        # Логотип и название
        title_layout = QVBoxLayout()
        title_label = QLabel("🎤 Sendi")
        title_label.setObjectName("titleLabel")
        subtitle_label = QLabel("Голосовой помощник нового поколения")
        subtitle_label.setObjectName("subtitleLabel")
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        
        # Статус подключения
        status_layout = QVBoxLayout()
        self.connection_status = QLabel("🔴 Не подключен")
        self.connection_status.setObjectName("statusLabel")
        self.microphone_status = QLabel("Микрофон: Неактивен")
        self.microphone_status.setObjectName("microphoneStatus")
        
        status_layout.addWidget(self.connection_status)
        status_layout.addWidget(self.microphone_status)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addLayout(status_layout)
        
        layout.addWidget(header_frame)
        
    def create_tabs(self, layout):
        """Создание вкладок"""
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("tabWidget")
        
        # Вкладка управления
        self.create_control_tab()
        
        # Вкладка команд
        self.create_commands_tab()
        
        # Вкладка логов
        self.create_logs_tab()
        
        layout.addWidget(self.tab_widget)
        
    def create_control_tab(self):
        """Создание вкладки управления"""
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        control_layout.setContentsMargins(30, 30, 30, 30)
        
        # Основные кнопки управления
        buttons_frame = QFrame()
        buttons_frame.setObjectName("buttonsFrame")
        buttons_layout = QVBoxLayout(buttons_frame)
        
        # Кнопка прослушивания
        self.listen_button = QPushButton("🎤 Начать прослушивание")
        self.listen_button.setObjectName("primaryButton")
        self.listen_button.setMinimumHeight(60)
        
        # Кнопка остановки
        self.stop_button = QPushButton("⏹ Остановить")
        self.stop_button.setObjectName("secondaryButton")
        self.stop_button.setMinimumHeight(50)
        self.stop_button.setEnabled(False)
        
        # Кнопка тестирования TTS
        self.test_tts_button = QPushButton("🔊 Тест голоса")
        self.test_tts_button.setObjectName("tertiaryButton")
        self.test_tts_button.setMinimumHeight(50)
        
        buttons_layout.addWidget(self.listen_button)
        buttons_layout.addWidget(self.stop_button)
        buttons_layout.addWidget(self.test_tts_button)
        
        control_layout.addWidget(buttons_frame)
        control_layout.addStretch()
        
        # Информация о командах
        info_frame = QFrame()
        info_frame.setObjectName("infoFrame")
        info_layout = QVBoxLayout(info_frame)
        
        info_title = QLabel("💡 Быстрый старт")
        info_title.setObjectName("infoTitle")
        
        info_text = QLabel(
            "1. Нажмите 'Начать прослушивание'\n"
            "2. Произнесите любую команду\n"
            "3. Следите за результатами во вкладке 'Логи'"
        )
        info_text.setObjectName("infoText")
        
        info_layout.addWidget(info_title)
        info_layout.addWidget(info_text)
        
        control_layout.addWidget(info_frame)
        
        self.tab_widget.addTab(control_widget, "🎮 Управление")
        
    def create_commands_tab(self):
        """Создание вкладки с командами"""
        commands_widget = QWidget()
        commands_layout = QVBoxLayout(commands_widget)
        commands_layout.setContentsMargins(30, 30, 30, 30)
        
        # Заголовок
        commands_title = QLabel("📋 Доступные команды")
        commands_title.setObjectName("sectionTitle")
        commands_layout.addWidget(commands_title)
        
        # Область прокрутки для команд
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("scrollArea")
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Системные команды
        self.create_command_section(scroll_layout, "💻 Системные команды", [
            ("🕐 Время", "показывает текущее время", ["время", "который час", "текущее время"]),
            ("📅 Дата", "показывает текущую дату", ["дата", "какое число", "сегодня"]),
            ("💻 Система", "информация о системе", ["система", "информация о системе", "характеристики"]),
            ("⚙️ Процессы", "список запущенных процессов", ["процессы", "задачи", "что запущено"]),
            ("🌐 Браузер", "открывает браузер по умолчанию", ["открой браузер", "браузер", "интернет"]),
            ("📁 Создать папку", "создает папку на рабочем столе", ["создай папку", "новая папка", "создать папку"])
        ])
        
        # Веб-команды
        self.create_command_section(scroll_layout, "🌐 Веб-команды и приложения", [
            ("📧 Проверить почту", "открывает почту Mail.ru", ["проверь почту", "почта", "майл", "email", "письма"]),
            ("💬 Открыть Telegram", "открывает Telegram Desktop", ["открой телеграм", "телеграм", "telegram"]),
            ("🎵 Включить музыку", "открывает OperaGX и Spotify", ["включи музыку", "музыка", "спотифай", "spotify", "опера"]),
            ("🔒 Включить VPN", "запускает Psiphon VPN", ["включи vpn", "vpn", "псифон", "psiphon"])
        ])
        
        scroll_area.setWidget(scroll_widget)
        commands_layout.addWidget(scroll_area)
        
        self.tab_widget.addTab(commands_widget, "📋 Команды")
        
    def create_command_section(self, layout, title, commands):
        """Создание секции команд"""
        section_frame = QFrame()
        section_frame.setObjectName("commandSection")
        section_layout = QVBoxLayout(section_frame)
        
        # Заголовок секции
        section_title = QLabel(title)
        section_title.setObjectName("commandSectionTitle")
        section_layout.addWidget(section_title)
        
        # Команды
        for icon_name, description, keywords in commands:
            command_frame = QFrame()
            command_frame.setObjectName("commandItem")
            command_layout = QHBoxLayout(command_frame)
            
            # Иконка и название
            icon_label = QLabel(icon_name)
            icon_label.setObjectName("commandIcon")
            
            # Описание
            desc_layout = QVBoxLayout()
            desc_label = QLabel(description)
            desc_label.setObjectName("commandDescription")
            
            keywords_text = ", ".join([f"'{kw}'" for kw in keywords])
            keywords_label = QLabel(f"Ключевые слова: {keywords_text}")
            keywords_label.setObjectName("commandKeywords")
            
            desc_layout.addWidget(desc_label)
            desc_layout.addWidget(keywords_label)
            
            command_layout.addWidget(icon_label)
            command_layout.addLayout(desc_layout)
            command_layout.addStretch()
            
            section_layout.addWidget(command_frame)
        
        layout.addWidget(section_frame)
        
    def create_logs_tab(self):
        """Создание вкладки логов"""
        logs_widget = QWidget()
        logs_layout = QVBoxLayout(logs_widget)
        logs_layout.setContentsMargins(30, 30, 30, 30)
        
        # Заголовок
        logs_title = QLabel("📝 Журнал событий")
        logs_title.setObjectName("sectionTitle")
        logs_layout.addWidget(logs_title)
        
        # Область логов
        self.logs_text = QTextEdit()
        self.logs_text.setObjectName("logsText")
        self.logs_text.setReadOnly(True)
        self.logs_text.setPlaceholderText("Здесь будут отображаться все события и команды...")
        
        logs_layout.addWidget(self.logs_text)
        
        # Кнопки управления логами
        logs_buttons_layout = QHBoxLayout()
        
        self.clear_logs_button = QPushButton("🗑 Очистить логи")
        self.clear_logs_button.setObjectName("tertiaryButton")
        
        self.save_logs_button = QPushButton("💾 Сохранить логи")
        self.save_logs_button.setObjectName("tertiaryButton")
        
        logs_buttons_layout.addWidget(self.clear_logs_button)
        logs_buttons_layout.addWidget(self.save_logs_button)
        logs_buttons_layout.addStretch()
        
        logs_layout.addLayout(logs_buttons_layout)
        
        self.tab_widget.addTab(logs_widget, "📝 Логи")
        
    def create_status_bar(self):
        """Создание статус бара"""
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: #2d3748;
                color: #e2e8f0;
                padding: 5px;
                border-top: 1px solid #4a5568;
            }
        """)
        
    def setup_connections(self):
        """Настройка соединений сигналов"""
        self.listen_button.clicked.connect(self.start_listening)
        self.stop_button.clicked.connect(self.stop_listening)
        self.test_tts_button.clicked.connect(self.test_tts)
        self.clear_logs_button.clicked.connect(self.clear_logs)
        self.save_logs_button.clicked.connect(self.save_logs)
        
        # Подключение сигналов голосового помощника
        self.voice_assistant.speech_recognized.connect(self.add_log)
        self.voice_assistant.status_changed.connect(self.update_status)
        
    def start_listening(self):
        """Начать прослушивание"""
        if not self.voice_assistant.isRunning():
            self.voice_assistant.running = True
            self.voice_assistant.start()
        self.listen_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.connection_status.setText("🟢 Подключен")
        self.microphone_status.setText("Микрофон: Активен")
        
    def stop_listening(self):
        """Остановить прослушивание"""
        if self.voice_assistant.isRunning():
            self.voice_assistant.stop()
        self.listen_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.connection_status.setText("🔴 Не подключен")
        self.microphone_status.setText("Микрофон: Неактивен")
        
    def test_tts(self):
        """Тест голоса"""
        self.voice_assistant.speak("Привет! Я Sendi, ваш голосовой помощник.")
        self.add_log("🔊 Тест голоса выполнен")
        
    def add_log(self, message):
        """Добавить сообщение в логи"""
        self.logs_text.append(f"[{self.get_current_time()}] {message}")
        # Автопрокрутка к последнему сообщению
        self.logs_text.verticalScrollBar().setValue(
            self.logs_text.verticalScrollBar().maximum()
        )
        
    def update_status(self, status):
        """Обновить статус"""
        self.connection_status.setText(status)
        
    def clear_logs(self):
        """Очистить логи"""
        self.logs_text.clear()
        
    def save_logs(self):
        """Сохранить логи в файл"""
        from PyQt5.QtWidgets import QFileDialog
        filename, _ = QFileDialog.getSaveFileName(
            self, "Сохранить логи", "", "Text Files (*.txt)"
        )
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.logs_text.toPlainText())
            self.add_log(f"Логи сохранены в файл: {filename}")
            
    def get_current_time(self):
        """Получить текущее время"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
        
    def get_modern_stylesheet(self):
        """Получить современные стили"""
        return """
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #1a202c, stop:1 #2d3748);
        }
        
        QTabWidget::pane {
            border: none;
            background: transparent;
        }
        
        QTabWidget::tab-bar {
            alignment: center;
        }
        
        QTabBar::tab {
            background: #4a5568;
            color: #e2e8f0;
            padding: 12px 24px;
            margin: 0 4px;
            border-radius: 8px 8px 0 0;
            font-weight: bold;
            font-size: 14px;
        }
        
        QTabBar::tab:selected {
            background: #667eea;
            color: white;
        }
        
        QTabBar::tab:hover {
            background: #5a67d8;
            color: white;
        }
        
        #headerFrame {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #667eea, stop:1 #764ba2);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 10px;
        }
        
        #titleLabel {
            color: white;
            font-size: 28px;
            font-weight: bold;
            margin: 0;
        }
        
        #subtitleLabel {
            color: #e2e8f0;
            font-size: 14px;
            margin: 0;
        }
        
        #statusLabel {
            color: white;
            font-size: 16px;
            font-weight: bold;
        }
        
        #microphoneStatus {
            color: #e2e8f0;
            font-size: 12px;
        }
        
        #buttonsFrame {
            background: #2d3748;
            border-radius: 15px;
            padding: 30px;
            border: 1px solid #4a5568;
        }
        
        #primaryButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #667eea, stop:1 #764ba2);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
            padding: 15px;
        }
        
        #primaryButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #5a67d8, stop:1 #6b46c1);
        }
        
        #primaryButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #4c51bf, stop:1 #553c9a);
        }
        
        #secondaryButton {
            background: #e53e3e;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 14px;
            font-weight: bold;
            padding: 12px;
        }
        
        #secondaryButton:hover {
            background: #c53030;
        }
        
        #tertiaryButton {
            background: #4a5568;
            color: #e2e8f0;
            border: none;
            border-radius: 10px;
            font-size: 14px;
            font-weight: bold;
            padding: 12px;
        }
        
        #tertiaryButton:hover {
            background: #5a67d8;
            color: white;
        }
        
        #infoFrame {
            background: #2d3748;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #4a5568;
        }
        
        #infoTitle {
            color: #667eea;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        #infoText {
            color: #e2e8f0;
            font-size: 14px;
            line-height: 1.5;
        }
        
        #sectionTitle {
            color: #667eea;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        
        #scrollArea {
            border: none;
            background: transparent;
        }
        
        #commandSection {
            background: #2d3748;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid #4a5568;
        }
        
        #commandSectionTitle {
            color: #667eea;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
        }
        
        #commandItem {
            background: #4a5568;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
        }
        
        #commandIcon {
            color: #f6ad55;
            font-size: 16px;
            font-weight: bold;
            min-width: 120px;
        }
        
        #commandDescription {
            color: #e2e8f0;
            font-size: 14px;
            font-weight: bold;
        }
        
        #commandKeywords {
            color: #a0aec0;
            font-size: 12px;
            font-style: italic;
        }
        
        #logsText {
            background: #2d3748;
            color: #e2e8f0;
            border: 1px solid #4a5568;
            border-radius: 8px;
            padding: 15px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 13px;
            line-height: 1.4;
        }
        
        QScrollBar:vertical {
            background: #4a5568;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background: #667eea;
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #5a67d8;
        }
        """


def main():
    """Главная функция"""
    app = QApplication(sys.argv)
    
    # Установка стиля приложения
    app.setStyle('Fusion')
    
    # Создание и отображение главного окна
    window = ModernMainWindow()
    window.show()
    
    # Запуск приложения
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 