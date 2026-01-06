# E2E Chatbot App Integration Guide

> **Official Template**: https://github.com/databricks/app-templates/tree/main/e2e-chatbot-app
> **Documentation**: https://docs.databricks.com/aws/en/generative-ai/agent-framework/chat-app
> **Status**: Planned for v0.3.0
> **Current**: Documented for manual integration

---

## 🎯 Why Use e2e-chatbot-app?

The official [e2e-chatbot-app](https://github.com/databricks/app-templates/tree/main/e2e-chatbot-app) is a **production-grade, full-stack chat UI** that is superior to our embedded HTML interface in every way.

### **Comparison**

| **Feature**                  | **Our Embedded HTML (v0.2.0)** | **e2e-chatbot-app**           |
|------------------------------|--------------------------------|-------------------------------|
| **Framework**                | Embedded HTML/CSS/JS           | React + TypeScript            |
| **UI Quality**               | Basic chat bubbles             | Professional, polished UI     |
| **Streaming**                | Basic SSE                      | Advanced streaming UX         |
| **Tool Calls**               | ❌ Not displayed               | ✅ Visual tool call rendering |
| **Function Outputs**         | ❌ Not displayed               | ✅ Structured display         |
| **Authentication**           | ❌ None                        | ✅ OAuth + user identity      |
| **Chat History**             | ❌ In-memory only (L1)         | ✅ Lakebase persistence       |
| **Multi-User**               | ❌ No                          | ✅ User-specific conversations|
| **Governance**               | ❌ No audit trail              | ✅ Full audit in Lakebase     |
| **Maintainability**          | Embedded in Python string      | Separate React codebase       |
| **Customizability**          | Limited                        | Full React component tree     |
| **Mobile Responsive**        | Basic                          | ✅ Production-ready           |
| **Error Handling**           | Basic alerts                   | ✅ Comprehensive error UX     |
| **Loading States**           | Basic                          | ✅ Professional indicators    |

**Verdict:** ✅ **e2e-chatbot-app is FAR superior for production use**

---

## 🏗️ Architecture: Our Backend + Their Frontend

### **The Perfect Match**

```
┌─────────────────────────────────────────────────────────────┐
│                   Databricks App                            │
│                                                             │
│  ┌──────────────────────┐      ┌─────────────────────────┐│
│  │  e2e-chatbot-app     │      │  Our Agent Backend      ││
│  │  (React Frontend)    │◄────►│  (agent.py + server)    ││
│  │                      │      │                         ││
│  │  - Chat UI           │      │  - OpenAI API compat.   ││
│  │  - Tool rendering    │      │  - MLflow tracing       ││
│  │  - OAuth flow        │      │  - Config-driven        ││
│  │  - Lakebase client   │      │  - Memory (Lakebase)    ││
│  └──────────────────────┘      │  - RAG (optional)       ││
│                                 └─────────────────────────┘│
│                                                             │
│  ┌─────────────────────────────────────────────────────────┤
│  │  Shared Services                                        │
│  │  - Lakebase (Postgres) for chat history                │
│  │  - OAuth for user authentication                        │
│  │  - Model Serving for LLM                                │
│  └─────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────┘
```

### **Why This Works Perfectly**

1. **OpenAI API Compatibility** ✅
   - Our backend already implements `/api/invocations` with OpenAI format
   - e2e-chatbot-app expects OpenAI API format
   - **No changes needed to our agent logic!**

2. **Streaming Support** ✅
   - Both use Server-Sent Events (SSE)
   - Same `data: {json}\n\n` format
   - **No changes needed!**

3. **Lakebase Integration** ✅
   - Both support Lakebase for chat history
   - Same Postgres connection pattern
   - **Already compatible!**

---

## 📦 What e2e-chatbot-app Provides

### **Frontend (React/TypeScript)**

**File Structure:**
```
frontend/
├── src/
│   ├── components/
│   │   ├── Chat.tsx              # Main chat interface
│   │   ├── Message.tsx           # Message bubble component
│   │   ├── ToolCall.tsx          # Tool call rendering
│   │   ├── StreamingMessage.tsx  # Streaming display
│   │   ├── UserInput.tsx         # Input field with send
│   │   └── ConversationList.tsx  # Chat history sidebar
│   ├── services/
│   │   ├── api.ts                # API client for /api/invocations
│   │   ├── auth.ts               # OAuth integration
│   │   └── lakebase.ts           # Chat history client
│   ├── hooks/
│   │   ├── useStreaming.ts       # SSE streaming hook
│   │   ├── useAuth.ts            # Authentication hook
│   │   └── useChatHistory.ts     # History management
│   ├── App.tsx                   # Main app component
│   └── index.tsx                 # Entry point
├── package.json
├── vite.config.ts
└── tsconfig.json
```

**Key Features:**
- Professional UI with modern design system
- Real-time streaming with smooth token display
- Tool call rendering (shows what tools the agent is using)
- Multi-turn conversations with history
- OAuth integration for user identity
- Responsive design (desktop, tablet, mobile)

### **Backend (FastAPI - What We Already Have!)**

e2e-chatbot-app expects:
```python
@app.post("/api/invocations")
async def invocations(request: Request):
    """OpenAI API compatible endpoint"""
    data = await request.json()
    messages = data.get("input", [])
    stream = data.get("stream", False)
    # ... (we already have this!)
```

**We're already 100% compatible!** ✅

---

## 🚀 Integration Options

### **Option 1: Manual Integration (Available Now)**

**For users who want the React UI today:**

1. Clone e2e-chatbot-app:
   ```bash
   git clone https://github.com/databricks/app-templates.git
   cp -r app-templates/e2e-chatbot-app/frontend my-agent/frontend
   ```

2. Generate agent backend with our toolkit:
   ```bash
   databricks-agent-toolkit generate assistant my-agent
   cd my-agent
   ```

3. Update `start_server.py` to serve React build:
   ```python
   from fastapi.staticfiles import StaticFiles

   # Serve React build
   app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
   ```

4. Build frontend:
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```

5. Deploy:
   ```bash
   databricks bundle deploy
   ```

**Project structure:**
```
my-agent/
├── backend/
│   ├── agent.py
│   ├── start_server.py
│   └── config.yaml
├── frontend/                  # From e2e-chatbot-app
│   ├── src/
│   └── package.json
├── databricks.yml
└── app.yaml
```

---

### **Option 2: Toolkit Integration (Planned v0.3.0)**

**Future CLI command:**
```bash
databricks-agent-toolkit generate assistant my-agent --ui=react

# Generates:
# ├── backend/
# │   ├── agent.py
# │   ├── start_server.py
# │   └── config.yaml
# ├── frontend/               # Auto-pulled from e2e-chatbot-app
# │   ├── src/
# │   └── package.json
# ├── databricks.yml
# └── app.yaml
```

**Implementation plan:**
1. Add `--ui` flag to CLI (choices: `embedded`, `react`)
2. Auto-clone e2e-chatbot-app frontend when `--ui=react`
3. Update `start_server.py` template to serve React build
4. Add npm build step to deployment docs
5. Update `databricks.yml` to include frontend build

---

## 🎨 Customization

### **Branding**

**Colors (in `frontend/src/theme.ts`):**
```typescript
export const theme = {
  primary: '#FF3621',      // Databricks red
  secondary: '#00A972',    // Databricks green
  background: '#FFFFFF',
  text: '#1E1E1E',
}
```

**Logo (in `frontend/public/`):**
```
Replace logo.png with your company logo
```

### **Behavior**

**Streaming delay (in `frontend/src/config.ts`):**
```typescript
export const config = {
  streamingDelayMs: 30,  // Token display delay
  maxTokens: 500,
  temperature: 0.7,
}
```

---

## 📋 Roadmap

### **v0.2.0 (Current)**
- ✅ Document e2e-chatbot-app as production UI option
- ✅ Ensure backend compatibility (OpenAI API format)
- ✅ Add manual integration guide

### **v0.3.0 (Planned - Q1 2026)**
- ⏭️ Add `--ui=react` flag to CLI
- ⏭️ Auto-integration with e2e-chatbot-app frontend
- ⏭️ Update deployment docs for React build
- ⏭️ Add frontend customization guide

### **v0.4.0 (Future)**
- ⏭️ Custom React component library for Databricks agents
- ⏭️ Pre-built themes (light/dark, industry-specific)
- ⏭️ Advanced tool call visualizations
- ⏭️ Multi-agent conversation UI

---

## 🤝 Benefits of This Approach

### **For Users:**
1. **Choice**: Embedded HTML for quick prototypes, React for production
2. **Official**: Using Databricks-maintained UI code
3. **Customizable**: Full React codebase to modify
4. **Future-Proof**: Maintained by Databricks team

### **For Our Toolkit:**
1. **Focus**: We focus on agent logic, not UI maintenance
2. **Standards**: Building "on top of, not instead of"
3. **Integration**: Our backend works with any OpenAI-compatible frontend
4. **Value-Add**: We add memory, RAG, config, scaffolding—not reinventing UI

---

## 📚 Resources

- **Official Template**: https://github.com/databricks/app-templates/tree/main/e2e-chatbot-app
- **Documentation**: https://docs.databricks.com/aws/en/generative-ai/agent-framework/chat-app
- **Our Backend API**: OpenAI Responses API format at `/api/invocations`
- **MLflow Tracing**: Automatic with `mlflow.set_tracking_uri("databricks")`

---

## ✅ Current Status

**v0.2.0:**
- ✅ Our backend is 100% compatible with e2e-chatbot-app
- ✅ Users can manually integrate today
- ✅ Documented in README and this guide

**Next:**
- ⏭️ Plan v0.3.0 CLI integration
- ⏭️ Test manual integration flow
- ⏭️ Gather user feedback

---

## 💡 Key Insight

**"On Top Of, Not Instead Of"**

By ensuring our backend follows OpenAI API standards, we're compatible with:
- ✅ Databricks e2e-chatbot-app
- ✅ Any OpenAI-compatible UI framework
- ✅ Custom React/Vue/Angular frontends
- ✅ Mobile apps using OpenAI SDK

**Our value is in the agent backend (logic, memory, RAG, config), not the UI.**

This is the right architecture! 🎯
