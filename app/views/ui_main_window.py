from PySide6.QtWidgets import (QVBoxLayout, QWidget, QPushButton, QTableWidget, QComboBox, QHBoxLayout, QLineEdit,
                               QStackedWidget)

from app.models.database import AccessLevel


# ui_main_window.py
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 800)

        self.centralwidget = QWidget(MainWindow)
        self.verticalLayout = QVBoxLayout(self.centralwidget)

        # Кнопки переключения между таблицами
        self.switch_layout = QHBoxLayout()

        self.btn_components = QPushButton("Комплектующие")
        self.btn_components.setCheckable(True)
        self.btn_components.setChecked(True)
        self.switch_layout.addWidget(self.btn_components)

        self.btn_users = QPushButton("Пользователи")
        self.btn_users.setCheckable(True)
        self.switch_layout.addWidget(self.btn_users)

        self.verticalLayout.addLayout(self.switch_layout)

        # Область для таблиц (будет показываться только одна)
        self.table_stack = QStackedWidget()
        self.verticalLayout.addWidget(self.table_stack)

        # Таблица комплектующих
        self.components_widget = QWidget()
        self.components_layout = QVBoxLayout(self.components_widget)



        # Фильтры для компонентов
        self.filter_layout = QHBoxLayout()
        self.category_filter = QComboBox()
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Поиск по названию...")
        self.filter_layout.addWidget(self.category_filter)
        self.filter_layout.addWidget(self.search_field)
        self.components_layout.addLayout(self.filter_layout)

        self.table_components = QTableWidget()
        self.components_layout.addWidget(self.table_components)
        self.table_stack.addWidget(self.components_widget)

        # Таблица пользователей
        self.users_widget = QWidget()
        self.users_layout = QVBoxLayout(self.users_widget)

        self.table_users = QTableWidget()
        self.users_layout.addWidget(self.table_users)
        self.table_stack.addWidget(self.users_widget)

        # Кнопки управления
        self.button_layout = QHBoxLayout()
        self.button_refresh = QPushButton("Обновить")
        self.button_logout = QPushButton("Выйти")
        self.button_layout.addWidget(self.button_refresh)
        self.button_layout.addWidget(self.button_logout)
        self.verticalLayout.addLayout(self.button_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        ### позьователи
        self.users_control_layout = QHBoxLayout()

        self.combo_access_level = QComboBox()
        self.combo_access_level.addItem("Неподтверждённый", AccessLevel.UNVERIFIED)
        self.combo_access_level.addItem("Работник", AccessLevel.WORKER)
        self.combo_access_level.addItem("Админ", AccessLevel.ADMIN)

        self.btn_update_access = QPushButton("Изменить права")
        self.btn_delete_user = QPushButton("Удалить пользователя")

        self.users_control_layout.addWidget(self.combo_access_level)
        self.users_control_layout.addWidget(self.btn_update_access)
        self.users_control_layout.addWidget(self.btn_delete_user)

        self.users_layout.addLayout(self.users_control_layout)