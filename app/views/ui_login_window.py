from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QSizePolicy,
    QLineEdit, QWidget)

class Ui_login_window(object):
    def setupUi(self, login_window):
        if not login_window.objectName():
            login_window.setObjectName(u"login_window")
        login_window.setFixedSize(400, 275)
        self.centralwidget = QWidget(login_window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.button_sign_in = QPushButton(self.centralwidget)
        self.button_sign_in.setObjectName(u"button_sign_in")
        self.button_sign_in.setGeometry(QRect(50, 120, 301, 61))
        font = QFont()
        font.setFamilies([u"14pt Constantia"])
        font.setPointSize(20)
        self.button_sign_in.setFont(font)
        self.button_sign_up = QPushButton(self.centralwidget)
        self.button_sign_up.setObjectName(u"button_sign_up")
        self.button_sign_up.setGeometry(QRect(50, 190, 301, 61))
        self.button_sign_up.setFont(font)
        self.line_login = QLineEdit(self.centralwidget)
        self.line_login.setObjectName(u"line_login")
        self.line_login.setGeometry(QRect(60, 20, 281, 41))
        font1 = QFont()
        font1.setFamilies([u"14pt Constantia"])
        font1.setPointSize(16)
        self.line_login.setFont(font1)
        self.line_login.setPlaceholderText("Логин")
        self.line_password = QLineEdit(self.centralwidget)
        self.line_password.setObjectName(u"line_password")
        self.line_password.setGeometry(QRect(60, 70, 281, 41))
        self.line_password.setFont(font1)
        self.line_password.setPlaceholderText("Пароль")
        self.line_password.setEchoMode(QLineEdit.Password)
        login_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(login_window)

        QMetaObject.connectSlotsByName(login_window)
    # setupUi

    def retranslateUi(self, login_window):
        login_window.setWindowTitle(QCoreApplication.translate("login_window", u"Окно входа", None))
        self.button_sign_in.setText(QCoreApplication.translate("login_window", u"\u0412\u0445\u043e\u0434", None))
        self.button_sign_up.setText(QCoreApplication.translate("login_window", u"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f", None))
    # retranslateUi