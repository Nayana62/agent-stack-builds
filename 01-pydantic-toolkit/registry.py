from textwrap import indent

from models import Tool, ToolParameter
import json

class ToolRegistry:
    def __init__(self):
        self.tools: dict[str, Tool] = {}

    def add(self, tool: Tool):
        if tool.name in self.tools:
            raise ValueError("tool with the name already exists")
        else:
            self.tools[tool.name] = tool

    def remove(self, name: str):
        if name not in self.tools:
            raise ValueError(f"tool with {name} does not exist")
        else:
            del self.tools[name]

    def get(self, name: str) -> Tool:
        if name not in self.tools:
            raise ValueError(f"tool with {name} does not exist")
        else:
            tool = self.tools[name]
            return tool

    def get_schema(self, name: str) -> dict:
        if name not in self.tools:
            raise ValueError(f"tool with {name} does not exist")
        else:
            tool = self.get(name)
            return tool.model_json_schema()

    def list_tools(self) -> list[Tool]:
        return list(self.tools.values())

    def search(self, keyword: str) -> list[Tool]:
        search_result: list[Tool] = []
        for tool in self.tools.values():
            if keyword.lower() in tool.name.lower() or keyword.lower() in tool.description.lower():
                search_result.append(tool)
        return search_result


    def save(self, filepath: str):
        with open(filepath, "w") as f:
            json.dump(
                [tool.model_dump() for tool in self.tools.values()],
                f,
                indent=2
            )


    def load(self, filepath: str):
        with open(filepath, "r") as f:
            data = json.load(f)
        for tool_data in data:
            tool = Tool(**tool_data)
            self.add(tool)


if __name__ == "__main__":
    registry = ToolRegistry()

    registry.add(Tool(
        name="create_ticket",
        description="Creates a support ticket",
        parameters=[
            ToolParameter(name="title", param_type="string", description="Title of the ticket"),
            ToolParameter(name="priority", param_type="integer", description="Priority from 1 to 5"),
        ]
    ))

    registry.add(Tool(
        name="lookup_customer",
        description="Finds a customer by their ID",
        parameters=[
            ToolParameter(name="customer_id", param_type="string", description="The customer's unique ID"),
        ]
    ))

    registry.add(Tool(
        name="check_order_status",
        description="Checks the current status of an order",
        parameters=[
            ToolParameter(name="order_id", param_type="string", description="The order's unique ID"),
        ]
    ))

    # List all
    print("All tools:", [t.name for t in registry.list_tools()])

    # Search
    print("Search 'customer':", [t.name for t in registry.search("customer")])

    # Save
    registry.save("tools.json")
    print("Saved to tools.json")

    # Load into a fresh registry
    new_registry = ToolRegistry()
    new_registry.load("tools.json")
    print("Loaded tools:", [t.name for t in new_registry.list_tools()])

    print(json.dumps(registry.get_schema("create_ticket"), indent=2))