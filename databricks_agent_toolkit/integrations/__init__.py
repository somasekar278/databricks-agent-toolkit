"""
Databricks Agent Toolkit - Integrations Module

Pre-wired integrations to all Databricks services for agentic development.

Core integrations:
- DatabricksLLM: Easy Model Serving client
- DatabricksMCPTools: Managed MCP servers (Vector Search, Genie, UC Functions, DBSQL)
- UnityAgentArtifacts: Unity Catalog for prompts, configs, functions
- Lakebase: Vector search & memory
- DatabricksAppDeployment: One-command deployment to Databricks Apps

Example:
    from databricks_agent_toolkit.integrations import (
        DatabricksLLM,
        DatabricksMCPTools,
        UnityAgentArtifacts
    )
    
    # Initialize (auto-auth via Databricks SDK)
    llm = DatabricksLLM(endpoint="databricks-claude-sonnet-4-5")
    mcp = DatabricksMCPTools(servers={
        "vector_search": {"catalog": "prod", "schema": "docs"}
    })
    uc = UnityAgentArtifacts(catalog="main", schema="agents")
    
    # Use with any framework (LangGraph, LangChain, custom)
    response = await llm.chat(messages=[...])
"""

try:
    from .model_serving import DatabricksLLM
    from .mcp_databricks import DatabricksMCPTools
    from .unity_catalog import UnityAgentArtifacts
    from .lakebase import Lakebase
    from .apps import DatabricksAppDeployment
    from .auth import get_workspace_client, check_authentication
    
    __all__ = [
        "DatabricksLLM",
        "DatabricksMCPTools",
        "UnityAgentArtifacts",
        "Lakebase",
        "DatabricksAppDeployment",
        "get_workspace_client",
        "check_authentication",
    ]
except ImportError as e:
    # Integrations require databricks-sdk and mlflow
    # Install with: pip install databricks-agent-toolkit[databricks]
    import warnings
    warnings.warn(
        f"Databricks integrations not available: {e}\n"
        "Install with: pip install databricks-agent-toolkit[databricks]"
    )
    __all__ = []

__version__ = "0.1.0"

