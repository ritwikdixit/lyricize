import requests
import json

print('please type text:')
text = input()
response = requests.post('http://127.0.0.1:5000/lyrics', {'Body':text})
print(response.content)