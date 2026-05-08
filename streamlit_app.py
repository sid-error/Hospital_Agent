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
                        pass # Handled automatically by Monocle traces

                    elif hasattr(part, 'text') and part.text:
                        full_response += part.text

        
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
            


        # Emergency Filter
        if emergency_filter(prompt):
            alert_msg = "🚨 **[EMERGENCY ALERT] !!! Life-threatening symptoms detected! !!!**\nPlease call 911 immediately or go to the nearest Emergency Room."

            
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
    st.header("Observability & Telemetry")
    st.markdown("""
    **All trace data is fully managed by Monocle and OpenTelemetry!** 🚀
    
    The legacy Python logging system has been completely removed. Every action your agents take is now automatically recorded as an OpenTelemetry trace.
    
    ### How to view your traces:
    1. **On Disk (.jsonl):** All telemetry is securely aggregated into a single file at `logs/traces.jsonl` (one JSON trace per line) instead of thousands of tiny files.
    2. **In Jaeger (Web):** Traces are streamed live to your local Jaeger database. Open `http://localhost:16686` in your browser to view interactive Gantt charts of the Agent executions!
    """)
    
    if st.button("Refresh Trace List"):
        st.rerun()

    trace_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "traces.jsonl")
    if os.path.exists(trace_file):
        st.success(f"Trace file is active: `{trace_file}`")
        try:
            file_size = os.path.getsize(trace_file)
            st.text(f"File Size: {file_size / 1024:.2f} KB")
        except:
            pass
    else:
        st.info("No traces generated yet. Try sending a chat message to the agents first!")
