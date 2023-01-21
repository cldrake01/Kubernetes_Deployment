# Native:
import os
import json
import asyncio
import websockets
# External:
import openai
import smtplib
import imaplib

openai.organization = "org-qcHPiKIimtg6ssjx0Xla5AGH"
openai.api_key = "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"
openai.Model.retrieve("text-davinci-003")
# openai.Model.list()

# Connect to the email server
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login("your_email@gmail.com", "your_password")

# Select the inbox
mail.select("inbox")

# Search for unread messages
status, messages = mail.search(None, "UNSEEN")

# Get the first unread message
message_id = messages[0].split()[0]

# Fetch the message
status, message = mail.fetch(message_id, "(RFC822)")

# Parse the message
message = message[0][1]

# Convert the message to JSON
message_json = json.dumps(message.decode())

async def send_to_websocket(websocket, path):
    await websocket.send(message_json)

# Connect to the websocket server
websocket = websockets.serve(send_to_websocket, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(websocket)
asyncio.get_event_loop().run_forever()

response = openai.Completion.create(model="text-davinci-003", prompt="Say this is a test", temperature=0, max_tokens=7)

# Load the JSON file
with open("response.json", "r") as json_file:
    data = json.load(json_file)

# Extract the email information from the JSON file
name = data["name"]
email = data["email address"]
timestamp = data["timestamp"]
text = data["text"]

# Create the email message
message = f"Dear {name},\n\n{text}\n\nSincerely,\nYour Name\nTimestamp:{timestamp}"

# Connect to the email server
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

# Log in to the email account
server.login("your_email@gmail.com", "your_password")

# Send the email
server.sendmail("your_email@gmail.com", email, message)

# Close the connection to the email server
server.quit()

