import json
import os
import shutil
import uuid
import platform
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QMessageBox, QProgressBar,
    QGroupBox, QGridLayout, QFrame, QComboBox, QScrollArea, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve, QRect, QSize, QPropertyAnimation, QSequentialAnimationGroup
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon, QPainter, QLinearGradient, QBrush, QPen


# --- Localization System ---
LANGUAGES = {
    "en": {
        "title": "Windsurf Reset Tool",
        "version": "v1.4 (FULL FREE APP)",
        "select_language": "Select Language:",
        "reset_button": "Reset Device IDs",
        "view_button": "View Configuration",
        "about_button": "About",
        "exit_button": "Exit",
        "current_ids": "Current Device Identifiers",
        "new_ids": "New Device Identifiers",
        "backup_title": "Backup Configuration",
        "backup_prompt": "Would you like to create a backup before resetting?",
        "reset_confirm": "Are you sure you want to reset the device identifiers?",
        "yes": "Yes",
        "no": "No",
        "cancel": "Cancel",
        "success": "Success",
        "error": "Error",
        "warning": "Warning",
        "info": "Information",
        "backup_created": "Backup created successfully:",
        "reset_success": "Device identifiers have been successfully reset! 🎉",
        "no_config": "Configuration file not found.",
        "creating_backup": "Creating backup...",
        "loading_config": "Loading configuration...",
        "generating_ids": "Generating new identifiers...",
        "saving_config": "Saving configuration...",
        "complete": "Complete!",
        "about_text": "Windsurf Reset Tool v1.4\n\nThis tool resets Windsurf device identifiers and creates backups of your configuration.\n\nSupports: Windows, macOS, Linux\n\nCreated by: Sparki (@gde_ryzen), for bugs: sparkiabuz1@gmail.com \n\n© 2025",
        "status_ready": "Ready",
        "unsupported_os": "Unsupported OS: {0}",
        "base_dir_missing": "Base directory does not exist: {0}",
        "version_name_stable": "Windsurf",
        "version_name_next": "Windsurf Next",
        "config_location": "Configuration Location:",
        "operations": "Operations",
        "display": "Display",
        "select_version": "Select Windsurf Version:",
        "version_stable": "Windsurf (Stable)",
        "version_next": "Windsurf Next (Insiders)",
        "reinstall_hint": "If you experience errors in Windsurf, or your account gets logged out, it's recommended to reinstall Windsurf.",
    },
    "ru": {
        "title": "Инструмент Сброса Windsurf",
        "version": "v1.4 (FULL FREE APP)",
        "select_language": "Выбор языка:",
        "reset_button": "Сбросить ID устройства",
        "view_button": "Просмотреть конфигурацию",
        "about_button": "О программе",
        "exit_button": "Выход",
        "current_ids": "Текущие Идентификаторы Устройства",
        "new_ids": "Новые Идентификаторы Устройства",
        "backup_title": "Резервная копия конфигурации",
        "backup_prompt": "Хотите создать резервную копию перед сбросом?",
        "reset_confirm": "Вы уверены, что хотите сбросить идентификаторы устройства?",
        "yes": "Да",
        "no": "Нет",
        "cancel": "Отмена",
        "success": "Успешно",
        "error": "Ошибка",
        "warning": "Предупреждение",
        "info": "Информация",
        "backup_created": "Резервная копия успешно создана:",
        "reset_success": "Идентификаторы устройства успешно сброшены! 🎉",
        "no_config": "Файл конфигурации не найден.",
        "creating_backup": "Создание резервной копии...",
        "loading_config": "Загрузка конфигурации...",
        "generating_ids": "Генерация новых идентификаторов...",
        "saving_config": "Сохранение конфигурации...",
        "complete": "Завершено!",
        "about_text": "Инструмент Сброса Windsurf v1.4\n\nЭтот инструмент сбрасывает идентификаторы устройства Windsurf и создаёт резервные копии конфигурации.\n\nПоддерживаемые ОС: Windows, macOS, Linux\n\nСоздал: Sparki (@gde_ryzen), по ошибкам: sparkiabuz1@gmail.com \n\n© 2025",
        "status_ready": "Готов",
        "unsupported_os": "Неподдерживаемая ОС: {0}",
        "base_dir_missing": "Базовая директория не найдена: {0}",
        "version_name_stable": "Windsurf",
        "version_name_next": "Windsurf Next",
        "config_location": "Расположение конфигурации:",
        "operations": "Операции",
        "display": "Отображение",
        "select_version": "Выбор версии Windsurf:",
        "version_stable": "Windsurf (Стабильная)",
        "version_next": "Windsurf Next (Инсайдерская)",
        "reinstall_hint": "Если в Windsurf возникают ошибки или слетает аккаунт, рекомендуется переустановить Windsurf."
    },
}


