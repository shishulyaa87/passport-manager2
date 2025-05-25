import requests

BASE_URL = 'http://127.0.0.1:5000/api'

def register_user(username, password):
    response = requests.post(f'{BASE_URL}/register', json={
        'username': username,
        'password': password
    })
    return response.status_code, response.json().get('message')

def login_user(username, password):
    response = requests.post(f'{BASE_URL}/login', json={
        'username': username,
        'password': password
    })
    return response.status_code, response.json().get('message')

def save_password(username, service, login, password):
    response = requests.post(f'{BASE_URL}/save_password', json={
        'username': username,
        'service': service,
        'login': login,
        'password': password
    })
    return response.status_code, response.json().get('message')

def get_passwords(username):
    response = requests.get(f'{BASE_URL}/passwords/{username}')
    if response.status_code == 200:
        return response.json()
    else:
        return []

def delete_password(username, service, login):
    response = requests.post(f'{BASE_URL}/delete_password', json={
        'username': username,
        'service': service,
        'login': login
    })
    return response.status_code, response.json().get('message')
