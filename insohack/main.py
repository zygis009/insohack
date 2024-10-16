from dotenv import load_dotenv
import json
from llm_access import create_client, send_conversation_message, send_single_message, flush_conversation
import re


def extract_data(text):
    # Regex to find everything after <END_OF_CONVERSATION>
    pattern = r'<END_OF_CONVERSATION>\s*(\{.*?\})'

    # Search for the JSON in the text
    match = re.search(pattern, text, re.DOTALL)

    if match:
        json_str = match.group(1)  # Capture the JSON part
        try:
            # Convert the JSON string to a Python dictionary
            json_data = json.loads(json_str)
            return json_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        return None


load_dotenv()

client, resp = create_client()

result = None

while True:
    user_input = input(resp.content[0].text + "\n")

    if user_input == "exit":
        break

    resp = send_conversation_message(client, user_input)

    result = extract_data(resp.content[0].text)
    if result is not None:
        break

print(result)