import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from weatherTool import get_weather
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

os.environ["OPENWEATHERMAP_API_KEY"] = ""
os.environ["LANGCHAIN_API_KEY"] = ""
os.environ["LANGCHAIN_TRACING_V2"] = "TRUE"
os.environ["LANGCHAIN_PROJECT"] = "myFirstlanggraph"
system_template = "You are a helpful AI agent that can use tools to find weather information and answer questions."                

#llm = ChatGroq(groq_api_key = "", model_name = "Gemma2-9b-It")
llm = ChatGroq(
    api_key = "",
    model="deepseek-r1-distill-llama-70b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
    # other params...
)
class State(TypedDict):
    messages:Annotated[list, add_messages]

gather_info_prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    MessagesPlaceholder("messages")
])
tools = [get_weather]
llm_with_tool = llm.bind_tools(tools)
#myModel = gather_info_prompt_template | llm_with_tool
def chatbot(state:State) -> State:    
    return {"messages": llm_with_tool.invoke(state["messages"])}

graph_builder = StateGraph(State)


graph_builder.add_node(chatbot, "chatbot")
graph_builder.add_node("tools", ToolNode(tools))
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)

graph_builder.add_edge("tools", "chatbot")

graph = graph_builder.compile()



def main():
    """Main function to run the AI agent."""
    print("\n=== Weather Assistant ===")
    print("Example questions:")
    print("- What's the weather in Tokyo?")
    print("- How's the weather in New York?")
    print("\nType 'quit' or 'q' to exit\n")

    while True:
        user_input = input("\nAsk about weather: ").strip()
        if user_input.lower() in ['quit', 'q']:
            print("Goodbye!")
            break
        if not user_input:
            print("Please enter a question.")
            continue

        events = graph.stream({"messages": ("user", user_input)}, stream_mode="values")
        for event in events:
            event["messages"][-1].pretty_print()

if __name__ == "__main__":
    main()
