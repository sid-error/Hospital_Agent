# 🏥 Medical Expert System (ADK)

A multi-agent medical triage and specialist consultation system built using the **Google Agent Development Kit (ADK)** and **Gemini 2.5 Pro**.

## 🚀 Features
- **Receptionist Orchestrator**: Primary entry point that triages symptoms and consults specialists.
- **Specialist Agents**: Decentralized A2A microservices for Neurology, Cardiology, Pulmonology, Nephrology, and Gastrology.
- **Bidirectional Handoffs**: The Receptionist seamlessly transfers control to specialists, and specialists can transfer control *back* if the conversation shifts out of their domain.
- **Web Grounding**: Specialists delegate medical research to a dedicated `search_agent` sub-agent that uses the `google_search` built-in tool.
- **Streamlit Dashboard**: A beautiful, custom-built chat interface for interacting with the system.
- **Monocle Telemetry**: Full integration with `monocle_apptrace` to generate OpenTelemetry JSON traces of all Agent and Tool executions.

## 🛠️ Setup

1. **Clone & Navigate**:
   ```bash
   cd Hospital_Agents
   ```

2. **Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   - Create a `.env` file based on `.env.example`.
   - Add your `GEMINI_API_KEY=your_api_key_here` (or `GOOGLE_API_KEY`).

## 📂 Project Structure
- `medical_agent/`: The Orchestrator agent that routes the patient.
- `cardiologist/`, `neurologist/`, etc.: Independent A2A specialist agents with their own `server.py` and `agent.json`.
- `streamlit_app.py`: The custom frontend UI.
- `start_servers.bat` / `.ps1`: Scripts to launch the background A2A uvicorn servers.
- `hospital_logger.py`: Centralized Monocle telemetry configuration.

## 🎮 How to Run & Test the System

Follow these steps in order to fully boot the system and its observability infrastructure:

### 1. Start the Jaeger Observability Backend
The system streams all Agent traces (token counts, sub-agent handoffs, and LLM payloads) to a local Jaeger instance.
To start Jaeger, run the included binary in a terminal:
```bash
.\jaeger-1.57.0-windows-amd64\jaeger-all-in-one.exe
```
*(Leave this terminal window open. You can view the Jaeger UI by visiting `http://localhost:16686` in your browser).*

### 2. Start the A2A Backend Servers
Because this system uses decentralized Agent-to-Agent routing, you must start the specialist microservices.
Open a **new** terminal (Anaconda Prompt or PowerShell) and run:
```bash
start_servers.bat
```
*(This will boot 5 background `uvicorn` servers on ports 8001-8005).*

### 3. Launch the Streamlit Frontend
In the same terminal where you ran `start_servers.bat`, launch the user interface:
```bash
streamlit run streamlit_app.py
```

### 4. Test the System
1. Open the Streamlit URL provided in your terminal (usually `http://localhost:8501`).
2. Type a symptom into the chat, for example: *"I have a terrible headache."*
3. Watch the UI as the Receptionist delegates the task to the Neurologist.
4. **Verify Traces on Disk (.jsonl):** Click on the "Observability & Telemetry" tab in Streamlit to verify that the raw traces are being appended to the `logs/traces.jsonl` file.
5. **Verify Traces in Jaeger:** Open your web browser to `http://localhost:16686/` (Jaeger). Select `hospital_system` under the "Service" dropdown and click "Find Traces" to view the detailed Agent execution Gantt charts!

## 🧠 Architecture
The system uses a **Bidirectional Transfer of Control (A2A)** model with **Agent Cards**. 

- The `receptionist` orchestrates multiple remote specialist agents by invoking their Agent Cards (`agent.json`) via local HTTP ports.
- When a specialist detects a symptom outside their field, they use `TransferToAgentTool` to hand control back to the receptionist, creating a highly autonomous, fluid multi-agent conversation.
- **Observability:** `Monocle` telemetry traces every execution step. It securely aggregates all trace logs into a single local file (`logs/traces.jsonl`) and simultaneously streams them via OTLP directly to a local **Jaeger** instance for rich visualizations.
