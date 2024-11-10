# utils.py

import logging
import json
logger = logging.getLogger(__name__)

def read_json_file(file_path):
    """Read a JSON file containing multiple JSONS and return a list of dictionaries."""
    try:
        with open(file_path, 'r') as file:
            json_objects = []
            for idx, line in enumerate(file):
                try:
                    json_object = json.loads(line)
                    json_objects.append(json_object)
                except json.JSONDecodeError as e:
                    # skip the erroneous event JSON object
                    print(f"Error decoding JSON object: {e}")
                    print(f"skipping the JSON object with the index = {idx}")
                    continue
            return json_objects
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

def extract_unique_emails(data):
    """
    Extracts unique emails from event data.
    """
    try:
        emails = {event['creator']['email'] for event in data}
        logger.info(f"Extracted unique emails: {emails}")
        return emails
    except Exception as e:
        logger.error(f"Error extracting unique emails: {e}")
        return set()

def divide_emails_into_groups(emails, num_groups):
    """
    Divides emails into `num_groups` groups.
    """
    try:
        groups = [[] for _ in range(num_groups)]
        for idx, email in enumerate(emails):
            groups[idx % num_groups].append(email)
        logger.info(f"Divided emails into {num_groups} groups: {groups}")
        return groups
    except Exception as e:
        logger.error(f"Error dividing emails into groups: {e}")
        return []
