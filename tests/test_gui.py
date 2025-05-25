import os
import tempfile
import pytest
from PySide6.QtCore import QTimer, Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QMessageBox, QApplication, QDialog
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

    with temp_db_connection(db_url):
        from app.models.database import categories, get_connection
        conn = get_connection()
        conn.execute(categories.insert().values(name="Процессоры", description="CPU компоненты"))
        conn.execute(categories.insert().values(name="Память", description="RAM модули"))
        conn.commit()

    yield db_url

    try:
        os.unlink(temp_file.name)
    except:
        pass


@pytest.fixture
def logged_in_user(qtbot, temp_db):
    """Создает пользователя с админскими правами"""
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

        def click_messagebox_ok():
            for widget in QApplication.topLevelWidgets():
                if isinstance(widget, QMessageBox):
                    ok_button = widget.button(QMessageBox.StandardButton.Ok)
                    if ok_button:
                        QTest.mouseClick(ok_button, qt_api.QtCore.Qt.LeftButton)
                        break

        QTimer.singleShot(100, click_messagebox_ok)
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

        yield main_win, conn


def test_user_registration(qtbot, temp_db):
    """Тест регистрации пользователя"""
    with temp_db_connection(temp_db):
        init_db(temp_db)

        login_win = LoginWindow()
        qtbot.addWidget(login_win)

        login_win.show_register_window()
        reg_win = login_win.register_window
        qtbot.addWidget(reg_win)

        # Заполняем форму регистрации
        reg_win.ui.line_name.setText("Тест")
        reg_win.ui.line_last_name.setText("Пользователь")
        reg_win.ui.line_login.setText("testuser")
        reg_win.ui.line_password.setText("1234")
        reg_win.ui.line_password_confirm.setText("1234")

        def click_messagebox_ok():
            for widget in QApplication.topLevelWidgets():
                if isinstance(widget, QMessageBox):
                    ok_button = widget.button(QMessageBox.StandardButton.Ok)
                    if ok_button:
                        QTest.mouseClick(ok_button, qt_api.QtCore.Qt.LeftButton)
                        break

        QTimer.singleShot(100, click_messagebox_ok)
        qtbot.mouseClick(reg_win.ui.button_register, qt_api.QtCore.Qt.LeftButton)

        # Проверяем, что пользователь создан
        conn = get_connection()
        result = conn.execute(users.select().where(users.c.login == "testuser")).fetchone()
        assert result is not None
        assert result.name == "Тест"
        assert result.last_name == "Пользователь"


def test_user_login(qtbot, temp_db):
    """Тест входа пользователя в систему"""
    with temp_db_connection(temp_db):
        init_db(temp_db)

        # Сначала регистрируем пользователя
        login_win = LoginWindow()
        qtbot.addWidget(login_win)

        login_win.show_register_window()
        reg_win = login_win.register_window
        qtbot.addWidget(reg_win)

        reg_win.ui.line_name.setText("Тест")
        reg_win.ui.line_last_name.setText("Пользователь")
        reg_win.ui.line_login.setText("testuser")
        reg_win.ui.line_password.setText("1234")
        reg_win.ui.line_password_confirm.setText("1234")

        def click_messagebox_ok():
            for widget in QApplication.topLevelWidgets():
                if isinstance(widget, QMessageBox):
                    ok_button = widget.button(QMessageBox.StandardButton.Ok)
                    if ok_button:
                        QTest.mouseClick(ok_button, qt_api.QtCore.Qt.LeftButton)
                        break

        QTimer.singleShot(100, click_messagebox_ok)
        qtbot.mouseClick(reg_win.ui.button_register, qt_api.QtCore.Qt.LeftButton)

        # Теперь тестируем вход
        login_win.ui.line_login.setText("testuser")
        login_win.ui.line_password.setText("1234")
        qtbot.mouseClick(login_win.ui.button_sign_in, qt_api.QtCore.Qt.LeftButton)

        # Проверяем, что главное окно открылось
        assert hasattr(login_win, 'unverified_window')
        assert login_win.unverified_window is not None


def test_edit_component_dialog_creation(qtbot, logged_in_user):
    """Тест создания диалога редактирования компонента"""
    main_win, conn = logged_in_user

    categories = get_all_categories()
    dialog = EditComponentDialog(categories, main_win)
    qtbot.addWidget(dialog)
    dialog.show()
    qtbot.wait(200)

    # Проверяем, что диалог создался правильно
    assert dialog.isVisible()
    assert dialog.category_combo.count() > 0
    assert dialog.name_edit is not None
    assert dialog.desc_edit is not None
    assert dialog.quantity_spin is not None
    assert dialog.price_edit is not None


def test_add_component_workflow(qtbot, logged_in_user):
    """Тест полного процесса добавления компонента"""
    main_win, conn = logged_in_user

    categories = get_all_categories()
    dialog = EditComponentDialog(categories, main_win)
    qtbot.addWidget(dialog)
    dialog.show()
    qtbot.wait(200)

    # Заполняем поля
    dialog.name_edit.setText("Тестовый компонент")
    dialog.desc_edit.setText("Тестовое описание")
    dialog.quantity_spin.setValue(10)
    dialog.price_edit.setText("199.99")
    dialog.category_combo.setCurrentIndex(0)

    # Проверяем данные
    data = dialog.get_data()
    assert data["name"] == "Тестовый компонент"
    assert data["description"] == "Тестовое описание"
    assert data["quantity"] == 10
    assert data["price"] == 199.99
    assert data["category_id"] is not None

    # Сохраняем компонент в базу данных
    from app.models.database import add_component
    success = add_component(**data)
    assert success

    # Проверяем в базе данных
    result = conn.execute(components.select()).fetchall()
    assert len(result) == 1

    component = result[0]
    assert component.name == "Тестовый компонент"
    assert component.description == "Тестовое описание"
    assert component.quantity == 10
    assert float(component.price) == 199.99