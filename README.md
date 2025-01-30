# WSL Script Runner for Flow Launcher

A Flow Launcher plugin that allows you to quickly find and execute your WSL shell scripts from anywhere in Windows.

![WSL Script Runner Demo](Images/app.png)

## Features

- 🔍 Quickly find your shell scripts using fuzzy search
- ⚡ Execute WSL scripts directly from Flow Launcher
- 📝 Open scripts in VS Code for editing
- 📁 Configurable scripts directory
- 🖱️ Right-click menu for additional actions
- 🚀 No need to open WSL terminal manually

## Installation

### Method 1: Flow Launcher Plugin Manager
```
pm install WSL Script Runner
```

### Method 2: Manual Installation
1. Download the latest release from the [releases page](https://github.com/YourRepo/releases)
2. Extract the zip file to `%APPDATA%\FlowLauncher\Plugins`
3. Restart Flow Launcher

## Requirements

- Windows 10/11 with WSL installed
- Flow Launcher
- VS Code with WSL extension (for editing scripts)

## Usage

1. Type `wsl` in Flow Launcher to activate the plugin
2. Start typing to search for your scripts
3. Press Enter to execute the selected script
4. Right-click or Shift+Enter for additional options:
   - Open script in editor (VS Code)
   - Open scripts directory
   - Configure scripts directory

## Configuration

By default, the plugin looks for scripts in `~/scripts` in your WSL home directory. You can change this by:

1. Type `wsl` in Flow Launcher
2. Right-click on any result
3. Select "Configure Scripts Directory"
4. Edit the `settings.json` file that opens

Example `settings.json`:
```json
{
    "scripts_dir": "~/my-scripts"
}
```

## Development

### Prerequisites
- Python 3.8 or higher
- Windows 10/11 with WSL
- Flow Launcher

### Setup
1. Clone the repository
```bash
git clone https://github.com/renzocastillo/WSLScriptRunner
```

2. Create a symbolic link in Flow Launcher's plugin directory
```powershell
mklink /D "%APPDATA%\FlowLauncher\Plugins\Flow.Launcher.Plugin.WSLScriptRunner" "path\to\your\clone"
```

### Project Structure
```
Flow.Launcher.Plugin.WSLScriptRunner/
├── main.py              # Main plugin code
├── plugin.json          # Plugin metadata
├── README.md           # This file
├── Images/
│   └── app.png         # Plugin icon
└── lib/
    └── flowlauncher.py # Flow Launcher interface
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. By contributing to this project, you agree to license your work under the GNU General Public License v3.0.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details. This means you are free to use, modify, and distribute this software, but any derivative work must also be licensed under the GPL v3.0.

## Acknowledgments

- Flow Launcher team for creating an amazing launcher
- WSL team for making Linux integration possible on Windows
