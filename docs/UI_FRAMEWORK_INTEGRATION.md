# UI Framework Integration Guide

> **Making it Easy to Use Official Databricks UI Templates**
> **Status**: Implementation Roadmap for v0.3.0
> **Goal**: One command to get agent backend + official UI

---

## 🎯 The Problem

**Currently:**
```bash
# Users have to manually:
1. Generate our agent backend
2. Clone official Databricks UI template
3. Figure out how to connect them
4. Modify configuration files
5. Deploy with correct structure
```

**Goal:**
```bash
# One command, fully integrated:
databricks-agent-toolkit generate chatbot my-bot --ui=streamlit
# ✅ Agent backend (agent.py + start_server.py)
# ✅ Streamlit UI from official template
# ✅ Pre-configured to work together
# ✅ Ready to deploy
```

---

## 📋 Official Databricks Chatbot UI Templates

From https://github.com/databricks/app-templates:

| **Template**                | **Framework**      | **Best For**                          | **Complexity** |
|-----------------------------|--------------------|---------------------------------------|----------------|
| `streamlit-chatbot-app`     | Streamlit (Python) | Quick prototypes, data scientists     | Low            |
| `gradio-chatbot-app`        | Gradio (Python)    | ML demos, simple interfaces           | Low            |
| `dash-chatbot-app`          | Plotly Dash        | Data apps with charts                 | Medium         |
| `shiny-chatbot-app`         | Shiny (R/Python)   | Statistical apps, R users             | Medium         |
| `e2e-chatbot-app`           | React/TypeScript   | Production, enterprise                | High           |
| `e2e-chatbot-app-next`      | Next.js            | Modern production, SSR                | High           |

---

## 🏗️ Proposed CLI Enhancement

### **Add `--ui` Flag**

```python
# databricks_agent_toolkit/cli/generate.py

parser.add_argument(
    "--ui",
    choices=["embedded", "streamlit", "gradio", "dash", "shiny", "react", "nextjs"],
    default="embedded",
    help="UI framework (default: embedded HTML)"
)

parser.add_argument(
    "--ui-repo",
    default="https://github.com/databricks/app-templates.git",
    help="UI templates repository (default: official Databricks repo)"
)
```

### **Usage Examples**

```bash
# Default: Our embedded HTML (quick prototypes)
databricks-agent-toolkit generate chatbot my-bot
# Output: my-bot/ with agent.py, start_server.py, embedded HTML

# Streamlit UI (Python-native, easy)
databricks-agent-toolkit generate chatbot my-bot --ui=streamlit
# Output: my-bot/ with agent backend + Streamlit UI

# Gradio UI (ML demos)
databricks-agent-toolkit generate assistant my-assistant --ui=gradio --enable-rag
# Output: my-assistant/ with memory, RAG, + Gradio UI

# React UI (production)
databricks-agent-toolkit generate assistant my-prod-bot --ui=react
# Output: my-prod-bot/ with agent backend + React/TypeScript frontend
```

---

## 🔧 Technical Implementation

### **Architecture**

```
User runs:
databricks-agent-toolkit generate chatbot my-bot --ui=streamlit

Toolkit does:
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Generate Agent Backend (Our Code)                  │
│ ✅ agent.py (with DatabricksLLM)                           │
│ ✅ start_server.py (FastAPI with /api/invocations)        │
│ ✅ config.yaml                                             │
│ ✅ databricks.yml                                          │
│ ✅ requirements.txt                                        │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Clone Official UI Template                         │
│ Git sparse checkout from databricks/app-templates          │
│ Copy only: streamlit-chatbot-app/ → frontend/             │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Configure Integration                              │
│ Update start_server.py to integrate with Streamlit         │
│ Update config files to point to our backend                │
│ Generate integration glue code                             │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Generate Unified README                            │
│ Instructions for: local dev, config, deployment            │
└─────────────────────────────────────────────────────────────┘
```

### **Project Structure (Post-Generation)**

