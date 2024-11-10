

import asyncio
import random
import time
import logging

# Set up logging for this module
logger = logging.getLogger(__name__)

class Event:
    """
    Represents an event with details like ID, description, and creator email.
    """
    def __init__(self, details):
        self.id = details['id']
        self.description = details
        self.email_id = details['creator']['email']
        self.event_ready_time_stamp = None
        self.event_execution_start_time_stamp = None
        self.wait_time = None
        self.start_time = None
        self.end_time = None
        self.duration = None

    def __str__(self):
        return f"Event {self.id}: {self.description}"

class Agent:
    """
    Represents an agent that can process events.
    """
    def __init__(self, id, emails):
        self.id = id
        self.emails = set(emails)
        self.available = True
        self.agent_ready_time_stamp = time.time() * 1000
        self.agent_execution_start_time_stamp = None
        self.is_available = True
        self.history = []
        self.lock = asyncio.Lock()

    async def execute_agent(self, event):
        """
        Simulates the agent executing an event.
        """
        async with self.lock:
            try:
                logger.info(f"Agent {self.id} starting to process event {event.id}.")
                self.is_available = False
                self.agent_execution_start_time_stamp = time.time() * 1000
                self.agent_wait_time = self.agent_execution_start_time_stamp - self.agent_ready_time_stamp
                logger.info(f"Agent {self.id} wait time {self.agent_wait_time} milliseconds before starting.")
                
                event.start_time = time.time() * 1000
                processing_time = random.randint(1, 5)
                await asyncio.sleep(processing_time)
                
                logger.info(f"Agent {self.id} processed event {event.id} in {processing_time} seconds.")
                event.end_time = time.time() * 1000
                event.duration = event.end_time - event.start_time
                
                # Log the agent's history for this event
                self.history.append({
                    "event_id": event.id,
                    "processing_time": processing_time,  # Time taken to process the event
                    "wait_time": self.agent_wait_time,   # Time agent waited before starting
                    "pass_status": "Success"             # Event processed successfully
                })
                
                self.is_available = True
            except Exception as e:
                logger.error(f"Error while executing event {event.id} by Agent {self.id}: {e}")
                self.history.append({
                    "event_id": event.id,
                    "processing_time": 0,
                    "wait_time": self.agent_wait_time,
                    "pass_status": "Error"
                })
                self.is_available = True

    def is_agent_available(self, event):
        """
        Check if the agent is available for the event.
        """
        if self.is_available and event.email_id in self.emails:
            return True
        return False

class AgentPool:
    """
    Manages a pool of agents for processing events.
    """
    def __init__(self, num_agents: int, email_groups: list):
        self.agents = asyncio.Queue()
        for i in range(num_agents):
            self.agents.put_nowait(Agent(str(i), email_groups[i]))

    async def get_available_agent(self, event):
        """
        Retrieves an available agent from the pool for an event.
        """
        try:
            agent = await self.agents.get()
            if agent.is_agent_available(event):
                return agent
            else:
                self.agents.put_nowait(agent)
                logger.info(f"Agent {agent.id} is not available for event {event.id}, checking next.")
                return None
        except asyncio.QueueEmpty:
            logger.info(f"No agents available for event {event.id}.")
            return None

    async def get_agent(self, event):
        """
        Retrieves an agent from the pool, retrying until one is available.
        """
        try:
            while True:
                agent = await self.get_available_agent(event)
                if agent is not None:
                    agent.agent_ready_time_stamp = time.time() * 1000
                    logger.info(f"Agent {agent.id} is ready for event {event.id}.")
                    return agent
                
                # If no agent is available, wait for some time before trying again
                logger.info(f"Waiting for an agent to become available for event {event.id}.")
                await asyncio.sleep(1)  # 1 second retry interval
        except Exception as e:
            logger.error(f"Error in getting agent for event {event.id}: {e}")
            return None

    async def return_agent(self, agent):
        """
        Return the agent to the pool after processing an event.
        """
        await self.agents.put(agent)

    async def log_agent_metadata(self):
        """
        Logs metadata for all agents in the pool.
        """
        while not self.agents.empty():
            agent = await self.agents.get()
            logger.info(f"Agent {agent.id} metadata: {agent.history}")


class EventProcessor:
    """
    Coordinates the dispatch of events to agents for processing.
    """
    def __init__(self, num_agents, email_groups: list, event_list: list):
        self.agent_pool = AgentPool(num_agents=num_agents, email_groups=email_groups)
        self.event_list = asyncio.Queue()
        self.number_of_events_completed = 0
        self.number_of_events_failed = 0  
        for event in event_list:
            self.event_list.put_nowait(Event(event))  # Use put_nowait for async Queue

    async def dispatch_event(self, event):
        """
        Dispatches an event to an available agent for processing.
        """
        try:
            agent = await self.agent_pool.get_agent(event)  # Get a ready agent
            if agent:
                event.execution_start_time_stamp = time.time() * 1000
                event.wait_time = event.execution_start_time_stamp - event.start_time
                logger.info(f"Event {event.id} waited for {event.wait_time} milliseconds before processing.")
                await agent.execute_agent(event)  # Execute the event on the agent
                await self.agent_pool.return_agent(agent)  # Return the agent to the pool
                self.number_of_events_completed += 1
                
            else:
                logger.info(f"No available agent for event {event.id}.")
                self.number_of_events_failed += 1
        except Exception as e:
            logger.error(f"Error in dispatching event {event.id}: {e}")
            self.number_of_events_failed += 1

    async def run(self):
        """
        Runs the event processor, dispatching all events to available agents.
        """
        tasks = []
        try:
            while not self.event_list.empty():
                event = await self.event_list.get()  # Use await for async Queue
                event.start_time = time.time() * 1000
                logger.info(f"Dispatching event {event.id} to an available agent.")
                tasks.append(self.dispatch_event(event))

            await asyncio.gather(*tasks)
            await self.agent_pool.log_agent_metadata()
        except Exception as e:
            logger.error(f"Error in running event processor: {e}")

