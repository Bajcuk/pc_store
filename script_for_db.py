"""
Скрипт для заполнения базы данных тестовыми данными
Создает категории и комплектующие для компьютерного магазина
"""

import random
from app.models.database import (
    init_db, get_connection, categories, components,
    temp_db_connection, DatabaseManager
)
import sqlalchemy as db

# Данные для заполнения
CATEGORIES_DATA = [
    {"name": "Процессоры", "description": "Центральные процессоры для компьютеров"},
    {"name": "Материнские платы", "description": "Основные платы для сборки ПК"},
    {"name": "Оперативная память", "description": "Модули ОЗУ различных типов и объемов"},
    {"name": "Видеокарты", "description": "Графические адаптеры для игр и работы"},
    {"name": "Жесткие диски", "description": "HDD и SSD накопители для хранения данных"},
    {"name": "Блоки питания", "description": "Источники питания для компьютеров"},
    {"name": "Корпуса", "description": "Корпуса для сборки компьютеров"},
    {"name": "Системы охлаждения", "description": "Кулеры и системы водяного охлаждения"},
    {"name": "Периферия", "description": "Клавиатуры, мыши, мониторы и другие устройства"},
    {"name": "Сетевое оборудование", "description": "Роутеры, сетевые карты, кабели"}
]

