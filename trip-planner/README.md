# Trip Planner Agents

Generated from SOTA Agent Framework template.

## Overview

This project implements AI agents for trip planner using the SOTA Agent Framework.

## Project Structure

```
.
├── trip_planner/           # Agent implementations
│   ├── __init__.py
│   └── agents.py
├── config/                  # Configuration files
│   └── trip_planner_config.yaml
├── tests/                   # Tests
│   └── test_trip_planner.py
├── examples/                # Usage examples
│   └── example_usage.py
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## Getting Started

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Edit `config/trip_planner_config.yaml` to customize agent behavior:

```yaml
agents:
  trip_planner_agent:
    enabled: true
    execution_mode: "in_process"  # or "ray_task" for distributed
    timeout: 30
```

### 3. Usage

```python
from agents import AgentRouter
from shared.schemas import AgentInput

# Load agents
router = AgentRouter.from_yaml("config/trip_planner_config.yaml")

# Create input
agent_input = AgentInput(
    request_id="req_123",
    data=your_data
)

# Execute
result = await router.route("trip_planner_agent", agent_input)
```

### 4. Run Example

```bash
python examples/example_usage.py
```

## Development

### Run Tests

```bash
pytest tests/
```

### Add New Agent

1. Create agent class in `trip_planner/agents.py`
2. Add configuration in `config/trip_planner_config.yaml`
3. Write tests in `tests/test_trip_planner.py`

## Next Steps

- [ ] Implement your domain-specific logic in agent classes
- [ ] Customize configuration for your deployment
- [ ] Add integration with your existing pipeline
- [ ] Write additional tests
- [ ] Deploy to your environment

## Resources

- [SOTA Agent Framework Documentation](../docs/)
- [Template Guide](../docs/TEMPLATE_GUIDE.md)
- [Configuration System](../docs/CONFIGURATION_SYSTEM.md)

## License

MIT
