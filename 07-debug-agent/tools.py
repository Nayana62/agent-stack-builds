import os
import subprocess
from langchain_core.tools import tool

BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mock_codebase")
IGNORE_DIRS = {"__pycache__", ".pytest_cache", ".git", "node_modules"}


def list_files() -> str:
    """List all files in the project directory recursively. Use this to understand the project structure before diving into specific files."""
    files = []
    for root, dirs, filenames in os.walk(BASE_PATH):
        # This modifies dirs IN-PLACE so os.walk skips them
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for filename in filenames:
            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, BASE_PATH)
            files.append(relative_path)
    return "\n".join(files)


@tool
def read_file(file_path: str) -> str:
    """Read the contents of a specific file. Pass the relative path from the project root (e.g. 'auth.py' or 'tests/test_auth.py')."""
    full_path = os.path.join(BASE_PATH, file_path)
    try:
        with open(full_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."


@tool
def search_code(keyword: str) -> str:
    """Search for a keyword across all files in the project. Returns matching filenames, line numbers, and line content. Use this to trace where functions or variables are defined and used."""
    matches = []
    for root, dirs, filenames in os.walk(BASE_PATH):
        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, BASE_PATH)
            try:
                with open(full_path, "r") as f:
                    for line_num, line in enumerate(f, start=1):
                        if keyword in line:
                            matches.append(
                                f"{relative_path}:{line_num}: {line.rstrip()}"
                            )
            except Exception:
                continue

    if not matches:
        return f"No matches found for '{keyword}'."
    return "\n".join(matches)


@tool
def write_file(file_path: str, content: str) -> str:
    """Write content to a file, replacing its entire contents. Use this to apply a bug fix after identifying the issue. Pass the relative path from the project root."""
    full_path = os.path.join(BASE_PATH, file_path)
    try:
        with open(full_path, "w") as f:
            f.write(content)
        return f"Successfully wrote to '{file_path}'."
    except Exception as e:
        return f"Error writing to '{file_path}': {e}"


@tool
def execute_command(command: str) -> str:
    """Execute a shell command in the project directory. Use this to run tests (e.g. 'python tests/test_auth.py') or run code to see error messages. Returns both stdout and stderr."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=BASE_PATH,
            timeout=30,
        )
        output = ""
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}"
        return output if output else "Command completed with no output."
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds."
    except Exception as e:
        return f"Error executing command: {e}"