COMPONENTS_DATA = {
    "Процессоры": [
        {"name": "Intel Core i9-13900K", "description": "24-ядерный процессор с частотой 3.0 ГГц", "price": 45000,
         "quantity": 15},
        {"name": "AMD Ryzen 9 7950X", "description": "16-ядерный процессор с частотой 4.5 ГГц", "price": 52000,
         "quantity": 12},
        {"name": "Intel Core i7-13700K", "description": "16-ядерный процессор с частотой 3.4 ГГц", "price": 35000,
         "quantity": 20},
        {"name": "AMD Ryzen 7 7800X3D", "description": "8-ядерный игровой процессор", "price": 38000, "quantity": 18},
        {"name": "Intel Core i5-13600K", "description": "14-ядерный процессор среднего класса", "price": 25000,
         "quantity": 25},
        {"name": "AMD Ryzen 5 7600X", "description": "6-ядерный процессор для игр", "price": 22000, "quantity": 30},
        {"name": "Intel Core i3-13100", "description": "4-ядерный бюджетный процессор", "price": 12000, "quantity": 40},
        {"name": "AMD Ryzen 3 4300G", "description": "4-ядерный процессор с встроенной графикой", "price": 8000,
         "quantity": 35},
        {"name": "Intel Core i9-12900K", "description": "16-ядерный процессор предыдущего поколения", "price": 40000,
         "quantity": 10},
        {"name": "AMD Ryzen 9 5950X", "description": "16-ядерный процессор AM4", "price": 35000, "quantity": 8},
    ],

    "Материнские платы": [
        {"name": "ASUS ROG STRIX Z790-E", "description": "Игровая материнская плата Intel Z790", "price": 28000,
         "quantity": 12},
        {"name": "MSI MAG B650 TOMAHAWK", "description": "Материнская плата AMD B650", "price": 18000, "quantity": 15},
        {"name": "Gigabyte AORUS X670E MASTER", "description": "Премиальная плата AMD X670E", "price": 45000,
         "quantity": 8},
        {"name": "ASRock B550M PRO4", "description": "Компактная плата формата mATX", "price": 8500, "quantity": 25},
        {"name": "ASUS PRIME B550-PLUS", "description": "Базовая плата для AMD Ryzen", "price": 12000, "quantity": 20},
        {"name": "MSI B450 GAMING PLUS MAX", "description": "Игровая плата с поддержкой Ryzen 5000", "price": 7500,
         "quantity": 30},
        {"name": "Gigabyte H610M H", "description": "Бюджетная плата Intel H610", "price": 5500, "quantity": 35},
        {"name": "ASUS TUF GAMING B550M-PLUS", "description": "Защищенная плата mATX", "price": 11000, "quantity": 18},
        {"name": "MSI PRO Z690-A", "description": "Профессиональная плата Intel Z690", "price": 16000, "quantity": 14},
        {"name": "ASRock X570 PHANTOM GAMING 4", "description": "Игровая плата AMD X570", "price": 13500,
         "quantity": 16},
    ],

    "Оперативная память": [
        {"name": "Corsair Vengeance LPX 32GB DDR4-3200", "description": "Комплект из 2 модулей по 16GB", "price": 9500,
         "quantity": 22},
        {"name": "G.SKILL Trident Z5 RGB 32GB DDR5-6000", "description": "RGB память DDR5 высокой производительности",
         "price": 18000, "quantity": 15},
        {"name": "Kingston FURY Beast 16GB DDR4-3200", "description": "Игровая память 16GB", "price": 4500,
         "quantity": 40},
        {"name": "Crucial Ballistix 16GB DDR4-3600", "description": "Высокочастотная память для разгона", "price": 5200,
         "quantity": 35},
        {"name": "Corsair Dominator Platinum RGB 64GB DDR4-3200", "description": "Премиальная память большого объема",
         "price": 32000, "quantity": 6},
        {"name": "G.SKILL Ripjaws V 8GB DDR4-2400", "description": "Бюджетная память 8GB", "price": 2800,
         "quantity": 50},
        {"name": "Samsung M378A1K43CB2-CRC 8GB DDR4-2400", "description": "OEM память Samsung", "price": 2500,
         "quantity": 45},
        {"name": "HyperX Predator 16GB DDR4-4000", "description": "Высокочастотная игровая память", "price": 6800,
         "quantity": 25},
        {"name": "Corsair Vengeance RGB Pro 16GB DDR4-3600", "description": "RGB память с подсветкой", "price": 6200,
         "quantity": 30},
        {"name": "G.SKILL Trident Z Neo 32GB DDR4-3600", "description": "Оптимизированная для AMD Ryzen",
         "price": 12500, "quantity": 18},
    ],

    "Видеокарты": [
        {"name": "NVIDIA GeForce RTX 4090", "description": "Топовая видеокарта 24GB GDDR6X", "price": 140000,
         "quantity": 5},
        {"name": "AMD Radeon RX 7900 XTX", "description": "Флагманская видеокарта AMD 24GB", "price": 85000,
         "quantity": 8},
        {"name": "NVIDIA GeForce RTX 4070 Ti", "description": "Высокопроизводительная карта 12GB", "price": 65000,
         "quantity": 12},
        {"name": "AMD Radeon RX 7700 XT", "description": "Игровая видеокарта 12GB GDDR6", "price": 42000,
         "quantity": 15},
        {"name": "NVIDIA GeForce RTX 4060", "description": "Карта среднего класса 8GB", "price": 32000, "quantity": 20},
        {"name": "AMD Radeon RX 6600", "description": "Бюджетная игровая карта 8GB", "price": 18000, "quantity": 25},
        {"name": "NVIDIA GeForce GTX 1660 Super", "description": "Популярная карта 6GB GDDR6", "price": 15000,
         "quantity": 30},
        {"name": "AMD Radeon RX 580 8GB", "description": "Проверенная временем карта", "price": 12000, "quantity": 18},
        {"name": "NVIDIA GeForce RTX 3060", "description": "Карта для 1080p игр 12GB", "price": 28000, "quantity": 22},
        {"name": "AMD Radeon RX 7600", "description": "Новая карта начального уровня", "price": 24000, "quantity": 28},
    ],

    "Жесткие диски": [
        {"name": "Samsung 980 PRO 1TB NVMe SSD", "description": "Быстрый SSD M.2 для игр", "price": 8500,
         "quantity": 30},
        {"name": "WD Black SN850X 2TB NVMe SSD", "description": "Игровой SSD высокой производительности",
         "price": 16000, "quantity": 18},
        {"name": "Crucial MX4 1TB SATA SSD", "description": "Надежный SATA SSD", "price": 6200, "quantity": 35},
        {"name": "Seagate Barracuda 2TB HDD", "description": "Жесткий диск для хранения данных", "price": 4500,
         "quantity": 40},
        {"name": "WD Blue 1TB HDD", "description": "Надежный HDD для повседневных задач", "price": 3200,
         "quantity": 45},
        {"name": "Kingston NV2 500GB NVMe SSD", "description": "Бюджетный M.2 SSD", "price": 3800, "quantity": 50},
        {"name": "Samsung 970 EVO Plus 500GB", "description": "Популярный M.2 SSD", "price": 5500, "quantity": 38},
        {"name": "Toshiba P300 3TB HDD", "description": "Объемный диск для хранения", "price": 6800, "quantity": 25},
        {"name": "ADATA XPG SX8200 Pro 1TB", "description": "Производительный M.2 SSD", "price": 7200, "quantity": 28},
        {"name": "WD Red Plus 4TB NAS HDD", "description": "Диск для сетевых хранилищ", "price": 9500, "quantity": 15},
    ],

    "Блоки питания": [
        {"name": "Corsair RM850x 850W 80+ Gold", "description": "Модульный БП высокой эффективности", "price": 12500,
         "quantity": 20},
        {"name": "EVGA SuperNOVA 750 G5 750W", "description": "Полностью модульный БП", "price": 9800, "quantity": 25},
        {"name": "Seasonic Focus GX-650 650W", "description": "Тихий и эффективный БП", "price": 8200, "quantity": 30},
        {"name": "be quiet! Pure Power 11 500W", "description": "Бесшумный БП для офисных ПК", "price": 5500,
         "quantity": 35},
        {"name": "Thermaltake Toughpower GF1 850W", "description": "Игровой БП с RGB подсветкой", "price": 11000,
         "quantity": 18},
        {"name": "Cooler Master MWE Gold 650V2", "description": "Надежный БП среднего класса", "price": 6800,
         "quantity": 32},
        {"name": "FSP Hydro G Pro 750W", "description": "Полумодульный БП", "price": 7500, "quantity": 28},
        {"name": "Chieftec Proton 600W", "description": "Бюджетный БП для базовых систем", "price": 4200,
         "quantity": 40},
        {"name": "Seasonic Prime TX-1000 1000W", "description": "Премиальный БП для мощных систем", "price": 18500,
         "quantity": 8},
        {"name": "be quiet! Straight Power 11 750W", "description": "Профессиональный БП", "price": 9200,
         "quantity": 22},
    ],

    "Корпуса": [
        {"name": "Fractal Design Define 7", "description": "Тихий корпус с отличной вентиляцией", "price": 12000,
         "quantity": 15},
        {"name": "NZXT H7 Flow", "description": "Современный корпус с RGB подсветкой", "price": 9500, "quantity": 20},
        {"name": "Corsair 4000D Airflow", "description": "Популярный корпус среднего размера", "price": 8200,
         "quantity": 25},
        {"name": "be quiet! Pure Base 500DX", "description": "Бесшумный корпус с отличным охлаждением", "price": 7800,
         "quantity": 22},
        {"name": "Cooler Master MasterBox TD500", "description": "Игровой корпус с RGB вентиляторами", "price": 6500,
         "quantity": 28},
        {"name": "Phanteks Eclipse P300A", "description": "Компактный корпус с mesh-панелью", "price": 5200,
         "quantity": 30},
        {"name": "Thermaltake Versa H18", "description": "Бюджетный mATX корпус", "price": 2800, "quantity": 40},
        {"name": "Lian Li PC-O11 Dynamic", "description": "Премиальный корпус для водянки", "price": 14500,
         "quantity": 12},
        {"name": "SilverStone SG13", "description": "Компактный Mini-ITX корпус", "price": 4500, "quantity": 18},
        {"name": "Antec P120 Crystal", "description": "Корпус с закаленным стеклом", "price": 8800, "quantity": 16},
    ],

    "Системы охлаждения": [
        {"name": "Noctua NH-D15", "description": "Премиальный воздушный кулер", "price": 6500, "quantity": 20},
        {"name": "Corsair H100i RGB PLATINUM", "description": "СВО 240мм с RGB подсветкой", "price": 8900,
         "quantity": 15},
        {"name": "be quiet! Dark Rock Pro 4", "description": "Бесшумный башенный кулер", "price": 5800, "quantity": 25},
        {"name": "Arctic Liquid Freezer II 280", "description": "Эффективная СВО 280мм", "price": 7200, "quantity": 18},
        {"name": "Cooler Master Hyper 212 RGB", "description": "Популярный кулер с подсветкой", "price": 3200,
         "quantity": 40},
        {"name": "Deepcool AK620", "description": "Двухбашенный кулер", "price": 4500, "quantity": 30},
        {"name": "NZXT Kraken X63", "description": "СВО с LCD дисплеем", "price": 12000, "quantity": 12},
        {"name": "Scythe Fuma 2", "description": "Тихий и эффективный кулер", "price": 4200, "quantity": 28},
        {"name": "Thermaltake Water 3.0 360", "description": "Трехсекционная СВО", "price": 9800, "quantity": 10},
        {"name": "ID-Cooling SE-224-XT", "description": "Бюджетный башенный кулер", "price": 1800, "quantity": 50},
    ],

    "Периферия": [
        {"name": "Logitech G Pro X Superlight", "description": "Беспроводная игровая мышь", "price": 8500,
         "quantity": 25},
        {"name": "SteelSeries Apex Pro", "description": "Механическая клавиатура", "price": 15000, "quantity": 18},
        {"name": "ASUS ROG Swift PG279QM 27\"", "description": "Игровой монитор 1440p 240Hz", "price": 42000,
         "quantity": 8},
        {"name": "HyperX Cloud Alpha", "description": "Игровая гарнитура", "price": 6500, "quantity": 30},
        {"name": "Razer DeathAdder V3", "description": "Эргономичная игровая мышь", "price": 4200, "quantity": 35},
        {"name": "Corsair K70 RGB MK.2", "description": "Механическая клавиатура с RGB", "price": 9800, "quantity": 22},
        {"name": "BenQ ZOWIE XL2411K 24\"", "description": "Профессиональный игровой монитор", "price": 18000,
         "quantity": 15},
        {"name": "SteelSeries Arctis 7", "description": "Беспроводная гарнитура", "price": 8900, "quantity": 20},
        {"name": "Logitech MX Master 3", "description": "Офисная беспроводная мышь", "price": 5500, "quantity": 28},
        {"name": "HyperX Alloy FPS Pro", "description": "Компактная игровая клавиатура", "price": 6200, "quantity": 25},
    ],

    "Сетевое оборудование": [
        {"name": "ASUS AX6000 RT-AX88U", "description": "Wi-Fi 6 роутер высокого класса", "price": 22000,
         "quantity": 12},
        {"name": "TP-Link Archer AX73", "description": "Двухдиапазонный Wi-Fi 6 роутер", "price": 8500, "quantity": 20},
        {"name": "Netgear Nighthawk AX12", "description": "Игровой Wi-Fi 6E роутер", "price": 28000, "quantity": 8},
        {"name": "Intel Wi-Fi 6E AX210", "description": "Wi-Fi карта PCI-E", "price": 2800, "quantity": 35},
        {"name": "TP-Link TG-3468 Gigabit", "description": "Сетевая карта 1Gb Ethernet", "price": 1200, "quantity": 50},
        {"name": "D-Link DGS-1016A", "description": "16-портовый коммутатор", "price": 3500, "quantity": 15},
        {"name": "Ubiquiti UniFi Dream Machine", "description": "Профессиональный роутер", "price": 35000,
         "quantity": 6},
        {"name": "Mikrotik hAP ac2", "description": "Маршрутизатор для дома/офиса", "price": 4200, "quantity": 18},
        {"name": "Cat6 UTP кабель 305м", "description": "Сетевой кабель витая пара", "price": 8500, "quantity": 10},
        {"name": "Powerline адаптер TP-Link", "description": "Адаптер интернет через розетку", "price": 3200,
         "quantity": 25},
    ]
}


