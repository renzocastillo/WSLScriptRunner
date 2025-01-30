import json
import sys
from abc import ABCMeta, abstractmethod

class FlowLauncher(metaclass=ABCMeta):
    def __init__(self):
        """
        Initialize the launcher
        """
        if len(sys.argv) > 1:
            request = json.loads(sys.argv[1])
            method_name = request.get("method", "query")
            method = getattr(self, method_name)
            params = request.get("parameters", [])
            results = method(*params) if isinstance(params, list) else method(params)
            print(json.dumps({"result": results, "debugMessage": ""}))

    @abstractmethod
    def query(self, param: str = "") -> list:
        """
        Query is the entry point for your plugin,
        the param is what user typed after the plugin action keyword.
        """
        return []

    def context_menu(self, data) -> list:
        """
        Optional context menu implementation
        """
        return [] 