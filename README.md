# insohack
Repository for the Insocial AI hackathon

## Formatting
### Anthropic message format:
```
Message(
    id='msg_12345abcd...',
    content=[TextBlock(
    text="Hello! I'm happy to hear that you just bought (...)",
    type='text')],
    model='claude-3-haiku-20240307',
    role='assistant',
    stop_reason='end_turn',
    stop_sequence=None,
    type='message',
    usage=Usage(input_tokens=106, output_tokens=49)
)
```