def populate_categories():
    """Заполняет таблицу категорий"""
    conn = get_connection()

    print("Добавление категорий...")
    for category_data in CATEGORIES_DATA:
        try:
            query = categories.insert().values(**category_data)
            conn.execute(query)
            print(f"✓ Добавлена категория: {category_data['name']}")
        except Exception as e:
            print(f"✗ Ошибка при добавлении категории {category_data['name']}: {e}")

    conn.commit()
    print(f"Добавлено категорий: {len(CATEGORIES_DATA)}\n")


def populate_components():
    """Заполняет таблицу комплектующих"""
    conn = get_connection()

    # Получаем ID категорий
    categories_query = db.select(categories)
    categories_result = conn.execute(categories_query).fetchall()

    # Создаем словарь для соответствия названий категорий и их ID
    category_name_to_id = {cat.name: cat.category_id for cat in categories_result}

    print("Добавление комплектующих...")
    total_components = 0

    for category_name, components_list in COMPONENTS_DATA.items():
        if category_name not in category_name_to_id:
            print(f"✗ Категория {category_name} не найдена!")
            continue

        category_id = category_name_to_id[category_name]

        for component_data in components_list:
            try:
                # Добавляем небольшую случайность к количеству товара (±5)
                base_quantity = component_data['quantity']
                random_quantity = base_quantity + random.randint(-5, 5)
                random_quantity = max(0, random_quantity)  # Не меньше 0

                component_insert_data = {
                    **component_data,
                    'category_id': category_id,
                    'quantity': random_quantity
                }

                query = components.insert().values(**component_insert_data)
                conn.execute(query)
                total_components += 1
                print(f"✓ Добавлен товар: {component_data['name']} (кол-во: {random_quantity})")

            except Exception as e:
                print(f"✗ Ошибка при добавлении товара {component_data['name']}: {e}")

    conn.commit()
    print(f"\nВсего добавлено товаров: {total_components}")


