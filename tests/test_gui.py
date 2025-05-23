import os
import tempfile
import pytest
from PySide6.QtWidgets import QMessageBox
from pytestqt.qt_compat import qt_api

from app.controllers.login_window import LoginWindow
from app.models.database import init_db, get_connection, temp_db_connection, users, components, AccessLevel
from app.views.ui_edit_component import EditComponentDialog
from app.models.database import get_all_categories

@pytest.fixture
def temp_db():
    """Создаем временную базу данных для тестов"""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_file.close()
    db_url = f'sqlite:///{temp_file.name}'

    # Инициализируем временную БД и добавляем тестовые категории
    with temp_db_connection(db_url):
        from app.models.database import categories, get_connection
        conn = get_connection()
        conn.execute(categories.insert().values(name="Процессоры", description="CPU компоненты"))
        conn.execute(categories.insert().values(name="Память", description="RAM модули"))
        conn.commit()

    yield db_url

    # Очистка
    try:
        os.unlink(temp_file.name)
    except:
        pass


def test_register_login_add_component(qtbot, temp_db):
    # Инициализация с временной БД
    with temp_db_connection(temp_db):
        init_db(temp_db)

        login_win = LoginWindow()
        qtbot.addWidget(login_win)

        # Регистрация
        login_win.show_register_window()
        reg_win = login_win.register_window
        qtbot.addWidget(reg_win)

        reg_win.ui.line_name.setText("Тест")
        reg_win.ui.line_last_name.setText("Пользователь")
        reg_win.ui.line_login.setText("testuser")
        reg_win.ui.line_password.setText("1234")
        reg_win.ui.line_password_confirm.setText("1234")
        qtbot.mouseClick(reg_win.ui.button_register, qt_api.QtCore.Qt.LeftButton)

        # Повышаем уровень доступа
        conn = get_connection()
        conn.execute(users.update().where(users.c.login == "testuser").values(access_level=AccessLevel.ADMIN))
        conn.commit()

        # Вход
        login_win.ui.line_login.setText("testuser")
        login_win.ui.line_password.setText("1234")
        qtbot.mouseClick(login_win.ui.button_sign_in, qt_api.QtCore.Qt.LeftButton)

        main_win = login_win.main_window
        qtbot.addWidget(main_win)

        # Добавление компонента
        qtbot.mouseClick(main_win.ui.button_add, qt_api.QtCore.Qt.LeftButton)
        dialog = EditComponentDialog(get_all_categories(), main_win)
        qtbot.addWidget(dialog)

        dialog.name_edit.setText("Новый компонент")
        dialog.desc_edit.setText("Тестовое описание")
        dialog.quantity_spin.setValue(10)
        dialog.price_edit.setText("199.99")
        dialog.category_combo.setCurrentIndex(0)

        qtbot.mouseClick(dialog.save_btn, qt_api.QtCore.Qt.LeftButton)

        # Проверка добавления
        result = conn.execute(components.select()).fetchall()
        assert any(comp.name == "Новый компонент" for comp in result)
