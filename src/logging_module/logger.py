"""
Система логирования для приложения
"""

import os
import datetime
from typing import List, Optional


class Logger:
    """Система логирования"""
    
    def __init__(self, log_file: Optional[str] = None, max_entries: int = 1000):
        self.log_file = log_file or "logs/sendi.log"
        self.max_entries = max_entries
        self.log_entries: List[str] = []
        
        # Создание директории для логов
        self._ensure_log_directory()
    
    def _ensure_log_directory(self):
        """Создание директории для логов"""
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
    
    def log(self, level: str, source: str, message: str) -> str:
        """
        Добавление записи в лог
        
        Args:
            level: Уровень логирования (INFO, ERROR, WARNING, DEBUG)
            source: Источник сообщения
            message: Текст сообщения
            
        Returns:
            str: Созданная запись лога
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{level}] {source}: {message}"
        
        # Добавление в память
        self.log_entries.append(entry)
        
        # Ограничение количества записей в памяти
        if len(self.log_entries) > self.max_entries:
            self.log_entries = self.log_entries[-self.max_entries:]
        
        # Запись в файл
        self._write_to_file(entry)
        
        return entry
    
    def _write_to_file(self, entry: str):
        """Запись в файл"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(entry + '\n')
        except Exception as e:
            print(f"Ошибка записи в лог: {e}")
    
    def get_recent_logs(self, count: int = 50) -> List[str]:
        """
        Получение последних записей
        
        Args:
            count: Количество записей
            
        Returns:
            List[str]: Список записей
        """
        return self.log_entries[-count:] if self.log_entries else []
    
    def clear_logs(self):
        """Очистка логов"""
        self.log_entries.clear()
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("")
        except Exception as e:
            print(f"Ошибка очистки лога: {e}")
    
    def export_logs(self, filename: Optional[str] = None) -> tuple[bool, str]:
        """
        Экспорт логов в файл
        
        Args:
            filename: Имя файла для экспорта
            
        Returns:
            tuple[bool, str]: (успех, сообщение)
        """
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"logs/sendi_logs_{timestamp}.txt"
        
        try:
            # Создание директории для экспорта
            export_dir = os.path.dirname(filename)
            if export_dir and not os.path.exists(export_dir):
                os.makedirs(export_dir, exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                for entry in self.log_entries:
                    f.write(entry + '\n')
            return True, f"Логи экспортированы в {filename}"
        except Exception as e:
            return False, f"Ошибка экспорта: {str(e)}"
    
    def get_log_statistics(self) -> dict:
        """
        Получение статистики логов
        
        Returns:
            dict: Статистика логов
        """
        if not self.log_entries:
            return {
                'total_entries': 0,
                'file_size': 0,
                'oldest_entry': None,
                'newest_entry': None
            }
        
        try:
            file_size = os.path.getsize(self.log_file) if os.path.exists(self.log_file) else 0
        except:
            file_size = 0
        
        return {
            'total_entries': len(self.log_entries),
            'file_size': file_size,
            'oldest_entry': self.log_entries[0] if self.log_entries else None,
            'newest_entry': self.log_entries[-1] if self.log_entries else None
        } 