def clear_data():
    """Очищает таблицы компонентов и категорий"""
    conn = get_connection()

    print("Очистка существующих данных...")
    try:
        # Сначала удаляем компоненты (из-за внешнего ключа)
        conn.execute(components.delete())
        # Затем категории
        conn.execute(categories.delete())
        conn.commit()
        print("✓ Данные очищены")
    except Exception as e:
        print(f"✗ Ошибка при очистке данных: {e}")
        conn.rollback()


def populate_database(clear_existing=True, db_url='sqlite:///database.db'):
    """Основная функция для заполнения базы данных"""
    print("=== Заполнение базы данных ===")
    print(f"База данных: {db_url}")

    try:
        # Инициализация подключения
        init_db(db_url)

        if clear_existing:
            clear_data()

        # Заполнение данных
        populate_categories()
        populate_components()

        print("=== Заполнение завершено успешно! ===")

        # Статистика
        conn = get_connection()
        categories_count = conn.execute(db.select(db.func.count()).select_from(categories)).scalar()
        components_count = conn.execute(db.select(db.func.count()).select_from(components)).scalar()

        print(f"Итого в базе данных:")
        print(f"- Категорий: {categories_count}")
        print(f"- Товаров: {components_count}")

    except Exception as e:
        print(f"✗ Критическая ошибка: {e}")
        return False

    return True


