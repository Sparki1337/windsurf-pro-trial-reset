#!/usr/bin/env python3
# coding: utf-8

import argparse
import subprocess
import sys
from pathlib import Path


def get_version() -> str:
    return "1.3"


def build(version: str) -> int:
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir

    main_py = project_root / "windsurf_reset_gui.py"

    print("="*60)
    print("🚀 Сборка Windsurf Reset Tool (One File)")
    print("="*60)

    if not main_py.exists():
        print(f"❌ [Ошибка] Не найден файл приложения: {main_py}")
        return 1
    
    print(f"✅ Файл приложения: {main_py.name}")
    print(f"✅ Версия: {version}")

    use_msvc = sys.version_info >= (3, 13)
    compiler_flag = "--msvc=latest" if use_msvc else "--mingw64"

    # Путь к файлу иконки — ищем рядом со скриптом сборки
    icon_path = project_root / "123.ico"
    if icon_path.exists():
        icon_arg = f"--windows-icon-from-ico={icon_path}"
    else:
        icon_arg = None
        print(f"⚠️ Иконка не найдена: {icon_path} — сборка продолжится без иконки")

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
        "--windows-company-name=Sparki",
        "--windows-product-name=Windsurf Reset Tool",
        "--windows-file-description=Windsurf Device ID Reset Tool - FULL FREE APP (by Sparki)",
        f"--windows-file-version={version}",
        f"--windows-product-version={version}",
        "--windows-console-mode=disable",
        "--output-dir=build",
        "--output-filename=WindsurfResetTool",
        str(main_py),
    ]

    # Вставляем аргумент иконки только если файл существует
    if icon_arg:
        # Вставим перед флагами версии чтобы было видно в выводе опций
        cmd.insert(cmd.index(f"--windows-file-description=Windsurf Device ID Reset Tool - FULL FREE APP (by Sparki)") + 1, icon_arg)

    print(f"\n🔧 Компилятор: {'MSVC (latest)' if use_msvc else 'MinGW-w64'}")
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
        print(f"📁 Результат: build/WindsurfResetTool.exe")
        print("="*60)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print("="*60)
        print(f"❌ [Ошибка] Nuitka завершилась с ошибкой, код: {e.returncode}")
        print("="*60)
        return e.returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Сборка Windsurf Reset Tool в один файл (onefile) с помощью Nuitka",
    )
    parser.add_argument(
        "-v",
        "--version",
        dest="version",
        default=None,
        help="Версия приложения (например, 1.3). Если не указана, будет использована 1.3",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    version = args.version or get_version()
    
    print(f"📦 Версия: {version}")
    
    sys.exit(build(version=version))

