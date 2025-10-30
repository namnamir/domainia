import sys
import runpy
import tomllib


def get_version():
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
    return data["project"]["version"]


def main():
    print("Welcome to Domainia Scanner!")

    if len(sys.argv) == 1:
        # Show __init__.py help
        sys.argv = ["__init__.py", "-h"]
        runpy.run_module("__init__", run_name="__main__")
        return

    cmd = sys.argv[1].lower()
    if cmd == "scan":
        print("[*] Running the scanner...")
        # Forward remaining CLI args to __init__.py's argparse
        sys.argv = ["__init__.py", *sys.argv[2:]]
        # Execute __init__ as if run directly (so its if __name__ == '__main__' block runs)
        runpy.run_module("__init__", run_name="__main__")
    elif cmd == "help":
        # Show __init__.py help
        sys.argv = ["__init__.py", "-h"]
        runpy.run_module("__init__", run_name="__main__")
    elif cmd == "version":
        print(f"Domainia Scanner version {get_version()}")
    else:
        # Forward unknown subcommand to __init__ help for clarity
        sys.argv = ["__init__.py", "-h"]
        runpy.run_module("__init__", run_name="__main__")


if __name__ == "__main__":
    main()
