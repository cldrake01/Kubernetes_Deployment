import email
import imaplib
import json
import smtplib
import time
import openai
import re
from typing import Tuple


# import pymongo as pymongo


class EmailClient:

    def __init__(self, email: str,
                 password: str,
                 openai_api_key: str,
                 openai_org: str,
                 respone_conduct: str = "Answer any questions asked of you: ",
                 client_params: str = ""
                 ):

        self.client_email = email
        self.client_email_password = password
        self.response_conduct = respone_conduct
        self.client_params = client_params
        openai.organization = openai_org
        openai.api_key = openai_api_key

    def check_unread_emails(self) -> (str, email.message.EmailMessage):
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(self.client_email, self.client_email_password)
        mail.select("inbox")
        status, messages = mail.search(None, "UNSEEN")
        if len(messages) == 0:
            print("No unread messages in inbox.")
        message_id = messages[0].split()[0]

        status, message = mail.fetch(message_id, "(RFC822)")
        msg = email.message_from_bytes(message[0][1])
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    plain_text = part.get_payload(decode=True).decode()
                    pattern = re.compile('<.*?>')
                    processed_plain_text = pattern.sub('', plain_text)
                    return processed_plain_text, msg
        else:
            plain_text = msg.get_payload(decode=True).decode()
            pattern = re.compile('<.*?>')
            processed_plain_text = pattern.sub('', plain_text)
            return processed_plain_text, msg

    def generate_response(self, param_plain_text: str) -> dict:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=self.client_params + self.response_conduct + param_plain_text,
            temperature=0,
            max_tokens=1000
        )
        return response

    def save_response(self, response: dict):
        response_str = json.dumps(response)
        with open("response.json", "w") as json_file:
            json.dump(response_str, json_file)

    def extract_email_info(self, msg: email.message.EmailMessage) -> Tuple[str, str]:
        name = msg['From']
        carat_email = msg['Return-Path']
        decarated_email = carat_email[1:-1]
        return name, decarated_email


email_client = EmailClient(email="websockettesting503@gmail.com",
                           password="iwmzaxcczhhksbzo",
                           respone_conduct="Act as if you are a claim adjuster representing a life insurance company, "
                                           "respond to"
                                           " client emails and fillings accordingly. "
                                           "emails, and evaluate submitted claims; assume reasonable restrictions. ",
                           client_params="Our institution does not provide reimbursements 130% greater than the cost "
                                         "of our clients"
                                         "sustained injuries, damages. or otherwise.",
                           openai_api_key="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",
                           openai_org="org-qcHPiKIimtg6ssjx0Xla5AGH")

while True:
    try:

        """

        client = pymongo.MongoClient(
            "mongodb+srv://frac:frac1@cluster0.ithicjt.mongodb.net/?retryWrites=true&w=majority")
        db = client.test
        print(f"DB: {db}")
        
        """

        outer_plain_text, outer_msg = email_client.check_unread_emails()
        print(f"plain_text: {outer_plain_text}")
        print(f"msg: {outer_msg}")

        outer_response = email_client.generate_response(outer_plain_text)
        print(f"response: {outer_response}")

        email_client.save_response(outer_response)

        email_client.extract_email_info(outer_msg)

        outer_json_text = json.loads(json.dumps(outer_response))
        print(f"json_text: {outer_json_text}")

        outer_text = outer_json_text['choices'][0]['text']
        print(f"text: {outer_text}")

        outer_name, sender_email = email_client.extract_email_info(outer_msg)

        # Create the email message
        outer_message = f"Dear {outer_name},\n\n{outer_text}\n"

        # Send the email message
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_client.client_email, email_client.client_email_password)
        server.sendmail(email_client.client_email, sender_email, outer_message)
        server.quit()
    except IndexError as e:
        print(f"There are no emails to process currently, checking again in one minute.")
        time.sleep(60)
    except Exception as j:
        print(f"{j}")
        time.sleep(60)
