import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from app.controllers.login_window import LoginWindow
from app.utils.styles import load_styles
from app.models.database import init_db

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("resources/icons/app_icon.ico"))
    load_styles(app)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())