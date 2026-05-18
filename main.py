import argparse
import asyncio

from chimera.services.terminal import print_heading
from chimera.workflow import run


def main() -> None:
    parser = argparse.ArgumentParser(prog="chimera", description="Run AI workflow.", add_help=True)
    parser.add_argument("-p", "--project-name", help="Project name to run workflow on", type=str)
    args = parser.parse_args()

    asyncio.run(print_heading())
    asyncio.run(run(project_name=args.project_name))


if __name__ == "__main__":
    main()
