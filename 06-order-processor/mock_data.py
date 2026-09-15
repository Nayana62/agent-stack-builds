INVENTORY = {
    "laptop": 10,
    "mouse": 50,
    "keyboard": 30,
    "monitor": 5,
    "headphones": 0,  # out of stock
}

SAMPLE_ORDERS = [
    {
        "order_id": "ORD-001",
        "customer_name": "Alice",
        "items": ["laptop", "mouse"],
        "total": 1200.00,  # over $1000 → needs human review
    },
    {
        "order_id": "ORD-002",
        "customer_name": "Bob",
        "items": ["keyboard", "mouse"],
        "total": 80.00,  # under $1000 → auto fulfill
    },
    {
        "order_id": "ORD-003",
        "customer_name": "Charlie",
        "items": ["headphones"],
        "total": 150.00,  # headphones out of stock → should stop
    },
    {
        "order_id": "ORD-004",
        "customer_name": "",  # no name → invalid
        "items": ["laptop"],
        "total": 999.00,
    },
]
