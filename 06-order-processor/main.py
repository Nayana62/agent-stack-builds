from graph import graph
from mock_data import SAMPLE_ORDERS
from langgraph.types import Command

for order in SAMPLE_ORDERS:
    thread_id = order["order_id"]
    config = {"configurable": {"thread_id": thread_id}}

    print(
        f"\n--- {order['order_id']} ({order['customer_name']}, ${order['total']}) ---"
    )

    result = graph.invoke(order, config)  # type ignore

    # Check if the graph paused for human review
    snapshot = graph.get_state(config)
    if snapshot.next:  # there's a node waiting to run
        print(f"  Paused for human review!")
        print(f"  Interrupt: {snapshot.tasks[0].interrupts[0].value}")

        # Simulate human approving
        result = graph.invoke(Command(resume="pass"), config)

    print(f"  Final state: {result}")
    print("===================================")
    print(graph.get_graph().draw_mermaid())
    print("===================================")
