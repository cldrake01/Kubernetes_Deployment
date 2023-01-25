# Native:
import os
import sys
import time
import json
import email
import asyncio
import smtplib
import imaplib

# External:
import openai

while True:
    try:
        app_password = "iwmzaxcczhhksbzo"

        openai.organization = "org-qcHPiKIimtg6ssjx0Xla5AGH"
        openai.api_key = "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"
        # openai.Model.retrieve("text-davinci-003")
        # openai.Model.list()

        # Connect to the email server
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login("websockettesting503@gmail.com", app_password)

        # Select the inbox
        mail.select("inbox")

        # Search for unread messages
        status, messages = mail.search(None, "UNSEEN")
        print(f"Messages: {messages}")

        if len(messages) == 0:
            print("No unread messages in inbox.")
            sys.exit(1)

        # Get the first unread message
        message_id = messages[0].split()[0]
        print(f"Message ID: {message_id}")

        # Fetch the message
        status, message = mail.fetch(message_id, "(RFC822)")

        msg = email.message_from_bytes(message[0][1])

        if msg.is_multipart():
            # Iterate over the different parts of the email message
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    plain_text = part.get_payload(decode=True).decode()
                    # Use regular expression to filter out the HTML tags
                    import re

                    pattern = re.compile('<.*?>')
                    plain_text = pattern.sub('', plain_text)
        else:
            plain_text = msg.get_payload(decode=True).decode()
            # Use regular expression to filter out the HTML tags
            import re

            pattern = re.compile('<.*?>')
            plain_text = pattern.sub('', plain_text)

        print(f"Plaintext: {plain_text}")

        """

        This functionality isn't needed yet.

        async def send_to_websocket(websocket, path):
            await websocket.send(message_json)

        # Connect to the websocket server
        websocket = websockets.serve(send_to_websocket, "localhost", 8000)

        asyncio.get_event_loop().run_until_complete(websocket)

        """

        response = openai.Completion.create(model="text-davinci-003",
                                            prompt="Answer any questions asked of you below:"
                                                   + plain_text,
                                            temperature=0,
                                            max_tokens=700)

        # Load the JSON file
        response_str = json.dumps(response)
        with open("response.json", "w") as json_file:
            json.dump(response_str, json_file)

        json_text = json.loads(response_str)

        text = json_text['choices'][0]['text']

        # message = message[0][1]
        # print(f"Message: {message}")

        # Convert the message to JSON
        # message_json = json.dumps(message.decode())
        # print(f"Message JSON: {message.decode()}")

        # Extract the email information from the JSON file
        name = "Collin Drake"

        carat_email = msg['Return-Path']

        email = carat_email[1:-1]

        # timestamp = data["timestamp"]

        # Create the email message
        # message = f"Dear {name},\n\n{text}\n\nSincerely,\nYour Name\nTimestamp:{timestamp}"
        message = f"Dear: {name},\n\n{text}\n\nSincerely,\nChatGPT\n"

        # Connect to the email server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        # Log in to the email account
        server.login("websockettesting503@gmail.com", app_password)

        # Send the email
        try:
            server.sendmail("websockettesting503@gmail.com", email, message)
            print(f"Email to {email} sent successfully.")
        except Exception as e:
            print(f"An error occurred while sending the email: {e}")

        # Close the connection to the email server
        server.quit()

        time.sleep(600)
    except Exception as e:
        print(f"There are no emails to process currently, I'll check again in one minute. Causation for check: {e}")
        time.sleep(10)
        print("Checking my inbox again.")
        time.sleep(6)
        continue
