from importlib import import_module

_MAPPING = {
    "terminal": "talos.tools.terminal:TerminalTool",
    "code_writer": "talos.tools.code_writer:CodeWriterTool",
}


def create_tools(names, *, base_dir):
    tools = {}
    for name in names:
        if name not in _MAPPING:
            raise ValueError(f"Unknown tool: {name}")
        mod_path, cls_name = _MAPPING[name].split(":")
        cls = getattr(import_module(mod_path), cls_name)
        tools[name] = cls(base_dir=base_dir)
    return tools