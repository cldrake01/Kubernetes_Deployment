import os
import re
import sys
import json
import email
import asyncio
import smtplib
import imaplib
import openai


class EmailServer:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com")
        self.msg = None

    def login(self):
        self.mail.login(self.username, self.password)

    def select_inbox(self):
        self.mail.select("inbox")

    def search_unread(self):
        status, messages = self.mail.search(None, "UNSEEN")
        if len(messages) == 0:
            print("No unread messages in inbox.")
            sys.exit(1)
        return messages[0].split()[0]

    def fetch_message(self):
        global plain_text
        message = self.mail.fetch(self.search_unread(), "(RFC822)")
        self.msg = email.message_from_string(message[0][1])
        if self.msg.is_multipart():
            for part in self.msg.walk():
                if part.get_content_type() == 'text/plain':
                    plain_text = part.get_payload(decode=True).decode()
                    pattern = re.compile('<.*?>')
                    plain_text = pattern.sub('', plain_text)
        else:
            plain_text = self.msg.get_payload(decode=True).decode()
            pattern = re.compile('<.*?>')
            plain_text = pattern.sub('', plain_text)
        return plain_text

    def logout(self):
        self.mail.logout()


class OpenAIAPI:
    def __init__(self, api_key, organization):
        self.api_key = api_key
        self.organization = organization
        openai.api_key = api_key
        openai.organization = organization

    def generate_response(self, prompt):
        return openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=0, max_tokens=700)


class Email:
    def __init__(self, email_server, password):
        self.sender = email_server.username
        self.recipient = email_server.outer_msg['From']
        self.message = self.create_message()
        self.name = email_server.outer_msg['From'].split()[0]
        self.password = password

    def create_message(self):
        message = f"Dear {self.name},\n\n{response_str}\n\nSincerely,\nYour Name"
        return message

    def send(self):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(self.sender, self.password)
        server.sendmail(self.sender, self.recipient, self.message)
        print(f"Email sent to {self.recipient}.")
        server.quit()


class Runner:
    def __init__(self):
        self.app_password = "iwmzaxcczhhksbzo"
        self.openai_api = OpenAIAPI("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",
                                    "org-qcHPiKIimtg6ssjx0Xla5AGH")
        self.email_server = EmailServer("websockettesting503@gmail.com", self.app_password)

    def run(self):
        self.email_server.login()
        self.email_server.select_inbox()
        message = self.email_server.fetch_message()
        print(message)
        response = self.openai_api.generate_response(message)
        sent_email = Email("cldrake01@bvsd.org", response["choices"], "Collin Drake")
        sent_email.send(self.app_password)
        self.email_server.logout()


if __name__ == '__main__':
    runner = Runner()
    runner.run()
