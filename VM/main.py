import os
import json
import openai

openai.organization = "org-qcHPiKIimtg6ssjx0Xla5AGH"
openai.api_key = "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"
openai.Model.retrieve("text-davinci-003")
# openai.Model.list()

response = openai.Completion.create(model="text-davinci-003", prompt="Say this is a test", temperature=0, max_tokens=7)

print(json.dumps(response["choices"]))
