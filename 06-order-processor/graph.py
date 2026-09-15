from typing import Literal, TypedDict
from mock_data import INVENTORY, SAMPLE_ORDERS
from langgraph.types import interrupt


class OrderState(TypedDict):
    # Input fields (come from the order)
    order_id: str
    customer_name: str
    items: list[str]
    total: float
    # Output fields (each node writes one of these)
    valid_order: bool | None
    in_stock: bool | None
    payment_status: Literal["failed", "successful"] | None
    needs_human_review: bool | None
    human_review_status: Literal["pass", "fail"] | None
    fulfillment_status: Literal["fulfilled", "cancelled"] | None


def validate_order(state: OrderState) -> dict:
    if not state["customer_name"] or not state["items"] or state["total"] <= 0:
        return {"valid_order": False}
    return {"valid_order": True}


def check_inventory(state: OrderState) -> dict:
    for item in state["items"]:
        if INVENTORY[item] == 0:
            return {"in_stock": False}
    return {"in_stock": True}


def process_payment(state: OrderState) -> dict:
    return {"payment_status": "successful"}


def human_review(state: OrderState) -> dict:
    decision = interrupt(
        {
            "message": f"Order {state['order_id']} for ${state['total']} needs approval",
            "items": state["items"],
            "customer": state["customer_name"],
        }
    )
    return {"human_review_status": decision}


def auto_fulfill(state: OrderState) -> dict:
    return {"fulfillment_status": "fulfilled"}


def route_after_validation(state: OrderState) -> str:
    if state["valid_order"] == True:
        return "check_inventory"
    else:
        return END


def route_after_check_inventory(state: OrderState) -> str:
    if state["in_stock"] == True:
        return "process_payment"
    else:
        return END


def route_after_payment(state: OrderState) -> str:
    if state["total"] > 1000:
        return "human_review"
    return "auto_fulfill"


from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver

# Create the graph
builder = StateGraph(OrderState)

# Add nodes
builder.add_node("validate_order", validate_order)
builder.add_node("check_inventory", check_inventory)
builder.add_node("process_payment", process_payment)
builder.add_node("human_review", human_review)
builder.add_node("auto_fulfill", auto_fulfill)

# Add edges
builder.add_edge(START, "validate_order")
builder.add_conditional_edges("validate_order", route_after_validation)
builder.add_conditional_edges("check_inventory", route_after_check_inventory)
builder.add_conditional_edges("process_payment", route_after_payment)
builder.add_edge("human_review", "auto_fulfill")
builder.add_edge("auto_fulfill", END)

# Compile
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)
