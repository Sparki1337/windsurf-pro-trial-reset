# Changelog

All notable changes to this project will be documented in this file.

## [1.4.0] - 2025-01-11

### Added
- 🖥️ **Cross-Platform Support**: Full support for Windows, macOS, and Linux
- 🌐 Platform detection and automatic path configuration
- 📊 System information display in status bar (shows current OS)
- 🔧 Multi-platform build scripts with target selection (`-p windows/macos/linux/all`)
- 🤖 GitHub Actions workflow for automated builds on all platforms
- 📦 Platform-specific output files (.exe for Windows, .app for macOS, .bin for Linux)

### Changed
- 🎯 Updated version to 1.4 across all components
- 📝 Enhanced README with cross-platform installation instructions
- 🔄 Improved build scripts (build.py and build_onefile.py) with platform targeting
- 💬 Updated "About" dialog to mention cross-platform support
- 🛠️ Better compiler selection based on platform (MSVC/MinGW for Windows, Clang for macOS, GCC for Linux)

### Fixed
- 🔍 Path handling now works correctly on all operating systems
- 🗂️ Configuration file location detection for macOS and Linux
- ⚙️ Build process respects platform-specific requirements

### Technical Details
- Windows: `%APPDATA%\Windsurf\...`
- macOS: `~/Library/Application Support/Windsurf/...`
- Linux: `~/.config/Windsurf/...`

### Important Notes
- **Platform Support**: Now supports **Windows, macOS, and Linux**! 🎉
- **Cross-Compilation**: Note that you need to build on the target platform (e.g., build macOS version on a Mac)
- **Automated Builds**: Use GitHub Actions for automatic multi-platform builds

## [1.3.0] - 2025-01-11

### Added
- Support for Windsurf Next (Insiders) version
- Version selector in UI
- Configuration location display
- Reinstall hint after successful reset
- Enhanced error handling with localized messages

### Changed
- Improved UI layout with compact cards
- Better progress bar visibility
- Enhanced gradient animations
- Optimized window sizing

### Fixed
- Language switching now properly updates all UI elements
- Configuration path updates when switching versions
- Better error messages for missing configuration files

### Important Notes
- **Platform Support**: Currently **Windows only**. macOS and Linux support is planned for future releases.
