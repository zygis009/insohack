# Download the helper library from https://www.twilio.com/docs/python/install
import os
from dotenv import load_dotenv
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure

if __name__ == '__main__':
  load_dotenv()
  client = Client(os.environ["TWILIO_ACCOUNT_ID"], os.environ["TWILIO_API_TOKEN"])

  call = client.calls.create(
    url="http://demo.twilio.com/docs/voice.xml",
    to=os.environ["NUMBER_TO"],
    from_=os.environ["NUMBER_FROM"]
  )

  print(call.sid)