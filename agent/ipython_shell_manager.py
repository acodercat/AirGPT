from IPython.core.interactiveshell import InteractiveShell
from typing import Optional

class IPythonShellManager:
    _instance: Optional['IPythonShellManager'] = None
    
    def __new__(cls) -> 'IPythonShellManager':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._shells = {}
        return cls._instance

    def get_shell(self, id: str) -> InteractiveShell:
        if id not in self._shells:
            new_shell = InteractiveShell.instance()
            self._shells[id] = new_shell
            print(f"Created new shell with id {id}")
        else:
            print(f"Reusing shell with id {id}")
        return self._shells[id]

    def remove_shell(self, id: str) -> None:
        if id in self._shells:
            del self._shells[id]
            print(f"Removed shell with id {id}")
        else:
            print(f"Attempted to remove non-existent shell with id {id}")

    def setup_environment(self, shell: InteractiveShell, code: str) -> None:
        if code:
            try:
                shell.run_cell(code)
            except Exception as e:
                print(f"Error running preloaded code: {e}")

ipython_shell_manager = IPythonShellManager()