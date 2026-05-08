import os
from google.adk.agents import Agent
from google.adk.tools.google_search_tool import google_search

from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
import sys
import os

# Add parent directory to path so hospital_logger can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# --- 1. SPECIALIST AGENT DEFINITIONS (VIA A2A AGENT CARDS) ---

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

neurologist = RemoteA2aAgent(
    name="Neurologist",
    agent_card=os.path.join(base_dir, "neurologist", "agent.json"),
    description="Specialist in brain and nervous system disorders."
)

cardiologist = RemoteA2aAgent(
    name="Cardiologist",
    agent_card=os.path.join(base_dir, "cardiologist", "agent.json"),
    description="Specialist in heart and vascular health."
)

pulmonologist = RemoteA2aAgent(
    name="Pulmonologist",
    agent_card=os.path.join(base_dir, "pulmonologist", "agent.json"),
    description="Specialist in respiratory health."
)

nephrologist = RemoteA2aAgent(
    name="Nephrologist",
    agent_card=os.path.join(base_dir, "nephrologist", "agent.json"),
    description="Specialist in kidney health."
)

gastrologist = RemoteA2aAgent(
    name="Gastrologist",
    agent_card=os.path.join(base_dir, "gastrologist", "agent.json"),
    description="Specialist in digestive health."
)

# --- 2. RECEPTIONIST (ORCHESTRATOR) AGENT DEFINITION ---

triage_instruction = """
You are the Receptionist (Primary Orchestrator). Do not invent a personal name for yourself; refer to yourself only as 'the Receptionist'.
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

IMPORTANT: Do not diagnose. Use the transfer_to_agent tool to grant control to the correct specialist.
"""

receptionist = Agent(
    name="receptionist",
    model="gemini-2.5-pro",
    description="Primary orchestrator for medical triage.",
    instruction=triage_instruction,
    tools=[],
    sub_agents=[
        neurologist,
        cardiologist,
        pulmonologist,
        nephrologist,
        gastrologist
    ]
)

# Required for adk web discovery
root_agent = receptionist
