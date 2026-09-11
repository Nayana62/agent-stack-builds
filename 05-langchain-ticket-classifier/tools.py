from langchain_core.tools import tool
from mock_data import CUSTOMERS, KNOWLEDGE_BASE


@tool
def lookup_customer(customer_id: str) -> dict | None:
    """Look up customer details by their ID like C-1001."""
    return CUSTOMERS.get(customer_id)


@tool
def check_knowledge_base(keyword: str) -> dict | None:
    """Search knowledge base articles by keyword like login, billing, api, export."""
    return KNOWLEDGE_BASE.get(keyword.lower())
