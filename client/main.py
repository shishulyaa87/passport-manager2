from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
import os
from db import init_db

init_db()


# Пути к файлам
KV_DIR = os.path.join(os.path.dirname(__file__), 'kv')

# Загружаем KV файлы
Builder.load_file(os.path.join(KV_DIR, 'login_screen.kv'))
Builder.load_file(os.path.join(KV_DIR, 'register_screen.kv'))
Builder.load_file(os.path.join(KV_DIR, 'password_manager_screen.kv'))
Builder.load_file(os.path.join(KV_DIR, 'generator_screen.kv'))

from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.password_manager_screen import PasswordManagerScreen
from screens.generator_screen import GeneratorScreen


class PassportManagerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = ''

    def build(self):
        sm = ScreenManager()

        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(PasswordManagerScreen(name='password_manager'))
        sm.add_widget(GeneratorScreen(name='generator'))

        sm.current = 'login'
        return sm


if __name__ == '__main__':
    PassportManagerApp().run()
