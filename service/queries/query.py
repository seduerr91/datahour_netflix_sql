import requests

payload = {'question': "What was the most popular show?"}
response = requests.post(url="http://localhost:8010/question", json=payload)

print(f"### Question: {payload['question']}\n")
print(f"### Response: {response.text}\n")