import requests
import json

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = '{\n  "model": "llama3.2:1b",\n  "prompt":"The biggest tree in the world?"\n}'

response = requests.post('http://localhost:11434/api/generate', headers=headers, data=data, stream=True)

full_response = ""

for line in response.iter_lines():
    if line:
        try:
            json_line = json.loads(line.decode('utf-8'))
            full_response += json_line['response']
        except json.JSONDecodeError:
            print("Ошибка декодирования JSON:", line)

print(full_response)
