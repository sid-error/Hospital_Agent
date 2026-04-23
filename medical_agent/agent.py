import os
from google.adk.agents import Agent
from google.adk.tools.google_search_tool import google_search
from google.adk.tools.agent_tool import AgentTool

# --- 1. SPECIALIST AGENT DEFINITIONS ---

neurologist = Agent(
    name="Neurologist",
    model="gemini-2.5-pro",
    description="Specialist in brain and nervous system disorders.",
    instruction="You are a Senior Neurologist. Focus on brain health. Use 'google_search' for clinical guidelines.",
    tools=[google_search]
)

cardiologist = Agent(
    name="Cardiologist",
    model="gemini-2.5-pro",
    description="Specialist in heart and vascular health.",
    instruction="You are a Senior Cardiologist. Focus on heart health. Use 'google_search' for latest cardiac research.",
    tools=[google_search]
)

pulmonologist = Agent(
    name="Pulmonologist",
    model="gemini-2.5-pro",
    description="Specialist in respiratory health.",
    instruction="You are a Senior Pulmonologist. Focus on lung health. Use 'google_search' for respiratory data.",
    tools=[google_search]
)

nephrologist = Agent(
    name="Nephrologist",
    model="gemini-2.5-pro",
    description="Specialist in kidney health.",
    instruction="You are a Senior Nephrologist. Focus on renal function. Use 'google_search' for kidney research.",
    tools=[google_search]
)

gastrologist = Agent(
    name="Gastrologist",
    model="gemini-2.5-pro",
    description="Specialist in digestive health.",
    instruction="You are a Senior Gastrologist. Focus on stomach and liver health. Use 'google_search' for GI guidelines.",
    tools=[google_search]
)

# --- 2. RECEPTIONIST (ORCHESTRATOR) AGENT DEFINITION ---

triage_instruction = """
You are the Receptionist (Primary Orchestrator).
GOAL: Identify the correct specialist for the patient based on symptoms.

PROCESS:
1. Greet the patient.
2. Ask for symptoms and vitals.
3. Use the 'Patient Chart' in the session state to track findings.
4. Consult the appropriate specialized agent using your tools.

SPECIALIST MAPPING:
- Cardiologist: Heart, chest pain, palpitations.
- Neurologist: Brain, nerves, seizures, headaches.
- Pulmonologist: Lungs, breathing, coughing.
- Nephrologist: Kidneys, urinary issues.
- Gastrologist: Stomach, digestion, liver.

IMPORTANT: Do not diagnose. Use the specialist tools to get expert opinions.
"""

receptionist = Agent(
    name="receptionist",
    model="gemini-2.5-pro",
    description="Primary orchestrator for medical triage.",
    instruction=triage_instruction,
    tools=[
        AgentTool(agent=neurologist),
        AgentTool(agent=cardiologist),
        AgentTool(agent=pulmonologist),
        AgentTool(agent=nephrologist),
        AgentTool(agent=gastrologist)
    ]
)

# Required for adk web discovery
root_agent = receptionist
