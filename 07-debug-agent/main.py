from graph import agent
import time

# Config: thread_id enables checkpointing, recursion_limit caps iterations
config = {
    "configurable": {
        "thread_id": "debug-session-1",
    },
    "recursion_limit": 25,  # Max graph steps (each reason + act = ~2 steps, so 25 ≈ 10-12 tool calls)
}

user_message = "The tests in tests/test_auth.py are failing with a KeyError on 'role'. Can you investigate and fix the bug?"
# user_message = "what was the error you fixed before?"

max_retries = 3
result = None

for attempt in range(max_retries):
    try:
        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_message}]},
            config=config,
        )
        break
    except Exception as e:
        if "rate" in str(e).lower() or "429" in str(e):
            wait = 30 * (attempt + 1)
            print(f"Rate limited. Waiting {wait}s...")
            time.sleep(wait)
        else:
            raise

if result is None:
    print("Failed after all retries.")
else:
    for message in result["messages"]:
        print(f"\n{'='*60}")
        if message.type == "ai":
            # Show text content if present
            if isinstance(message.content, str) and message.content:
                print(f"[AI]: {message.content[:1000]}")
            elif isinstance(message.content, list):
                for block in message.content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        print(f"[AI]: {block['text'][:1000]}")

            # Show tool calls if present
            if hasattr(message, "tool_calls") and message.tool_calls:
                for tc in message.tool_calls:
                    print(f"[AI → tool call]: {tc['name']}({tc['args']})")

        elif message.type == "tool":
            print(f"[Tool: {message.name}]: {message.content[:1000]}")

        elif message.type == "human":
            print(f"[Human]: {message.content}")
