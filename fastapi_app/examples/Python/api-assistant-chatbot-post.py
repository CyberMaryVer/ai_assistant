import requests

user_id = '123'
your_company = 'your_company'
endpoint_url = f'https://{your_company}.com/api/assistant/chatbot/{user_id}'

payload = {
  "user_input": "string",
}

response = requests.post(endpoint_url, json=payload)
if response.status_code == 200:
    print('Response:', response.json())
else:
    print('Error:', response.text)
