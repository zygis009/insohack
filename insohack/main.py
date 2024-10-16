from dotenv import load_dotenv
from llm_access import create_client, send_conversation_message, send_single_message, flush_conversation


load_dotenv()

client, resp = create_client()

while True:
    user_input = input(resp.content[0].text + "\n")

    if user_input == "exit":
        break

    resp = send_conversation_message(client, user_input)

