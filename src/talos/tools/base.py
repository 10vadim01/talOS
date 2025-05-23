class BaseTool:
    def __init__(self, base_dir):
        self.base_dir = base_dir
    def execute(self, **kwargs):
        raise NotImplementedError