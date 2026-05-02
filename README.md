# ✈️ Multi-Agent Hospitality System
### Powered by Mistral AI · Built with Streamlit · CrewAI-inspired Architecture

---

## 🏗️ Project Architecture

```
multi_agent_hospitality/
│
├── app.py                        ← Streamlit frontend
├── requirements.txt
├── .env.example
│
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py           ← Master controller & state manager
│   ├── researcher.py             ← Researcher Agent (data sourcing)
│   └── writer.py                 ← Writer Agent (itinerary synthesis)
│
└── .vscode/
    ├── launch.json               ← Run config for VS Code
    └── settings.json
```

### Agent Pipeline

```
[User Input via Streamlit]
        │
        ▼
 ┌──────────────────┐
 │   Orchestrator   │  ← Manages state, coordinates hand-offs
 └────────┬─────────┘
          │  Phase 1: Research Request
          ▼
 ┌──────────────────┐
 │ Researcher Agent │  ← Queries Mistral for hotels, flights,
 │                  │    trains, buses, attractions, restaurants
 └────────┬─────────┘
          │  Phase 2: Structured JSON Hand-off
          ▼
 ┌──────────────────┐
 │   Writer Agent   │  ← Synthesises data into Markdown itinerary
 └────────┬─────────┘
          │  Phase 3: Final Assembly
          ▼
 ┌──────────────────┐
 │  Streamlit UI    │  ← Displays itinerary, hotels, transport tabs
 └──────────────────┘
```

---

## 🚀 VS Code Setup (Step-by-Step)

### 1. Clone / Create Project Folder
```bash
# Create project folder
mkdir multi_agent_hospitality
cd multi_agent_hospitality
# Copy all project files here
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up API Key
```bash
# Copy example env file
cp .env.example .env

# Edit .env and paste your Mistral API key:
# MISTRAL_API_KEY=your_key_here
```

Get your free Mistral API key at: https://console.mistral.ai

### 5. Open in VS Code
```bash
code .
```

### 6. Select Python Interpreter
- Press `Ctrl+Shift+P` → "Python: Select Interpreter"
- Choose the `venv` interpreter

### 7. Run the App

**Option A — Terminal:**
```bash
streamlit run app.py
```

**Option B — VS Code Debugger:**
- Press `F5` or go to Run → Start Debugging
- Select "Run Streamlit App"

App opens at: **http://localhost:8501**

---

## 🌟 Features

| Feature | Details |
|---|---|
| 🏨 Hotel Tiers | Premium (4★), Luxury (5★), Ultra-Luxury (👑) |
| ✈️ Flights | Airline, route, duration, class, price, tips |
| 🚄 Trains | Operator, route, duration, class, booking tips |
| 🚌 Buses | Operator, route, duration, price |
| 🗺️ Attractions | Category, entry fee, best time to visit |
| 🍽️ Restaurants | Cuisine, price range, must-try dishes |
| 📅 Itinerary | Day-by-day Morning / Afternoon / Evening plan |
| ⬇️ Export | Download full trip as JSON |

---

## 🔑 Mistral API

The project uses `mistral-large-latest` for both agents.

- Researcher Agent: `temperature=0.4` (factual, structured JSON)
- Writer Agent: `temperature=0.7` (creative, engaging prose)

**Free tier**: https://console.mistral.ai (includes generous free credits)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | Mistral AI (mistral-large-latest) |
| Agent Framework | Custom CrewAI-inspired orchestration |
| Language | Python 3.10+ |

---

## 📦 Dependencies

```
streamlit>=1.35.0
mistralai>=1.0.0
python-dotenv>=1.0.0
```

---

## 💡 Extending the Project

- Add a **Booking Agent** that integrates with real APIs (Amadeus, Booking.com)
- Add **Memory** using LangChain's conversation buffer
- Add **Tool Calling** for real-time flight/hotel price APIs
- Deploy to **Streamlit Community Cloud** for free hosting