class WindsurfResetError(Exception):
    """Custom exception for Windsurf reset-related errors."""
    pass


# --- Custom Widgets ---
class GradientButton(QPushButton):
    """Custom button with gradient background and hover animation."""
    
    def __init__(self, text: str, color1: str, color2: str, parent=None):
        super().__init__(text, parent)
        self.color1 = QColor(color1)
        self.color2 = QColor(color2)
        self.is_hovered = False
        self.setMinimumHeight(45)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Add shadow effect
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0, 140))
        self.shadow.setOffset(0, 3)
        self.setGraphicsEffect(self.shadow)
        
    def enterEvent(self, event):
        """Mouse enter - enhance shadow."""
        self.is_hovered = True
        self.shadow.setBlurRadius(30)
        self.shadow.setOffset(0, 8)
        self.update()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        """Mouse leave - restore shadow."""
        self.is_hovered = False
        self.shadow.setBlurRadius(20)
        self.shadow.setOffset(0, 5)
        self.update()
        super().leaveEvent(event)
        
    def paintEvent(self, event):
        """Custom paint with gradient."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Create gradient
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        
        if self.is_hovered and self.isEnabled():
            # Brighter gradient on hover
            gradient.setColorAt(0, self.color2.lighter(120))
            gradient.setColorAt(1, self.color1.lighter(120))
        else:
            gradient.setColorAt(0, self.color1)
            gradient.setColorAt(1, self.color2)
        
        # Draw rounded rectangle
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        
        if not self.isEnabled():
            painter.setOpacity(0.5)
            
        painter.drawRoundedRect(self.rect(), 12, 12)
        
        # Draw text
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())


class CardWidget(QFrame):
    """Custom card widget with gradient and shadow."""
    
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.title_text = title
        self.setFrameShape(QFrame.Shape.StyledPanel)
        
        # Add shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)
        
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(12, 12, 12, 12)
        self.main_layout.setSpacing(8)
        
        # Title if provided
        if title:
            title_label = QLabel(title)
            title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
            title_label.setStyleSheet("color: #21c0ae;")
            self.main_layout.addWidget(title_label)
            
    def paintEvent(self, event):
        """Custom paint with gradient background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Create gradient
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(45, 45, 45))
        gradient.setColorAt(1, QColor(30, 30, 30))
        
        # Draw rounded rectangle
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor(21, 143, 130), 2))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 15, 15)


class AnimatedProgressBar(QProgressBar):
    """Custom progress bar with animation."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTextVisible(True)
        self.setMinimumHeight(28)
        self.setMaximumHeight(28)
        
        # Add shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(33, 192, 174, 80))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        
        self.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 14px;
                background-color: #2d2d2d;
                color: #ffffff;
                font-weight: bold;
                font-size: 11px;
                text-align: center;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0A4A43, stop:0.5 #158F82, stop:1 #21c0ae);
                border-radius: 14px;
            }
        """)


