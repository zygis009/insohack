import os
import anthropic
import csv_to_prompt

prompt = csv_to_prompt.get_prompt("Google", "../processed.csv")

conversation = [{"role": "user", "content": "Hello. What is the goal of this conversation?"}]


def create_client():
    key = os.getenv('LLM_API_KEY')
    client = anthropic.Client(api_key=key)
    init_msg = _init_message(client)
    return client, init_msg


def _init_message(client):
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        system=prompt,
        messages=[{"role": "user", "content": "Hello"}],
    )
    conversation.append({"role": "assistant", "content": message.content[0].text})
    return message


def send_conversation_message(client, content):
    conversation.append({"role": "user", "content": content})
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        system=prompt,
        messages=conversation,
    )

    conversation.append({"role": "assistant", "content": message.content[0].text})
    return message


def send_single_message(client, content):
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        system=prompt,
        messages=[{"role": "user", "content": content}],
    )
    return message


def flush_conversation(client):
    global conversation
    conversation = [{"role": "user", "content": "Hello"}]
    _init_message(client)