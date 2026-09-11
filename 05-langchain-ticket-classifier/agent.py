from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import ToolMessage, HumanMessage
from models import TicketClassification
from tools import lookup_customer, check_knowledge_base

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a support ticket classifier. Your job is to read a customer support ticket and classify it.

When you receive a ticket:
1. Look for a customer/account ID (like C-1234). If you find one, use the lookup_customer tool to get their info.
2. Identify the main issue and use check_knowledge_base with a relevant keyword to find related help articles.
3. Based on the ticket text, customer info, and knowledge base results, classify the ticket.""",
        ),
        ("human", "{ticket}"),
    ]
)

tools = [lookup_customer, check_knowledge_base]
tool_map = {t.name: t for t in tools}
model_with_tools = model.bind_tools(tools)


def classify_ticket(ticket: str) -> TicketClassification:
    # Step 1: format the prompt and call the model
    messages = prompt.invoke({"ticket": ticket}).to_messages()
    response = model_with_tools.invoke(messages)
    messages.append(response)

    # Step 2: if the model wants to call tools, execute them
    while response.tool_calls:
        for tool_call in response.tool_calls:
            tool = tool_map[tool_call["name"]]
            result = tool.invoke(tool_call["args"])
            messages.append(
                ToolMessage(content=str(result), tool_call_id=tool_call["id"])
            )
        response = model_with_tools.invoke(messages)
        messages.append(response)

    # Step 3: now get structured output
    structured_model = model.with_structured_output(TicketClassification)
    messages.append(
        HumanMessage(
            content="Now classify this ticket using the information you gathered."
        )
    )
    result = structured_model.invoke(messages)
    return TicketClassification.model_validate(result)
