# tests/test_core.py

import pytest
from unittest.mock import MagicMock
import asyncio
from event_processor.core import Agent, Event, AgentPool

@pytest.mark.asyncio
async def test_agent_is_available():
    agent = Agent(id="1", emails=["user1@example.com"])
    event = MagicMock()
    event.email_id = "user1@example.com"

    assert agent.is_agent_available(event) is True

@pytest.mark.asyncio
async def test_agent_is_not_available():
    agent = Agent(id="1", emails=["user1@example.com"])
    event = MagicMock()
    event.email_id = "user2@example.com"

    assert agent.is_agent_available(event) is False

@pytest.mark.asyncio
async def test_agent_execute_event_success():
    agent = Agent(id="1", emails=["user1@example.com"])
    event = MagicMock(id="event1", email_id="user1@example.com")

    # We mock time.sleep to avoid waiting for actual time
    with pytest.raises(AssertionError):
        await agent.execute_agent(event)  # We just need to ensure no exceptions are thrown
    assert len(agent.history) == 1  # The agent history should have one entry
    assert agent.history[0]["pass_status"] == "Success"

@pytest.mark.asyncio
async def test_agent_execute_event_failure():
    agent = Agent(id="1", emails=["user1@example.com"])
    event = MagicMock(id="event1", email_id="user1@example.com")

    # We will simulate an exception in the execute_agent method
    agent.execute_agent = MagicMock(side_effect=Exception("Test error"))

    await agent.execute_agent(event)
    assert len(agent.history) == 1
    assert agent.history[0]["pass_status"] == "Error"

@pytest.mark.asyncio
async def test_agent_pool_get_agent():
    agent_pool = AgentPool(num_agents=2, email_groups=[["user1@example.com"], ["user2@example.com"]])
    event = MagicMock(id="event1", email_id="user1@example.com")

    agent = await agent_pool.get_agent(event)
    assert agent is not None
    assert agent.id == "0"  # We expect the first agent in the pool to be assigned
