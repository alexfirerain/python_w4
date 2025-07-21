from requests import get
# просто тестируем, как что возвращает сервер (должен работать)

print(get('http://127.0.0.1:5000/api/news').json())