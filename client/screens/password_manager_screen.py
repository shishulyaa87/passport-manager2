from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty, ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
import requests
from kivy.core.clipboard import Clipboard

class PasswordManagerScreen(Screen):
    username = StringProperty('')
    message = StringProperty('')
    all_passwords = ListProperty([])

    def on_enter(self):
        self.ids.login_label.text = f"Пользователь: {self.username}"
        self.refresh_passwords()
        self.ids.search_service.bind(text=self.filter_passwords)
        self.ids.search_login.bind(text=self.filter_passwords)
        self.ids.search_password.bind(text=self.filter_passwords)
        self.setup_top_buttons()

    def setup_top_buttons(self):
        top_layout = self.ids.top_buttons_layout
        top_layout.clear_widgets()

        add_btn = Button(text='Добавить пароль', size_hint=(None, None), size=(180, 40), font_size=14)
        add_btn.bind(on_release=lambda x: self.add_password())

        gen_btn = Button(text='Перейти к генератору', size_hint=(None, None), size=(200, 40), font_size=14)
        gen_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'generator'))

        top_layout.add_widget(add_btn)
        top_layout.add_widget(gen_btn)

    def refresh_passwords(self):
        if not self.username:
            self.message = "Не указан пользователь"
            return
        try:
            url = f'http://127.0.0.1:5000/api/passwords/{self.username}'
            response = requests.get(url)
            if response.status_code != 200:
                self.message = f"Ошибка: {response.text}"
                return
            self.all_passwords = response.json()
            self.filter_passwords()
            self.message = ''
        except Exception as e:
            self.message = f"Ошибка: {e}"

    def filter_passwords(self, *args):
        service_filter = self.ids.search_service.text.lower()
        login_filter = self.ids.search_login.text.lower()
        password_filter = self.ids.search_password.text.lower()
        filtered = [
            p for p in self.all_passwords
            if service_filter in p['service'].lower()
            and login_filter in p['login'].lower()
            and password_filter in p['password'].lower()
        ]
        self.display_passwords(filtered)

    def display_passwords(self, passwords):
        layout = self.ids.passwords_layout
        layout.clear_widgets()
        for entry in passwords:
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)

            row.add_widget(Label(text=entry['service'], size_hint_x=0.2))
            row.add_widget(Label(text=entry['login'], size_hint_x=0.2))

            pass_label = Label(text='******', size_hint_x=0.2)
            row.add_widget(pass_label)

            def make_toggle_pass(label, real_pass):
                def toggle(instance):
                    label.text = real_pass if label.text == '******' else '******'
                return toggle

            show_btn = Button(text='Показать', size_hint_x=0.12, font_size=12)
            show_btn.bind(on_release=make_toggle_pass(pass_label, entry['password']))

            copy_login_btn = Button(text='Копировать логин', size_hint_x=0.18, font_size=12)
            copy_login_btn.bind(on_release=lambda btn, t=entry['login']: Clipboard.copy(t))

            copy_pass_btn = Button(text='Копировать пароль', size_hint_x=0.18, font_size=12)
            copy_pass_btn.bind(on_release=lambda btn, t=entry['password']: Clipboard.copy(t))

            edit_btn = Button(text="Редактировать", size_hint_x=0.15, font_size=12)
            edit_btn.bind(on_release=lambda inst, s=entry['service'], l=entry['login']: self.edit_password(s, l))

            del_btn = Button(text="Удалить", size_hint_x=0.1, font_size=12)
            del_btn.bind(on_release=lambda inst, s=entry['service'], l=entry['login']: self.delete_password(s, l))

            row.add_widget(show_btn)
            row.add_widget(copy_login_btn)
            row.add_widget(copy_pass_btn)
            row.add_widget(edit_btn)
            row.add_widget(del_btn)

            layout.add_widget(row)

    def open_password_popup(self, mode='add', service='', login='', password=''):
        popup_layout = GridLayout(cols=2, spacing=10, padding=10)

        popup_layout.add_widget(Label(text='Сервис:'))
        service_input = TextInput(text=service)
        popup_layout.add_widget(service_input)

        popup_layout.add_widget(Label(text='Логин:'))
        login_input = TextInput(text=login)
        popup_layout.add_widget(login_input)

        popup_layout.add_widget(Label(text='Пароль:'))
        password_input = TextInput(text=password, password=True)
        popup_layout.add_widget(password_input)

        def on_save(instance):
            s, l, p = service_input.text.strip(), login_input.text.strip(), password_input.text.strip()
            if not s or not l or not p:
                self.message = "Все поля обязательны"
                return
            if mode == 'add':
                self.save_new_password(s, l, p)
            else:
                self.update_password(service, login, s, l, p)
            popup.dismiss()

        save_btn = Button(text='Сохранить', size_hint_y=None, height=40)
        save_btn.bind(on_release=on_save)

        cancel_btn = Button(text='Отмена', size_hint_y=None, height=40)
        cancel_btn.bind(on_release=lambda x: popup.dismiss())

        popup_layout.add_widget(save_btn)
        popup_layout.add_widget(cancel_btn)

        popup = Popup(title='Добавить пароль' if mode == 'add' else 'Редактировать пароль',
                      content=popup_layout, size_hint=(0.8, 0.5))
        popup.open()

    def add_password(self):
        self.open_password_popup(mode='add')

    def edit_password(self, service, login):
        try:
            url = f'http://127.0.0.1:5000/api/passwords/{self.username}'
            response = requests.get(url)
            if response.status_code != 200:
                self.message = f"Ошибка: {response.text}"
                return

            entry = next((p for p in response.json() if p['service'] == service and p['login'] == login), None)
            if not entry:
                self.message = "Запись не найдена"
                return

            self.open_password_popup(mode='edit', service=service, login=login, password=entry['password'])
        except Exception as e:
            self.message = f"Ошибка: {e}"

    def save_new_password(self, service, login, password):
        try:
            url = 'http://127.0.0.1:5000/api/save_password'
            data = {'username': self.username, 'service': service, 'login': login, 'password': password}
            response = requests.post(url, json=data)
            if response.status_code in (200, 201):
                self.message = "Пароль добавлен"
                self.refresh_passwords()
            else:
                self.message = f"Ошибка: {response.json().get('message')}"
        except Exception as e:
            self.message = f"Ошибка соединения: {e}"

    def update_password(self, old_service, old_login, new_service, new_login, new_password):
        try:
            url = 'http://127.0.0.1:5000/api/update_password'
            data = {
                'username': self.username,
                'old_service': old_service,
                'old_login': old_login,
                'new_service': new_service,
                'new_login': new_login,
                'new_password': new_password
            }
            response = requests.post(url, json=data)
            if response.status_code == 200:
                self.message = "Пароль обновлён"
                self.refresh_passwords()
            else:
                self.message = f"Ошибка обновления: {response.text}"
        except Exception as e:
            self.message = f"Ошибка: {e}"

    def delete_password(self, service, login):
        try:
            url = 'http://127.0.0.1:5000/api/delete_password'
            response = requests.post(url, json={'username': self.username, 'service': service, 'login': login})
            if response.status_code == 200:
                self.message = f"Пароль для {service} удалён"
                self.refresh_passwords()
            else:
                self.message = f"Ошибка удаления: {response.text}"
        except Exception as e:
            self.message = f"Ошибка соединения: {e}"
