#!/usr/bin/env python3
# coding: utf-8

import argparse
import subprocess
import sys
import platform
from pathlib import Path


def build_for_platform(target_platform: str, project_root: Path) -> int:
    """Сборка для конкретной платформы."""
    main_py = project_root / "windsurf_reset_gui.py"
    current_system = platform.system()
    
    # Маппинг названий платформ
    platform_map = {
        "windows": "Windows",
        "macos": "Darwin",
        "linux": "Linux"
    }
    
    system = platform_map.get(target_platform.lower(), current_system)
    
    print("\n" + "="*60)
    print(f"🚀 Сборка для {target_platform.upper()} (PyInstaller)")
    print("="*60)
    
    # Проверка кросс-компиляции
    if system != current_system:
        print(f"⚠️  ВНИМАНИЕ: Кросс-компиляция!")
        print(f"   Текущая ОС: {current_system}")
        print(f"   Целевая ОС: {system}")
        print(f"   PyInstaller не поддерживает полноценную кросс-компиляцию!")
        response = input("\n   Продолжить? (y/n): ").lower()
        if response != 'y':
            print("   ❌ Сборка отменена пользователем")
            return 1
    
    print(f"✅ Файл приложения: {main_py.name}")
    print(f"✅ Версия: 1.4")
    print(f"🖥️  Целевая платформа: {system}")

    # Icon path (only for Windows)
    icon_path = project_root / "123.ico"
    icon_args = []
    if system == "Windows" and icon_path.exists():
        icon_args = ["--icon=123.ico"]
    
    # Platform-specific options
    windowed_flag = "--windowed" if system in ["Windows", "Darwin"] else "--windowed"
    
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        windowed_flag,
        "--clean",
        "--name=WindsurfResetTool",
        "--distpath=dist",
        "--workpath=build",
        "--specpath=build",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui", 
        "--hidden-import=PyQt6.QtWidgets",
        "--collect-submodules=PyQt6",
    ] + icon_args + [str(main_py)]

    print(f"\n🐍 Python: {sys.version_info.major}.{sys.version_info.minor}")
    print("📦 Включённые пакеты: PyQt6")
    print("\n⚙️  Запуск PyInstaller...")
    print("⏱️  Время сборки: ~3-5 минут")
    print("="*60)
    
    try:
        result = subprocess.run(cmd, check=True)
        print("="*60)
        print("✅ Сборка завершена!")
        
        # Platform-specific output file
        if system == "Windows":
            output_file = "dist\\WindsurfResetTool.exe"
        elif system == "Darwin":
            output_file = "dist/WindsurfResetTool"
        else:  # Linux
            output_file = "dist/WindsurfResetTool"
        
        print(f"📁 Результат: {output_file}")
        print("="*60)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print("="*60)
        print(f"❌ Ошибка сборки, код: {e.returncode}")
        print("\n💡 Попробуйте:")
        print("   pip install --upgrade pyinstaller PyQt6")
        print("="*60)
        return e.returncode


def build(platforms: list = None) -> int:
    """Главная функция сборки."""
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir
    main_py = project_root / "windsurf_reset_gui.py"

    print("="*60)
    print("🚀 Сборка Windsurf Reset Tool (PyInstaller)")
    print("="*60)

    if not main_py.exists():
        print(f"❌ Файл не найден: {main_py}")
        return 1
    
    # Если платформы не указаны, используем текущую
    if not platforms:
        current_system = platform.system()
        platform_name = {"Windows": "windows", "Darwin": "macos", "Linux": "linux"}.get(current_system, "windows")
        platforms = [platform_name]
    
    print(f"📋 Платформы для сборки: {', '.join(platforms)}")
    
    results = {}
    for target_platform in platforms:
        result = build_for_platform(target_platform, project_root)
        results[target_platform] = result
        
        if result != 0:
            print(f"\n⚠️  Сборка для {target_platform} завершилась с ошибкой!")
            if len(platforms) > 1:
                response = input("   Продолжить сборку для других платформ? (y/n): ").lower()
                if response != 'y':
                    break
    
    # Итоговый отчёт
    if len(platforms) > 1:
        print("\n" + "="*60)
        print("📊 ИТОГОВЫЙ ОТЧЁТ")
        print("="*60)
        for plat, code in results.items():
            status = "✅ Успешно" if code == 0 else "❌ Ошибка"
            print(f"   {plat.upper()}: {status}")
        print("="*60)
    
    # Возвращаем 0 только если все сборки успешны
    return 0 if all(code == 0 for code in results.values()) else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Сборка Windsurf Reset Tool с помощью PyInstaller",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python build.py                    # Сборка для текущей ОС
  python build.py -p windows         # Сборка только для Windows
  python build.py -p macos           # Сборка только для macOS
  python build.py -p linux           # Сборка только для Linux
  python build.py -p all             # Сборка для всех платформ
        """
    )
    parser.add_argument(
        "-p",
        "--platform",
        dest="platform",
        default=None,
        choices=["windows", "macos", "linux", "all"],
        help="Целевая платформа для сборки (windows/macos/linux/all). По умолчанию - текущая ОС",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    
    # Определяем список платформ для сборки
    platforms = None
    if args.platform:
        if args.platform == "all":
            platforms = ["windows", "macos", "linux"]
        else:
            platforms = [args.platform]
    
    sys.exit(build(platforms=platforms))

