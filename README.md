# insohack
Repository for the Insocial AI hackathon

## Getting started
### Local server
```bash
cd insohack
python server.py
```
Make sure the server is available in the internet and add that url with endpoint /webhook in the environment variables

### Call endpoint 
Call the POST /create-call endpoint to start a call


## Environment variables
Add .env file with
´´´
TWILIO_ACCOUNT_ID="acc_id"
TWILIO_API_TOKEN="auth_token"
NUMBER_FROM="caller number"
NUMBER_TO="called number"
WEBHOOK_URL="your_webhook_url"
´´´

## Formatting
### Anthropic message format:
```
Message(
    id='msg_12345abcd...',
    content=[TextBlock(
    text="Hello! I'm happy to hear that you just bought (...)",
    type='text')],
    model='claude-3-5-sonnet-20240620',
    role='assistant',
    stop_reason='end_turn',
    stop_sequence=None,
    type='message',
    usage=Usage(input_tokens=106, output_tokens=49)
)
```
