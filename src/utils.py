import importlib
import json
import sys
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path


def load_config():
    config_path = Path(__file__).parent / "user.json"

    config_arg = None
    for arg in sys.argv[1:]:
        if arg == "-c" or arg == "--config":
            config_arg = ("next", arg)
            break
        if arg.startswith("-c=") or arg.startswith("--config="):
            config_arg = ("equals", arg.split("=", 1)[1])
            break

    if config_arg is not None:
        if config_arg[0] == "equals":
            config_path = Path(config_arg[1]).expanduser().resolve()
        else:
            try:
                idx = sys.argv.index(config_arg[1]) + 1
                config_path = Path(sys.argv[idx]).expanduser().resolve()
            except (ValueError, IndexError):
                exit("Missing value for --config option.")

    if config_path.exists():
        return json.loads(config_path.read_bytes())
    return None


def get_loader_class(config):
    # Load data loader from config. Default loader is EODFileLoader
    loader_name = config.get("LOADER", "EODFileLoader")

    loader_module = importlib.import_module(f"loaders.{loader_name}")

    return getattr(loader_module, loader_name)


def parse_cli_options():
    # Add CLI options
    parser = ArgumentParser(
        description="Python CLI tool to plot RRG charts",
        epilog="https://github.com/BennyThadikaran/RRG-Lite",
    )

    parser.add_argument(
        "-c",
        "--config",
        type=lambda x: Path(x).expanduser().resolve(),
        metavar="filepath",
        help="Custom config file",
    )

    parser.add_argument(
        "-d",
        "--date",
        type=datetime.fromisoformat,
        metavar="str",
        help="ISO format date YYYY-MM-DD.",
    )

    parser.add_argument(
        "--tf",
        action="store",
        default="weekly",
        help="Timeframe string.",
    )

    parser.add_argument(
        "-t",
        "--tail",
        type=int,
        default=4,
        metavar="int",
        help="Length of tail. Default 3",
    )

    parser.add_argument(
        "-b",
        "--benchmark",
        default=None,
        metavar="str",
        help="Benchmark index name",
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-f",
        "--file",
        type=lambda x: Path(x).expanduser().resolve(),
        default=None,
        metavar="filepath",
        help="File containing list of stocks. One on each line",
    )

    group.add_argument(
        "--sym",
        nargs="+",
        metavar="SYM",
        help="Space separated list of stock symbols.",
    )

    group.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Print the current version.",
    )

    return parser.parse_args()
