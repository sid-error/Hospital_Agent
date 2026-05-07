import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import hospital_logger
import os
from dotenv import load_dotenv
load_dotenv()
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from pulmonologist.agent import root_agent

base_dir = os.path.dirname(os.path.abspath(__file__))
app = to_a2a(root_agent, agent_card=os.path.join(base_dir, "agent.json"))

