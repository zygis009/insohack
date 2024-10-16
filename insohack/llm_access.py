import os
import anthropic

with open ('prompt.txt', 'r') as file:
    prompt = file.read()

def create_client():
    key = os.getenv('LLM_API_KEY')
    client = anthropic.Client(api_key=key)

    return client


def send_user_message(client, content):
    message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1024,
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": content}
    ]
)