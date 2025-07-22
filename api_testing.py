from requests import get, post, delete

# просто тестируем, как что возвращает сервер (должен работать)

# print(get('http://127.0.0.1:5000/api/news').json())
# print(get('http://127.0.0.1:5000/api/news/1').json())
# print(get('http://127.0.0.1:5000/api/news/1000').json())
# print(get('http://127.0.0.1:5000/api/news/q').json())

print(post('http://127.0.0.1:5000/api/news', json={}).json())
print(post('http://127.0.0.1:5000/api/news', json={'user_id': '1'}).json())
print(post('http://127.0.0.1:5000/api/news', json={'title': 'новость', 'content': 'дивные дела!', 'user_id': 1, 'is_private': 0}).json())
# и токен прилепить, чтоб кто попало новости не постил

print(delete('http://127.0.0.1:5000/api/news/500').json())

# ДЗ: сделать апдэйт методом PUT