# Event Processing System

This is an asynchronous event processing system where multiple agents process incoming events in parallel. Each agent handles events based on specific email assignments, and the system tracks how long each event waited for an agent, how long it took to process, and whether it was successfully completed or encountered an error. The results are logged for monitoring purposes.

## Features

- **Multiple Agents**: A pool of agents are available to handle events. Each agent is assigned specific email groups and can process events associated with those emails.
- **Event Processing**: Each event is dispatched to an available agent. If no agent is available, the system retries until an agent is available.
- **Logging**: Logs all key activities, such as event dispatching, agent assignment, and errors. Logs are written to both the console and a file (`event_processor.log`).
- **Error Handling**: Logs error details when an agent fails to process an event.
- **Metrics Tracking**: Tracks the number of events completed successfully and the number of events that failed.

## Requirements

- Python 3.7+ (for `asyncio` support)
- No external dependencies beyond Python's standard library

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/event-processing-system.git
   cd event-processing-system
