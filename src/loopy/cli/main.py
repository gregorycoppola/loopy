import argparse
from rich.console import Console

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Loopy BP experiments.")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("triangle", help="Run triangle graph experiment.")
    subparsers.add_parser("square", help="Run square graph experiment.")
    subparsers.add_parser("dating", help="Run dating graph experiment.")
    args = parser.parse_args()

    if args.command == "triangle":
        from loopy.experiments.triangle import run
        run()
    elif args.command is None:
        parser.print_help()
    else:
        console.print(f"[yellow]Command '{args.command}' not yet implemented.[/yellow]")

if __name__ == "__main__":
    main()