from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                               QPushButton, QMainWindow)
from PySide6.QtCore import Qt

class Ui_RegisterWindow(object):
    def setupUi(self, RegisterWindow):
        RegisterWindow.setObjectName("RegisterWindow")
        RegisterWindow.setWindowTitle("Регистрация")
        RegisterWindow.setFixedSize(400, 350)

        self.centralwidget = QWidget(RegisterWindow)
        self.layout = QVBoxLayout(self.centralwidget)

        # Поля ввода
        self.label_info = QLabel("Введите данные для регистрации:")
        self.layout.addWidget(self.label_info)

        self.line_name = QLineEdit()
        self.line_name.setPlaceholderText("Имя")
        self.layout.addWidget(self.line_name)

        self.line_last_name = QLineEdit()
        self.line_last_name.setPlaceholderText("Фамилия")
        self.layout.addWidget(self.line_last_name)

        self.line_login = QLineEdit()
        self.line_login.setPlaceholderText("Логин")
        self.layout.addWidget(self.line_login)

        self.line_password = QLineEdit()
        self.line_password.setPlaceholderText("Пароль")
        self.line_password.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.line_password)

        self.line_password_confirm = QLineEdit()
        self.line_password_confirm.setPlaceholderText("Подтвердите пароль")
        self.line_password_confirm.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.line_password_confirm)

        # Кнопка регистрации
        self.button_register = QPushButton("Зарегистрироваться")
        self.layout.addWidget(self.button_register)

        self.label_status = QLabel()
        self.label_status.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_status)

        RegisterWindow.setCentralWidget(self.centralwidget)
