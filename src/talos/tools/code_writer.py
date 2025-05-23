import os
from .base import BaseTool

class CodeWriterTool(BaseTool):
    def execute(self, path: str, content: str) -> str:
        abs_root = os.path.abspath(self.base_dir)
        abs_path = os.path.abspath(os.path.join(self.base_dir, path))
        if not abs_path.startswith(abs_root):
            return "[DENIED] path outside sandbox"

        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as fp:
            fp.write(content)
        return f"[OK] wrote {path}"