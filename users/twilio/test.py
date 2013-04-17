from twilio.rest import TwilioRestClient

account = "ACad5b697d43118d36082e78894c07fdbd"
token = "b625061400a44d2a8c8e0784412f8785"
client = TwilioRestClient(account, token)

message = client.sms.messages.create(to="+19162762760", from_="+15308838474",
                                     body="Coding is fun")