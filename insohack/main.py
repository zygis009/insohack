from dotenv import load_dotenv
from llm_access import create_client, send_conversation_message, send_single_message, flush_conversation


load_dotenv()

client = create_client()

resp = send_conversation_message(client, "Hello")
print(resp)

resp2 = send_conversation_message(client, "The paintjob")
print(resp2)

