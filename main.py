import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox,
    QTableView, QLineEdit, QLabel, QHeaderView, QMessageBox, QInputDialog, QDialog,
    QRadioButton, QGroupBox, QDateEdit
)
from PyQt5.QtCore import Qt, QAbstractTableModel
from sqlalchemy import create_engine, MetaData, Table, select, or_, func, text, and_
from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime, timedelta

# СТРОКА ПОДКЛЮЧЕНИЯ
DB_URL = "postgresql+psycopg2://Zona:qwerty@localhost:5432/Hotel_db"

# --- SQLAlchemy engine и сессия ---
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()
guests_table = Table('guests', metadata, autoload_with=engine)
rooms_table = Table('rooms', metadata, autoload_with=engine)
room_categories_table = Table('roomcategories', metadata, autoload_with=engine)
services_table = Table('services', metadata, autoload_with=engine)
bookings_table = Table('bookings', metadata, autoload_with=engine)

class ChartsWindow(QDialog):
    """Окно для построения графиков"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Графики")
        self.resize(800, 600)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Верхняя часть с выбором типа графика
        chart_type_group = QGroupBox("Тип графика")
        chart_type_layout = QHBoxLayout()
        
        self.rb_histogram = QRadioButton("Гистограмма")
        self.rb_linear = QRadioButton("Линейный график")
        self.rb_pie = QRadioButton("Круговая диаграмма")
        
        self.rb_histogram.setChecked(True)  # По умолчанию выбрана гистограмма
        
        chart_type_layout.addWidget(self.rb_histogram)
        chart_type_layout.addWidget(self.rb_linear)
        chart_type_layout.addWidget(self.rb_pie)
        chart_type_group.setLayout(chart_type_layout)
        layout.addWidget(chart_type_group)
        
        # Выбор данных для графика
        data_group = QGroupBox("Данные для графика")
        data_layout = QHBoxLayout()
        
        self.rb_room_occupancy = QRadioButton("Заселяемость номеров")
        self.rb_custom = QRadioButton("Статистика по категориям номеров")
        
        self.rb_room_occupancy.setChecked(True)  # По умолчанию выбрана заселяемость
        
        data_layout.addWidget(self.rb_room_occupancy)
        data_layout.addWidget(self.rb_custom)
        data_group.setLayout(data_layout)
        layout.addWidget(data_group)
        
        # Выбор периода
        period_group = QGroupBox("Период")
        period_layout = QHBoxLayout()
        
        period_layout.addWidget(QLabel("От:"))
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(datetime.now().date() - timedelta(days=30))  # По умолчанию 30 дней назад
        period_layout.addWidget(self.date_from)
        
        period_layout.addWidget(QLabel("До:"))
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(datetime.now().date())  # По умолчанию сегодня
        period_layout.addWidget(self.date_to)
        
        period_group.setLayout(period_layout)
        layout.addWidget(period_group)
        
        # Область для отображения графика
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self.btn_generate = QPushButton("Построить график")
        self.btn_generate.clicked.connect(self.generate_chart)
        self.btn_close = QPushButton("Закрыть")
        self.btn_close.clicked.connect(self.close)
        
        buttons_layout.addWidget(self.btn_generate)
        buttons_layout.addWidget(self.btn_close)
        layout.addLayout(buttons_layout)
    
    def generate_chart(self):
        """Генерация и отображение графика на основе выбранных параметров"""
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            # Получаем выбранные даты
            date_from = self.date_from.date().toPyDate()
            date_to = self.date_to.date().toPyDate()
            
            # Построение графика заселяемости номеров
            if self.rb_room_occupancy.isChecked():
                self.plot_room_occupancy(ax, date_from, date_to)
            # Построение графика дохода по категориям номеров
            elif self.rb_custom.isChecked():
                self.plot_revenue_by_category(ax, date_from, date_to)
            
            self.canvas.draw()
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, f"Произошла ошибка: {e}", 
                   horizontalalignment='center', verticalalignment='center')
            self.canvas.draw()
            QMessageBox.critical(self, "Ошибка", f"Ошибка при построении графика: {e}")
    
    def plot_room_occupancy(self, ax, date_from, date_to):
        """Построение графика заселяемости номеров"""
        try:
            # Проверяем, есть ли данные в таблице bookings
            count_check = session.execute(select(func.count()).select_from(bookings_table)).scalar()
            
            if count_check == 0:
                ax.text(0.5, 0.5, "Нет данных в таблице бронирований", 
                       horizontalalignment='center', verticalalignment='center')
                return
                
            # Запрос для получения количества занятых номеров по датам
            query = text("""
                SELECT date_trunc('day', checkindate) as check_date, COUNT(*) as count 
                FROM bookings 
                WHERE checkindate BETWEEN :date_from AND :date_to
                GROUP BY date_trunc('day', checkindate)
                ORDER BY date_trunc('day', checkindate)
            """)
            
            result = session.execute(query, {"date_from": date_from, "date_to": date_to}).fetchall()
            
            if not result:
                ax.text(0.5, 0.5, "Нет данных за выбранный период", 
                       horizontalalignment='center', verticalalignment='center')
                return
            
            dates = [row[0] for row in result]
            counts = [row[1] for row in result]
            
            # В зависимости от выбранного типа графика
            if self.rb_histogram.isChecked():
                ax.bar(dates, counts, width=0.6)
                ax.set_title("Гистограмма заселяемости номеров")
            elif self.rb_linear.isChecked():
                ax.plot(dates, counts, 'o-', linewidth=2)
                ax.set_title("Линейный график заселяемости номеров")
            elif self.rb_pie.isChecked():
                # Для круговой диаграммы сгруппируем данные иначе
                # Получим заселяемость по категориям номеров
                cat_query = text("""
                    SELECT c.name, COUNT(*) as count 
                    FROM bookings b
                    JOIN roomcategories c ON b.categoryid = c.categoryid
                    WHERE b.checkindate BETWEEN :date_from AND :date_to
                    GROUP BY c.name
                """)
                cat_result = session.execute(cat_query, {"date_from": date_from, "date_to": date_to}).fetchall()
                
                if cat_result:
                    labels = [row[0] for row in cat_result]
                    sizes = [row[1] for row in cat_result]
                    ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
                    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
                    ax.set_title("Круговая диаграмма заселяемости по категориям")
                else:
                    ax.text(0.5, 0.5, "Нет данных за выбранный период", 
                           horizontalalignment='center', verticalalignment='center')
            
            ax.set_xlabel("Дата")
            ax.set_ylabel("Количество заселений")
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
            plt.tight_layout()
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            ax.text(0.5, 0.5, f"Ошибка при построении графика: {e}", 
                   horizontalalignment='center', verticalalignment='center')
    
    def plot_revenue_by_category(self, ax, date_from, date_to):
        """Построение графика дохода по категориям номеров"""
        try:
            # Проверяем, есть ли данные в таблице bookings
            count_check = session.execute(select(func.count()).select_from(bookings_table)).scalar()
            
            if count_check == 0:
                ax.text(0.5, 0.5, "Нет данных в таблице бронирований", 
                       horizontalalignment='center', verticalalignment='center')
                return
            
            # Проверяем, есть ли у нас колонка totalamount
            try:
                # Пробуем получить колонку totalamount
                session.execute(select(bookings_table.c.totalamount).limit(1))
                has_totalamount = True
            except Exception:
                has_totalamount = False
                
            if has_totalamount:
                # Запрос для получения дохода по категориям номеров
                query = text("""
                    SELECT c.name, SUM(b.totalamount) as total 
                    FROM bookings b
                    JOIN roomcategories c ON b.categoryid = c.categoryid
                    WHERE b.checkindate BETWEEN :date_from AND :date_to
                    GROUP BY c.name
                    ORDER BY total DESC
                """)
            else:
                # Альтернативный запрос без поля totalamount (просто подсчет количества бронирований)
                query = text("""
                    SELECT c.name, COUNT(*) as count 
                    FROM bookings b
                    JOIN roomcategories c ON b.categoryid = c.categoryid
                    WHERE b.checkindate BETWEEN :date_from AND :date_to
                    GROUP BY c.name
                    ORDER BY count DESC
                """)
            
            result = session.execute(query, {"date_from": date_from, "date_to": date_to}).fetchall()
            
            if not result:
                ax.text(0.5, 0.5, "Нет данных за выбранный период", 
                       horizontalalignment='center', verticalalignment='center')
                return
            
            categories = [row[0] for row in result]
            values = [row[1] if row[1] else 0 for row in result]
            
            y_label = "Доход" if has_totalamount else "Количество бронирований"
            
            # В зависимости от выбранного типа графика
            if self.rb_histogram.isChecked():
                ax.bar(categories, values)
                ax.set_title(f"Гистограмма по категориям номеров")
            elif self.rb_linear.isChecked():
                ax.plot(categories, values, 'o-', linewidth=2)
                ax.set_title(f"Линейный график по категориям номеров")
            elif self.rb_pie.isChecked():
                ax.pie(values, labels=categories, autopct='%1.1f%%', shadow=True, startangle=90)
                ax.axis('equal')
                ax.set_title(f"Круговая диаграмма по категориям номеров")
            
            ax.set_xlabel("Категория номера")
            ax.set_ylabel(y_label)
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
            plt.tight_layout()
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            ax.text(0.5, 0.5, f"Ошибка при построении графика: {e}", 
                   horizontalalignment='center', verticalalignment='center')

class SQLTableModel(QAbstractTableModel):
    """Модель для отображения SQL-данных в QTableView"""
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            else:
                return section + 1
        return None

class HotelApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Гостиница")
        self.resize(1000, 600)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Макет:"))
        self.hotel_combo = QComboBox()
        self.hotel_combo.addItem("Гостиница")
        top_layout.addWidget(self.hotel_combo)
        main_layout.addLayout(top_layout)

        content_layout = QHBoxLayout()
        left_panel = QVBoxLayout()
        self.btn_clients = QPushButton("Клиенты")
        self.btn_rooms = QPushButton("Номерной фонд")
        self.btn_services = QPushButton("Доп. услуги")
        self.btn_bookings = QPushButton("Бронирования")
        self.btn_charts = QPushButton("Графики")
        for btn in [self.btn_clients, self.btn_rooms, self.btn_services, self.btn_bookings, self.btn_charts]:
            left_panel.addWidget(btn)
        left_panel.addStretch()
        content_layout.addLayout(left_panel)

        right_panel = QVBoxLayout()
        
        # Добавляем панель фильтрации
        filter_layout = QHBoxLayout()
        self.search_line = QLineEdit()
        self.search_line.setPlaceholderText("Поиск...")
        filter_layout.addWidget(self.search_line)
        
        self.btn_advanced_filter = QPushButton("Расширенный фильтр")
        filter_layout.addWidget(self.btn_advanced_filter)
        
        self.btn_reset_filter = QPushButton("Сбросить")
        filter_layout.addWidget(self.btn_reset_filter)
        
        right_panel.addLayout(filter_layout)

        self.table = QTableView()
        right_panel.addWidget(self.table)

        btns_layout = QHBoxLayout()
        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Редактировать")
        self.btn_delete = QPushButton("Удалить")
        btns_layout.addWidget(self.btn_add)
        btns_layout.addWidget(self.btn_edit)
        btns_layout.addWidget(self.btn_delete)
        right_panel.addLayout(btns_layout)

        content_layout.addLayout(right_panel)
        main_layout.addLayout(content_layout)

        # Сигналы
        self.btn_clients.clicked.connect(self.show_clients)
        self.btn_rooms.clicked.connect(self.show_rooms)
        self.btn_services.clicked.connect(self.show_services)
        self.btn_bookings.clicked.connect(self.show_bookings)
        self.btn_charts.clicked.connect(self.show_charts)
        self.search_line.textChanged.connect(self.filter_table)
        self.btn_advanced_filter.clicked.connect(self.show_advanced_filter)
        self.btn_reset_filter.clicked.connect(self.reset_filters)
        self.btn_add.clicked.connect(self.add_entry)
        self.btn_edit.clicked.connect(self.edit_entry)
        self.btn_delete.clicked.connect(self.delete_entry)

        # По умолчанию показываем клиентов
        self.current_section = "clients"
        self.show_clients()

    def fetch_clients(self, filter_text=""):
        """Получение и фильтрация клиентов из БД"""
        try:
            query = select(guests_table)
            if filter_text:
                like = f"%{filter_text}%"
                query = query.where(
                    or_(
                        guests_table.c.lastname.ilike(like),
                        guests_table.c.firstname.ilike(like),
                        guests_table.c.email.ilike(like),
                        guests_table.c.phone.ilike(like)
                    )
                )
            result = session.execute(query).fetchall()
            headers = ["ID", "Фамилия", "Имя", "Отчество", "Дата рождения", "Город", "Паспорт", "Телефон", "Email"]
            data = [
                [
                    row.guestid, row.lastname, row.firstname, row.middlename,
                    row.dateofbirth, row.placeofbirth,
                    f"{row.passportseries or ''} {row.passportnumber or ''}",
                    row.phone, row.email
                ]
                for row in result
            ]
            return data, headers
        except Exception as e:
            print(f"Ошибка при получении клиентов: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить клиентов: {e}")
            return [], ["ID", "Фамилия", "Имя", "Отчество", "Дата рождения", "Город", "Паспорт", "Телефон", "Email"]

    def fetch_rooms(self, filter_text=""):
        """Получение и фильтрация номеров из БД"""
        try:
            # Присоединяем категории номеров
            query = select(
                rooms_table.c.roomid,
                rooms_table.c.roomnumber,
                room_categories_table.c.name.label("Category"),
                room_categories_table.c.description
            ).join(room_categories_table, rooms_table.c.categoryid == room_categories_table.c.categoryid)
            
            if filter_text:
                like = f"%{filter_text}%"
                query = query.where(
                    or_(
                        rooms_table.c.roomnumber.ilike(like),
                        room_categories_table.c.name.ilike(like),
                        room_categories_table.c.description.ilike(like)
                    )
                )
            
            result = session.execute(query).fetchall()
            headers = ["ID", "Номер", "Категория", "Описание"]
            data = [list(row) for row in result]
            return data, headers
        except Exception as e:
            print(f"Ошибка при получении номеров: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить номерной фонд: {e}")
            return [], ["ID", "Номер", "Категория", "Описание"]

    def fetch_services(self, filter_text=""):
        """Получение и фильтрация услуг из БД"""
        try:
            query = select(
                services_table.c.serviceid,
                services_table.c.name,
                services_table.c.description,
                services_table.c.baseprice,
                services_table.c.priceunit
            )
            if filter_text:
                like = f"%{filter_text}%"
                query = query.where(
                    or_(
                        services_table.c.name.ilike(like),
                        services_table.c.description.ilike(like),
                        services_table.c.priceunit.ilike(like)
                    )
                )
            result = session.execute(query).fetchall()
            headers = ["ID", "Название", "Описание", "Базовая цена", "Ед. измерения"]
            data = [list(row) for row in result]
            return data, headers
        except Exception as e:
            print(f"Ошибка при получении услуг: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить услуги: {e}")
            return [], ["ID", "Название", "Описание", "Базовая цена", "Ед. измерения"]

    def fetch_bookings(self, filter_text=""):
        """Получение и фильтрация бронирований из БД"""
        try:
            # Присоединяем клиента и категорию номера
            query = select(
                bookings_table.c.bookingid,
                guests_table.c.lastname,
                guests_table.c.firstname,
                bookings_table.c.bookingdate,
                bookings_table.c.checkindate,
                bookings_table.c.checkoutdate,
                room_categories_table.c.name.label("Category"),
                bookings_table.c.status
            ).join(guests_table, bookings_table.c.clientid == guests_table.c.guestid)
            query = query.join(room_categories_table, bookings_table.c.categoryid == room_categories_table.c.categoryid)
            if filter_text:
                like = f"%{filter_text}%"
                query = query.where(
                    or_(
                        guests_table.c.lastname.ilike(like),
                        guests_table.c.firstname.ilike(like),
                        room_categories_table.c.name.ilike(like),
                        bookings_table.c.status.ilike(like)
                    )
                )
            result = session.execute(query).fetchall()
            headers = ["ID", "Фамилия", "Имя", "Дата бронирования", "Заезд", "Выезд", "Категория", "Статус"]
            data = [list(row) for row in result]
            return data, headers
        except Exception as e:
            print(f"Ошибка при получении бронирований: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить бронирования: {e}")
            return [], ["ID", "Фамилия", "Имя", "Дата бронирования", "Заезд", "Выезд", "Категория", "Статус"]

    def show_clients(self):
        self.current_section = "clients"
        data, headers = self.fetch_clients()
        self.model = SQLTableModel(data, headers)
        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def show_rooms(self):
        self.current_section = "rooms"
        data, headers = self.fetch_rooms()
        self.model = SQLTableModel(data, headers)
        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def show_services(self):
        self.current_section = "services"
        data, headers = self.fetch_services()
        self.model = SQLTableModel(data, headers)
        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def show_bookings(self):
        self.current_section = "bookings"
        data, headers = self.fetch_bookings()
        self.model = SQLTableModel(data, headers)
        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def show_charts(self):
        """Отображение окна с графиками"""
        try:
            charts_window = ChartsWindow(self)
            charts_window.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при открытии окна графиков: {e}")

    def filter_table(self, text):
        """Фильтрация по всей таблице простым поиском текста"""
        if self.current_section == "clients":
            data, headers = self.fetch_clients(text)
        elif self.current_section == "rooms":
            data, headers = self.fetch_rooms(text)
        elif self.current_section == "services":
            data, headers = self.fetch_services(text)
        elif self.current_section == "bookings":
            data, headers = self.fetch_bookings(text)
        else:
            return
        self.model = SQLTableModel(data, headers)
        self.table.setModel(self.model)
        
    def show_advanced_filter(self):
        """Показать расширенный фильтр в зависимости от текущей таблицы"""
        if self.current_section == "clients":
            self.advanced_filter_clients()
        elif self.current_section == "rooms":
            QMessageBox.information(self, "Информация", "Расширенный фильтр для номеров пока не реализован")
        elif self.current_section == "services":
            QMessageBox.information(self, "Информация", "Расширенный фильтр для услуг пока не реализован")
        elif self.current_section == "bookings":
            QMessageBox.information(self, "Информация", "Расширенный фильтр для бронирований пока не реализован")

    def advanced_filter_clients(self):
        """Расширенная фильтрация клиентов по различным критериям"""
        if self.current_section != "clients":
            QMessageBox.warning(self, "Предупреждение", "Этот фильтр доступен только для таблицы клиентов")
            return
            
        # Создаем диалог фильтра
        dialog = QDialog(self)
        dialog.setWindowTitle("Расширенный фильтр клиентов")
        dialog.setMinimumWidth(400)
        
        form_layout = QVBoxLayout(dialog)
        
        # Поля фильтра
        form_layout.addWidget(QLabel("Фамилия:"))
        lastname_filter = QLineEdit()
        form_layout.addWidget(lastname_filter)
        
        form_layout.addWidget(QLabel("Имя:"))
        firstname_filter = QLineEdit()
        form_layout.addWidget(firstname_filter)
        
        form_layout.addWidget(QLabel("Город:"))
        city_filter = QLineEdit()
        form_layout.addWidget(city_filter)
        
        form_layout.addWidget(QLabel("Телефон:"))
        phone_filter = QLineEdit()
        form_layout.addWidget(phone_filter)
        
        form_layout.addWidget(QLabel("Email:"))
        email_filter = QLineEdit()
        form_layout.addWidget(email_filter)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        apply_btn = QPushButton("Применить")
        reset_btn = QPushButton("Сбросить")
        cancel_btn = QPushButton("Отмена")
        
        buttons_layout.addWidget(apply_btn)
        buttons_layout.addWidget(reset_btn)
        buttons_layout.addWidget(cancel_btn)
        
        form_layout.addLayout(buttons_layout)
        
        # Обработка нажатий
        apply_btn.clicked.connect(lambda: self.apply_client_filter(
            lastname_filter.text(),
            firstname_filter.text(),
            city_filter.text(),
            phone_filter.text(),
            email_filter.text(),
            dialog
        ))
        
        reset_btn.clicked.connect(lambda: self.reset_filters(dialog))
        cancel_btn.clicked.connect(dialog.reject)
        
        dialog.exec_()
    
    def apply_client_filter(self, lastname, firstname, city, phone, email, dialog):
        """Применить фильтры для клиентов"""
        try:
            # Построение запроса с несколькими условиями
            conditions = []
            query = select(guests_table)
            
            if lastname:
                conditions.append(guests_table.c.lastname.ilike(f"%{lastname}%"))
            
            if firstname:
                conditions.append(guests_table.c.firstname.ilike(f"%{firstname}%"))
            
            if city:
                conditions.append(guests_table.c.placeofbirth.ilike(f"%{city}%"))
            
            if phone:
                conditions.append(guests_table.c.phone.ilike(f"%{phone}%"))
            
            if email:
                conditions.append(guests_table.c.email.ilike(f"%{email}%"))
            
            # Если есть условия, добавляем их в запрос
            if conditions:
                query = query.where(or_(*conditions))
            
            result = session.execute(query).fetchall()
            headers = ["ID", "Фамилия", "Имя", "Отчество", "Дата рождения", "Город", "Паспорт", "Телефон", "Email"]
            data = [
                [
                    row.guestid, row.lastname, row.firstname, row.middlename,
                    row.dateofbirth, row.placeofbirth,
                    f"{row.passportseries or ''} {row.passportnumber or ''}",
                    row.phone, row.email
                ]
                for row in result
            ]
            
            self.model = SQLTableModel(data, headers)
            self.table.setModel(self.model)
            dialog.accept()
            
        except Exception as e:
            print(f"Ошибка применения фильтра: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось применить фильтр: {e}")
    
    def reset_filters(self, dialog=None):
        """Сбросить все фильтры"""
        if self.current_section == "clients":
            self.show_clients()
        elif self.current_section == "rooms":
            self.show_rooms()
        elif self.current_section == "services":
            self.show_services()
        elif self.current_section == "bookings":
            self.show_bookings()
            
        if dialog:
            dialog.accept()

    def add_entry(self):
        if self.current_section == "clients":
            self.add_client()
        elif self.current_section == "rooms":
            self.add_room()
        elif self.current_section == "services":
            self.add_service()
        elif self.current_section == "bookings":
            self.add_booking()

    def edit_entry(self):
        if self.current_section == "clients":
            self.edit_client()
        elif self.current_section == "rooms":
            self.edit_room()
        elif self.current_section == "services":
            self.edit_service()
        elif self.current_section == "bookings":
            self.edit_booking()

    def delete_entry(self):
        if self.current_section == "clients":
            self.delete_client()
        elif self.current_section == "rooms":
            self.delete_room()
        elif self.current_section == "services":
            self.delete_service()
        elif self.current_section == "bookings":
            self.delete_booking()
            
    def delete_client(self):
        idx = self.table.currentIndex()
        if not idx.isValid():
            QMessageBox.warning(self, "Ошибка", "Выберите клиента для удаления")
            return
        
        row = idx.row()
        guest_id = self.model._data[row][0]
        guest_name = f"{self.model._data[row][1]} {self.model._data[row][2]}"
        
        reply = QMessageBox.question(
            self, "Подтверждение удаления", 
            f"Вы уверены, что хотите удалить клиента {guest_name}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Проверяем, есть ли связанные записи в bookings
                bookings_check = session.execute(
                    select(bookings_table).where(bookings_table.c.clientid == guest_id)
                ).fetchall()
                
                if bookings_check:
                    QMessageBox.warning(
                        self, "Ошибка удаления", 
                        "Невозможно удалить клиента, так как с ним связаны бронирования.\n"
                        "Сначала удалите связанные бронирования."
                    )
                    return
                
                delete_stmt = guests_table.delete().where(guests_table.c.guestid == guest_id)
                session.execute(delete_stmt)
                session.commit()
                self.show_clients()
                QMessageBox.information(self, "Успех", f"Клиент {guest_name} успешно удален")
            except Exception as e:
                print(f"Ошибка при удалении клиента: {e}")
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить клиента: {e}")
                session.rollback()
    
    def delete_room(self):
        idx = self.table.currentIndex()
        if not idx.isValid():
            QMessageBox.warning(self, "Ошибка", "Выберите номер для удаления")
            return
        
        row = idx.row()
        room_id = self.model._data[row][0]
        room_number = self.model._data[row][1]
        
        reply = QMessageBox.question(
            self, "Подтверждение удаления", 
            f"Вы уверены, что хотите удалить номер {room_number}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                delete_stmt = rooms_table.delete().where(rooms_table.c.roomid == room_id)
                session.execute(delete_stmt)
                session.commit()
                self.show_rooms()
                QMessageBox.information(self, "Успех", f"Номер {room_number} успешно удален")
            except Exception as e:
                print(f"Ошибка при удалении номера: {e}")
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить номер: {e}")
                session.rollback()
    
    def delete_service(self):
        idx = self.table.currentIndex()
        if not idx.isValid():
            QMessageBox.warning(self, "Ошибка", "Выберите услугу для удаления")
            return
        
        row = idx.row()
        service_id = self.model._data[row][0]
        service_name = self.model._data[row][1]
        
        reply = QMessageBox.question(
            self, "Подтверждение удаления", 
            f"Вы уверены, что хотите удалить услугу '{service_name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                delete_stmt = services_table.delete().where(services_table.c.serviceid == service_id)
                session.execute(delete_stmt)
                session.commit()
                self.show_services()
                QMessageBox.information(self, "Успех", f"Услуга '{service_name}' успешно удалена")
            except Exception as e:
                print(f"Ошибка при удалении услуги: {e}")
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить услугу: {e}")
                session.rollback()
    
    def delete_booking(self):
        idx = self.table.currentIndex()
        if not idx.isValid():
            QMessageBox.warning(self, "Ошибка", "Выберите бронирование для удаления")
            return
        
        row = idx.row()
        booking_id = self.model._data[row][0]
        client_name = f"{self.model._data[row][1]} {self.model._data[row][2]}"
        dates = f"{self.model._data[row][4]} - {self.model._data[row][5]}"
        
        reply = QMessageBox.question(
            self, "Подтверждение удаления", 
            f"Вы уверены, что хотите удалить бронирование клиента {client_name} на даты {dates}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Устанавливаем соединение с БД и создаем транзакцию
                conn = engine.connect()
                trans = conn.begin()
                
                try:
                    # 1. Сначала удаляем связанные записи в bookingoccupants
                    bookingoccupants_table = Table('bookingoccupants', metadata, autoload_with=engine)
                    delete_occupants = bookingoccupants_table.delete().where(
                        bookingoccupants_table.c.bookingid == booking_id
                    )
                    conn.execute(delete_occupants)
                    
                    # 2. Проверка на stayoccupants и stays
                    stays_table = Table('stays', metadata, autoload_with=engine)
                    stayoccupants_table = Table('stayoccupants', metadata, autoload_with=engine)
                    
                    # Получаем связанные stays
                    stays = conn.execute(
                        select(stays_table.c.stayid).where(stays_table.c.bookingid == booking_id)
                    ).fetchall()
                    
                    # Для каждого stay удаляем связанные записи
                    for stay in stays:
                        stay_id = stay[0]
                        
                        # Удаляем записи в serviceusage
                        serviceusage_table = Table('serviceusage', metadata, autoload_with=engine)
                        delete_serviceusage = serviceusage_table.delete().where(
                            serviceusage_table.c.stayid == stay_id
                        )
                        conn.execute(delete_serviceusage)
                        
                        # Удаляем stayoccupants
                        delete_stayoccupants = stayoccupants_table.delete().where(
                            stayoccupants_table.c.stayid == stay_id
                        )
                        conn.execute(delete_stayoccupants)
                    
                    # Удаляем stays
                    delete_stays = stays_table.delete().where(
                        stays_table.c.bookingid == booking_id
                    )
                    conn.execute(delete_stays)
                    
                    # 3. Наконец удаляем само бронирование
                    delete_booking = bookings_table.delete().where(
                        bookings_table.c.bookingid == booking_id
                    )
                    conn.execute(delete_booking)
                    
                    # Если всё успешно, фиксируем транзакцию
                    trans.commit()
                    self.show_bookings()
                    QMessageBox.information(self, "Успех", "Бронирование успешно удалено")
                except Exception as e:
                    # В случае ошибки отменяем все изменения
                    trans.rollback()
                    raise e
                finally:
                    # Закрываем соединение
                    conn.close()
                    
            except Exception as e:
                print(f"Ошибка при удалении бронирования: {e}")
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить бронирование: {e}")

    def add_client(self):
        last_name, ok1 = QInputDialog.getText(self, "Добавить клиента", "Фамилия:")
        if not ok1 or not last_name:
            return
        first_name, ok2 = QInputDialog.getText(self, "Добавить клиента", "Имя:")
        if not ok2 or not first_name:
            return
        
        # Запрашиваем все остальные поля
        middle_name, ok3 = QInputDialog.getText(self, "Добавить клиента", "Отчество:")
        if not ok3:
            middle_name = None
        
        date_of_birth, ok4 = QInputDialog.getText(self, "Добавить клиента", "Дата рождения (ГГГГ-ММ-ДД):")
        if not ok4 or not date_of_birth:
            date_of_birth = None
        
        place_of_birth, ok5 = QInputDialog.getText(self, "Добавить клиента", "Место рождения:")
        if not ok5:
            place_of_birth = None
        
        passport_series, ok6 = QInputDialog.getText(self, "Добавить клиента", "Серия паспорта:")
        if not ok6:
            passport_series = None
        
        passport_number, ok7 = QInputDialog.getText(self, "Добавить клиента", "Номер паспорта:")
        if not ok7:
            passport_number = None
        
        passport_issue_date, ok8 = QInputDialog.getText(self, "Добавить клиента", "Дата выдачи паспорта (ГГГГ-ММ-ДД):")
        if not ok8:
            passport_issue_date = None
        
        passport_issued_by, ok9 = QInputDialog.getText(self, "Добавить клиента", "Кем выдан паспорт:")
        if not ok9:
            passport_issued_by = None
        
        address, ok10 = QInputDialog.getText(self, "Добавить клиента", "Адрес:")
        if not ok10:
            address = None
        
        phone, ok11 = QInputDialog.getText(self, "Добавить клиента", "Телефон:")
        if not ok11:
            phone = None
        
        email, ok12 = QInputDialog.getText(self, "Добавить клиента", "Email:")
        if not ok12:
            email = None
        
        discount_card, ok13 = QInputDialog.getText(self, "Добавить клиента", "Номер дисконтной карты:")
        if not ok13:
            discount_card = None
            
        # Расширенная вставка с учетом всех полей
        try:
            ins = guests_table.insert().values(
                lastname=last_name,
                firstname=first_name,
                middlename=middle_name,
                dateofbirth=date_of_birth,
                placeofbirth=place_of_birth,
                passportseries=passport_series,
                passportnumber=passport_number,
                passportissuedate=passport_issue_date,
                passportissuedby=passport_issued_by,
                address=address,
                phone=phone,
                email=email,
                discountcardnumber=discount_card
            )
            session.execute(ins)
            session.commit()
            self.show_clients()
        except Exception as e:
            print(f"Ошибка при добавлении клиента: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить клиента: {e}")
            session.rollback()

    def edit_client(self):
        idx = self.table.currentIndex()
        if not idx.isValid():
            QMessageBox.warning(self, "Ошибка", "Выберите клиента для редактирования")
            return
        row = idx.row()
        guest_id = self.model._data[row][0]
        
        # Получаем данные из выбранной строки
        last_name, ok1 = QInputDialog.getText(self, "Редактировать клиента", "Фамилия:", text=self.model._data[row][1])
        if not ok1 or not last_name:
            return
        first_name, ok2 = QInputDialog.getText(self, "Редактировать клиента", "Имя:", text=self.model._data[row][2])
        if not ok2 or not first_name:
            return
        
        # Дополнительные поля
        middle_name, ok3 = QInputDialog.getText(self, "Редактировать клиента", "Отчество:", text=self.model._data[row][3] if self.model._data[row][3] != 'None' else "")
        if not ok3:
            middle_name = None
            
        # Получим информацию о клиенте из БД для полей, которых нет в таблице
        client_info = session.execute(select(guests_table).where(guests_table.c.guestid == guest_id)).fetchone()
        
        date_of_birth, ok4 = QInputDialog.getText(self, "Редактировать клиента", "Дата рождения (ГГГГ-ММ-ДД):", 
                                                text=str(self.model._data[row][4]) if self.model._data[row][4] != 'None' else "")
        if not ok4 or not date_of_birth:
            date_of_birth = None
            
        place_of_birth, ok5 = QInputDialog.getText(self, "Редактировать клиента", "Место рождения:", 
                                                 text=str(self.model._data[row][5]) if self.model._data[row][5] != 'None' else "")
        if not ok5:
            place_of_birth = None
        
        # Серия и номер паспорта могут быть в одном поле в таблице, но хранятся отдельно в БД
        passport_parts = self.model._data[row][6].split() if self.model._data[row][6] != 'None' else ["", ""]
        passport_series = passport_parts[0] if len(passport_parts) > 0 else ""
        passport_number = passport_parts[1] if len(passport_parts) > 1 else ""
        
        passport_series, ok6 = QInputDialog.getText(self, "Редактировать клиента", "Серия паспорта:", 
                                                  text=passport_series)
        if not ok6:
            passport_series = None
        
        passport_number, ok7 = QInputDialog.getText(self, "Редактировать клиента", "Номер паспорта:", 
                                                  text=passport_number)
        if not ok7:
            passport_number = None
        
        # Эти поля могут отсутствовать в таблице, но есть в БД
        passport_issue_date, ok8 = QInputDialog.getText(self, "Редактировать клиента", "Дата выдачи паспорта (ГГГГ-ММ-ДД):", 
                                                       text=str(client_info.passportissuedate) if client_info.passportissuedate else "")
        if not ok8:
            passport_issue_date = None
        
        passport_issued_by, ok9 = QInputDialog.getText(self, "Редактировать клиента", "Кем выдан паспорт:", 
                                                     text=str(client_info.passportissuedby) if client_info.passportissuedby else "")
        if not ok9:
            passport_issued_by = None
        
        address, ok10 = QInputDialog.getText(self, "Редактировать клиента", "Адрес:", 
                                           text=str(client_info.address) if client_info.address else "")
        if not ok10:
            address = None
        
        phone, ok11 = QInputDialog.getText(self, "Редактировать клиента", "Телефон:", 
                                         text=str(self.model._data[row][7]) if self.model._data[row][7] != 'None' else "")
        if not ok11:
            phone = None
        
        email, ok12 = QInputDialog.getText(self, "Редактировать клиента", "Email:", 
                                         text=str(self.model._data[row][8]) if self.model._data[row][8] != 'None' else "")
        if not ok12:
            email = None
        
        discount_card, ok13 = QInputDialog.getText(self, "Редактировать клиента", "Номер дисконтной карты:", 
                                                 text=str(client_info.discountcardnumber) if client_info.discountcardnumber else "")
        if not ok13:
            discount_card = None
        
        try:
            upd = guests_table.update().where(guests_table.c.guestid == guest_id).values(
                lastname=last_name, 
                firstname=first_name,
                middlename=middle_name,
                dateofbirth=date_of_birth,
                placeofbirth=place_of_birth,
                passportseries=passport_series,
                passportnumber=passport_number,
                passportissuedate=passport_issue_date,
                passportissuedby=passport_issued_by,
                address=address,
                phone=phone,
                email=email,
                discountcardnumber=discount_card
            )
            session.execute(upd)
            session.commit()
            self.show_clients()
        except Exception as e:
            print(f"Ошибка при редактировании клиента: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить клиента: {e}")
            session.rollback()

    def add_room(self):
        room_number, ok1 = QInputDialog.getText(self, "Добавить номер", "Номер комнаты:")
        if not ok1 or not room_number:
            return
        # Получаем список категорий
        categories = session.execute(select(room_categories_table.c.categoryid, room_categories_table.c.name)).fetchall()
        if not categories:
            QMessageBox.warning(self, "Ошибка", "Нет категорий номеров. Сначала добавьте категорию.")
            return
        cat_names = [cat.name for cat in categories]
        cat_id_map = {cat.name: cat.categoryid for cat in categories}
        cat_name, ok2 = QInputDialog.getItem(self, "Категория номера", "Выберите категорию:", cat_names, editable=False)
        if not ok2 or not cat_name:
            return
        category_id = cat_id_map[cat_name]
        
        try:
            ins = rooms_table.insert().values(roomnumber=room_number, categoryid=category_id)
            session.execute(ins)
            session.commit()
            self.show_rooms()
        except Exception as e:
            print(f"Ошибка при добавлении номера: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить номер: {e}")
            session.rollback()

    def edit_room(self):
        idx = self.table.currentIndex()
        if not idx.isValid():
            QMessageBox.warning(self, "Ошибка", "Выберите номер для редактирования")
            return
        row = idx.row()
        room_id = self.model._data[row][0]
        room_number, ok1 = QInputDialog.getText(self, "Редактировать номер", "Номер комнаты:", text=self.model._data[row][1])
        if not ok1 or not room_number:
            return
        # Получаем список категорий
        categories = session.execute(select(room_categories_table.c.categoryid, room_categories_table.c.name)).fetchall()
        if not categories:
            QMessageBox.warning(self, "Ошибка", "Нет категорий номеров. Сначала добавьте категорию.")
            return
        cat_names = [cat.name for cat in categories]
        cat_id_map = {cat.name: cat.categoryid for cat in categories}
        cat_name, ok2 = QInputDialog.getItem(self, "Категория номера", "Выберите категорию:", cat_names, editable=False)
        if not ok2 or not cat_name:
            return
        category_id = cat_id_map[cat_name]
        upd = rooms_table.update().where(rooms_table.c.roomid == room_id).values(roomnumber=room_number, categoryid=category_id)
        session.execute(upd)
        session.commit()
        self.show_rooms()

    def add_service(self):
        name, ok1 = QInputDialog.getText(self, "Добавить услугу", "Название:")
        if not ok1 or not name:
            return
        description, ok2 = QInputDialog.getText(self, "Добавить услугу", "Описание:")
        if not ok2:
            description = ""
        base_price, ok3 = QInputDialog.getDouble(self, "Добавить услугу", "Базовая цена:", decimals=2)
        if not ok3:
            return
        price_unit, ok4 = QInputDialog.getText(self, "Добавить услугу", "Ед. измерения:")
        if not ok4:
            price_unit = ""
        
        try:
            ins = services_table.insert().values(
                name=name, 
                description=description, 
                baseprice=base_price, 
                priceunit=price_unit
            )
            session.execute(ins)
            session.commit()
            self.show_services()
        except Exception as e:
            print(f"Ошибка при добавлении услуги: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить услугу: {e}")
            session.rollback()

    def edit_service(self):
        idx = self.table.currentIndex()
        if not idx.isValid():
            QMessageBox.warning(self, "Ошибка", "Выберите услугу для редактирования")
            return
        row = idx.row()
        service_id = self.model._data[row][0]
        name, ok1 = QInputDialog.getText(self, "Редактировать услугу", "Название:", text=self.model._data[row][1])
        if not ok1 or not name:
            return
        description, ok2 = QInputDialog.getText(self, "Редактировать услугу", "Описание:", text=self.model._data[row][2])
        if not ok2:
            description = ""
        base_price, ok3 = QInputDialog.getDouble(self, "Редактировать услугу", "Базовая цена:", value=float(self.model._data[row][3]), decimals=2)
        if not ok3:
            return
        price_unit, ok4 = QInputDialog.getText(self, "Редактировать услугу", "Ед. измерения:", text=self.model._data[row][4])
        if not ok4:
            price_unit = ""
            
        try:
            upd = services_table.update().where(services_table.c.serviceid == service_id).values(
                name=name, 
                description=description, 
                baseprice=base_price, 
                priceunit=price_unit
            )
            session.execute(upd)
            session.commit()
            self.show_services()
        except Exception as e:
            print(f"Ошибка при редактировании услуги: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить услугу: {e}")
            session.rollback()

    def add_booking(self):
        # Выбор клиента
        clients = session.execute(select(guests_table.c.guestid, guests_table.c.lastname, guests_table.c.firstname)).fetchall()
        if not clients:
            QMessageBox.warning(self, "Ошибка", "Нет клиентов. Сначала добавьте клиента.")
            return
        client_names = [f"{c.lastname} {c.firstname}" for c in clients]
        client_id_map = {f"{c.lastname} {c.firstname}": c.guestid for c in clients}
        client_name, ok1 = QInputDialog.getItem(self, "Клиент", "Выберите клиента:", client_names, editable=False)
        if not ok1 or not client_name:
            return
        client_id = client_id_map[client_name]
        # Выбор категории номера
        categories = session.execute(select(room_categories_table.c.categoryid, room_categories_table.c.name)).fetchall()
        if not categories:
            QMessageBox.warning(self, "Ошибка", "Нет категорий номеров. Сначала добавьте категорию.")
            return
        cat_names = [cat.name for cat in categories]
        cat_id_map = {cat.name: cat.categoryid for cat in categories}
        cat_name, ok2 = QInputDialog.getItem(self, "Категория номера", "Выберите категорию:", cat_names, editable=False)
        if not ok2 or not cat_name:
            return
        category_id = cat_id_map[cat_name]
        # Даты
        booking_date, ok3 = QInputDialog.getText(self, "Дата бронирования", "Введите дату (ГГГГ-ММ-ДД):")
        if not ok3 or not booking_date:
            return
        checkin_date, ok4 = QInputDialog.getText(self, "Дата заезда", "Введите дату (ГГГГ-ММ-ДД):")
        if not ok4 or not checkin_date:
            return
        checkout_date, ok5 = QInputDialog.getText(self, "Дата выезда", "Введите дату (ГГГГ-ММ-ДД):")
        if not ok5 or not checkout_date:
            return
        status, ok6 = QInputDialog.getText(self, "Статус", "Статус (Pending/Confirmed/Cancelled/Completed):")
        if not ok6 or not status:
            status = "Pending"
        
        try:
            ins = bookings_table.insert().values(
                clientid=client_id, 
                bookingdate=booking_date, 
                checkindate=checkin_date, 
                checkoutdate=checkout_date, 
                categoryid=category_id, 
                status=status
            )
            session.execute(ins)
            session.commit()
            self.show_bookings()
        except Exception as e:
            print(f"Ошибка при добавлении бронирования: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить бронирование: {e}")
            session.rollback()

    def edit_booking(self):
        idx = self.table.currentIndex()
        if not idx.isValid():
            QMessageBox.warning(self, "Ошибка", "Выберите бронирование для редактирования")
            return
        row = idx.row()
        booking_id = self.model._data[row][0]
        # Аналогично add_booking, но с подстановкой текущих значений
        # Клиент
        clients = session.execute(select(guests_table.c.guestid, guests_table.c.lastname, guests_table.c.firstname)).fetchall()
        client_names = [f"{c.lastname} {c.firstname}" for c in clients]
        client_id_map = {f"{c.lastname} {c.firstname}": c.guestid for c in clients}
        current_client = f"{self.model._data[row][1]} {self.model._data[row][2]}"
        client_name, ok1 = QInputDialog.getItem(self, "Клиент", "Выберите клиента:", client_names, editable=False, current=client_names.index(current_client) if current_client in client_names else 0)
        if not ok1 or not client_name:
            return
        client_id = client_id_map[client_name]
        # Категория
        categories = session.execute(select(room_categories_table.c.categoryid, room_categories_table.c.name)).fetchall()
        cat_names = [cat.name for cat in categories]
        cat_id_map = {cat.name: cat.categoryid for cat in categories}
        current_cat = self.model._data[row][6]
        cat_name, ok2 = QInputDialog.getItem(self, "Категория номера", "Выберите категорию:", cat_names, editable=False, current=cat_names.index(current_cat) if current_cat in cat_names else 0)
        if not ok2 or not cat_name:
            return
        category_id = cat_id_map[cat_name]
        # Даты
        booking_date, ok3 = QInputDialog.getText(self, "Дата бронирования", "Введите дату (ГГГГ-ММ-ДД):", text=str(self.model._data[row][3]))
        if not ok3 or not booking_date:
            return
        checkin_date, ok4 = QInputDialog.getText(self, "Дата заезда", "Введите дату (ГГГГ-ММ-ДД):", text=str(self.model._data[row][4]))
        if not ok4 or not checkin_date:
            return
        checkout_date, ok5 = QInputDialog.getText(self, "Дата выезда", "Введите дату (ГГГГ-ММ-ДД):", text=str(self.model._data[row][5]))
        if not ok5 or not checkout_date:
            return
        status, ok6 = QInputDialog.getText(self, "Статус", "Статус (Pending/Confirmed/Cancelled/Completed):", text=str(self.model._data[row][7]))
        if not ok6 or not status:
            status = "Pending"
        upd = bookings_table.update().where(bookings_table.c.bookingid == booking_id).values(clientid=client_id, bookingdate=booking_date, checkindate=checkin_date, checkoutdate=checkout_date, categoryid=category_id, status=status)
        session.execute(upd)
        session.commit()
        self.show_bookings()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HotelApp()
    window.show()
    sys.exit(app.exec_())
