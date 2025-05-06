import sys
from datetime import datetime, timedelta
from sqlalchemy import create_engine, MetaData, Table, select, insert
from sqlalchemy.orm import sessionmaker

# СТРОКА ПОДКЛЮЧЕНИЯ
DB_URL = "postgresql+psycopg2://Zona:qwerty@localhost:5432/Hotel_db"

# --- SQLAlchemy engine и сессия ---
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()

try:
    # Загружаем существующие таблицы
    guests_table = Table('guests', metadata, autoload_with=engine)
    rooms_table = Table('rooms', metadata, autoload_with=engine)
    room_categories_table = Table('roomcategories', metadata, autoload_with=engine)
    bookings_table = Table('bookings', metadata, autoload_with=engine)
    
    print("Заполнение тестовыми данными началось...")
    
    # 1. Добавляем категории номеров (если их нет)
    existing_categories = session.execute(select(room_categories_table)).fetchall()
    if not existing_categories:
        print("Добавление категорий номеров...")
        categories = [
            {"name": "Стандарт", "description": "Стандартный номер с одной двуспальной кроватью", "baseprice": 2500.00},
            {"name": "Люкс", "description": "Просторный номер с гостиной и спальней", "baseprice": 5000.00},
            {"name": "Семейный", "description": "Номер с двумя спальнями для семейного отдыха", "baseprice": 4000.00},
            {"name": "Бизнес", "description": "Номер с рабочей зоной для деловых поездок", "baseprice": 3500.00},
        ]
        for category in categories:
            session.execute(room_categories_table.insert().values(**category))
        session.commit()
    
    # Получаем ID категорий
    category_ids = {row.name: row.categoryid for row in session.execute(select(room_categories_table.c.categoryid, room_categories_table.c.name))}
    
    # 2. Добавляем номера (если их нет)
    existing_rooms = session.execute(select(rooms_table)).fetchall()
    if not existing_rooms:
        print("Добавление номеров...")
        rooms = [
            {"roomnumber": "101", "categoryid": category_ids["Стандарт"]},
            {"roomnumber": "102", "categoryid": category_ids["Стандарт"]},
            {"roomnumber": "103", "categoryid": category_ids["Стандарт"]},
            {"roomnumber": "201", "categoryid": category_ids["Люкс"]},
            {"roomnumber": "202", "categoryid": category_ids["Люкс"]},
            {"roomnumber": "301", "categoryid": category_ids["Семейный"]},
            {"roomnumber": "302", "categoryid": category_ids["Семейный"]},
            {"roomnumber": "401", "categoryid": category_ids["Бизнес"]},
            {"roomnumber": "402", "categoryid": category_ids["Бизнес"]},
        ]
        for room in rooms:
            session.execute(rooms_table.insert().values(**room))
        session.commit()
    
    # 3. Добавляем гостей (если их нет)
    existing_guests = session.execute(select(guests_table)).fetchall()
    if not existing_guests:
        print("Добавление гостей...")
        guests = [
            {
                "lastname": "Иванов", 
                "firstname": "Иван", 
                "middlename": "Иванович",
                "dateofbirth": "1985-05-15",
                "placeofbirth": "Москва",
                "passportseries": "1234", 
                "passportnumber": "567890",
                "phone": "+7 (900) 123-45-67",
                "email": "ivanov@example.com"
            },
            {
                "lastname": "Петров", 
                "firstname": "Петр", 
                "middlename": "Петрович",
                "dateofbirth": "1990-10-20",
                "placeofbirth": "Санкт-Петербург",
                "passportseries": "2345", 
                "passportnumber": "678901",
                "phone": "+7 (900) 234-56-78",
                "email": "petrov@example.com"
            },
            {
                "lastname": "Сидорова", 
                "firstname": "Анна", 
                "middlename": "Михайловна",
                "dateofbirth": "1988-07-10",
                "placeofbirth": "Казань",
                "passportseries": "3456", 
                "passportnumber": "789012",
                "phone": "+7 (900) 345-67-89",
                "email": "sidorova@example.com"
            },
            {
                "lastname": "Козлов", 
                "firstname": "Алексей", 
                "middlename": "Сергеевич",
                "dateofbirth": "1980-03-25",
                "placeofbirth": "Новосибирск",
                "passportseries": "4567", 
                "passportnumber": "890123",
                "phone": "+7 (900) 456-78-90",
                "email": "kozlov@example.com"
            },
            {
                "lastname": "Смирнова", 
                "firstname": "Ольга", 
                "middlename": "Александровна",
                "dateofbirth": "1995-12-05",
                "placeofbirth": "Екатеринбург",
                "passportseries": "5678", 
                "passportnumber": "901234",
                "phone": "+7 (900) 567-89-01",
                "email": "smirnova@example.com"
            }
        ]
        for guest in guests:
            session.execute(guests_table.insert().values(**guest))
        session.commit()
    
    # Получаем ID гостей
    guest_ids = [row.guestid for row in session.execute(select(guests_table.c.guestid))]
    
    # 4. Добавляем бронирования
    existing_bookings = session.execute(select(bookings_table)).fetchall()
    if not existing_bookings or len(existing_bookings) < 10:  # Если бронирований мало или их нет
        print("Добавление бронирований...")
        
        # Проверяем, есть ли столбец totalamount в таблице bookings
        has_totalamount = False
        for column in bookings_table.columns:
            if column.name == 'totalamount':
                has_totalamount = True
                break
        
        # Даты для бронирований (за последние 60 дней и на 30 дней вперед)
        today = datetime.now().date()
        date_range = [(today - timedelta(days=60-i)) for i in range(90)]
        
        # Создаем тестовые бронирования
        for i in range(20):  # Создаем 20 бронирований
            guest_id = guest_ids[i % len(guest_ids)]  # Циклически выбираем гостей
            start_date = date_range[i % len(date_range)]
            
            # Создаем бронирование на 1-7 дней
            stay_length = (i % 7) + 1
            end_date = start_date + timedelta(days=stay_length)
            
            # Статус бронирования
            statuses = ["Новое", "Подтверждено", "Отменено", "Завершено"]
            status = statuses[i % len(statuses)]
            
            # Выбираем категорию
            category_id = list(category_ids.values())[i % len(category_ids)]
            
            # Создаем базовое бронирование
            booking_data = {
                "clientid": guest_id,
                "bookingdate": start_date - timedelta(days=10),  # Бронирование было сделано за 10 дней
                "checkindate": start_date,
                "checkoutdate": end_date,
                "categoryid": category_id,
                "status": status
            }
            
            # Добавляем totalamount, если такой столбец существует
            if has_totalamount:
                # Вычисляем примерную стоимость
                category_price = next((row.baseprice for row in session.execute(
                    select(room_categories_table.c.baseprice)
                    .where(room_categories_table.c.categoryid == category_id)
                )), 2000)
                booking_data["totalamount"] = category_price * stay_length
            
            # Вставляем данные
            session.execute(bookings_table.insert().values(**booking_data))
        
        session.commit()
    
    print("Тестовые данные успешно добавлены!")

except Exception as e:
    print(f"Ошибка при заполнении базы данных: {e}")
    session.rollback()
finally:
    session.close() 