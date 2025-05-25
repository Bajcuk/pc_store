from PySide6.QtWidgets import QMainWindow, QMessageBox
from app.views.ui_login_window import Ui_login_window
from app.controllers.main_window import MainWindow
from app.controllers.client_window import ClientWindow
from app.controllers.register_window import RegisterWindow
from app.models.database import register_user, authenticate_user, AccessLevel


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_login_window()
        self.ui.setupUi(self)
        self.ui.line_login.setFocus()

        self.setup_connections()
        self.main_window = None
        self.client_window = None
        self.register_window = None

    def setup_connections(self):
        self.ui.button_sign_in.clicked.connect(self.authenticate)
        self.ui.button_sign_up.clicked.connect(self.show_register_window)

        self.ui.line_login.returnPressed.connect(self.focus_password)
        self.ui.line_password.returnPressed.connect(self.authenticate)

    def authenticate(self):
        login = self.ui.line_login.text().strip()
        password = self.ui.line_password.text().strip()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return

        user = authenticate_user(login, password)
        if user:
            if user['access_level'] == AccessLevel.CLIENT:
                self.show_client_window(user)
            else:
                self.show_main_window(user)
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def show_client_window(self, user_data):
        self.client_window = ClientWindow(self, user_data)
        self.hide()
        self.client_window.show()

    def show_main_window(self, user_data):
        self.main_window = MainWindow(self, user_data)
        self.hide()
        self.main_window.show()

    def show_register_window(self):
        if not self.register_window:
            self.register_window = RegisterWindow(self)
        self.register_window.show()

    def focus_password(self):
        self.ui.line_password.setFocus()
