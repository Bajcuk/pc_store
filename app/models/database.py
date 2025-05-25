import sqlalchemy as db
from sqlalchemy import Enum
import bcrypt
from contextlib import contextmanager
from datetime import datetime

engine = None
connection = None
metadata = db.MetaData()


class AccessLevel:
    CLIENT = "Клиент"
    WORKER = "Работник"
    ADMIN = "Админ"


class OrderStatus:
    ASSEMBLING = "Собирается"
    READY = "Готов к получению"
    ISSUED = "Выдан"


users = db.Table('users', metadata,
                 db.Column('user_id', db.Integer, primary_key=True),
                 db.Column('name', db.Text, nullable=False),
                 db.Column('last_name', db.Text, nullable=False),
                 db.Column('login', db.Text, unique=True, nullable=False),
                 db.Column('hashed_password', db.Text, nullable=False),
                 db.Column('access_level', Enum(
                     AccessLevel.CLIENT,
                     AccessLevel.WORKER,
                     AccessLevel.ADMIN,
                     name='access_level_enum'),
                           nullable=False,
                           default=AccessLevel.CLIENT))

categories = db.Table('categories', metadata,
                      db.Column('category_id', db.Integer, primary_key=True),
                      db.Column('name', db.Text, nullable=False, unique=True),
                      db.Column('description', db.Text))

components = db.Table('components', metadata,
                      db.Column('component_id', db.Integer, primary_key=True),
                      db.Column('name', db.Text),
                      db.Column('description', db.Text),
                      db.Column('quantity', db.Integer),
                      db.Column('price', db.Float),
                      db.Column('category_id', db.Integer, db.ForeignKey('categories.category_id')))

orders = db.Table('orders', metadata,
                  db.Column('order_id', db.Integer, primary_key=True),
                  db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
                  db.Column('order_date', db.DateTime, default=datetime.now),
                  db.Column('status', Enum(
                      OrderStatus.ASSEMBLING,
                      OrderStatus.READY,
                      OrderStatus.ISSUED,
                      name='order_status_enum'),
                            nullable=False,
                            default=OrderStatus.ASSEMBLING),
                  db.Column('total_price', db.Float))

order_items = db.Table('order_items', metadata,
                       db.Column('order_item_id', db.Integer, primary_key=True),
                       db.Column('order_id', db.Integer, db.ForeignKey('orders.order_id')),
                       db.Column('component_id', db.Integer, db.ForeignKey('components.component_id')),
                       db.Column('quantity', db.Integer),
                       db.Column('price', db.Float))


class DatabaseManager:
    def __init__(self, db_url='sqlite:///database.db'):
        self.db_url = db_url
        self.engine = None
        self.connection = None

    def connect(self):
        self.engine = db.create_engine(self.db_url)
        self.connection = self.engine.connect()
        metadata.create_all(self.engine)
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
        if self.engine:
            self.engine.dispose()
            self.engine = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def get_connection():
    if connection is None:
        raise Exception("База данных не инициализирована.")
    return connection


def init_db(db_url='sqlite:///database.db'):
    global engine, connection
    engine = db.create_engine(db_url)
    connection = engine.connect()
    metadata.create_all(engine)


@contextmanager
def temp_db_connection(db_url):
    global engine, connection
    original_engine = engine
    original_connection = connection

    try:
        engine = db.create_engine(db_url)
        connection = engine.connect()
        metadata.create_all(engine)
        yield connection
    finally:
        if connection:
            connection.close()
        if engine:
            engine.dispose()
        engine = original_engine
        connection = original_connection


