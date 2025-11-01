# 🔧 Windsurf Reset Tool (Works on versions 1.12.21) (Работает на версии 1.12.21) | New versions 1.12.21+ (Outdated!!!) (НЕ АКТУАЛЬНО!!!) 

[English](#english) | [Русский](#russian)

---

<a name="english"></a>
## 📖 English

### Description

**Windsurf Reset Tool** is a free cross-platform GUI application that allows you to reset device identifiers for Windsurf IDE (and Windsurf Next Insiders version). The tool generates new device IDs and creates automatic backups of your configuration files.

**Supported Platforms**: Windows, macOS, Linux

### ✨ Features

- 🔄 **Reset Device Identifiers**: Generate new device IDs with one click
- 💾 **Automatic Backups**: Create timestamped backups before making changes
- 🌍 **Multilingual**: Full support for English and Russian
- 🚀 **Version Support**: Works with both Windsurf (Stable) and Windsurf Next (Insiders)
- 👁️ **View Configuration**: View current device identifiers
- 🖥️ **Cross-Platform**: Full support for **Windows**, **macOS**, and **Linux**

### 🎯 Use Cases

- Reset trial period for Windsurf Pro
- Fix device identification issues
- Generate new telemetry IDs
- Create configuration backups

### 📋 Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 20.04+, Debian 10+, Fedora 32+, etc.)
- Python 3.8+
- PyQt6 6.6.0+

### 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/Sparki1337/windsurf-pro-trial-reset.git
cd windsurf-pro-trial-reset
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python windsurf_reset_gui.py
```

### 📦 Building Executable

To build a standalone executable using Nuitka:

```bash
python build.py
```

For a single-file executable:

```bash
python build_onefile.py
```

The executable will be created in the `build/` directory.

### 🎮 Usage

1. **Select Language**: Choose your preferred language (English/Russian)
2. **Select Version**: Choose Windsurf version (Stable or Next)
3. **View Configuration**: Click "View Configuration" to see current device IDs
4. **Reset IDs**: Click "Reset Device IDs" to generate new identifiers
5. **Backup**: You'll be prompted to create a backup (recommended)

### ⚠️ Important Notes

- **Always create a backup** before resetting IDs
- **Close Windsurf** before running the reset operation
- After reset, it's **recommended to reinstall Windsurf** if you experience any errors
- Backup files are saved with timestamps in the format: `storage.json.backup_YYYYMMDD_HHMMSS`

### 📂 Configuration Locations

**Windows:**
- Stable: `%APPDATA%\Windsurf\User\globalStorage\storage.json`
- Next: `%APPDATA%\Windsurf - Next\User\globalStorage\storage.json`

**macOS:**
- Stable: `~/Library/Application Support/Windsurf/User/globalStorage/storage.json`
- Next: `~/Library/Application Support/Windsurf - Next/User/globalStorage/storage.json`

**Linux:**
- Stable: `~/.config/Windsurf/User/globalStorage/storage.json`
- Next: `~/.config/Windsurf - Next/User/globalStorage/storage.json`

> The application automatically detects your operating system and uses the correct path.

### 🛠️ Technical Details

The tool modifies the following device identifiers in the Windsurf configuration:
- `telemetry.machineId` - Machine identifier (64 hex characters)
- `telemetry.macMachineId` - MAC-based machine identifier (64 hex characters)
- `telemetry.devDeviceId` - Device identifier (UUID format)

### 📝 License

This project is released under the MIT License. See [LICENSE](LICENSE) file for details.

### 👨‍💻 Author

Created by **Sparki** ([@gde_ryzen](https://t.me/gde_ryzen))

For bug reports: sparkiabuz1@gmail.com

### 🤝 Contributing

Contributions, issues, and feature requests are welcome!

Feel free to check the [issues page](https://github.com/Sparki1337/windsurf-pro-trial-reset/issues).

### ⭐ Support

If you found this tool helpful, please give it a ⭐ on GitHub!

---

<a name="russian"></a>
## 📖 Русский

### Описание

**Windsurf Reset Tool** — это бесплатное кросс-платформенное приложение с графическим интерфейсом, позволяющее сбрасывать идентификаторы устройства для Windsurf IDE (и инсайдерской версии Windsurf Next). Инструмент генерирует новые ID устройства и создаёт автоматические резервные копии конфигурационных файлов.

**Поддерживаемые платформы**: Windows, macOS, Linux

### ✨ Возможности

- 🔄 **Сброс ID устройства**: Генерация новых идентификаторов в один клик
- 💾 **Автоматические резервные копии**: Создание бэкапов с временными метками перед изменениями
- 🌍 **Многоязычность**: Полная поддержка английского и русского языков
- 🚀 **Поддержка версий**: Работает как с Windsurf (стабильная), так и с Windsurf Next (инсайдерская)
- 👁️ **Просмотр конфигурации**: Просмотр текущих идентификаторов устройства
- 🖥️ **Кросс-платформенность**: Полная поддержка **Windows**, **macOS** и **Linux**

### 🎯 Варианты использования

- Сброс пробного периода Windsurf Pro
- Исправление проблем с идентификацией устройства
- Генерация новых телеметрических ID
- Создание резервных копий конфигурации

### 📋 Требования

- **Операционная система**: Windows 10/11, macOS 10.14+, или Linux (Ubuntu 20.04+, Debian 10+, Fedora 32+, и т.д.)
- Python 3.8+
- PyQt6 6.6.0+

### 🚀 Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Sparki1337/windsurf-pro-trial-reset.git
cd windsurf-pro-trial-reset
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Запустите приложение:
```bash
python windsurf_reset_gui.py
```

### 📦 Сборка исполняемого файла

Для сборки standalone исполняемого файла с помощью Nuitka:

```bash
python build.py
```

Для создания однофайлового исполняемого файла:

```bash
python build_onefile.py
```

Исполняемый файл будет создан в директории `build/`.

### 🎮 Использование

1. **Выбор языка**: Выберите предпочитаемый язык (English/Русский)
2. **Выбор версии**: Выберите версию Windsurf (стабильная или Next)
3. **Просмотр конфигурации**: Нажмите "Просмотреть конфигурацию" для просмотра текущих ID устройства
4. **Сброс ID**: Нажмите "Сбросить ID устройства" для генерации новых идентификаторов
5. **Резервная копия**: Вам будет предложено создать резервную копию (рекомендуется)

### ⚠️ Важные примечания

- **Всегда создавайте резервную копию** перед сбросом ID
- **Закройте Windsurf** перед выполнением операции сброса
- После сброса **рекомендуется переустановить Windsurf**, если возникают какие-либо ошибки
- Файлы резервных копий сохраняются с временными метками в формате: `storage.json.backup_YYYYMMDD_HHMMSS`

### 📂 Расположение конфигурации

**Windows:**
- Стабильная: `%APPDATA%\Windsurf\User\globalStorage\storage.json`
- Next: `%APPDATA%\Windsurf - Next\User\globalStorage\storage.json`

**macOS:**
- Стабильная: `~/Library/Application Support/Windsurf/User/globalStorage/storage.json`
- Next: `~/Library/Application Support/Windsurf - Next/User/globalStorage/storage.json`

**Linux:**
- Стабильная: `~/.config/Windsurf/User/globalStorage/storage.json`
- Next: `~/.config/Windsurf - Next/User/globalStorage/storage.json`

> Приложение автоматически определяет вашу операционную систему и использует правильный путь.

### 🛠️ Технические детали

Инструмент изменяет следующие идентификаторы устройства в конфигурации Windsurf:
- `telemetry.machineId` - Идентификатор машины (64 hex символа)
- `telemetry.macMachineId` - Идентификатор машины на основе MAC (64 hex символа)
- `telemetry.devDeviceId` - Идентификатор устройства (формат UUID)

### 📝 Лицензия

Этот проект распространяется под лицензией MIT. Подробности см. в файле [LICENSE](LICENSE).

### 👨‍💻 Автор

Создано **Sparki** ([@gde_ryzen](https://t.me/gde_ryzen))

По вопросам ошибок: sparkiabuz1@gmail.com

### 🤝 Вклад в проект

Приветствуются дополнения, сообщения об ошибках и запросы на добавление функций!

Загляните на [страницу issues](https://github.com/Sparki1337/windsurf-pro-trial-reset/issues).

### ⭐ Поддержка

Если этот инструмент был вам полезен, поставьте ⭐ на GitHub!

---

© 2025 Sparki. All rights reserved.