class ResetWorker(QThread):
    """Worker thread for reset operation."""
    progress = pyqtSignal(str, int)
    finished = pyqtSignal(bool, str, dict)
    
    def __init__(self, create_backup=True, windsurf_version="stable", language: str = "en"):
        super().__init__()
        self.create_backup = create_backup
        self.windsurf_version = windsurf_version
        # language code for localized messages inside worker
        self.language = language

    def t_local(self, key: str) -> str:
        """Local translation helper for worker (uses worker language)."""
        return LANGUAGES.get(self.language, LANGUAGES["en"]).get(key, key)
        
    def run(self):
        try:
            storage_file = self.get_storage_file()
            backup_path = None
            
            # Step 1: Create backup if requested
            if self.create_backup and storage_file.exists():
                self.progress.emit("creating_backup", 20)
                backup_path = self.backup_file(storage_file)
                
            # Step 2: Load existing config
            self.progress.emit("loading_config", 40)
            data = {}
            if storage_file.exists():
                try:
                    with open(storage_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except json.JSONDecodeError:
                    pass
                    
            # Step 3: Generate new IDs
            self.progress.emit("generating_ids", 60)
            new_ids = self.generate_device_ids()
            data.update(new_ids)
            
            # Step 4: Save config
            self.progress.emit("saving_config", 80)
            storage_file.parent.mkdir(parents=True, exist_ok=True)
            with open(storage_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
                
            # Step 5: Complete
            self.progress.emit("complete", 100)
            
            result_msg = ""
            if backup_path:
                result_msg = f"{self.t_local('backup_created')} {backup_path}\n\n"
            
            self.finished.emit(True, result_msg, new_ids)
            
        except Exception as e:
            self.finished.emit(False, str(e), {})
            
    def get_storage_file(self) -> Path:
        """Get Windsurf storage file path."""
        system = platform.system()
        paths = {
            "Windows": Path(os.getenv("APPDATA", "")),
            "Darwin": Path.home() / "Library" / "Application Support",
            "Linux": Path.home() / ".config",
        }
        
        base_path = paths.get(system)
        if not base_path:
            # raise localized message
            raise WindsurfResetError(self.t_local('unsupported_os').format(system))
        
        # Select folder based on version
        windsurf_folder = "Windsurf - Next" if self.windsurf_version == "next" else "Windsurf"
        storage_path = base_path / windsurf_folder / "User" / "globalStorage" / "storage.json"
        
        if not base_path.exists():
            raise WindsurfResetError(self.t_local('base_dir_missing').format(base_path))
            
        return storage_path
        
    def backup_file(self, file_path: Path) -> Optional[Path]:
        """Create backup of the file."""
        if file_path.exists():
            backup_path = file_path.with_name(
                f"{file_path.name}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            shutil.copy2(file_path, backup_path)
            return backup_path
        return None
        
    def generate_device_ids(self) -> Dict[str, str]:
        """Generate new device IDs."""
        return {
            "telemetry.machineId": os.urandom(32).hex(),
            "telemetry.macMachineId": os.urandom(32).hex(),
            "telemetry.devDeviceId": str(uuid.uuid4()),
        }


class WindsurfResetGUI(QMainWindow):
    """Main GUI window for Windsurf Reset Tool."""
    
    def __init__(self):
        super().__init__()
        self.current_language = "en"
        self.windsurf_version = "stable"
        self.init_ui()
        
    def t(self, key: str) -> str:
        """Get translated string."""
        return LANGUAGES.get(self.current_language, LANGUAGES["en"]).get(key, key)
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(f"{self.t('title')} {self.t('version')}")
        self.setMinimumSize(800, 620)
        self.setStyleSheet(self.get_stylesheet())
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Header
        header_card = self.create_header_card()
        main_layout.addWidget(header_card)
        
        # Language, version, and config in one row
        top_row = QHBoxLayout()
        top_row.setSpacing(10)
        
        lang_card = self.create_language_card()
        top_row.addWidget(lang_card, 1)
        
        version_card = self.create_version_card()
        top_row.addWidget(version_card, 1)
        
        config_card = self.create_config_card()
        top_row.addWidget(config_card, 2)
        
        main_layout.addLayout(top_row)
        
        # Operations
        operations_card = self.create_operations_card()
        main_layout.addWidget(operations_card)
        
        # Display
        display_card = self.create_display_card()
        main_layout.addWidget(display_card)
        
        # Progress bar
        self.progress_bar = AnimatedProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Status bar
        system_name = platform.system()
        system_display = {"Windows": "Windows", "Darwin": "macOS", "Linux": "Linux"}.get(system_name, system_name)
        self.status_label = QLabel(f"🟢 {self.t('status_ready')} | 🖥️ {system_display}")
        self.status_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.status_label.setStyleSheet("color: #21c0ae; padding: 5px;")
        main_layout.addWidget(self.status_label)
        
        # Center window
        self.center_window()
        
    def create_header_card(self) -> CardWidget:
        """Create compact header card."""
        card = CardWidget()
        card.setMaximumHeight(75)
        
        # Custom gradient background for header
        card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0A4A43, stop:0.5 #158F82, stop:1 #21c0ae);
                border: none;
                border-radius: 12px;
            }
        """)
        
        layout = QHBoxLayout()
        
        # Title
        title_label = QLabel(f"🔧 {self.t('title')}")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #ffffff;")
        layout.addWidget(title_label)
        
        layout.addStretch()
        
        # Version badge
        version_label = QLabel(self.t('version'))
        version_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        version_label.setStyleSheet("""
            color: #ffffff;
            background-color: rgba(255, 255, 255, 0.2);
            padding: 6px 15px;
            border-radius: 15px;
        """)
        layout.addWidget(version_label)
        
        card.main_layout.addLayout(layout)
        return card
        
    def create_language_card(self) -> CardWidget:
        """Create language selector card."""
        card = CardWidget(f"🌍 {self.t('select_language')}")
        card.setMaximumHeight(120)
        card.setMinimumHeight(90)
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("🇬🇧 English", "en")
        self.lang_combo.addItem("🇷🇺 Русский", "ru")
        self.lang_combo.setMinimumHeight(38)
        self.lang_combo.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.lang_combo.setStyleSheet("""
            QComboBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3d3d3d, stop:1 #2d2d2d);
                color: #ffffff;
                border: 2px solid #158F82;
                border-radius: 19px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QComboBox:hover {
                border-color: #21c0ae;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #21c0ae;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: #ffffff;
                selection-background-color: #158F82;
                border: 2px solid #158F82;
                border-radius: 8px;
                padding: 5px;
            }
        """)
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        card.main_layout.addWidget(self.lang_combo)
        
        return card
        
    def create_version_card(self) -> CardWidget:
        """Create Windsurf version selector card."""
        card = CardWidget(f"🔀 {self.t('select_version')}")
        card.setMaximumHeight(120)
        card.setMinimumHeight(90)
        
        self.version_combo = QComboBox()
        self.version_combo.addItem("📦 " + self.t('version_stable'), "stable")
        self.version_combo.addItem("🚀 " + self.t('version_next'), "next")
        self.version_combo.setMinimumHeight(38)
        self.version_combo.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.version_combo.setStyleSheet("""
            QComboBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3d3d3d, stop:1 #2d2d2d);
                color: #ffffff;
                border: 2px solid #158F82;
                border-radius: 19px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QComboBox:hover {
                border-color: #21c0ae;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #21c0ae;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: #ffffff;
                selection-background-color: #158F82;
                border: 2px solid #158F82;
                border-radius: 8px;
                padding: 5px;
            }
        """)
        self.version_combo.currentIndexChanged.connect(self.change_version)
        card.main_layout.addWidget(self.version_combo)
        
        return card
        
    def create_config_card(self) -> CardWidget:
        """Create config location card."""
        card = CardWidget(f"📁 {self.t('config_location')}")
        card.setMaximumHeight(120)
        card.setMinimumHeight(90)
        
        # Create label and save reference for updates
        self.config_path_label = QLabel()
        self.config_path_label.setFont(QFont("Consolas", 9))
        self.config_path_label.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.3);
            color: #ffffff;
            padding: 10px 12px;
            border-radius: 6px;
            border-left: 3px solid #21c0ae;
            line-height: 1.4;
        """)
        self.config_path_label.setWordWrap(True)
        self.config_path_label.setMinimumHeight(50)
        
        # Set initial path
        try:
            storage_file = self.get_storage_file()
            self.config_path_label.setText(str(storage_file))
        except Exception as e:
            self.config_path_label.setText(f"❌ {str(e)}")
            self.config_path_label.setStyleSheet("color: #ff6b6b; padding: 5px; font-size: 10px;")
        
        card.main_layout.addWidget(self.config_path_label)
        return card
        
    def create_operations_card(self) -> CardWidget:
        """Create operations card with gradient buttons."""
        card = CardWidget(f"⚙️ {self.t('operations')}")
        
        layout = QGridLayout()
        layout.setSpacing(10)
        
        # Reset button - primary action
        self.reset_btn = GradientButton(f"🔄 {self.t('reset_button')}", "#0A4A43", "#21c0ae")
        self.reset_btn.clicked.connect(self.reset_device_ids)
        layout.addWidget(self.reset_btn, 0, 0)
        
        # View button
        self.view_btn = GradientButton(f"👁️ {self.t('view_button')}", "#0A4A43", "#158F82")
        self.view_btn.clicked.connect(self.view_config)
        layout.addWidget(self.view_btn, 0, 1)
        
        # About button
        self.about_btn = GradientButton(f"ℹ️ {self.t('about_button')}", "#1e5f73", "#2a8fa8")
        self.about_btn.clicked.connect(self.show_about)
        layout.addWidget(self.about_btn, 1, 0)
        
        # Exit button
        self.exit_btn = GradientButton(f"🚪 {self.t('exit_button')}", "#8B0000", "#DC143C")
        self.exit_btn.clicked.connect(self.close)
        layout.addWidget(self.exit_btn, 1, 1)
        
        card.main_layout.addLayout(layout)
        return card
        
    def create_display_card(self) -> CardWidget:
        """Create display card with styled text area."""
        card = CardWidget(f"📊 {self.t('display')}")
        
        # Text display
        self.display_text = QTextEdit()
        self.display_text.setReadOnly(True)
        self.display_text.setMinimumHeight(160)
        self.display_text.setMaximumHeight(180)
        self.display_text.setStyleSheet("""
            QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e1e1e, stop:1 #0d0d0d);
                color: #21c0ae;
                border: 2px solid #158F82;
                border-radius: 10px;
                padding: 10px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
                selection-background-color: #158F82;
                selection-color: #ffffff;
            }
            QScrollBar:vertical {
                background: #1e1e1e;
                width: 10px;
                border-radius: 5px;
                margin: 1px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #158F82, stop:1 #21c0ae);
                border-radius: 5px;
                min-height: 25px;
            }
            QScrollBar::handle:vertical:hover {
                background: #21c0ae;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Add shadow to text area
        text_shadow = QGraphicsDropShadowEffect()
        text_shadow.setBlurRadius(12)
        text_shadow.setColor(QColor(0, 0, 0, 100))
        text_shadow.setOffset(0, 3)
        self.display_text.setGraphicsEffect(text_shadow)
        
        self.display_text.setText(f"🟢 {self.t('status_ready')}")
        card.main_layout.addWidget(self.display_text)
        
        return card
        
    def get_stylesheet(self) -> str:
        """Get main window stylesheet with beautiful gradients."""
        return """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a1a1a, stop:1 #0d0d0d);
            }
            QWidget {
                color: #ffffff;
                font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
            }
            QLabel {
                color: #ffffff;
            }
            QMessageBox {
                background-color: #2d2d2d;
            }
            QMessageBox QLabel {
                color: #ffffff;
                font-size: 13px;
                padding: 10px;
            }
            QMessageBox QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0A4A43, stop:1 #158F82);
                color: #ffffff;
                border: 2px solid #21c0ae;
                border-radius: 10px;
                padding: 10px 25px;
                font-weight: bold;
                min-width: 90px;
                font-size: 12px;
            }
            QMessageBox QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #158F82, stop:1 #21c0ae);
            }
            QMessageBox QPushButton:pressed {
                background: #0A4A43;
            }
        """
        
    def change_language(self, index: int):
        """Change application language."""
        new_lang = self.lang_combo.itemData(index)
        if new_lang != self.current_language:
            self.current_language = new_lang
            self.update_ui_texts()
            
    def change_version(self, index: int):
        """Change Windsurf version."""
        new_version = self.version_combo.itemData(index)
        if new_version != self.windsurf_version:
            self.windsurf_version = new_version
            self.update_config_path()
            
    def update_ui_texts(self):
        """Update all UI texts after language change."""
        self.setWindowTitle(f"{self.t('title')} {self.t('version')}")
        self.reset_btn.setText(f"🔄 {self.t('reset_button')}")
        self.view_btn.setText(f"👁️ {self.t('view_button')}")
        self.about_btn.setText(f"ℹ️ {self.t('about_button')}")
        self.exit_btn.setText(f"🚪 {self.t('exit_button')}")
        
        # Update status with system info
        system_name = platform.system()
        system_display = {"Windows": "Windows", "Darwin": "macOS", "Linux": "Linux"}.get(system_name, system_name)
        self.status_label.setText(f"🟢 {self.t('status_ready')} | 🖥️ {system_display}")
        
        # Update display text if it shows ready status (use localized keyword)
        if self.t('status_ready') in self.display_text.toPlainText():
            self.display_text.setText(f"🟢 {self.t('status_ready')}")
            
    def update_config_path(self):
        """Update config path display when version changes."""
        try:
            storage_file = self.get_storage_file()
            self.config_path_label.setText(str(storage_file))
            self.config_path_label.setStyleSheet("""
                background-color: rgba(0, 0, 0, 0.3);
                color: #ffffff;
                padding: 10px 12px;
                border-radius: 6px;
                border-left: 3px solid #21c0ae;
                line-height: 1.4;
            """)
            # Update status with version name
            version_name = "Windsurf Next" if self.windsurf_version == "next" else "Windsurf"
            # Localized version name
            version_name = self.t('version_name_next') if self.windsurf_version == "next" else self.t('version_name_stable')
            self.status_label.setText(f"🟢 {self.t('status_ready')} - {version_name}")
        except Exception as e:
            self.config_path_label.setText(f"❌ {str(e)}")
            self.config_path_label.setStyleSheet("color: #ff6b6b; padding: 5px; font-size: 10px;")
            self.status_label.setText(f"⚠️ {str(e)}")
                
    def reset_device_ids(self):
        """Reset device IDs with confirmation."""
        reply = QMessageBox.question(
            self,
            self.t('warning'),
            self.t('reset_confirm'),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Ask about backup
            backup_reply = QMessageBox.question(
                self,
                self.t('backup_title'),
                self.t('backup_prompt'),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            
            create_backup = (backup_reply == QMessageBox.StandardButton.Yes)
            
            # Disable buttons
            self.set_buttons_enabled(False)
            
            # Show progress bar
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            # Start worker thread
            # Give language to worker for localized messages
            self.worker = ResetWorker(create_backup, self.windsurf_version, language=self.current_language)
            self.worker.progress.connect(self.update_progress)
            self.worker.finished.connect(self.reset_finished)
            self.worker.start()
            
    def update_progress(self, message_key: str, value: int):
        """Update progress bar."""
        self.progress_bar.setValue(value)
        self.status_label.setText(f"⏳ {self.t(message_key)}")
        
    def reset_finished(self, success: bool, message: str, new_ids: dict):
        """Handle reset completion."""
        self.progress_bar.setVisible(False)
        self.set_buttons_enabled(True)
        
        system_name = platform.system()
        system_display = {"Windows": "Windows", "Darwin": "macOS", "Linux": "Linux"}.get(system_name, system_name)
        
        if success:
            self.status_label.setText(f"✅ {self.t('complete')} | 🖥️ {system_display}")
            
            # Display new IDs
            display_text = f"✅ {self.t('reset_success')}\n\n"
            if message:
                display_text += message
            
            display_text += f"🔑 {self.t('new_ids')}:\n"
            display_text += "=" * 80 + "\n"
            for key, value in new_ids.items():
                display_text += f"{key}:\n  {value}\n\n"
                
            self.display_text.setText(display_text)
            
            QMessageBox.information(
                self,
                self.t('success'),
                self.t('reset_success')
            )
            QMessageBox.information(
                self,
                self.t('info'),
                self.t('reinstall_hint')
            )
        else:
            self.status_label.setText(f"❌ {self.t('error')} | 🖥️ {system_display}")
            self.display_text.setText(f"❌ Error:\n{message}")
            
            QMessageBox.critical(
                self,
                self.t('error'),
                f"{self.t('error')}: {message}"
            )
            
    def view_config(self):
        """View current configuration."""
        system_name = platform.system()
        system_display = {"Windows": "Windows", "Darwin": "macOS", "Linux": "Linux"}.get(system_name, system_name)
        
        try:
            storage_file = self.get_storage_file()
            
            if not storage_file.exists():
                self.display_text.setText(f"ℹ️ {self.t('no_config')}")
                QMessageBox.information(
                    self,
                    self.t('info'),
                    self.t('no_config')
                )
                return
                
            with open(storage_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            # Filter telemetry data
            telemetry_data = {k: v for k, v in data.items() if k.startswith("telemetry")}
            
            display_text = f"🔑 {self.t('current_ids')}:\n"
            display_text += "=" * 80 + "\n"
            
            for key, value in telemetry_data.items():
                display_text += f"{key}:\n  {value}\n\n"
                
            self.display_text.setText(display_text)
            self.status_label.setText(f"✅ {self.t('complete')} | 🖥️ {system_display}")
            
        except Exception as e:
            error_msg = f"❌ {self.t('error')}: {str(e)}"
            self.display_text.setText(error_msg)
            self.status_label.setText(f"❌ {self.t('error')} | 🖥️ {system_display}")
            
            QMessageBox.critical(
                self,
                self.t('error'),
                str(e)
            )
            
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            self.t('about_button'),
            self.t('about_text')
        )
        
    def set_buttons_enabled(self, enabled: bool):
        """Enable or disable all buttons."""
        self.reset_btn.setEnabled(enabled)
        self.view_btn.setEnabled(enabled)
        self.about_btn.setEnabled(enabled)
        self.exit_btn.setEnabled(enabled)
        
    def get_storage_file(self) -> Path:
        """Get Windsurf storage file path."""
        system = platform.system()
        paths = {
            "Windows": Path(os.getenv("APPDATA", "")),
            "Darwin": Path.home() / "Library" / "Application Support",
            "Linux": Path.home() / ".config",
        }
        
        base_path = paths.get(system)
        if not base_path:
            raise WindsurfResetError(f"Unsupported OS: {system}")
        
        # Select folder based on version
        windsurf_folder = "Windsurf - Next" if self.windsurf_version == "next" else "Windsurf"
        storage_path = base_path / windsurf_folder / "User" / "globalStorage" / "storage.json"
        
        if not base_path.exists():
            raise WindsurfResetError(f"Base directory does not exist: {base_path}")
            
        return storage_path
        
    def center_window(self):
        """Center window on screen."""
        frame_geometry = self.frameGeometry()
        screen_center = self.screen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Dark palette
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(26, 26, 26))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Base, QColor(30, 30, 30))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 45, 45))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 45))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.ColorRole.Link, QColor(33, 192, 174))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(21, 143, 130))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    
    app.setPalette(palette)
    
    window = WindsurfResetGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

