import argparse
import sys
from typing import Any, IO, Optional

from jinja2 import Environment, Template
import yaml


class UnknownBase(Exception):
    def __init__(self, base: str):
        super().__init__(f"Unknown base: {base}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render snapcraft.yaml for a specific base")
    parser.add_argument("base", help="core base to use")
    parser.add_argument("-o", "--output", help="output file", default="snapcraft.yaml", type=argparse.FileType("w"))
    parser.add_argument("-t", "--template", help="template file", default="snapcraft-template.yaml", type=argparse.FileType())
    parser.add_argument("-d", "--data", help="data file with per-base variables", default="bases.yaml", type=argparse.FileType())
    return parser.parse_args()


def get_base_data(fd: IO, base: str) -> Optional[dict[str, dict[str, Any]]]:
    data = yaml.safe_load(fd)
    base_data = data.get(base)
    if base_data is not None:
        base_data["base"] = base
    return base_data


def render_template(template_file: IO, out_file: IO, data: dict[str, Any]):
    template = Template(template_file.read())
    out_file.write(template.render(**data))


def main() -> int:
    args = parse_args()
    data = get_base_data(args.data, args.base)
    if data is None:
        print(f"Unknown base {args.base}", file=sys.stderr)
        return 1
    render_template(args.template, args.output, data)
    print(f"Generated {args.output.name} for {args.base} base", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
