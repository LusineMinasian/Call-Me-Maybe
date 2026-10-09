import argparse
import sys
from typing import Sequence

DEFAULT_FUNCTIONS = "data/input/functions_definition.json"
DEFAULT_INPUT = "data/input/function_calling_tests.json"
DEFAULT_OUTPUT = "data/output/function_calls.json"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments.

    Args:
        argv: Arguments to parse, or None to use ``sys.argv``.

    Returns:
        The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog="python -m src",
        description="Translate prompts into function calls.",
    )
    parser.add_argument(
        "--functions_definition",
        default=DEFAULT_FUNCTIONS,
        help="path to the functions definition JSON file",
    )
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT,
        help="path to the JSON file with the prompts",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="path of the JSON file to write",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the program.

    Args:
        argv: Arguments to parse, or None to use ``sys.argv``.

    Returns:
        The process exit code.
    """
    args = parse_args(argv)
    print(f"functions: {args.functions_definition}")
    print(f"input:     {args.input}")
    print(f"output:    {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())