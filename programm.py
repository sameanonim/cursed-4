import psycopg2
import json
from main_postgres import DownloadDatafromHH
from DBManager import DBManager
from DBConnector import ConnectDatabase

# подключение к базе данных
connect_db = ConnectDatabase('config.ini')

# запускает программу из main_postgres.py и затем открываем файл data_list.json и загружаем данные в переменную vacancies
DownloadDatafromHH()

with open("data_list.json", "r", encoding='utf-8') as f:
    vacancies = json.load(f)

class Primary(ConnectDatabase):
    # Создаем метод __init__ для инициализации объекта класса и установки соединения с БД
    def __init__(self, filename):
        # Сохраняем параметры соединения в атрибутах объекта
        super().__init__(filename)

    def create_tables(self):
        # Создаем таблицу для хранения данных о работодателях
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS company (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                url VARCHAR(255) NOT NULL,
                description TEXT
            );
        """)
        # Создаем таблицу для хранения данных о вакансиях
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancy (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                company_name VARCHAR(255) NOT NULL,
                url VARCHAR(255) NOT NULL,
                description TEXT,
                remote_work TEXT,
                salary INTEGER
            );
        """)
        # Сохраняем изменения в БД
        self.conn.commit()

    def insert_company(self, name, website):
        # Вставляем данные о работодателе в таблицу company
        self.cur.execute("""
            INSERT INTO company (name, website) VALUES (%s, %s) RETURNING id;
        """, (name, website))
        # Получаем id вставленной записи
        company_id = self.cur.fetchone()
        # Сохраняем изменения в БД
        self.conn.commit()
        # Возвращаем id вставленной записи
        return company_id

    def insert_vacancy(self, name, description, salary, currency, company_id):
        # Вставляем данные о вакансии в таблицу vacancy
        self.cur.execute("""
            INSERT INTO vacancy (name, company_name, url, description, remote_work, salary) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
        """, (name, description, salary, currency, company_id))
        # Получаем id вставленной записи
        vacancy_id = self.cur.fetchone()
        # Сохраняем изменения в БД
        self.conn.commit()
        # Возвращаем id вставленной записи
        return vacancy_id

    def get_companies(self):
        # Получаем все данные о работодателях из таблицы company
        self.cur.execute("""
            SELECT * FROM company;
        """)
        # Возвращаем список кортежей с данными о работодателях
        return self.cur.fetchall()

    def get_vacancies(self):
        # Получаем все данные о вакансиях из таблицы vacancy
        self.cur.execute("""
            SELECT * FROM vacancy;
        """)
        # Возвращаем список кортежей с данными о вакансиях
        return self.cur.fetchall()

    def __del__(self):
        # Закрываем подключение к БД и курсор
        super().__init__