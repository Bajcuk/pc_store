import sqlalchemy as db
from sqlalchemy import Enum
import bcrypt

engine = db.create_engine('sqlite:///database.db')
connection = engine.connect()
metadata = db.MetaData()


class AccessLevel:
    UNVERIFIED = "Неподтверждённый пользователь"
    WORKER = "Работник"
    ADMIN = "Админ"


users = db.Table('users', metadata,
                 db.Column('user_id', db.Integer, primary_key=True),
                 db.Column('name', db.Text, nullable=False),
                 db.Column('last_name', db.Text, nullable=False),
                 db.Column('login', db.Text, unique=True, nullable=False),
                 db.Column('hashed_password', db.Text, nullable=False),
                 db.Column('access_level', Enum(
                     AccessLevel.UNVERIFIED,
                     AccessLevel.WORKER,
                     AccessLevel.ADMIN,
                     name='access_level_enum'),
                           nullable=False,
                           default=AccessLevel.UNVERIFIED))

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

metadata.create_all(engine)

"""Аутентификация"""

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
        hashed_pwd = hash_password(password)
        query = users.insert().values(
            name=name,
            last_name=last_name,
            login=login,
            hashed_password=hashed_pwd,
            access_level=AccessLevel.UNVERIFIED
        )
        connection.execute(query)
        connection.commit()
        return True
    except Exception as e:
        print(f"Ошибка регистрации: {e}")
        return False

def authenticate_user(login, password):
    query = db.select(users).where(users.c.login == login)
    result = connection.execute(query).fetchone()

    if result and verify_password(password, result.hashed_password):
        return {
            'user_id': result.user_id,
            'name': result.name,
            'last_name': result.last_name,
            'login': result.login,
            'access_level': result.access_level
        }
    return None


"""Таблицы компонентов и категорий"""
def get_components_with_category_name():
    query = db.select(
        components,
        categories.c.name.label("category_name")
    ).select_from(
        components.join(categories)
    )
    return connection.execute(query).fetchall()

def get_categories_with_count():
    query = db.select(
        categories,
        db.func.count(components.c.component_id).label("items_count")
    ).select_from(
        categories.outerjoin(components)
    ).group_by(categories.c.category_id)
    return connection.execute(query).fetchall()


def get_components_by_category(category_id=None):
    query = db.select(
        components,
        categories.c.name.label("category_name")
    ).select_from(
        components.join(categories)
    )

    if category_id:
        query = query.where(components.c.category_id == category_id)

    return connection.execute(query).fetchall()


def search_components_by_name(search_text, category_id=None):
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

    return connection.execute(query).fetchall()

def get_all_categories():
    query = db.select(categories)
    return connection.execute(query).fetchall()

def get_all_components():
    query = db.select(components)
    return connection.execute(query).fetchall()

def add_component(name, description, quantity, price, category_id):
    try:
        query = components.insert().values(
            name=name,
            description=description,
            quantity=quantity,
            price=price,
            category_id=category_id
        )
        connection.execute(query)
        connection.commit()
        return True
    except Exception as e:
        print(f"Ошибка добавления товара: {e}")
        return False

def update_component(component_id, name, description, quantity, price, category_id):
    try:
        query = components.update().where(components.c.component_id == component_id).values(
            name=name,
            description=description,
            quantity=quantity,
            price=price,
            category_id=category_id
        )
        result = connection.execute(query)
        connection.commit()
        return result.rowcount > 0
    except Exception as e:
        print(f"Ошибка обновления товара: {e}")
        return False

def delete_component(component_id):
    try:
        query = components.delete().where(components.c.component_id == component_id)
        result = connection.execute(query)
        connection.commit()
        return result.rowcount > 0
    except Exception as e:
        print(f"Ошибка удаления товара: {e}")
        return False



"""Таблицы пользователей"""
def get_all_users():
    query = db.select(users)
    return connection.execute(query).fetchall()

def update_user_access(user_id, new_access_level):
    try:
        query = users.update().where(users.c.user_id == user_id).values(
            access_level=new_access_level
        )
        result = connection.execute(query)
        connection.commit()
        return result.rowcount > 0
    except Exception as e:
        print(f"Ошибка обновления прав доступа: {e}")
        connection.rollback()
        return False

def delete_user(user_id):
    try:
        query = users.delete().where(users.c.user_id == user_id)
        result = connection.execute(query)
        connection.commit()
        return result.rowcount > 0
    except Exception as e:
        print(f"Ошибка удаления пользователя: {e}")
        connection.rollback()
        return False

def get_users_with_access_level():
    query = db.select(users)
    results = connection.execute(query).fetchall()

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








"""
hashed_pwd=hash_password("1234")

with engine.connect() as conn:
    insertion_query = users.insert().values(
       name="Роман",
       last_name="Байчук",
       login="Admin",
       hashed_password=hashed_pwd,
       access_level=AccessLevel.ADMIN)

    connection.execute(insertion_query)
    connection.commit()
"""

"""
    result = connection.execute(db.select(categories))
    for r in result:
        print(f"{r.category_id} | {r.name} | {r.description} ")"""