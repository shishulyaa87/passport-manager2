from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.app import App
import requests

class RegisterScreen(Screen):
    def register(self, instance):
        username = self.ids.username_input.text.strip()
        password = self.ids.password_input.text.strip()
        password_confirm = self.ids.confirm_password_input.text.strip()

        if not username or not password or not password_confirm:
            self.ids.message.color = (1, 0, 0, 1)
            self.ids.message.text = 'Все поля обязательны для заполнения'
            return

        if password != password_confirm:
            self.ids.message.color = (1, 0, 0, 1)
            self.ids.message.text = 'Пароли не совпадают'
            return

        try:
            url = 'http://127.0.0.1:5000/api/register'
            response = requests.post(url, json={'username': username, 'password': password})
            data = response.json()

            if response.status_code == 201:
                self.ids.message.color = (0, 1, 0, 1)
                self.ids.message.text = 'Регистрация прошла успешно!'

                app = App.get_running_app()
                app.username = username
                self.manager.get_screen('password_manager').username = app.username
                Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'password_manager'), 1.2)
            else:
                self.ids.message.color = (1, 0, 0, 1)
                self.ids.message.text = data.get('message', 'Ошибка регистрации')

        except Exception as e:
            self.ids.message.color = (1, 0, 0, 1)
            self.ids.message.text = f'Ошибка соединения: {e}'

    def go_to_login(self, instance):
        self.manager.current = 'login'
