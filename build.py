#!/usr/bin/env python3
# coding: utf-8

import subprocess
import sys
from pathlib import Path


def build():
    script_dir = Path(__file__).resolve().parent
    main_py = script_dir / "windsurf_reset_gui.py"

    print("="*60)
    print("🚀 Сборка Windsurf Reset Tool (PyInstaller)")
    print("="*60)

    if not main_py.exists():
        print(f"❌ Файл не найден: {main_py}")
        return 1
    
    print(f"✅ Файл приложения: {main_py.name}")
    print(f"✅ Версия: 1.2")

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--clean",
        "--name=WindsurfResetTool",
        "--distpath=dist",
        "--workpath=build",
        "--specpath=build",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui", 
        "--hidden-import=PyQt6.QtWidgets",
        "--collect-submodules=PyQt6",
        "--icon=WIndsurf_pro_trial_reset/123.ico",
        str(main_py),
    ]

    print(f"\n🐍 Python: {sys.version_info.major}.{sys.version_info.minor}")
    print("📦 Включённые пакеты: PyQt6")
    print("\n⚙️  Запуск PyInstaller...")
    print("⏱️  Время сборки: ~3-5 минут")
    print("="*60)
    
    try:
        result = subprocess.run(cmd, check=True)
        print("="*60)
        print("✅ Сборка завершена!")
        print(f"📁 Результат: dist\\WindsurfResetTool.exe")
        print("="*60)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print("="*60)
        print(f"❌ Ошибка сборки, код: {e.returncode}")
        print("\n💡 Попробуйте:")
        print("   pip install --upgrade pyinstaller PyQt6")
        print("="*60)
        return e.returncode


if __name__ == "__main__":
    sys.exit(build())

