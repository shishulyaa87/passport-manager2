from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.app import App
from kivy.core.clipboard import Clipboard
import random
import string

class GeneratorScreen(Screen):
    length = NumericProperty(12)
    use_uppercase = BooleanProperty(True)
    use_digits = BooleanProperty(True)
    use_symbols = BooleanProperty(True)
    generated_password = StringProperty("")
    status_message = StringProperty("")

    def generate(self):
        try:
            self.length = int(self.ids.length_input.text)
        except ValueError:
            self.status_message = "Введите число"
            return

        chars = string.ascii_lowercase
        if self.use_uppercase:
            chars += string.ascii_uppercase
        if self.use_digits:
            chars += string.digits
        if self.use_symbols:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?/"

        if not chars:
            self.generated_password = ""
            self.status_message = "Выберите символы"
            return

        if self.length < 1 or self.length > 128:
            self.generated_password = ""
            self.status_message = "Длина 1-128"
            return

        self.generated_password = ''.join(random.choices(chars, k=self.length))
        self.status_message = "Готово!"

    def copy_to_clipboard(self):
        if not self.generated_password:
            self.status_message = "Нет пароля"
            return
            
        Clipboard.copy(self.generated_password)
        self.status_message = "Скопировано!"
