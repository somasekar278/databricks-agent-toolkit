# Getting Started Guide

Quick start guide for building agents with this framework.

---

## Installation

```bash
# Basic installation
pip install sota-agent-framework

# With all features
pip install sota-agent-framework[all]

# With specific features
pip install sota-agent-framework[databricks,optimization]
```

---

## Choose Your Path

### 🤖 Have a Use Case? → Use `agent-architect`

Describe your use case, get instant architecture recommendations.

```bash
# From text
agent-architect "Build a fraud detection system with memory and self-improvement"

# From document
agent-architect --file requirements.pdf
```

**Output:**
- Complexity level (1-5)
- Required components
- Technology recommendations
- Architecture diagram
- Sample code

---

### 🎓 Want to Learn? → Use `agent-learn`

Build 5 progressively complex examples interactively.

```bash
agent-learn
```

**Learning Path:**

**Level 1: Simple Q&A Agent** (15 min)
- Basic LLM interaction
- Input/output handling
- LangGraph basics

**Level 2: Context-Aware Agent** (30 min)
- Vector search with Lakebase
- RAG pattern
- Context injection

**Level 3: Production API** (45 min)
- FastAPI wrapper
- Health checks
- Telemetry
- Databricks deployment

**Level 4: Complex Workflow** (60 min)
- Multi-agent orchestration
- LangGraph StateGraph
- Error handling
- Optimization

**Level 5: Autonomous Multi-Agent** (90 min)
- Self-improvement
- MCP integration
- Continuous learning
- Production monitoring

---

### 🚀 New to Agents? → Use `agent-setup`

Interactive wizard guides you through setup.

```bash
agent-setup
```

Configures:
- Databricks connection
- MLflow tracking
- Unity Catalog
- Telemetry
- MCP servers

---

### 🔧 Building an Agent? → Use `agent-generate`

Generate a working agent from template.

```bash
# Generate agent
agent-generate --domain "customer_support" --output ./my-agent

# Get recommendations
cd my-agent
agent-advisor .
```

**Generated Structure:**
```
my-agent/
├── agent.py              # Main agent logic (uses LangGraph)
├── config.yaml           # Configuration
├── scorers.py           # Custom MLflow scorers
├── main.py              # FastAPI app
├── deployment/          # Databricks Apps config
└── tests/               # Test suite
```

---

## Quick Start Example

### 1. Create Agent with LangGraph

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict
import dspy

# Configure LLM
lm = dspy.Databricks(model="databricks-dbrx-instruct")
dspy.settings.configure(lm=lm)

# Define state
class State(TypedDict):
    input: str
    analysis: str
    result: dict

# Define agent function
def analyze(state: State) -> State:
    # Use DSPy for reasoning
    class Analyze(dspy.Signature):
        input = dspy.InputField()
        analysis = dspy.OutputField()
    
    analyzer = dspy.ChainOfThought(Analyze)
    result = analyzer(input=state["input"])
    
    return {"analysis": result.analysis}

# Build workflow
workflow = StateGraph(State)
workflow.add_node("analyze", analyze)
workflow.set_entry_point("analyze")
workflow.add_edge("analyze", END)

# Compile
app = workflow.compile()

# Run
result = app.invoke({"input": "Analyze this..."})
print(result["analysis"])
```

### 2. Add Memory (Lakebase)

```python
from memory import LakebaseClient

# Initialize
memory = LakebaseClient()

# Create index (one-time)
memory.create_index(
    name="main.agents.knowledge",
    source_table="main.agents.documents",
    embedding_column="content"
)

# Search for context
def analyze_with_context(state: State) -> State:
    # Get relevant context
    context = memory.search(
        index_name="main.agents.knowledge",
        query=state["input"],
        num_results=5
    )
    
    # Use context in prompt
    analyzer = dspy.ChainOfThought(AnalyzeWithContext)
    result = analyzer(
        input=state["input"],
        context=[c["content"] for c in context]
    )
    
    return {"analysis": result.analysis}
```

### 3. Add Evaluation

```python
from mlflow.genai import evaluate
from mlflow.genai.scorers import Correctness, Safety
from evaluation.custom_scorers import latency_check

# Prepare eval data
eval_data = [
    {
        "inputs": {"input": "Test query"},
        "outputs": {"response": "Test response"},
        "expectations": {"expected_response": "Expected"}
    }
]

# Evaluate
result = evaluate(
    data=eval_data,
    scorers=[Correctness(), Safety(), latency_check]
)

