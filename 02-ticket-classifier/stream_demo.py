import asyncio
from agent import agent, MyDeps
from mock_data import CUSTOMERS, KNOWLEDGE_BASE

ticket = "URGENT: Our API is returning 500 errors and the whole team is blocked. Account C-1001."


async def main():
    deps = MyDeps(
        customers=CUSTOMERS,
        knowledge_base=KNOWLEDGE_BASE,
        ticket_text=ticket,
    )

    async with agent.run_stream(ticket, deps=deps) as result:
        async for chunk in result.stream_output():
            print(chunk)
            print("---")  # separator so you can see each partial update


asyncio.run(main())
