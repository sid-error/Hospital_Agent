from google.adk.agents import Agent
from google.adk.tools.google_search_tool import google_search
from google.adk.tools.transfer_to_agent_tool import TransferToAgentTool
from google.adk.tools.agent_tool import AgentTool

search_agent = Agent(
    name="search_agent",
    model="gemini-2.5-pro",
    description="Dedicated search assistant for medical research.",
    instruction="Use the google_search tool to find the information requested and provide a concise summary of the results.",
    tools=[google_search]
)

root_agent = Agent(
    name="Pulmonologist",
    model="gemini-2.5-pro",
    description="Specialist in respiratory health.",
    instruction="You are a Senior Pulmonologist. Focus on lung health. Do not invent a personal name for yourself; refer to yourself only as 'the Pulmonologist'. Use the 'search_agent' tool for respiratory data. If the patient asks about symptoms outside your specialization, use the transfer_to_agent tool to hand control back to the 'receptionist'.",
    tools=[AgentTool(agent=search_agent), TransferToAgentTool(agent_names=["receptionist"])]
)
