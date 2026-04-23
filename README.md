# 🏥 Medical Expert System (ADK)

A multi-agent medical triage and specialist consultation system built using the Google Agent Development Kit (ADK).

## Features
- **Receptionist Orchestrator**: Routes patients to specialists (Neurology, Cardiology, etc.)
- **Specialist Agents**: Equipped with `google_search` for late-breaking medical research.
- **Stateful Memory**: Maintains a persistent "Patient Chart" across agent handoffs.
- **Emergency Filter**: Pre-processes inputs for life-threatening symptoms.
- **Model**: Powered by `gemini-2.5-pro`.

## Prerequisites
- Python 3.10+
- Google API Key (Gemini)

## Setup
1. Clone the repository and navigate to the directory.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment:
   - Copy `.env.example` to `.env`
   - Add your `GOOGLE_GENAI_API_KEY` to `.env`

## Execution
### CLI Mode
Run the system as a script:
```bash
python medical_system.py
```

### ADK Web Interface
To use the visual browser interface:
1. Ensure you are in the `Hospital_Agents` directory.
2. Run:
   ```bash
   adk web
   ```
3. A browser window will open at `localhost:8000` (or similar) showing the `receptionist` agent.

## How it Works
1. **Triage**: The Receptionist greets you and asks for symptoms.
2. **Emergency Check**: If you mention "chest pain" or "can't breathe", it triggers an immediate emergency alert.
3. **Specialist Handoff**: Based on symptoms, you are transferred to a specialist.
4. **Specialized Consultation**: The specialist (e.g., Cardiologist) provides expert insights and can search the web for the latest medical data.
