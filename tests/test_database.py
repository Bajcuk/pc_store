import pytest
from app.models import database
from app.models.database import (
    init_db, register_user, authenticate_user, hash_password, verify_password,
    add_component, get_all_components, get_all_categories, update_component,
    delete_component, get_all_users, update_user_access, delete_user,
    categories, AccessLevel
)


@pytest.fixture
def test_db():
    original_engine = database.engine
    original_connection = database.connection
    original_metadata = database.metadata

    try:
        init_db('sqlite:///:memory:')

        test_categories = [
            {'name': 'Электроника', 'description': 'Электронные компоненты'},
            {'name': 'Инструменты', 'description': 'Рабочие инструменты'},
            {'name': 'Материалы', 'description': 'Строительные материалы'}
        ]

        for cat in test_categories:
            query = categories.insert().values(**cat)
            database.connection.execute(query)
        database.connection.commit()

        yield database.connection

    finally:
        if database.connection and database.connection != original_connection:
            database.connection.close()
        if database.engine and database.engine != original_engine:
            database.engine.dispose()

        database.engine = original_engine
        database.connection = original_connection
        database.metadata = original_metadata


@pytest.fixture(scope="session", autouse=True)
def isolate_tests():
    original_engine = database.engine
    original_connection = database.connection

    database.engine = None
    database.connection = None

    yield

    database.engine = original_engine
    database.connection = original_connection


class TestAuthentication:
    def test_password_hashing(self):
        password = "test_password_123"
        hashed = hash_password(password)

        assert hashed != password
        assert len(hashed) > 0

        assert verify_password(password, hashed) == True
        assert verify_password("wrong_password", hashed) == False

    def test_user_registration(self, test_db):
        result = register_user("Иван", "Иванов", "ivan123", "password123")
        assert result == True

        all_users = get_all_users()
        assert len(all_users) == 1
        assert all_users[0].name == "Иван"
        assert all_users[0].access_level == AccessLevel.UNVERIFIED

        result = register_user("Петр", "Петров", "ivan123", "password456")
        assert result == False

    def test_user_authentication(self, test_db):
        register_user("Мария", "Сидорова", "maria", "secret123")

        user = authenticate_user("maria", "secret123")
        assert user is not None
        assert user['name'] == "Мария"
        assert user['login'] == "maria"

        assert authenticate_user("maria", "wrong_password") is None
        assert authenticate_user("nonexistent", "password") is None


class TestUserManagement:
    def test_update_user_access(self, test_db):
        register_user("Админ", "Админов", "admin", "admin123")
        users_list = get_all_users()
        user_id = users_list[0].user_id

        result = update_user_access(user_id, AccessLevel.ADMIN)
        assert result == True

        updated_users = get_all_users()
        assert updated_users[0].access_level == AccessLevel.ADMIN

    def test_delete_user(self, test_db):
        register_user("Удаляемый", "Пользователь", "delete_me", "password")
        users_list = get_all_users()
        user_id = users_list[0].user_id

        result = delete_user(user_id)
        assert result == True

        remaining_users = get_all_users()
        assert len(remaining_users) == 0


class TestComponentManagement:
    def test_add_component(self, test_db):
        categories_list = get_all_categories()
        electronics_id = None
        for cat in categories_list:
            if cat.name == 'Электроника':
                electronics_id = cat.category_id
                break

        assert electronics_id is not None, "Категория 'Электроника' не найдена"

        result = add_component(
            name="Резистор 10кОм",
            description="Резистор углеродный 10кОм 0.25Вт",
            quantity=100,
            price=2.50,
            category_id=electronics_id
        )
        assert result == True

        components_list = get_all_components()
        assert len(components_list) == 1
        assert components_list[0].name == "Резистор 10кОм"
        assert components_list[0].quantity == 100

    def test_update_component(self, test_db):
        categories_list = get_all_categories()
        electronics_id = categories_list[0].category_id

        add_component("Тестовый компонент", "Описание", 50, 10.0, electronics_id)
        components_list = get_all_components()
        component_id = components_list[0].component_id

        result = update_component(
            component_id, "Обновлённый компонент", "Новое описание",
            75, 15.0, electronics_id
        )
        assert result == True

        updated_components = get_all_components()
        assert updated_components[0].name == "Обновлённый компонент"
        assert updated_components[0].quantity == 75

    def test_delete_component(self, test_db):
        categories_list = get_all_categories()
        electronics_id = categories_list[0].category_id

        add_component("Удаляемый компонент", "Описание", 10, 5.0, electronics_id)
        components_list = get_all_components()
        component_id = components_list[0].component_id

        result = delete_component(component_id)
        assert result == True

        remaining_components = get_all_components()
        assert len(remaining_components) == 0


class TestWrongCases:
    def test_add_component_invalid_category(self, test_db):
        result = add_component("Тест", "Описание", 10, 5.0, 9999)
        assert result == False

    def test_update_nonexistent_component(self, test_db):
        result = update_component(9999, "Тест", "Описание", 10, 5.0, 1)
        assert result == False

    def test_delete_nonexistent_component(self, test_db):
        result = delete_component(9999)
        assert result == False

    def test_update_nonexistent_user_access(self, test_db):
        result = update_user_access(9999, AccessLevel.ADMIN)
        assert result == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])