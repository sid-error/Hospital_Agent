import os
import json
import asyncio
# pyrefly: ignore [missing-import]
import streamlit as st
from typing import List, Dict, Any
from dotenv import load_dotenv

# ADK Imports
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

# Local Imports
from medical_agent.agent import receptionist
from hospital_logger import log_event, log_agent_handoff, logger

load_dotenv()

APP_NAME = "streamlit_medical_system"
USER_ID = "patient_streamlit"

def emergency_filter(user_input: str) -> bool:
    """Hard-coded check for life-threatening symptoms."""
    triggers = ["heart attack", "can't breathe", "unconscious", "heavy bleeding", "stroke symptoms", "chest pain"]
    input_lower = user_input.lower()
    for trigger in triggers:
        if trigger in input_lower:
            return True
    return False

# Initialize Session Service and Runner in Streamlit State
if 'session_service' not in st.session_state:
    st.session_state.session_service = InMemorySessionService()

if 'runner' not in st.session_state:
    st.session_state.runner = Runner(
        agent=receptionist,
        app_name=APP_NAME,
        session_service=st.session_state.session_service
    )

if 'session_id' not in st.session_state:
    # We must create the session asynchronously
    async def init_session():
        initial_state = {
            "patient_chart": {
                "symptoms": [],
                "vitals": {},
                "summary": "New patient admission."
            }
        }
        session = await st.session_state.session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state
        )
        return session.id
    
    st.session_state.session_id = asyncio.run(init_session())
    log_event("INFO", "system", "session_start", f"Streamlit Session initialized: {st.session_state.session_id}", session_id=st.session_state.session_id, user_id=USER_ID)

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to run the ADK asynchronously and yield chunks
async def run_adk_agent(user_input: str):
    session_id = st.session_state.session_id
    runner = st.session_state.runner
    
    current_agent = "receptionist"
    full_response = ""
    
    try:
        async for event in runner.run_async(
            session_id=session_id,
            user_id=USER_ID,
            new_message=types.Content(role='user', parts=[types.Part.from_text(text=user_input)])
        ):
            if hasattr(event, 'agent_name') and event.agent_name:
                current_agent = event.agent_name

            if hasattr(event, 'content') and getattr(event.content, 'parts', None):
                for part in event.content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        func_name = part.function_call.name
                        if func_name == "transfer_to_agent":
                            target = "unknown"
                            if hasattr(part.function_call, 'args') and 'agent_name' in part.function_call.args:
                                target = part.function_call.args['agent_name']
                            log_agent_handoff(current_agent, target, session_id=session_id)
                        else:
                            log_event("DEBUG", current_agent, "tool_call", f"Called tool: {func_name}", session_id=session_id)

                    elif hasattr(part, 'text') and part.text:
                        full_response += part.text
                        log_event("INFO", current_agent, "model_response", part.text.strip(), session_id=session_id)
        
        return full_response
    except Exception as e:
        logger.exception(f"Error during ADK execution: {e}")
        return f"System Error: {str(e)}"

# --- STREAMLIT UI ---
st.set_page_config(page_title="Hospital AI Agent", page_icon="🏥", layout="wide")

st.title("🏥 Hospital Triage System")

tab1, tab2 = st.tabs(["💬 Chat", "📜 System Logs"])

with tab1:
    st.markdown("Welcome! Please describe your symptoms.")
    
    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("What are your symptoms?"):
        # Add user message to UI and logs
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        log_event("INFO", "patient", "user_input", prompt, session_id=st.session_state.session_id)

        # Emergency Filter
        if emergency_filter(prompt):
            alert_msg = "🚨 **[EMERGENCY ALERT] !!! Life-threatening symptoms detected! !!!**\nPlease call 911 immediately or go to the nearest Emergency Room."
            log_event("WARNING", "system", "emergency_trigger", "Life-threatening symptoms detected.", session_id=st.session_state.session_id)
            
            st.session_state.messages.append({"role": "assistant", "content": alert_msg})
            with st.chat_message("assistant"):
                st.error(alert_msg)
        else:
            # ADK Runner Processing
            with st.chat_message("assistant"):
                with st.spinner("Consulting specialists..."):
                    # Run ADK and get response
                    response_text = asyncio.run(run_adk_agent(prompt))
                    
                    if not response_text:
                        response_text = "I'm sorry, I couldn't process that request properly."
                        
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})

with tab2:
    st.header("Raw JSON Logs")
    if st.button("Refresh Logs"):
        st.rerun()
        
    log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "hospital_agent.log")
    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as f:
            logs = f.readlines()
            
        # Display logs in reverse order (newest first)
        for line in reversed(logs):
            try:
                log_json = json.loads(line)
                
                # Format visually
                level_color = "green"
                level = log_json.get("level", "INFO")
                if level == "DEBUG": level_color = "blue"
                elif level == "WARNING": level_color = "orange"
                elif level == "ERROR": level_color = "red"
                elif level == "CRITICAL": level_color = "darkred"
                
                agent = log_json.get('agent', 'system')
                if agent == "HANDOFF": level_color = "purple"
                
                event_type = log_json.get('event', 'log')
                
                st.markdown(f"**<span style='color:{level_color}'>[{level}] [{event_type}]</span> {agent}**: {log_json.get('message')}", unsafe_allow_html=True)
                with st.expander("Raw Data"):
                    st.json(log_json)
            except:
                st.text(line)
    else:
        st.info("No logs found yet.")
