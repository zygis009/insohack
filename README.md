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

## Environment variables
Add .env file with
´´´
TWILIO_ACCOUNT_ID="acc_id"
TWILIO_API_TOKEN="auth_token"
NUMBER_FROM="caller number"
NUMBER_TO="called number"
WEBHOOK_URL="your_webhook_url"
´´´