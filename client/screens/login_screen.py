from kivy.uix.screenmanager import Screen
from kivy.app import App
import requests

class LoginScreen(Screen):
    def login(self, instance):
        username = self.ids.login_input.text.strip()
        password = self.ids.password_input.text.strip()

        if not username or not password:
            self.ids.message.color = (1, 0, 0, 1)
            self.ids.message.text = 'Введите логин и пароль'
            return

        try:
            url = 'http://127.0.0.1:5000/api/login'
            response = requests.post(url, json={'username': username, 'password': password})
            data = response.json()

            if response.status_code == 200:
                self.ids.message.color = (0, 1, 0, 1)
                self.ids.message.text = 'Успешный вход!'

                app = App.get_running_app()
                app.username = username
                self.manager.get_screen('password_manager').username = username
                self.manager.current = 'password_manager'
            else:
                self.ids.message.color = (1, 0, 0, 1)
                self.ids.message.text = data.get("message", "Ошибка входа")

        except Exception as e:
            self.ids.message.color = (1, 0, 0, 1)
            self.ids.message.text = f'Ошибка соединения: {e}'

    def go_to_register(self, instance):
        self.manager.current = 'register'
