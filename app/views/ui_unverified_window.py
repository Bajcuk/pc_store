from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QLabel,
                               QPushButton)
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication


class Ui_UnverifiedWindow(object):
    def setupUi(self, UnverifiedWindow):
        UnverifiedWindow.setObjectName("UnverifiedWindow")
        UnverifiedWindow.setWindowTitle("Ожидайте подтверждение")
        UnverifiedWindow.setFixedSize(400, 200)

        self.centralwidget = QWidget(UnverifiedWindow)
        self.verticalLayout = QVBoxLayout(self.centralwidget)

        self.label = QLabel("Ваш аккаунт ожидает подтверждения администратором.")
        self.label.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label)

        self.label_info = QLabel("Пожалуйста, подождите, пока администратор подтвердит вашу учетную запись.")
        self.label_info.setAlignment(Qt.AlignCenter)
        self.label_info.setWordWrap(True)
        self.verticalLayout.addWidget(self.label_info)

        self.btn_logout = QPushButton("Выйти")
        self.verticalLayout.addWidget(self.btn_logout)

        UnverifiedWindow.setCentralWidget(self.centralwidget)

        # Центрирование окна
        screen = QGuiApplication.primaryScreen().geometry()
        UnverifiedWindow.move(screen.center() - UnverifiedWindow.rect().center())