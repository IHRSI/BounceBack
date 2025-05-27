from twilio.rest import Client

# Twilio credentials
ACCOUNT_SID = "AC2ea96e020ca57048a182f76225f15bef"
AUTH_TOKEN = "678f08562671d6df78cc59be4988e450"

# Initialize Twilio Client
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Send SMS
message = client.messages.create(
    body="Hello from Twilio!",
    from_="+17157520371",  # Your Twilio number
    to="+918929846800"  # Recipient's phone number
)

print(f"Message sent! SID: {message.sid}")
