import click
from pathlib import Path
from talos.utils.yaml_loader import load_yaml
from talos.llm.ollama_client import OllamaClient
from talos.tools import create_tools
from talos.core.controller import AgentController
from talos.utils.logging import init_logger

@click.command()
@click.option(
    "-c", "--config",
    default="configs/default.yaml",
    type=click.Path(exists=True, dir_okay=False),
    help="Path to YAML configuration"
)
def main(config):
    cfg  = load_yaml(config)
    work = Path(cfg["target_directory"]).expanduser()
    work.mkdir(parents=True, exist_ok=True)

    logger = init_logger()

    client = OllamaClient(
        cfg["llm_server"]["ip"],
        cfg["llm_server"]["port"]
    )
    tools  = create_tools(cfg["utilities"], base_dir=work)
    agent  = AgentController(client, tools, cfg["project_description"])
    logger.info("Agent starting with %s", config)
    agent.run()

if __name__ == "__main__":
    main()