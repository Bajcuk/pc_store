from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import (QVBoxLayout, QWidget, QPushButton, QTableWidget, QComboBox,
                               QHBoxLayout, QLineEdit, QTabWidget, QLabel, QInputDialog)


class Ui_ClientWindow(object):
    def setupUi(self, ClientWindow):
        if not ClientWindow.objectName():
            ClientWindow.setObjectName("ClientWindow")
        ClientWindow.resize(1000, 700)

        self.centralwidget = QWidget(ClientWindow)
        self.verticalLayout = QVBoxLayout(self.centralwidget)

        self.tab_widget = QTabWidget()
        self.verticalLayout.addWidget(self.tab_widget)

        # Вкладка Товары
        self.tab_components = QWidget()
        self.components_layout = QVBoxLayout(self.tab_components)

        # Фильтры для товаров
        self.filter_layout = QHBoxLayout()
        self.category_filter = QComboBox()
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Поиск по названию...")
        self.filter_layout.addWidget(QLabel("Категория:"))
        self.filter_layout.addWidget(self.category_filter)
        self.filter_layout.addWidget(QLabel("Поиск:"))
        self.filter_layout.addWidget(self.search_field)
        self.filter_layout.addStretch()
        self.components_layout.addLayout(self.filter_layout)

        # Таблица товаров
        self.table_components = QTableWidget()
        self.components_layout.addWidget(self.table_components)

        # Кнопка добавления в корзину
        self.component_buttons_layout = QHBoxLayout()
        self.button_add_to_cart = QPushButton("Добавить в корзину")
        self.component_buttons_layout.addStretch()
        self.component_buttons_layout.addWidget(self.button_add_to_cart)
        self.components_layout.addLayout(self.component_buttons_layout)

        self.tab_widget.addTab(self.tab_components, "Товары")

        # Вкладка Корзина
        self.tab_cart = QWidget()
        self.cart_layout = QVBoxLayout(self.tab_cart)

        # Информация о корзине
        self.cart_info_layout = QHBoxLayout()
        self.label_cart_total = QLabel("Итого: 0.00 ₽")
        self.label_cart_total.setStyleSheet("font-size: 14pt; font-weight: bold;")
        self.cart_info_layout.addWidget(self.label_cart_total)
        self.cart_info_layout.addStretch()
        self.cart_layout.addLayout(self.cart_info_layout)

        # Таблица корзины
        self.table_cart = QTableWidget()
        self.cart_layout.addWidget(self.table_cart)

        # Кнопки управления корзиной
        self.cart_buttons_layout = QHBoxLayout()
        self.button_remove_from_cart = QPushButton("Удалить из корзины")
        self.button_clear_cart = QPushButton("Очистить корзину")
        self.button_create_order = QPushButton("Оформить заказ")
        self.button_create_order.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")

        self.cart_buttons_layout.addWidget(self.button_remove_from_cart)
        self.cart_buttons_layout.addWidget(self.button_clear_cart)
        self.cart_buttons_layout.addStretch()
        self.cart_buttons_layout.addWidget(self.button_create_order)
        self.cart_layout.addLayout(self.cart_buttons_layout)

        self.tab_widget.addTab(self.tab_cart, "Корзина")

        # Вкладка Мои заказы
        self.tab_orders = QWidget()
        self.orders_layout = QVBoxLayout(self.tab_orders)

        self.table_orders = QTableWidget()
        self.orders_layout.addWidget(self.table_orders)

        self.tab_widget.addTab(self.tab_orders, "Мои заказы")

        # Кнопки управления
        self.button_layout = QHBoxLayout()
        self.button_refresh = QPushButton("Обновить")
        self.button_logout = QPushButton("Выйти")

        self.button_layout.addWidget(self.button_refresh)
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.button_logout)
        self.verticalLayout.addLayout(self.button_layout)

        ClientWindow.setCentralWidget(self.centralwidget)