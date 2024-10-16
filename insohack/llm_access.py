import os
import anthropic

with open ('prompt.txt', 'r') as file:
    prompt = file.read()

conversation = [{"role": "system", "content": prompt}]


def create_client():
    key = os.getenv('LLM_API_KEY')
    client = anthropic.Client(api_key=key)

    return client


def send_conversation_message(client, content):
    conversation.append({"role": "user", "content": content})
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=conversation,
    )
    # Note: template (with assumptions) for parsing response
    conversation.append({"role": "assistant", "content": message["content"][0]["text"]})
    return message


def send_single_message(client, content):
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=[{"role": "system", "content": prompt}, {"role": "user", "content": content}],
    )
    return message


def flush_conversation():
    global conversation
    conversation = [{"role": "system", "content": prompt}]
