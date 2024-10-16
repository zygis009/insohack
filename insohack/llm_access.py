import os
import anthropic

with open('prompt.txt', 'r') as file:
    prompt = file.read()

conversation = [{"role": "user", "content": "Hello"}]


def create_client():
    key = os.getenv('LLM_API_KEY')
    client = anthropic.Client(api_key=key)
    init_msg = _init_message(client)
    return client, init_msg


def _init_message(client):
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        system=prompt,
        messages=[{"role": "user", "content": "Hello"}],
    )
    conversation.append({"role": "assistant", "content": message.content[0].text})
    return message


def send_conversation_message(client, content):
    conversation.append({"role": "user", "content": content})
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        system=prompt,
        messages=conversation,
    )
    # Message format:
    # Message(
    #   id='msg_015MXD4NyE5DMirqWRv8VHFs',
    #   content=[TextBlock(
    #       text="Hello! I'm happy to hear that you just bought (...)",
    #       type='text')],
    #   model='claude-3-haiku-20240307',
    #   role='assistant',
    #   stop_reason='end_turn',
    #   stop_sequence=None,
    #   type='message',
    #   usage=Usage(input_tokens=106, output_tokens=49)
    # )

    # Note: template (with assumptions) for parsing response
    conversation.append({"role": "assistant", "content": message.content[0].text})
    return message


def send_single_message(client, content):
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        system=prompt,
        messages=[{"role": "user", "content": content}],
    )
    return message


def flush_conversation(client):
    global conversation
    conversation = [{"role": "user", "content": "Hello"}]
    _init_message(client)