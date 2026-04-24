# 🏥 Medical Expert System (ADK)

A multi-agent medical triage and specialist consultation system built using the **Google Agent Development Kit (ADK)** and **Gemini 2.5 Pro**.

## 🚀 Features
- **Receptionist Orchestrator**: Primary entry point that triages symptoms and consults specialists.
- **Specialist Agents**: Specialized expertise in Neurology, Cardiology, Pulmonology, Nephrology, and Gastrology.
- **Bidirectional Handoffs**: The Receptionist seamlessly transfers control to specialists, and specialists can transfer control *back* if the conversation shifts out of their domain.
- **Web Grounding**: Specialists delegate medical research to a dedicated `search_agent` sub-agent that uses the `google_search` built-in tool.
- **Persistent Session State**: Maintains a "Patient Chart" (JSON) across the entire session.
- **Emergency Filter**: Hard-coded safety check for life-threatening symptoms (e.g., "chest pain").
- **ADK Web Support**: Fully compatible with the `adk web` visual interface.

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
   pip install google-adk
   pip install google-genai
   pip install python-dotenv
   pip install pydantic
   ```

4. **Environment Variables**:
   - Create a `.env` file based on `.env.example`.
   - Add your `GOOGLE_API_KEY=your_google_api_key_here`
   - Add your `GOOGLE_GENAI_API_KEY=your_google_api_key_here`

## 📂 Project Structure
- `medical_agent/`: Core agent package (discovered by ADK).
  - `agent.py`: Agent definitions (root_agent = receptionist).
- `medical_system.py`: CLI entry point for terminal interaction.
- `requirements.txt`: Project dependencies.
- `.env`: API key configuration.

## 🎮 How to Run

### 1. Visual Web Interface (Recommended)
Launch the interactive ADK browser interface with A2A enabled:
```bash
adk web --a2a
```
*Note: Run this from the `Hospital_Agents` root directory.*

### 2. Terminal CLI
Run the system directly in your terminal:
```bash
python medical_system.py
```

## 🧠 Architecture
The system uses a **Bidirectional Transfer of Control (A2A)** model with **Agent Cards**. 

- The `receptionist` orchestrates multiple remote specialist agents by invoking their Agent Cards (`agent.json`). 
- When a specialist detects a symptom outside their field, they use `TransferToAgentTool` to hand control back to the receptionist, creating a highly autonomous, fluid multi-agent conversation.
- **Search Wrapper:** To bypass a strict Gemini API limitation preventing the combination of Built-In Tools (`google_search`) and Function Calling (Handoffs), the `google_search` tool is wrapped inside a dedicated `search_agent`. The specialists invoke this sub-agent via standard `AgentTool` function calling, maintaining a stable and error-free API payload.
