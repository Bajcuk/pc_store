from PySide6.QtWidgets import QMainWindow, QMessageBox
from app.views.ui_register_window import Ui_RegisterWindow
from app.models.database import register_user


class RegisterWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_RegisterWindow()
        self.ui.setupUi(self)
        self.ui.line_name.setFocus()
        self.ui.button_register.clicked.connect(self.attempt_register)

        self.ui.line_name.returnPressed.connect(lambda: self.ui.line_last_name.setFocus())
        self.ui.line_last_name.returnPressed.connect(lambda: self.ui.line_login.setFocus())
        self.ui.line_login.returnPressed.connect(lambda: self.ui.line_password.setFocus())
        self.ui.line_password.returnPressed.connect(lambda: self.ui.line_password_confirm.setFocus())
        self.ui.line_password_confirm.returnPressed.connect(self.attempt_register)

    def attempt_register(self):
        name = self.ui.line_name.text().strip()
        last_name = self.ui.line_last_name.text().strip()
        login = self.ui.line_login.text().strip()
        password = self.ui.line_password.text().strip()
        password2 = self.ui.line_password_confirm.text().strip()

        if not all([name, last_name, login, password, password2]):
            self.ui.label_status.setText("Заполните все поля")
            return

        if password != password2:
            self.ui.label_status.setText("Пароли не совпадают")
            return

        if register_user(name, last_name, login, password):
            QMessageBox.information(self, "Успех", "Регистрация прошла успешно")
            self.close()
        else:
            self.ui.label_status.setText("Логин уже используется")

