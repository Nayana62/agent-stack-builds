import asyncio
from agent import agent, MyDeps
from mock_data import CUSTOMERS, KNOWLEDGE_BASE


async def main():
    deps = MyDeps(
        customers=CUSTOMERS,
        knowledge_base=KNOWLEDGE_BASE,
        ticket_text="",
    )

    ticket = "My export keeps failing with a timeout. Account C-1002."
    deps.ticket_text = ticket

    # First run — classify the ticket
    result1 = await agent.run(ticket, deps=deps)
    print("=== First classification ===")
    print(result1.output.model_dump_json(indent=2))

    # Follow-up — ask about the same ticket using message history
    followup = "Actually, this is affecting our entire team, not just me. Can you re-evaluate the priority?"
    deps.ticket_text = followup

    result2 = await agent.run(
        followup,
        deps=deps,
        message_history=result1.new_messages(),  # <-- this is the key part
    )
    print("\n=== After follow-up ===")
    print(result2.output.model_dump_json(indent=2))


asyncio.run(main())
