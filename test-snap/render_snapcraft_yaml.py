import argparse
import sys
from pathlib import Path
from typing import Any, IO, Optional

from jinja2 import Environment, Template
import yaml


BASE_DIR = Path(__file__).parent
TEMPLATE_FILE = BASE_DIR / "snapcraft-template.yaml"
DATA_FILE = BASE_DIR / "bases.yaml"
SNAPCRAFT_FILE = BASE_DIR / "snapcraft.yaml"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render snapcraft.yaml for a specific base")
    parser.add_argument("base", help="core base to use")
    return parser.parse_args()


def get_base_data(data_file: Path, base: str) -> Optional[dict[str, dict[str, Any]]]:
    with data_file.open() as fd:
        data = yaml.safe_load(fd)
    base_data = data.get(base)
    if base_data is not None:
        base_data["base"] = base
    return base_data


def render_template(template_file: Path, out_file: Path, data: dict[str, Any]):
    template = Template(template_file.read_text())
    out_file.write_text(template.render(**data))


def main() -> int:
    args = parse_args()
    data = get_base_data(DATA_FILE, args.base)
    if data is None:
        print(f"Unknown base {args.base}", file=sys.stderr)
        return 1
    render_template(TEMPLATE_FILE, SNAPCRAFT_FILE, data)
    print(f"Generated {SNAPCRAFT_FILE} for {args.base} base", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
