# 🔨 Инструкции по сборке

## 📋 Оглавление
- [Автоматическая сборка (GitHub Actions)](#автоматическая-сборка-github-actions)
- [Ручная сборка на Windows](#ручная-сборка-на-windows)
- [Ручная сборка на macOS](#ручная-сборка-на-macos)
- [Ручная сборка на Linux](#ручная-сборка-на-linux)
- [Параметры сборки](#параметры-сборки)

---

## 🤖 Автоматическая сборка (GitHub Actions)

GitHub Actions автоматически собирает приложение для всех платформ при каждом push или создании тега.

### Триггеры сборки:
- **Push в main/develop**: Создаёт артефакты сборки (доступны 30 дней)
- **Pull Request**: Тестирует сборку
- **Создание тега `v*`**: Создаёт GitHub Release с файлами для скачивания

### Как создать релиз:

```bash
# 1. Обновите версию в коде (уже сделано для v1.4)
# 2. Создайте и запушьте тег
git tag v1.4.0
git push origin v1.4.0

# 3. GitHub Actions автоматически:
#    - Соберёт приложение для Windows, macOS и Linux
#    - Создаст GitHub Release
#    - Прикрепит все файлы к релизу
```

### Где найти собранные файлы:
- **Релизы**: https://github.com/YOUR_USERNAME/windsurf-pro-trial-reset/releases
- **Артефакты**: Actions → последний запуск → Artifacts

---

## 🪟 Ручная сборка на Windows

### Требования:
- Windows 10/11
- Python 3.9+
- Visual Studio Build Tools или MinGW

### Установка зависимостей:

```powershell
# 1. Установите Python с python.org
# 2. Установите зависимости
pip install -r requirements.txt
pip install nuitka

# 3. (Опционально) Установите MinGW для компиляции
# Nuitka автоматически скачает MinGW при первой сборке
```

### Сборка:

```powershell
# Вариант 1: Nuitka (рекомендуется, быстрее работает)
python build_onefile.py

# Вариант 2: PyInstaller (проще, но больше размер)
pip install pyinstaller
python build.py

# Результат: build/WindsurfResetTool.exe
```

---

## 🍎 Ручная сборка на macOS

### Требования:
- macOS 10.14+
- Python 3.9+
- Xcode Command Line Tools

### Установка зависимостей:

```bash
# 1. Установите Homebrew (если нет)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Установите Python
brew install python@3.11

# 3. Установите Xcode Command Line Tools
xcode-select --install

# 4. Установите зависимости
pip3 install -r requirements.txt
pip3 install nuitka
```

### Сборка:

```bash
# Вариант 1: Nuitka (создаёт .app bundle)
python3 build_onefile.py

# Вариант 2: PyInstaller
pip3 install pyinstaller
python3 build.py

# Результат: build/WindsurfResetTool.app
```

### Запуск:

```bash
# Откройте .app
open build/WindsurfResetTool.app

# Если macOS блокирует: Системные настройки → Безопасность → Разрешить
```

---

## 🐧 Ручная сборка на Linux

### Требования:
- Ubuntu 20.04+ / Debian 10+ / Fedora 32+
- Python 3.9+
- GCC

### Установка зависимостей (Ubuntu/Debian):

```bash
# 1. Обновите систему
sudo apt update
sudo apt upgrade

# 2. Установите Python и инструменты
sudo apt install python3 python3-pip python3-dev build-essential

# 3. Установите зависимости для PyQt6
sudo apt install libxcb-xinerama0 libxcb-cursor0 libxcb-icccm4 \
                 libxcb-image0 libxcb-keysyms1 libxcb-randr0 \
                 libxcb-render-util0 libxcb-shape0 libxcb1 \
                 libdbus-1-3 libfontconfig1 libxkbcommon-x11-0

# 4. Установите зависимости проекта
pip3 install -r requirements.txt
pip3 install nuitka
```

### Установка зависимостей (Fedora):

```bash
sudo dnf install python3 python3-pip python3-devel gcc gcc-c++
sudo dnf install qt6-qtbase qt6-qtbase-gui
pip3 install -r requirements.txt
pip3 install nuitka
```

### Сборка:

```bash
# Вариант 1: Nuitka
python3 build_onefile.py

# Вариант 2: PyInstaller
pip3 install pyinstaller
python3 build.py

# Результат: build/WindsurfResetTool.bin
```

### Запуск:

```bash
# Сделайте исполняемым
chmod +x build/WindsurfResetTool.bin

# Запустите
./build/WindsurfResetTool.bin
```

---

## ⚙️ Параметры сборки

### build_onefile.py (Nuitka)

```bash
# Сборка для текущей ОС
python build_onefile.py

# Сборка для конкретной платформы
python build_onefile.py -p windows
python build_onefile.py -p macos
python build_onefile.py -p linux

# Сборка для всех платформ (требует соответствующие ОС)
python build_onefile.py -p all

# Указать версию
python build_onefile.py -v 1.5.0
```

### build.py (PyInstaller)

```bash
# Сборка для текущей ОС
python build.py

# Сборка для конкретной платформы
python build.py -p windows
python build.py -p macos
python build.py -p linux

# Сборка для всех платформ
python build.py -p all
```

### Справка:

```bash
python build_onefile.py --help
python build.py --help
```

---

## 🔍 Устранение проблем

### Windows

**Проблема**: "MSVC not found"
```powershell
# Решение 1: Используйте MinGW (автоматически)
python build_onefile.py

# Решение 2: Установите Visual Studio Build Tools
# https://visualstudio.microsoft.com/downloads/
```

**Проблема**: "Missing DLL"
```powershell
# Переустановите PyQt6
pip uninstall PyQt6
pip install PyQt6
```

### macOS

**Проблема**: "xcode-select: error"
```bash
# Установите Command Line Tools
xcode-select --install
```

**Проблема**: "App is damaged"
```bash
# Удалите карантин
xattr -cr build/WindsurfResetTool.app
```

### Linux

**Проблема**: "Qt platform plugin not found"
```bash
# Установите дополнительные Qt библиотеки
sudo apt install libxcb-xinerama0 libxcb-cursor0
```

**Проблема**: "Permission denied"
```bash
# Сделайте файл исполняемым
chmod +x build/WindsurfResetTool.bin
```

---

## 📊 Сравнение методов сборки

| Метод | Размер | Скорость запуска | Сложность |
|-------|--------|------------------|-----------|
| **Nuitka** | ~50MB | ⚡ Быстрая | Средняя |
| **PyInstaller** | ~80MB | 🐌 Медленная | Простая |
| **GitHub Actions** | - | - | Автомат |

**Рекомендация**: Используйте **Nuitka** для продакшена и **GitHub Actions** для релизов.

---

## 📝 Changelog

См. [CHANGELOG.md](../CHANGELOG.md) для истории версий.

---

© 2025 Sparki. All rights reserved.

