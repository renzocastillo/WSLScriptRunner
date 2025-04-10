import sys, os

# Add lib directory to path
parent_folder_path = os.path.dirname(__file__)
sys.path.append(os.path.join(parent_folder_path, 'lib'))

import subprocess
import json
from flowlauncher import FlowLauncher

class WSLScriptRunner(FlowLauncher):
    def __init__(self):
        self.settings = {}  # Initialize empty settings
        self.setting_scripts_dir = False  # Flag for settings mode
        self._initialize_settings()
        super().__init__()

    def _initialize_settings(self):
        """Initialize settings, creating settings.json if it doesn't exist"""
        self.settings = {}  # Start with empty settings
        try:
            settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
            if os.path.exists(settings_path):
                with open(settings_path, "r") as f:
                    loaded_settings = json.load(f)
                    if isinstance(loaded_settings, dict):
                        self.settings.update(loaded_settings)
        except Exception as e:
            print(f"Error loading settings: {str(e)}")

    def query(self, param: str = "") -> list:
        """
        Query is the entry point for your plugin,
        the param is what user typed after the plugin action keyword.
        """
        query = param.strip()

        # Handle settings command with path
        if query.lower().startswith('settings '):
            path = query[9:].strip()  # Get everything after "settings "
            if path:
                self.settings["scripts_dir"] = path
                try:
                    settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
                    with open(settings_path, "w") as f:
                        json.dump(self.settings, f, indent=2)
                    return [{
                        "Title": "Settings saved!",
                        "SubTitle": f"Scripts directory set to: {path}",
                        "IcoPath": "Images/app.png"
                    }]
                except Exception as e:
                    return [{
                        "Title": "Error saving settings",
                        "SubTitle": str(e),
                        "IcoPath": "Images/error.png"
                    }]

        # Handle bare settings command
        if query.lower() == 'settings':
            return [{
                "Title": "Enter scripts directory path",
                "SubTitle": "Type 'wsr settings YOUR_PATH' (e.g., wsr settings ~/scripts)",
                "IcoPath": "Images/app.png"
            }]

        if "scripts_dir" not in self.settings:
            return [{
                "Title": "Scripts directory not configured",
                "SubTitle": "Type 'wsr settings YOUR_PATH' to configure (e.g., wsr settings ~/scripts)",
                "IcoPath": "Images/error.png"
            }]

        scripts_dir = self.get_scripts_dir()
        if not scripts_dir:
            return [{
                "Title": "Error retrieving scripts directory",
                "SubTitle": "Check settings or ensure WSL is running.",
                "IcoPath": "Images/error.png"
            }]

        try:
            # List scripts in WSL
            list_cmd = f"find '{scripts_dir}' -maxdepth 1 -name '*.sh' -type f -exec basename {{}} \\;"
            scripts = subprocess.check_output(["wsl", "bash", "-c", list_cmd], 
                                           text=True,
                                           creationflags=subprocess.CREATE_NO_WINDOW).splitlines()
        except subprocess.CalledProcessError:
            return [{
                "Title": "Error reading scripts directory",
                "SubTitle": "Check if WSL is running and the directory exists",
                "IcoPath": "Images/error.png"
            }]

        results = []
        for script in scripts:
            if not query or query.lower() in script.lower():
                results.append({
                    "Title": script,
                    "SubTitle": f"Run {script}",
                    "IcoPath": "Images/app.png",
                    "JsonRPCAction": {
                        "method": "run_script",
                        "parameters": [script],
                        "dontHideAfterAction": False
                    },
                    "ContextData": {"script": script, "path": os.path.join(scripts_dir, script)}
                })

        if not query:
            results.insert(0, {
                "Title": "Configure Scripts Directory",
                "SubTitle": f"Current: {self.settings.get('scripts_dir', 'Not configured')}",
                "IcoPath": "Images/app.png"
            })

        return results if results else [{
            "Title": "No matching scripts found",
            "SubTitle": "Try a different search term or type 'settings' to configure",
            "IcoPath": "Images/app.png"
        }]

    def context_menu(self, data) -> list:
        """
        Optional context menu implementation
        """
        if not data:
            current_dir = self.settings.get("scripts_dir", "Not configured")
            return [{
                "Title": "Configure Scripts Directory",
                "SubTitle": f"Current: {current_dir}",
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method": "start_settings",
                    "parameters": [],
                    "dontHideAfterAction": True
                }
            }]
        
        script_data = data
        script_path = script_data.get("path", "")
        script_name = script_data.get("script", "")
        
        return [
            {
                "Title": f"Open script in editor",
                "SubTitle": f"Edit {script_name}",
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method": "edit_script",
                    "parameters": [script_path],
                    "dontHideAfterAction": False
                }
            },
            {
                "Title": "Open scripts directory",
                "SubTitle": self.settings.get("scripts_dir", "Not configured"),
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method": "open_scripts_dir",
                    "parameters": [],
                    "dontHideAfterAction": False
                }
            }
        ]

    def edit_script(self, script_path):
        try:
            subprocess.Popen(["wsl", "bash", "-c", f"code '{script_path}'"], 
                           creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception:
            return [{
                "Title": "Error opening editor",
                "SubTitle": "Make sure VS Code is installed in WSL",
                "IcoPath": "Images/error.png"
            }]
        return []

    def open_scripts_dir(self):
        scripts_dir = self.get_scripts_dir()
        if not scripts_dir:
            return [{
                "Title": "Error opening directory",
                "SubTitle": "Scripts directory is not accessible",
                "IcoPath": "Images/error.png"
            }]
        try:
            subprocess.Popen(["wsl", "bash", "-c", f"code '{scripts_dir}'"], 
                           creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception:
            return [{
                "Title": "Error opening directory",
                "SubTitle": "Make sure VS Code is installed in WSL",
                "IcoPath": "Images/error.png"
            }]
        return []

    def get_scripts_dir(self):
        if "scripts_dir" not in self.settings:
            return None
            
        scripts_dir = self.settings["scripts_dir"]
        try:
            resolved_path = subprocess.check_output(["wsl", "bash", "-c", f"echo $(eval echo {scripts_dir})"], 
                                                  text=True, 
                                                  creationflags=subprocess.CREATE_NO_WINDOW).strip()
            if not resolved_path:
                return None
            # Ensure the directory exists
            subprocess.check_output(["wsl", "bash", "-c", f"mkdir -p '{resolved_path}'"], 
                                  text=True,
                                  creationflags=subprocess.CREATE_NO_WINDOW)
            return resolved_path
        except subprocess.CalledProcessError:
            return None

    def run_script(self, script_name):
        scripts_dir = self.get_scripts_dir()
        if not scripts_dir:
            return [{
                "Title": "Error executing script",
                "SubTitle": "Scripts directory is not accessible.",
                "IcoPath": "Images/error.png"
            }]

        # Convert Windows path separators to Unix style
        script_path = os.path.join(scripts_dir, script_name).replace('\\', '/')
        try:
            # First ensure the script is executable
            subprocess.check_output(["wsl", "bash", "-c", f"chmod +x '{script_path}'"], 
                                 creationflags=subprocess.CREATE_NO_WINDOW)
            
            # Execute the script in WSL terminal
            subprocess.Popen([
                "wsl.exe",
                "--cd", os.path.dirname(script_path),
                "bash", "-ic", f"'{script_path}' ; echo '\\nPress Enter to close...' ; read"
            ])
            
        except Exception as e:
            return [{
                "Title": "Error executing script",
                "SubTitle": f"Error: {str(e)}",
                "IcoPath": "Images/error.png"
            }]
        return []

    def load_settings(self):
        self._initialize_settings()

    def save_settings(self):
        """Save current settings to settings.json"""
        try:
            settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
            os.makedirs(os.path.dirname(settings_path), exist_ok=True)  # Ensure directory exists
            with open(settings_path, "w") as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {str(e)}")

    def open_settings(self):
        try:
            # Update settings with the new scripts directory
            self.settings["scripts_dir"] = self.get_query()
            # Save to file
            settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
            with open(settings_path, "w") as f:
                json.dump(self.settings, f, indent=2)
            return [{
                "Title": "Settings saved",
                "SubTitle": f"Scripts directory set to: {self.settings['scripts_dir']}",
                "IcoPath": "Images/app.png"
            }]
        except Exception as e:
            print(f"Error saving settings: {str(e)}")
            return [{
                "Title": "Error saving settings",
                "SubTitle": str(e),
                "IcoPath": "Images/error.png"
            }]

    def get_plugin_metadata(self):
        return {
            "ID": "FlowLauncher.WSLScriptRunner",
            "ActionKeyword": "wsr",
            "Name": "WSL Script Runner",
            "Description": "Run your shell scripts in WSL",
            "Author": "renzo",
            "Version": "1.0.0",
            "Language": "python",
            "Website": "https://github.com/renzocastillo/WSLScriptRunner/",
            "ExecuteFileName": "main.py",
            "IcoPath": "Images/app.png"
        }

    def start_settings(self):
        """Start the settings input mode"""
        self.setting_scripts_dir = True
        return [{
            "Title": "Enter scripts directory path",
            "SubTitle": "Example: ~/scripts or /home/user/scripts",
            "IcoPath": "Images/app.png"
        }]

if __name__ == "__main__":
    WSLScriptRunner()