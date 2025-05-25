from PySide6.QtWidgets import (QVBoxLayout, QWidget, QPushButton, QTableWidget, QComboBox,
                               QHBoxLayout, QLineEdit, QTabWidget, QLabel)

from app.models.database import AccessLevel, OrderStatus

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)

        self.centralwidget = QWidget(MainWindow)
        self.verticalLayout = QVBoxLayout(self.centralwidget)

        self.tab_widget = QTabWidget()
        self.verticalLayout.addWidget(self.tab_widget)

        # Вкладка Комплектующие
        self.tab_components = QWidget()
        self.components_layout = QVBoxLayout(self.tab_components)

        self.filter_layout = QHBoxLayout()
        self.category_filter = QComboBox()
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Поиск по названию...")
        self.filter_layout.addWidget(self.category_filter)
        self.filter_layout.addWidget(self.search_field)
        self.components_layout.addLayout(self.filter_layout)

        self.table_components = QTableWidget()
        self.components_layout.addWidget(self.table_components)

        self.tab_widget.addTab(self.tab_components, "Комплектующие")

        # Вкладка Пользователи
        self.tab_users = QWidget()
        self.users_layout = QVBoxLayout(self.tab_users)

        self.table_users = QTableWidget()
        self.users_layout.addWidget(self.table_users)

        self.users_control_layout = QHBoxLayout()
        self.combo_access_level = QComboBox()
        self.combo_access_level.addItem("Клиент", AccessLevel.CLIENT)  # Добавить эту строку
        self.combo_access_level.addItem("Работник", AccessLevel.WORKER)
        self.combo_access_level.addItem("Админ", AccessLevel.ADMIN)
        self.btn_update_access = QPushButton("Изменить права")
        self.btn_delete_user = QPushButton("Удалить пользователя")

        self.users_control_layout.addWidget(self.combo_access_level)
        self.users_control_layout.addWidget(self.btn_update_access)
        self.users_control_layout.addWidget(self.btn_delete_user)

        self.users_layout.addLayout(self.users_control_layout)

        self.tab_widget.addTab(self.tab_users, "Пользователи")

        # Вкладка Заказы
        self.tab_orders = QWidget()
        self.orders_layout = QVBoxLayout(self.tab_orders)

        self.table_orders = QTableWidget()
        self.orders_layout.addWidget(self.table_orders)

        # Управление заказами
        self.orders_control_layout = QHBoxLayout()
        self.combo_order_status = QComboBox()
        self.combo_order_status.addItem(OrderStatus.ASSEMBLING)
        self.combo_order_status.addItem(OrderStatus.READY)
        self.combo_order_status.addItem(OrderStatus.ISSUED)
        self.btn_update_order_status = QPushButton("Изменить статус")

        self.orders_control_layout.addWidget(QLabel("Новый статус:"))
        self.orders_control_layout.addWidget(self.combo_order_status)
        self.orders_control_layout.addWidget(self.btn_update_order_status)
        self.orders_control_layout.addStretch()

        self.orders_layout.addLayout(self.orders_control_layout)

        self.tab_widget.addTab(self.tab_orders, "Заказы")


        # Кнопки управления
        self.button_layout = QHBoxLayout()
        self.button_add = QPushButton("Добавить")
        self.button_edit = QPushButton("Редактировать")
        self.button_delete = QPushButton("Удалить")
        self.button_refresh = QPushButton("Обновить")
        self.button_logout = QPushButton("Выйти")
        self.button_export = QPushButton("Экспорт в Excel")

        self.button_layout.addWidget(self.button_refresh)
        self.button_layout.addWidget(self.button_add)
        self.button_layout.addWidget(self.button_edit)
        self.button_layout.addWidget(self.button_delete)
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.button_export)
        self.button_layout.addWidget(self.button_logout)
        self.verticalLayout.addLayout(self.button_layout)
        MainWindow.setCentralWidget(self.centralwidget)
