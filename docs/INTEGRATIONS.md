# External Integrations Guide

**All external integrations in one place**: MCP, LangGraph, Databricks

---

## 📋 Table of Contents

- [Model Context Protocol (MCP)](#model-context-protocol-mcp)
- [LangGraph Orchestration](#langgraph-orchestration)
- [Databricks Integration](#databricks-integration)

---

## 🔌 Model Context Protocol (MCP)

**Purpose**: Standardized tool interfaces for external services

### Quick Start

```bash
# Install with MCP support
pip install sota-agent-framework[mcp]
```

### Usage

```python
from agents.mcp_client import AgentMCPClient

# Initialize MCP client
mcp_client = AgentMCPClient()

# Connect to MCP server (stdio-based)
await mcp_client.connect("python", "path/to/mcp_server.py")

# List available tools
tools = await mcp_client.list_tools()

# Call a tool
result = await mcp_client.call_tool("bin_lookup", {"bin": "123456"})

# Close when done
await mcp_client.close()
```

### Configuration

```yaml
# config/sota_config.yaml
mcp:
  enabled: true
  servers:
    - name: "fraud_tools"
      command: "python"
      args: ["mcp_servers/fraud_tools.py"]
    - name: "data_tools"
      command: "python"
      args: ["mcp_servers/data_tools.py"]
```

### Creating Custom MCP Servers

See `mcp-servers/` directory for examples.

**Full Documentation**: See `docs/MCP_INTEGRATION.md` (archived) for detailed guide

---

## 🔄 LangGraph Orchestration

**Purpose**: Plan → Act → Critique → Re-plan loops for complex workflows

### Quick Start

```bash
# Install with LangGraph support
pip install sota-agent-framework[agent-frameworks]
```

### Usage

```python
from orchestration.langgraph.workflow import AgentWorkflowGraph
from orchestration.langgraph.nodes import PlannerNode, ExecutorNode, CriticNode

# Create workflow
workflow = AgentWorkflowGraph(agent_router=router)

# Add nodes
workflow.add_node("planner", PlannerNode())
workflow.add_node("executor", ExecutorNode())
workflow.add_node("critic", CriticNode())

# Define edges
workflow.add_edge("planner", "executor")
workflow.add_conditional_edge("executor", "critic", should_replan)

# Run workflow
result = await workflow.run(input_data)
```

### Configuration

```yaml
# config/sota_config.yaml
langgraph:
  enabled: true
  max_iterations: 5
  planning:
    model: "gpt-4"
    temperature: 0.7
  critique:
    enabled: true
    threshold: 0.8
```

### When to Use

- ✅ Multi-step workflows
- ✅ Autonomous decision-making
- ✅ Self-correcting agents
- ✅ Complex task decomposition

**Full Documentation**: See `docs/LANGGRAPH_INTEGRATION.md` (archived) for detailed guide

---

## 🏢 Databricks Integration

**Purpose**: Native integration with Databricks for production deployments

### Quick Start

```bash
# Install with Databricks support
pip install sota-agent-framework[databricks]
```

### Features

#### 1. **Unity Catalog Integration**

```python
from uc_registry import PromptRegistry

# Store prompts in Unity Catalog
registry = PromptRegistry()
registry.register_prompt(
    name="fraud_detector_v2",
    content=prompt_text,
    metadata={"version": "2.0"}
)

# Retrieve later
prompt = registry.get_prompt("fraud_detector_v2")
```

#### 2. **Telemetry → Delta Lake**

```python
from telemetry import AgentTracer

# Traces automatically exported to Delta Lake
tracer = AgentTracer()

with tracer.trace_agent_execution():
    result = agent.execute(input_data)

# Query traces in Delta Lake
spark.read.table("main.sota_agents.traces")
```

#### 3. **Databricks-Native Visualization**

```python
from visualization import DatabricksVisualizer

# Works in Databricks notebooks
viz = DatabricksVisualizer()

# Execution graph (Mermaid)
viz.show_execution_graph(trace)

# Timeline (Plotly)
viz.show_timeline(trace)

# Log to MLflow
viz.log_to_mlflow(trace)
```

#### 4. **Infrastructure as Code (Terraform)**

```bash
cd infra/databricks
terraform init
terraform plan
terraform apply
```

**Provisions:**
- Unity Catalog (catalogs, schemas, volumes)
- Model Serving endpoints
- Compute clusters
- Databricks Jobs

### Configuration

```yaml
# config/sota_config.yaml
databricks:
  workspace_url: ${DATABRICKS_HOST}
  token: ${DATABRICKS_TOKEN}
  
  unity_catalog:
    catalog: "main"
    schema: "sota_agents"
    volume: "prompts"
  
  mlflow:
    experiment_name: "sota_agents"
    tracking_uri: "databricks"
  
  model_serving:
    endpoint_name: "agent-llm"
    workload_size: "Small"
```

### Databricks Notebook Example

```python
# Works seamlessly in Databricks notebooks
from sota_agent import AgentRouter
from visualization import DatabricksVisualizer

# Load agents
router = AgentRouter.from_yaml("config/agents.yaml")

# Execute
result = await router.route("fraud_detector", transaction_data)

# Visualize (renders natively in notebook)
viz = DatabricksVisualizer()
viz.show_execution_graph(result.trace)

# Data automatically in Delta Lake
display(spark.read.table("main.sota_agents.agent_executions"))
```

### Environment Detection

Framework auto-detects Databricks:

```python
import os

if "DATABRICKS_RUNTIME_VERSION" in os.environ:
    # Automatically uses Databricks-specific features
    # - Unity Catalog for storage
    # - MLflow for tracking
    # - displayHTML() for viz
    pass
```

**Full Documentation**: See `docs/archive/DATABRICKS_NATIVE_CHECKLIST.md` for deployment checklist

---

## 📦 Installation Matrix

| Integration | Install Command | Optional Features |
|-------------|----------------|-------------------|
| **MCP** | `pip install sota-agent-framework[mcp]` | Tool calling |
| **LangGraph** | `pip install sota-agent-framework[agent-frameworks]` | Orchestration |
| **Databricks** | `pip install sota-agent-framework[databricks]` | UC, MLflow, Viz |
| **All** | `pip install sota-agent-framework[all]` | Everything |

---

## 🎯 When to Use Each

| Integration | Use Case |
|-------------|----------|
| **MCP** | Need external tool APIs (BIN lookup, sanctions, etc.) |
| **LangGraph** | Complex multi-step workflows, autonomous agents |
| **Databricks** | Production deployment, data platform integration |

---

## 📚 Additional Resources

- **MCP Servers**: See `mcp-servers/` directory for examples
- **LangGraph Examples**: See `examples/langgraph_planning_workflow.py`
- **Terraform**: See `infra/databricks/main.tf`
- **Detailed Docs**: See `docs/archive/` for comprehensive guides

---

**All integrations are optional - use only what you need!** 🎯

