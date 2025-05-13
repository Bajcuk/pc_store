from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QSpinBox, QComboBox, QPushButton


class EditComponentDialog(QDialog):
    def __init__(self, categories, parent=None, component=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить товар" if not component else "Редактировать товар")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        # Поля формы
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Название")

        self.desc_edit = QLineEdit()
        self.desc_edit.setPlaceholderText("Описание")

        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(0, 9999)

        self.price_edit = QLineEdit()
        self.price_edit.setPlaceholderText("Цена")

        self.category_combo = QComboBox()
        for cat in categories:
            self.category_combo.addItem(cat.name, cat.category_id)

        # Кнопки
        self.save_btn = QPushButton("Сохранить")
        self.cancel_btn = QPushButton("Отмена")

        # Заполняем данные, если редактируем
        if component:
            self.name_edit.setText(component.name)
            self.desc_edit.setText(component.description)
            self.quantity_spin.setValue(component.quantity)
            self.price_edit.setText(str(component.price))
            index = self.category_combo.findData(component.category_id)
            if index >= 0:
                self.category_combo.setCurrentIndex(index)

        # Добавляем элементы в layout
        layout.addWidget(QLabel("Название:"))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("Описание:"))
        layout.addWidget(self.desc_edit)
        layout.addWidget(QLabel("Количество:"))
        layout.addWidget(self.quantity_spin)
        layout.addWidget(QLabel("Цена:"))
        layout.addWidget(self.price_edit)
        layout.addWidget(QLabel("Категория:"))
        layout.addWidget(self.category_combo)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.cancel_btn)

        self.setLayout(layout)

        # Подключение кнопок
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def get_data(self):
        return {
            "name": self.name_edit.text(),
            "description": self.desc_edit.text(),
            "quantity": self.quantity_spin.value(),
            "price": float(self.price_edit.text()),
            "category_id": self.category_combo.currentData()
        }