def populate_with_custom_db(db_url):
    """Заполнение базы данных по указанному URL"""
    db_manager = DatabaseManager(db_url)

    try:
        with db_manager as conn:
            print(f"=== Заполнение базы данных: {db_url} ===")

            # Очистка существующих данных
            print("Очистка существующих данных...")
            conn.execute(components.delete())
            conn.execute(categories.delete())
            conn.commit()

            # Заполнение категорий
            print("\nДобавление категорий...")
            for category_data in CATEGORIES_DATA:
                query = categories.insert().values(**category_data)
                conn.execute(query)
                print(f"✓ {category_data['name']}")
            conn.commit()

            # Получение ID категорий
            categories_result = conn.execute(db.select(categories)).fetchall()
            category_name_to_id = {cat.name: cat.category_id for cat in categories_result}

            # Заполнение компонентов
            print("\nДобавление компонентов...")
            total_components = 0

            for category_name, components_list in COMPONENTS_DATA.items():
                category_id = category_name_to_id[category_name]

                for component_data in components_list:
                    random_quantity = max(0, component_data['quantity'] + random.randint(-5, 5))

                    insert_data = {
                        **component_data,
                        'category_id': category_id,
                        'quantity': random_quantity
                    }

                    query = components.insert().values(**insert_data)
                    conn.execute(query)
                    total_components += 1

            conn.commit()

            print(f"\n✓ Успешно добавлено:")
            print(f"  - Категорий: {len(CATEGORIES_DATA)}")
            print(f"  - Товаров: {total_components}")

            return True

    except Exception as e:
        print(f"✗ Ошибка: {e}")
        return False


if __name__ == "__main__":
    # Заполнение основной базы данных
    success = populate_database(clear_existing=True)

    if success:
        print("\n🎉 База данных успешно заполнена!")
    else:
        print("\n❌ Ошибка при заполнении базы данных")