# main.py

import asyncio
from core import EventProcessor
from utils import extract_unique_emails, divide_emails_into_group, read_json_file
from logging_config import configure_logging

# Configure logging
DATASET_FILE_NAME = "ingested_event_100 (1).json"
configure_logging()

# Sample data and initialization
data = read_json_file(DATASET_FILE_NAME)

emails = extract_unique_emails(data)
email_groups = divide_emails_into_groups(emails, 2)

# Initialize and run the event processor
processor = EventProcessor(num_agents=2, email_groups=email_groups, event_list=data)
asyncio.run(processor.run())
