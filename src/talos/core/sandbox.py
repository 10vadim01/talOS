from pathlib import Path

def within_sandbox(base: Path, target: Path) -> bool:
    return target.resolve().is_relative_to(base.resolve())