```
my-bot/
├── backend/
│   ├── agent.py              # Our agent logic
│   ├── start_server.py       # FastAPI server
│   ├── config.yaml           # Agent configuration
│   └── requirements.txt
├── frontend/                 # From official template
│   ├── app.py               # Streamlit UI (or other framework)
│   ├── requirements.txt     # UI dependencies
│   └── config.py            # UI configuration
├── databricks.yml           # DABs deployment
├── app.yaml                 # App-specific config
└── README.md                # Unified setup guide
```

---

## 📦 Framework-Specific Integrations

### **1. Streamlit (Easiest)**

**Integration Pattern:**
```python
# frontend/app.py (Streamlit)
import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"  # Our FastAPI backend

st.title("My Chatbot")

if prompt := st.chat_input("Ask me anything..."):
    # Call our backend API
    response = requests.post(
        f"{BACKEND_URL}/api/invocations",
        json={"input": [{"role": "user", "content": prompt}], "stream": False}
    )

    st.chat_message("assistant").write(response.json()["output"][0]["content"])
```

**Deployment:**
```yaml
# databricks.yml
resources:
  apps:
    my-bot:
      name: my-bot
      source_code_path: .
      # Note: Streamlit runs as separate process, talks to FastAPI backend
```

---

### **2. Gradio (ML-Friendly)**

**Integration Pattern:**
```python
# frontend/app.py (Gradio)
import gradio as gr
import requests

BACKEND_URL = "http://localhost:8000"

def chat(message, history):
    response = requests.post(
        f"{BACKEND_URL}/api/invocations",
        json={"input": [{"role": "user", "content": message}]}
    )
    return response.json()["output"][0]["content"]

demo = gr.ChatInterface(chat)
demo.launch()
```

---

### **3. Dash (Data-Focused)**

**Integration Pattern:**
```python
# frontend/app.py (Dash)
from dash import Dash, html, dcc, Input, Output, State
import requests

BACKEND_URL = "http://localhost:8000"

app = Dash(__name__)

@app.callback(
    Output('chat-output', 'children'),
    Input('send-button', 'n_clicks'),
    State('user-input', 'value')
)
def update_output(n_clicks, value):
    if n_clicks:
        response = requests.post(
            f"{BACKEND_URL}/api/invocations",
            json={"input": [{"role": "user", "content": value}]}
        )
        return response.json()["output"][0]["content"]
```

---

### **4. React/Next.js (Production)**

**Integration Pattern:**
```typescript
// frontend/src/services/api.ts
export async function sendMessage(message: string) {
  const response = await fetch('/api/invocations', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      input: [{role: 'user', content: message}],
      stream: false
    })
  });
  return response.json();
}

// frontend/src/components/Chat.tsx
import { sendMessage } from '../services/api';

export function Chat() {
  const handleSubmit = async (message: string) => {
    const result = await sendMessage(message);
    setMessages([...messages, result.output[0]]);
  };
  // ... rest of component
}
```

---

## 🔌 Backend Compatibility Layer

### **Our Backend Already Provides:**

✅ **OpenAI API Format** (`/api/invocations`)
```json
POST /api/invocations
{
  "input": [{"role": "user", "content": "Hello"}],
  "stream": false
}
```

✅ **Streaming Support** (SSE)
```json
POST /api/invocations
{
  "input": [...],
  "stream": true
}
```

✅ **Health Check**
```json
GET /health
{"status": "healthy", "model": "...", "streaming": true}
```

**All official UI templates should work with this!**

---

## 🚀 Implementation Roadmap

### **Phase 1: Research (Week 1)**
- [ ] Clone databricks/app-templates
- [ ] Analyze each of the 6 chatbot templates
- [ ] Document their backend expectations
- [ ] Test our backend compatibility with each

### **Phase 2: Core Integration (Week 2)**
- [ ] Add `--ui` flag to CLI
- [ ] Implement git sparse checkout for UI templates
- [ ] Create integration adapters for each framework
- [ ] Update project structure generator

