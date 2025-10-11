#!/usr/bin/env python3
# coding: utf-8

import argparse
import subprocess
import sys
import platform
from pathlib import Path


def get_version() -> str:
    return "1.4"


def build_for_platform(version: str, target_platform: str, project_root: Path) -> int:
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
    print(f"🚀 Сборка для {target_platform.upper()}")
    print("="*60)
    
    # Проверка кросс-компиляции
    if system != current_system:
        print(f"⚠️  ВНИМАНИЕ: Кросс-компиляция!")
        print(f"   Текущая ОС: {current_system}")
        print(f"   Целевая ОС: {system}")
        print(f"   Сборка может не работать или потребовать дополнительных инструментов!")
        response = input("\n   Продолжить? (y/n): ").lower()
        if response != 'y':
            print("   ❌ Сборка отменена пользователем")
            return 1
    
    print(f"✅ Файл приложения: {main_py.name}")
    print(f"✅ Версия: {version}")
    print(f"🖥️  Целевая платформа: {system}")

    # Compiler flags for different platforms
    if system == "Windows":
        use_msvc = sys.version_info >= (3, 13)
        compiler_flag = "--msvc=latest" if use_msvc else "--mingw64"
    elif system == "Darwin":  # macOS
        compiler_flag = "--clang"
    else:  # Linux
        compiler_flag = "--gcc"

    # Путь к файлу иконки (только для Windows)
    icon_arg = None
    if system == "Windows":
        icon_path = project_root / "123.ico"
        if icon_path.exists():
            icon_arg = f"--windows-icon-from-ico={icon_path}"
        else:
            print(f"⚠️ Иконка не найдена: {icon_path} — сборка продолжится без иконки")

    # Base command
    cmd = [
        sys.executable,
        "-m",
        "nuitka",
        "--onefile",
        "--standalone",
        compiler_flag,
        "--enable-plugin=pyqt6",
        "--include-qt-plugins=platforms,styles,iconengines,imageformats",
        "--nofollow-import-to=tkinter",
        "--nofollow-import-to=unittest",
        "--nofollow-import-to=pydoc",
    ]
    
    # Platform-specific options
    if system == "Windows":
        cmd.extend([
            "--windows-company-name=Sparki",
            "--windows-product-name=Windsurf Reset Tool",
            "--windows-file-description=Windsurf Device ID Reset Tool - FULL FREE APP (by Sparki)",
            f"--windows-file-version={version}",
            f"--windows-product-version={version}",
            "--windows-console-mode=disable",
        ])
    elif system == "Darwin":  # macOS
        cmd.extend([
            "--macos-create-app-bundle",
            "--macos-app-name=WindsurfResetTool",
            "--disable-console",
        ])
    else:  # Linux
        cmd.extend([
            "--disable-console",
        ])
    
    cmd.extend([
        "--output-dir=build",
        "--output-filename=WindsurfResetTool",
        str(main_py),
    ])

    # Вставляем аргумент иконки только если файл существует (только для Windows)
    if icon_arg:
        # Вставим перед флагами версии чтобы было видно в выводе опций
        cmd.insert(cmd.index(f"--windows-file-description=Windsurf Device ID Reset Tool - FULL FREE APP (by Sparki)") + 1, icon_arg)

    # Display compiler info
    if system == "Windows":
        use_msvc = sys.version_info >= (3, 13)
        compiler_name = 'MSVC (latest)' if use_msvc else 'MinGW-w64'
    elif system == "Darwin":
        compiler_name = 'Clang'
    else:
        compiler_name = 'GCC'
    
    print(f"\n🔧 Компилятор: {compiler_name}")
    print(f"🐍 Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print(f"\n📦 Включённые пакеты:")
    print("   - PyQt6 (GUI framework)")
    
    print(f"\n⚙️  Запуск Nuitka...")
    print("⚠️  Сборка в один файл может занять 5-10 минут")
    print("="*60)
    
    try:
        result = subprocess.run(cmd, check=True, cwd=project_root)
        print("="*60)
        print("✅ Сборка завершена успешно!")
        
        # Platform-specific output file
        if system == "Windows":
            output_file = "build/WindsurfResetTool.exe"
        elif system == "Darwin":
            output_file = "build/WindsurfResetTool.app"
        else:  # Linux
            output_file = "build/WindsurfResetTool.bin"
        
        print(f"📁 Результат: {output_file}")
        print("="*60)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print("="*60)
        print(f"❌ [Ошибка] Nuitka завершилась с ошибкой, код: {e.returncode}")
        print("="*60)
        return e.returncode


def build(version: str, platforms: list = None) -> int:
    """Главная функция сборки."""
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir
    main_py = project_root / "windsurf_reset_gui.py"

    print("="*60)
    print("🚀 Сборка Windsurf Reset Tool (One File)")
    print("="*60)

    if not main_py.exists():
        print(f"❌ [Ошибка] Не найден файл приложения: {main_py}")
        return 1
    
    # Если платформы не указаны, используем текущую
    if not platforms:
        current_system = platform.system()
        platform_name = {"Windows": "windows", "Darwin": "macos", "Linux": "linux"}.get(current_system, "windows")
        platforms = [platform_name]
    
    print(f"📋 Платформы для сборки: {', '.join(platforms)}")
    
    results = {}
    for target_platform in platforms:
        result = build_for_platform(version, target_platform, project_root)
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
        description="Сборка Windsurf Reset Tool в один файл (onefile) с помощью Nuitka",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python build_onefile.py                    # Сборка для текущей ОС
  python build_onefile.py -p windows         # Сборка только для Windows
  python build_onefile.py -p macos           # Сборка только для macOS
  python build_onefile.py -p linux           # Сборка только для Linux
  python build_onefile.py -p all             # Сборка для всех платформ
  python build_onefile.py -v 1.5 -p windows  # Указать версию и платформу
        """
    )
    parser.add_argument(
        "-v",
        "--version",
        dest="version",
        default=None,
        help="Версия приложения (например, 1.4). Если не указана, будет использована 1.4",
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
    version = args.version or get_version()
    
    # Определяем список платформ для сборки
    platforms = None
    if args.platform:
        if args.platform == "all":
            platforms = ["windows", "macos", "linux"]
        else:
            platforms = [args.platform]
    
    print(f"📦 Версия: {version}")
    
    sys.exit(build(version=version, platforms=platforms))

