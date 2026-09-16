import os
import sqlite3
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
from tools import list_files, read_file, search_code, write_file, execute_command

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)
tools = [list_files, read_file, search_code, write_file, execute_command]


# Checkpoints live in a file next to this module, so sessions survive restarts.
# Note: SqliteSaver.from_conn_string() is a context manager — it closes the connection
# on exit, so it can't be used for a module-level saver. Build the connection directly.
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "checkpoints.sqlite")

# check_same_thread=False is safe here: SqliteSaver guards the connection with a lock
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
checkpointer = SqliteSaver(conn)

agent = create_agent(
    model=model,
    tools=tools,
    checkpointer=checkpointer,
    system_prompt="""You are a debugging assistant. You investigate bugs in a Python codebase, find the root cause, fix it, and verify the fix.

## How to work
1. List the project files to understand the structure.
2. Run the failing tests to see the actual error message.
3. Read only the files relevant to the error — start with the file mentioned in the traceback, then follow imports if needed.
4. Once you identify the root cause, stop investigating. Do not search or read more files to confirm what you already know.
5. Apply the fix by writing to the file.
6. Run the tests once to verify. If they pass, you are done.

## Rules
- Never re-read a file you have already read in this session.
- Never search for something you already found by reading a file.
- If you have enough information to identify the bug, fix it immediately — do not gather more evidence.
- One test run to verify is enough. Do not run the same tests twice with different commands.
- When explaining the fix, be specific: name the file, the line, the old value, and the new value.""",
)