### **Phase 3: Framework-Specific (Week 3-4)**
- [ ] Streamlit integration
- [ ] Gradio integration
- [ ] Dash integration
- [ ] Shiny integration
- [ ] React integration
- [ ] Next.js integration

### **Phase 4: Polish (Week 5)**
- [ ] Unified README generator
- [ ] Deploy testing for each framework
- [ ] Documentation and examples
- [ ] CLI help text updates

### **Phase 5: Release (v0.3.0)**
- [ ] Full test coverage
- [ ] Documentation site updates
- [ ] Blog post / announcement
- [ ] PyPI release

---

## 📝 Generated README Example

When user runs: `databricks-agent-toolkit generate chatbot my-bot --ui=streamlit`

They get:

```markdown
# my-bot

OpenAI API compatible chatbot with Streamlit UI.

## Architecture

- **Backend**: FastAPI (Python) at `http://localhost:8000`
  - Agent logic: `backend/agent.py`
  - API server: `backend/start_server.py`
  - OpenAI API compatible: `/api/invocations`

- **Frontend**: Streamlit (Python) at `http://localhost:8501`
  - UI code: `frontend/app.py`
  - Calls backend API

## Local Development

### Terminal 1: Start Backend
```bash
cd backend
pip install -r requirements.txt
python start_server.py
# Backend running at http://localhost:8000
```

### Terminal 2: Start Frontend
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
# UI opens at http://localhost:8501
```

## Configuration

Edit `backend/config.yaml`:
```yaml
model:
  endpoint: databricks-claude-sonnet-4-5
  temperature: 0.7
  streaming: true
```

## Deploy to Databricks Apps

```bash
databricks bundle deploy
```

Your app will be available at: `https://<workspace>/apps/<app-name>`

## Customization

### Change UI
Edit `frontend/app.py` (Streamlit code)

### Change Agent Logic
Edit `backend/agent.py` (agent behavior)

### Add Memory (Upgrade to L2)
```bash
databricks-agent-toolkit upgrade my-bot --add-memory
```

## API Documentation

Backend API docs: http://localhost:8000/docs
```

---

## 🎁 Bonus: Template Upgrade Path

**Allow users to switch UI later:**

```bash
# Start with embedded HTML
databricks-agent-toolkit generate chatbot my-bot

# Later, upgrade to Streamlit
databricks-agent-toolkit upgrade my-bot --ui=streamlit

# Or switch to React for production
databricks-agent-toolkit upgrade my-bot --ui=react
```

---

## ✅ Key Benefits

### **For Users:**
1. **One Command**: No manual template cloning/configuration
2. **Official UIs**: Using Databricks-maintained templates
3. **Best Practices**: Both backend and frontend follow standards
4. **Choice**: Pick the right UI for their use case
5. **Upgradeable**: Can switch UIs later

### **For Our Toolkit:**
1. **Focus**: We own the agent logic, not UI maintenance
2. **Standards**: Building "on top of" official templates
3. **Flexibility**: Works with any OpenAI-compatible UI
4. **Value-Add**: Integration, config, memory, RAG—not UI code

---

## 🎯 Success Metrics (v0.3.0)

- [ ] All 6 official UI templates integrated
- [ ] One-command generation works
- [ ] Local dev experience is smooth
- [ ] Databricks Apps deployment works
- [ ] Documentation is comprehensive
- [ ] User feedback is positive

---

## 📚 Resources

- **Official Templates**: https://github.com/databricks/app-templates
- **Our Backend API**: OpenAI Responses API at `/api/invocations`
- **Streaming**: Server-Sent Events (SSE) format
- **Deployment**: Databricks Asset Bundles (DABs)

---

## 💡 Philosophy: "On Top Of, Not Instead Of"

We're not creating custom UIs. We're:
1. ✅ Generating agent backends that follow standards
2. ✅ Integrating with official Databricks UI templates
3. ✅ Adding value (memory, RAG, config, scaffolding)
4. ✅ Making it easy to combine official components

**This is the right approach!** 🎯
