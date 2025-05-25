from PySide6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QSpinBox, QHeaderView, QInputDialog
from PySide6.QtCore import Qt

from app.views.ui_client_window import Ui_ClientWindow
from app.models.database import (
    get_components_with_category_name,
    get_all_categories,
    create_order,
    get_user_orders,
    get_order_items
)


class ClientWindow(QMainWindow):
    def __init__(self, login_window, user_data):
        super().__init__()
        self.ui = Ui_ClientWindow()
        self.ui.setupUi(self)
        self.login_window = login_window
        self.user_data = user_data
        self.setWindowTitle(f"Магазин ({user_data['name']})")

        self.cart = []  # Корзина товаров
        self.current_category_id = None
        self.current_search_text = ""

        self.load_components()
        self.load_categories()
        self.load_user_orders()
        self.update_cart_display()

        self.setup_connections()

    def setup_connections(self):
        self.ui.category_filter.currentIndexChanged.connect(self.on_category_changed)
        self.ui.search_field.textChanged.connect(self.on_search_changed)
        self.ui.button_refresh.clicked.connect(self.refresh_data)
        self.ui.button_logout.clicked.connect(self.logout)

        # Корзина
        self.ui.button_add_to_cart.clicked.connect(self.add_to_cart)
        self.ui.button_remove_from_cart.clicked.connect(self.remove_from_cart)
        self.ui.button_clear_cart.clicked.connect(self.clear_cart)
        self.ui.button_create_order.clicked.connect(self.create_order)

    def load_categories(self):
        try:
            self.ui.category_filter.clear()
            self.ui.category_filter.addItem("Все категории", None)
            categories = get_all_categories()
            for category in categories:
                self.ui.category_filter.addItem(
                    f"{category.name} ({category.description})", category.category_id
                )
            self.current_category_id = None
            self.ui.category_filter.setCurrentIndex(0)
        except Exception as e:
            print(f"Ошибка загрузки категорий: {e}")
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить список категорий")

    def load_components(self):
        try:
            components = get_components_with_category_name()
            self.ui.table_components.setColumnCount(6)
            self.ui.table_components.setHorizontalHeaderLabels([
                "ID", "Название", "Описание", "Количество", "Цена", "Категория"
            ])
            self.ui.table_components.setRowCount(len(components))

            for row_idx, component in enumerate(components):
                self.ui.table_components.setItem(row_idx, 0, QTableWidgetItem(str(component.component_id)))
                self.ui.table_components.setItem(row_idx, 1, QTableWidgetItem(component.name))
                self.ui.table_components.setItem(row_idx, 2, QTableWidgetItem(component.description))
                self.ui.table_components.setItem(row_idx, 3, QTableWidgetItem(str(component.quantity)))
                self.ui.table_components.setItem(row_idx, 4, QTableWidgetItem(f"{component.price:.2f} ₽"))
                self.ui.table_components.setItem(row_idx, 5, QTableWidgetItem(component.category_name))

                for col in [0, 3, 4]:
                    item = self.ui.table_components.item(row_idx, col)
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            self.ui.table_components.resizeColumnsToContents()
        except Exception as e:
            print(f"Ошибка загрузки товаров: {e}")
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить товары: {e}")

    def load_user_orders(self):
        try:
            orders = get_user_orders(self.user_data['user_id'])
            self.ui.table_orders.setColumnCount(4)
            self.ui.table_orders.setHorizontalHeaderLabels([
                "№ Заказа", "Дата", "Статус", "Сумма"
            ])
            self.ui.table_orders.setRowCount(len(orders))

            for row_idx, order in enumerate(orders):
                self.ui.table_orders.setItem(row_idx, 0, QTableWidgetItem(str(order.order_id)))
                self.ui.table_orders.setItem(row_idx, 1, QTableWidgetItem(order.order_date.strftime("%d.%m.%Y %H:%M")))
                self.ui.table_orders.setItem(row_idx, 2, QTableWidgetItem(order.status))
                self.ui.table_orders.setItem(row_idx, 3, QTableWidgetItem(f"{order.total_price:.2f} ₽"))

                for col in [0, 3]:
                    item = self.ui.table_orders.item(row_idx, col)
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            self.ui.table_orders.resizeColumnsToContents()
        except Exception as e:
            print(f"Ошибка загрузки заказов: {e}")
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить заказы: {e}")

    def on_category_changed(self, index):
        self.current_category_id = self.ui.category_filter.currentData()
        self.apply_filters()

    def on_search_changed(self, text):
        self.current_search_text = text.strip().lower()
        self.apply_filters()

    def apply_filters(self):
        try:
            all_components = get_components_with_category_name()
            filtered = []
            for comp in all_components:
                if (self.current_category_id is None or comp.category_id == self.current_category_id) and \
                        (not self.current_search_text or self.current_search_text in comp.name.lower()):
                    filtered.append(comp)
            self.update_components_table(filtered)
        except Exception as e:
            print(f"Ошибка фильтрации: {e}")
            QMessageBox.warning(self, "Ошибка", "Не удалось применить фильтры")

    def update_components_table(self, components):
        try:
            self.ui.table_components.setRowCount(len(components))
            for row_idx, comp in enumerate(components):
                self.ui.table_components.setItem(row_idx, 0, QTableWidgetItem(str(comp.component_id)))
                self.ui.table_components.setItem(row_idx, 1, QTableWidgetItem(comp.name))
                self.ui.table_components.setItem(row_idx, 2, QTableWidgetItem(comp.description))
                self.ui.table_components.setItem(row_idx, 3, QTableWidgetItem(str(comp.quantity)))
                self.ui.table_components.setItem(row_idx, 4, QTableWidgetItem(f"{comp.price:.2f} ₽"))
                self.ui.table_components.setItem(row_idx, 5, QTableWidgetItem(comp.category_name))

                for col in [0, 3, 4]:
                    item = self.ui.table_components.item(row_idx, col)
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.ui.table_components.resizeColumnsToContents()
        except Exception as e:
            print(f"Ошибка обновления таблицы товаров: {e}")

    def add_to_cart(self):
        try:
            # Проверяем, что выбрана строка
            selected_items = self.ui.table_components.selectedItems()
            if not selected_items:
                QMessageBox.warning(self, "Ошибка", "Выберите товар для добавления в корзину")
                return

            # Получаем номер выбранной строки
            row = selected_items[0].row()

            # Проверяем, что строка существует и содержит данные
            if row < 0 or row >= self.ui.table_components.rowCount():
                QMessageBox.warning(self, "Ошибка", "Неверно выбран товар")
                return

            # Получаем данные из строки с проверкой на None
            component_id_item = self.ui.table_components.item(row, 0)
            name_item = self.ui.table_components.item(row, 1)
            price_item = self.ui.table_components.item(row, 4)
            available_qty_item = self.ui.table_components.item(row, 3)

            if not all([component_id_item, name_item, price_item, available_qty_item]):
                QMessageBox.warning(self, "Ошибка", "Неполные данные о товаре")
                return

            try:
                component_id = int(component_id_item.text())
                name = name_item.text()
                # Убираем символ рубля и пробелы для парсинга цены
                price_text = price_item.text().replace(' ₽', '').replace(',', '.')
                price = float(price_text)
                available_qty = int(available_qty_item.text())
            except (ValueError, AttributeError) as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка в данных товара: {e}")
                return

            # Проверяем наличие товара
            if available_qty <= 0:
                QMessageBox.warning(self, "Ошибка", "Товар отсутствует на складе")
                return

            # Запрашиваем количество у пользователя
            quantity, ok = self.get_quantity_dialog("Добавить в корзину", "Количество:", 1, available_qty)
            if not ok or quantity <= 0:
                return

            # Проверяем, есть ли уже этот товар в корзине
            for item in self.cart:
                if item['component_id'] == component_id:
                    if item['quantity'] + quantity > available_qty:
                        QMessageBox.warning(self, "Ошибка", "Недостаточно товара на складе")
                        return
                    item['quantity'] += quantity
                    break
            else:
                # Добавляем новый товар в корзину
                self.cart.append({
                    'component_id': component_id,
                    'name': name,
                    'price': price,
                    'quantity': quantity
                })

            self.update_cart_display()
            QMessageBox.information(self, "Успех", f"Товар '{name}' добавлен в корзину (количество: {quantity})")

        except Exception as e:
            print(f"Ошибка добавления товара в корзину: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить товар в корзину: {e}")

    def remove_from_cart(self):
        try:
            selected = self.ui.table_cart.selectedItems()
            if not selected:
                QMessageBox.warning(self, "Ошибка", "Выберите товар в корзине для удаления")
                return

            row = selected[0].row()
            if row < 0 or row >= len(self.cart):
                QMessageBox.warning(self, "Ошибка", "Неверно выбран товар в корзине")
                return

            item_name = self.cart[row]['name']

            reply = QMessageBox.question(self, "Подтверждение",
                                         f"Удалить '{item_name}' из корзины?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                del self.cart[row]
                self.update_cart_display()
                QMessageBox.information(self, "Успех", f"Товар '{item_name}' удален из корзины")

        except Exception as e:
            print(f"Ошибка удаления товара из корзины: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить товар из корзины: {e}")

    def clear_cart(self):
        try:
            if not self.cart:
                QMessageBox.information(self, "Информация", "Корзина уже пуста")
                return

            reply = QMessageBox.question(self, "Подтверждение",
                                         "Очистить корзину?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.cart.clear()
                self.update_cart_display()
                QMessageBox.information(self, "Успех", "Корзина очищена")

        except Exception as e:
            print(f"Ошибка очистки корзины: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось очистить корзину: {e}")

    def create_order(self):
        try:
            if not self.cart:
                QMessageBox.warning(self, "Ошибка", "Корзина пуста")
                return

            total = sum(item['price'] * item['quantity'] for item in self.cart)
            reply = QMessageBox.question(self, "Подтверждение заказа",
                                         f"Создать заказ на сумму {total:.2f} ₽?",
                                         QMessageBox.Yes | QMessageBox.No)

            if reply == QMessageBox.Yes:
                order_id = create_order(self.user_data['user_id'], self.cart)
                if order_id:
                    QMessageBox.information(self, "Успех", f"Заказ №{order_id} создан успешно!")
                    self.cart.clear()
                    self.update_cart_display()
                    self.refresh_data()
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось создать заказ")

        except Exception as e:
            print(f"Ошибка создания заказа: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать заказ: {e}")

    def update_cart_display(self):
        try:
            self.ui.table_cart.setColumnCount(4)
            self.ui.table_cart.setHorizontalHeaderLabels([
                "Название", "Цена", "Количество", "Сумма"
            ])
            self.ui.table_cart.setRowCount(len(self.cart))

            total = 0
            for row_idx, item in enumerate(self.cart):
                subtotal = item['price'] * item['quantity']
                total += subtotal

                self.ui.table_cart.setItem(row_idx, 0, QTableWidgetItem(item['name']))
                self.ui.table_cart.setItem(row_idx, 1, QTableWidgetItem(f"{item['price']:.2f} ₽"))
                self.ui.table_cart.setItem(row_idx, 2, QTableWidgetItem(str(item['quantity'])))
                self.ui.table_cart.setItem(row_idx, 3, QTableWidgetItem(f"{subtotal:.2f} ₽"))

                for col in [1, 2, 3]:
                    cart_item = self.ui.table_cart.item(row_idx, col)
                    cart_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            self.ui.table_cart.resizeColumnsToContents()
            self.ui.label_cart_total.setText(f"Итого: {total:.2f} ₽")

        except Exception as e:
            print(f"Ошибка обновления отображения корзины: {e}")

    def get_quantity_dialog(self, title, label, min_val, max_val):
        """Диалог для ввода количества"""
        try:
            quantity, ok = QInputDialog.getInt(
                self,  # parent
                title,  # title
                label,  # label
                1,  # value (default value)
                min_val,  # min
                max_val,  # max
                1  # step
            )
            return quantity, ok
        except Exception as e:
            print(f"Ошибка диалога ввода количества: {e}")
            return 1, False

    def refresh_data(self):
        """Обновить данные"""
        try:
            self.current_category_id = None
            self.current_search_text = ""
            self.ui.search_field.clear()
            self.ui.category_filter.setCurrentIndex(0)
            self.load_categories()
            self.load_components()
            self.load_user_orders()
        except Exception as e:
            print(f"Ошибка обновления данных: {e}")
            QMessageBox.warning(self, "Ошибка", f"Не удалось обновить данные: {e}")

    def logout(self):
        """Выйти из системы"""
        try:
            self.close()
            self.login_window.show()
        except Exception as e:
            print(f"Ошибка выхода из системы: {e}")