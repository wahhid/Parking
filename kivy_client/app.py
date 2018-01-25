from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen

class LoginWindow(Widget):

    def login(self, *args):
        username = self.ids.username_input
        username_text = username.text
        password = self.ids.password_input
        password_text = password.text
        if username_text == "test" and password_text == "test":
            label = self.ids.success
            label.text = "Success"

class LatihanApp(App):
    def build(self):
        return LoginWindow()


if __name__ == '__main__':
    LatihanApp().run()