#!/usr/bin/env python3
"""
Запуск приложения Sendi с новой архитектурой
"""

import sys
import os
import subprocess
import importlib.util

def check_python_version():
    """Проверка версии Python"""
    if sys.version_info < (3, 7):
        print("❌ Ошибка: Требуется Python 3.7 или выше")
        print(f"   Текущая версия: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def check_dependencies():
    """Проверка и установка зависимостей"""
    required_packages = {
        'PyQt5': 'PyQt5',
        'pyttsx3': 'pyttsx3',
        'speech_recognition': 'SpeechRecognition',
        'pyaudio': 'pyaudio',
        'psutil': 'psutil'
    }
    
    missing_packages = []
    
    print("🔍 Проверка зависимостей...")
    
    for package, pip_name in required_packages.items():
        try:
            importlib.import_module(package)
            print(f"✅ {package} - OK")
        except ImportError:
            print(f"❌ {package} - НЕ НАЙДЕН")
            missing_packages.append(pip_name)
    
    if missing_packages:
        print(f"\n📦 Установка недостающих пакетов: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install'
            ] + missing_packages)
            print("✅ Зависимости установлены")
            return True
        except subprocess.CalledProcessError:
            print("❌ Ошибка установки зависимостей")
            print("Попробуйте установить вручную:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    
    return True

def check_audio_devices():
    """Проверка аудио устройств"""
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        
        # Проверка микрофонов
        mic_count = 0
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                mic_count += 1
        
        if mic_count > 0:
            print(f"✅ Найдено микрофонов: {mic_count}")
        else:
            print("⚠️  Микрофоны не найдены")
        
        p.terminate()
        return True
    except Exception as e:
        print(f"⚠️  Ошибка проверки аудио: {e}")
        return False

def check_system_requirements():
    """Проверка системных требований"""
    print("\n🔧 Проверка системных требований...")
    
    # Проверка операционной системы
    import platform
    os_name = platform.system()
    print(f"📱 Операционная система: {os_name}")
    
    # Проверка доступной памяти
    try:
        import psutil
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        print(f"💾 Оперативная память: {memory_gb:.1f} GB")
        
        if memory_gb < 2:
            print("⚠️  Рекомендуется минимум 2 GB RAM")
    except:
        print("⚠️  Не удалось проверить память")
    
    return True

def create_directories():
    """Создание необходимых директорий"""
    directories = ['logs', 'config', 'temp']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Создана директория: {directory}")

def main():
    """Главная функция запуска"""
    print("🚀 Запуск Sendi - Голосового помощника (Новая архитектура)")
    print("=" * 60)
    
    # Проверка версии Python
    if not check_python_version():
        sys.exit(1)
    
    # Проверка зависимостей
    if not check_dependencies():
        sys.exit(1)
    
    # Проверка системных требований
    check_system_requirements()
    
    # Проверка аудио устройств
    check_audio_devices()
    
    # Создание директорий
    create_directories()
    
    print("\n🎯 Запуск приложения...")
    print("=" * 60)
    
    try:
        # Импорт и запуск приложения
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        from main import main as app_main
        app_main()
    except KeyboardInterrupt:
        print("\n👋 Приложение остановлено пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка запуска приложения: {e}")
        print("\n🔍 Возможные решения:")
        print("1. Убедитесь, что все зависимости установлены")
        print("2. Проверьте подключение микрофона")
        print("3. Запустите от имени администратора (Windows)")
        print("4. Проверьте права доступа к аудио устройствам")
        sys.exit(1)

if __name__ == "__main__":
    main() 