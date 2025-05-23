from __future__ import annotations
import json, logging
from talos.utils.logging import init_logger

_LOG = init_logger("talos.controller")

class AgentController:
    def __init__(self, ollama_client, tools: dict, project_description: str):
        self.llm     = ollama_client
        self.tools   = tools
        self.history = []
        self.project = project_description

    def run(self):
        self._system_prompt()
        while True:
            prompt = self._compose_prompt()
            answer = self.llm.generate(prompt)
            if not answer:
                break

            try:
                action = json.loads(answer)
            except json.JSONDecodeError:
                action = None

            if isinstance(action, dict) and action.get("tool") in self.tools:
                res = self._run_tool(action)
                self._push_user(f"Tool output: {res}")
            else:                          
                print("\n=== AGENT OUTPUT ===\n" + answer)
                break

    def _system_prompt(self):
        sys = (
            "You are an autonomous coding agent.\n"
            f"Project: {self.project}\n"
            "Tools: terminal, code_writer (JSON format: "
            '{"tool":"terminal","command":"ls"} or '
            '{"tool":"code_writer","path":"main.py","content":"print(42)"} ).\n'
            "First plan, then act."
        )
        self.history.append(("system", sys))

    def _compose_prompt(self) -> str:
        return "\n".join(role + ": " + msg for role, msg in self.history)

    def _push_user(self, msg: str):
        self.history.append(("user", msg))

    def _run_tool(self, action: dict):
        tool_name = action.pop("tool")
        res = self.tools[tool_name].execute(**action)
        _LOG.info("ran %s with %s", tool_name, action)
        return res