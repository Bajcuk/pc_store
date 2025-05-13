from PySide6.QtWidgets import QMainWindow
from app.views.ui_unverified_window import Ui_UnverifiedWindow


class UnverifiedWindow(QMainWindow):
    def __init__(self, login_window):
        super().__init__()
        self.ui = Ui_UnverifiedWindow()
        self.ui.setupUi(self)
        self.login_window = login_window


        self.ui.btn_logout.clicked.connect(self.logout)

    def logout(self):
        self.close()
        self.login_window.show()