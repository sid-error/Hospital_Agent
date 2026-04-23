import os
import json
import asyncio
from typing import List, Dict, Any
from dotenv import load_dotenv

# ADK Imports
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

# Local Imports
from medical_agent.agent import receptionist

load_dotenv()

# --- 1. EMERGENCY FILTER ---

def emergency_filter(user_input: str) -> bool:
    """Hard-coded check for life-threatening symptoms."""
    triggers = ["heart attack", "can't breathe", "unconscious", "heavy bleeding", "stroke symptoms", "chest pain"]
    input_lower = user_input.lower()
    for trigger in triggers:
        if trigger in input_lower:
            return True
    return False

# --- 2. MAIN SYSTEM RUN LOOP ---

async def run_medical_system():
    print("--- 🏥 Medical Expert System Powered by ADK ---")
    print("Type 'exit' or 'quit' to end.\n")

    APP_NAME = "medical_system"
    USER_ID = "patient_001"
    
    session_service = InMemorySessionService()
    
    # Initialize session with Patient Chart state
    initial_state = {
        "patient_chart": {
            "symptoms": [],
            "vitals": {},
            "summary": "New patient admission."
        }
    }
    
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state
    )
    SESSION_ID = session.id

    runner = Runner(
        agent=receptionist,
        app_name=APP_NAME,
        session_service=session_service
    )

    while True:
        user_input = input("Patient: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # 1. Emergency Filter (Pre-process)
        if emergency_filter(user_input):
            print("\nAssistant: [EMERGENCY ALERT] 🚨 Life-threatening symptoms detected! 🚨")
            print("Please call 911 immediately or go to the nearest Emergency Room.")
            continue

        # 2. ADK Runner execution
        print("\nAssistant: ", end="", flush=True)
        try:
            async for event in runner.run_async(
                session_id=SESSION_ID,
                user_id=USER_ID,
                new_message=user_input
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            print(part.text, end="", flush=True)
            print("\n")
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    asyncio.run(run_medical_system())