# Функции аутентификации
def hash_password(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')


def verify_password(plain_password, hashed_password):
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except:
        return False


def register_user(name, last_name, login, password):
    try:
        conn = get_connection()
        hashed_pwd = hash_password(password)
        query = users.insert().values(
            name=name,
            last_name=last_name,
            login=login,
            hashed_password=hashed_pwd,
            access_level=AccessLevel.CLIENT
        )
        conn.execute(query)
        conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка регистрации: {e}")
        return False


def authenticate_user(login, password):
    conn = get_connection()
    query = db.select(users).where(users.c.login == login)
    result = conn.execute(query).fetchone()

    if result and verify_password(password, result.hashed_password):
        return {
            'user_id': result.user_id,
            'name': result.name,
            'last_name': result.last_name,
            'login': result.login,
            'access_level': result.access_level
        }
    return None


# Функции для компонентов и категорий
def get_components_with_category_name():
    conn = get_connection()
    query = db.select(
        components,
        categories.c.name.label("category_name")
    ).select_from(
        components.join(categories)
    )
    return conn.execute(query).fetchall()


def get_categories_with_count():
    conn = get_connection()
    query = db.select(
        categories,
        db.func.count(components.c.component_id).label("items_count")
    ).select_from(
        categories.outerjoin(components)
    ).group_by(categories.c.category_id)
    return conn.execute(query).fetchall()


def get_components_by_category(category_id=None):
    conn = get_connection()
    query = db.select(
        components,
        categories.c.name.label("category_name")
    ).select_from(
        components.join(categories)
    )

    if category_id:
        query = query.where(components.c.category_id == category_id)

    return conn.execute(query).fetchall()


def search_components_by_name(search_text, category_id=None):
    conn = get_connection()
    query = db.select(
        components,
        categories.c.name.label("category_name")
    ).select_from(
        components.join(categories)
    ).where(
        components.c.name.ilike(f"%{search_text}%")
    )

    if category_id:
        query = query.where(components.c.category_id == category_id)

    return conn.execute(query).fetchall()


def get_all_categories():
    conn = get_connection()
    query = db.select(categories)
    return conn.execute(query).fetchall()


def get_all_components():
    conn = get_connection()
    query = db.select(components)
    return conn.execute(query).fetchall()


def add_component(name, description, quantity, price, category_id):
    try:
        conn = get_connection()
        category_exists = conn.execute(
            db.select(categories).where(categories.c.category_id == category_id)
        ).fetchone()
        if not category_exists:
            raise ValueError("Категория не найдена")

        query = components.insert().values(
            name=name,
            description=description,
            quantity=quantity,
            price=price,
            category_id=category_id
        )
        conn.execute(query)
        conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка добавления товара: {e}")
        conn.rollback()
        return False


def update_component(component_id, name, description, quantity, price, category_id):
    try:
        conn = get_connection()
        query = components.update().where(components.c.component_id == component_id).values(
            name=name,
            description=description,
            quantity=quantity,
            price=price,
            category_id=category_id
        )
        result = conn.execute(query)
        conn.commit()
        return result.rowcount > 0
    except Exception as e:
        print(f"Ошибка обновления товара: {e}")
        return False


def delete_component(component_id):
    try:
        conn = get_connection()
        query = components.delete().where(components.c.component_id == component_id)
        result = conn.execute(query)
        conn.commit()
        return result.rowcount > 0
    except Exception as e:
        print(f"Ошибка удаления товара: {e}")
        return False


# Функции работы с пользователями
def get_all_users():
    conn = get_connection()
    query = db.select(users)
    return conn.execute(query).fetchall()


def update_user_access(user_id, new_access_level):
    try:
        conn = get_connection()
        query = users.update().where(users.c.user_id == user_id).values(
            access_level=new_access_level
        )
        result = conn.execute(query)
        conn.commit()
        return result.rowcount > 0
    except Exception as e:
        print(f"Ошибка обновления прав доступа: {e}")
        conn.rollback()
        return False


def delete_user(user_id):
    try:
        conn = get_connection()
        query = users.delete().where(users.c.user_id == user_id)
        result = conn.execute(query)
        conn.commit()
        return result.rowcount > 0
    except Exception as e:
        print(f"Ошибка удаления пользователя: {e}")
        conn.rollback()
        return False


def get_users_with_access_level():
    conn = get_connection()
    query = db.select(users)
    results = conn.execute(query).fetchall()

    users_list = []
    for user in results:
        users_list.append({
            'user_id': user.user_id,
            'name': user.name,
            'last_name': user.last_name,
            'login': user.login,
            'access_level': user.access_level
        })
    return users_list


# Функции для работы с заказами
def create_order(user_id, cart_items):
    try:
        conn = get_connection()

        # Рассчитываем общую стоимость заказа
        total_price = sum(item['price'] * item['quantity'] for item in cart_items)

        # Создаем заказ
        order_query = orders.insert().values(
            user_id=user_id,
            order_date=datetime.now(),
            status=OrderStatus.ASSEMBLING,
            total_price=total_price
        )
        result = conn.execute(order_query)
        order_id = result.inserted_primary_key[0]

        # Добавляем позиции заказа
        for item in cart_items:
            item_query = order_items.insert().values(
                order_id=order_id,
                component_id=item['component_id'],
                quantity=item['quantity'],
                price=item['price']
            )
            conn.execute(item_query)

            # Уменьшаем количество товара на складе
            update_query = components.update().where(
                components.c.component_id == item['component_id']
            ).values(
                quantity=components.c.quantity - item['quantity']
            )
            conn.execute(update_query)

        conn.commit()
        return order_id
    except Exception as e:
        print(f"Ошибка создания заказа: {e}")
        conn.rollback()
        return None


def get_orders_with_user_info():
    conn = get_connection()
    query = db.select(
        orders.c.order_id,
        orders.c.order_date,
        orders.c.status,
        orders.c.total_price,
        users.c.name,
        users.c.last_name
    ).select_from(
        orders.join(users)
    ).order_by(orders.c.order_date.desc())
    return conn.execute(query).fetchall()


def get_user_orders(user_id):
    conn = get_connection()
    query = db.select(orders).where(orders.c.user_id == user_id).order_by(orders.c.order_date.desc())
    return conn.execute(query).fetchall()


def get_order_items(order_id):
    conn = get_connection()
    query = db.select(
        order_items.c.quantity,
        order_items.c.price,
        components.c.name,
        components.c.description
    ).select_from(
        order_items.join(components)
    ).where(order_items.c.order_id == order_id)
    return conn.execute(query).fetchall()

def get_all_orders():
    """Получить все заказы с информацией о пользователях"""
    conn = get_connection()
    query = db.select(
        orders.c.order_id,
        orders.c.order_date,
        orders.c.status,
        orders.c.total_price,
        users.c.name,
        users.c.last_name,
        users.c.login
    ).select_from(
        orders.join(users)
    ).order_by(orders.c.order_date.desc())
    return conn.execute(query).fetchall()

def update_order_status(order_id, new_status):
    try:
        conn = get_connection()
        query = orders.update().where(orders.c.order_id == order_id).values(
            status=new_status
        )
        result = conn.execute(query)
        conn.commit()
        return result.rowcount > 0
    except Exception as e:
        print(f"Ошибка обновления статуса заказа: {e}")
        conn.rollback()
        return False