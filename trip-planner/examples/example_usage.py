'''
Example usage of Trip Planner agents

Generated from SOTA Agent Framework template.
'''

import asyncio
from agents import AgentRouter
from shared.schemas import AgentInput


async def main():
    '''Example usage of your agents.'''
    
    # Step 1: Load agents from config
    router = AgentRouter.from_yaml("config/trip_planner_config.yaml")
    print("✅ Agents loaded from config!")
    
    # Step 2: Create sample input
    agent_input = AgentInput(
        request_id="example_123",
        data={
            # Add your domain-specific data here
            "id": "sample_id",
            # ...
        },
        context={},
    )
    
    # Step 3: Execute agent
    print("\n🤖 Executing agent...")
    result = await router.route("trip_planner_agent", agent_input)
    
    # Step 4: Handle result
    print("\n✅ Agent completed!")
    print(f"Request ID: {result.request_id}")
    print(f"Score: {result.risk_score:.3f}")
    print(f"Action: {result.recommended_action}")
    print(f"Narrative: {result.risk_narrative}")
    print(f"Latency: {result.latency_ms:.2f}ms")


if __name__ == "__main__":
    asyncio.run(main())
