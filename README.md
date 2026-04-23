# 🏥 Medical Expert System (ADK)

A multi-agent medical triage and specialist consultation system built using the **Google Agent Development Kit (ADK)** and **Gemini 2.5 Pro**.

## 🚀 Features
- **Receptionist Orchestrator**: Primary entry point that triages symptoms and consults specialists.
- **Specialist Agents**: Specialized expertise in Neurology, Cardiology, Pulmonology, Nephrology, and Gastrology.
- **Web Grounding**: Specialists use `google_search` for real-time medical research.
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
Launch the interactive ADK browser interface:
```bash
adk web
```
*Note: Run this from the `Hospital_Agents` root directory.*

### 2. Terminal CLI
Run the system directly in your terminal:
```bash
python medical_system.py
```

## 🧠 Architecture
The system uses the **Agent-as-a-Tool** model. The `receptionist` agent treats specialized agents as expert tools. This architecture is chosen to resolve the technical conflict between Gemini's "Built-in Tools" (Search) and "Function Calling" (Handoffs) within a single agent context.
