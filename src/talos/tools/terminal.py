import subprocess
from .base import BaseTool

class TerminalTool(BaseTool):
    def execute(self, command: str) -> str:
        proc = subprocess.run(
            command, shell=True, cwd=self.base_dir,
            capture_output=True, text=True
        )
        return proc.stdout if proc.returncode == 0 else proc.stderr