print(f"View results: {result.mlflow_ui_url}")
```

### 4. Add Self-Improvement

Configure in `config/agent_config.yaml`:

```yaml
self_improvement_service:
  enabled: true
  check_interval_seconds: 300
  
  agents:
    my_agent:
      enabled: true
      thresholds:
        accuracy: 0.90
        error_rate: 0.03
      optimization:
        config_path: "config/optimization/my_agent.yaml"
```

### 5. Deploy to Databricks

```bash
# Generate deployment config
agent-deploy generate --app my-agent --output deployment/

# Deploy
databricks apps deploy -f deployment/databricks-app.yml
```

---

## Key Concepts

### We Integrate, Don't Reinvent

This framework provides:
- ✅ CLI tools for common tasks
- ✅ Configuration management
- ✅ Thin wrappers around native APIs
- ✅ Examples and templates

This framework uses (not reimplements):
- **LangGraph** - Orchestration
- **DSPy** - Reasoning
- **MLflow 3** - Evaluation & tracking
- **Lakebase** - Vector search
- **Databricks SDK** - UC, Model Serving
- **MCP** - Model Context Protocol

### Configuration

All settings in `config/agent_config.yaml`:

```yaml
agents:
  my_agent:
    model: "databricks-dbrx-instruct"
    temperature: 0.7
    max_tokens: 1000

evaluation:
  default_scorers:
    - Correctness
    - Safety

optimization:
  dspy:
    enabled: true
    optimizer: "BootstrapFewShot"

telemetry:
  enabled: true
  zerobus:
    table: "main.agents.telemetry"
```

---

## Next Steps

1. **Learn the Platform:** Read `docs/PLATFORM_INTEGRATION.md`
2. **Add Evaluation:** Read `docs/EVALUATION_GUIDE.md`
3. **Add Monitoring:** Read `docs/OBSERVABILITY_GUIDE.md`
4. **Deploy:** Read `docs/PLATFORM_INTEGRATION.md#databricks-deployment`

---

## Common Patterns

### RAG Agent

```python
from langgraph.graph import StateGraph
from memory import LakebaseClient

memory = LakebaseClient()

def retrieve(state):
    context = memory.search(
        index_name="main.agents.docs",
        query=state["input"],
        num_results=5
    )
    return {"context": context}

def generate(state):
    # Use context to generate response
    return {"response": generated_response}

workflow = StateGraph(State)
workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)
workflow.add_edge("retrieve", "generate")
workflow.set_entry_point("retrieve")
```

### Multi-Agent System

```python
def router(state):
    if state["type"] == "technical":
        return "tech_expert"
    return "general_agent"

workflow = StateGraph(State)
workflow.add_node("tech_expert", tech_agent)
workflow.add_node("general_agent", general_agent)
workflow.add_conditional_edges("START", router)
```

### Self-Improving Agent

```python
from mcp import McpClient

async with McpClient() as client:
    # Check performance
    perf = await client.call_databricks_tool(
        "check_performance",
        {"agent_id": "my_agent"}
    )
    
    if perf["status"] == "degraded":
        # Trigger optimization
        await client.call_databricks_tool(
            "trigger_optimization",
            {"agent_id": "my_agent"}
        )
```

---

## CLI Reference

```bash
# Main command
agent                    # Show all commands

# Setup & Generation
agent-setup              # Interactive setup wizard
agent-generate           # Generate agent from template
agent-architect          # Get architecture recommendations
agent-advisor            # Analyze existing agent

# Learning
agent-learn              # Interactive learning path

# Evaluation & Optimization
agent-benchmark          # Run MLflow 3 benchmarks
agent-optimize           # Optimize prompts (DSPy/TextGrad)

# Deployment & Operations
agent-deploy             # Generate deployment configs
agent-monitoring         # Setup monitoring service
agent-telemetry          # Setup Zerobus telemetry
```

---

## Getting Help

- **Full Documentation:** `docs/` folder
- **Platform Integration:** `docs/PLATFORM_INTEGRATION.md`
- **Evaluation:** `docs/EVALUATION_GUIDE.md`
- **Monitoring:** `docs/OBSERVABILITY_GUIDE.md`
- **Migration from v0.4:** `MIGRATION_GUIDE_V0.5.md`
- **GitHub:** https://github.com/somasekar278/universal-agent-template

---

**Start simple, scale to autonomous systems. Build ON TOP OF native platforms, not INSTEAD OF them.**

