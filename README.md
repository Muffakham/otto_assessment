# Otto Assessment: Mock event processing system with multiple agents

This is an asynchronous event processing system where multiple agents process incoming events in parallel. Each agent handles events based on specific email assignments, and the system tracks how long each event waited for an agent, how long it took to process, and whether it was successfully completed or encountered an error. The results are logged for monitoring purposes.

## Features

- **Multiple Agents**: A pool of agents are available to handle events. Each agent is assigned specific email groups and can process events associated with those emails.
- **Event Processing**: Each event is dispatched to an available agent. If no agent is available, the system retries until an agent is available, using an agent queue.
   - once an agent is assigned for an event, it mocks the processing time betwee 1 to 5 seconds.
   - Once the processing is completed, the agent is returned to queue.
   - An agent is considered available if it is not handling any other event and the email_id of the event is part of the email id group of the agent.
   - Each agent also logs a history of all the events it porcessed, keeping a track of waiting time, event ids and if the event got executed.
   - Sicne there is no time limit, all events get executed, but in case the execution time is limted, some event may not be completed.
   - The agent hisotry keeps track of those.
   - As per the question, the agent is to be slected randomly. But it gets delayed when taking into consideration user groups.
   - Randomly selected agents may not belong to user group of the event, therefore the agent handler keeps on bouncing from event to event.
   - This increases the wait time of both the agents and the events, hence an async queue has been used here to allocate agents.
   - The events are also stored in a seprate queue exhibiting the FIFO mechanism. 


## Requirements

- Python

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Muffakham/otto_assessment.git
   cd otto_assessment
