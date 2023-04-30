# Импортируем библиотеку psycopg2 для работы с БД Postgres
import psycopg2

# Создаем класс DBManager с атрибутами для хранения параметров соединения с БД
class DBManager:
    # Создаем метод __init__ для инициализации объекта класса и установки соединения с БД
    def __init__(self, dbname, user, password, host):
        # Сохраняем параметры соединения в атрибутах объекта
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        # Устанавливаем соединение с БД и создаем курсор для выполнения SQL-запросов
        self.conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host)
        self.cur = self.conn.cursor()
    
    # Создаем метод __del__ для закрытия соединения с БД при удалении объекта класса
    def __del__(self):
        # Закрываем курсор и соединение с БД
        self.cur.close()
        self.conn.close()
    
    # Создаем метод get_companies_and_vacancies_count для получения списка всех компаний и количества вакансий у каждой компании
    def get_companies_and_vacancies_count(self):
        # Выполняем SQL-запрос к таблицам employers и vacancies, используя группировку и агрегатную функцию COUNT
        self.cur.execute("""
            SELECT e.name, COUNT(v.id) AS vacancies_count
            FROM employers e
            JOIN vacancies v ON e.id = v.employer_id
            GROUP BY e.name
            ORDER BY vacancies_count DESC
        """)
        # Получаем результат запроса в виде списка кортежей
        result = self.cur.fetchall()
        # Возвращаем результат
        return result
    
    # Создаем метод get_all_vacancies для получения списка всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
    def get_all_vacancies(self):
        # Выполняем SQL-запрос к таблицам employers и vacancies, используя объединение таблиц по полю employer_id
        self.cur.execute("""
            SELECT e.name AS company_name, v.name AS vacancy_name, v.salary_from, v.salary_to, v.salary_currency, v.url AS vacancy_url
            FROM employers e
            JOIN vacancies v ON e.id = v.employer_id
            ORDER BY company_name, vacancy_name
        """)
        # Получаем результат запроса в виде списка кортежей
        result = self.cur.fetchall()
        # Возвращаем результат
        return result
    
    # Создаем метод get_avg_salary для получения средней зарплаты по вакансиям
    def get_avg_salary(self):
        # Выполняем SQL-запрос к таблице vacancies, используя агрегатную функцию AVG и условие для выборки только тех вакансий, у которых есть данные о зарплате
        self.cur.execute("""
            SELECT AVG((salary_from + salary_to) / 2) AS avg_salary
            FROM vacancies
            WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL AND salary_currency = 'RUR'
        """)
        # Получаем результат запроса в виде одного числа
        result = self.cur.fetchone()[0]
        # Возвращаем результат
        return result
    
    # Создаем метод get_vacancies_with_higher_salary для получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям
    def get_vacancies_with_higher_salary(self):
        # Выполняем SQL-запрос к таблицам employers и vacancies, используя объединение таблиц по полю employer_id и подзапрос для вычисления средней зарплаты
        self.cur.execute("""
            SELECT e.name AS company_name, v.name AS vacancy_name, v.salary_from, v.salary_to, v.salary_currency, v.url AS vacancy_url
            FROM employers e
            JOIN vacancies v ON e.id = v.employer_id
            WHERE (salary_from + salary_to) / 2 > (
                SELECT AVG((salary_from + salary_to) / 2) AS avg_salary
                FROM vacancies
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL AND salary_currency = 'RUR'
            )
            AND salary_currency = 'RUR'
            ORDER BY company_name, vacancy_name
        """)
        # Получаем результат запроса в виде списка кортежей
        result = self.cur.fetchall()
        # Возвращаем результат
        return result
    
    # Создаем метод get_vacancies_with_keyword для получения списка всех вакансий, в названии которых содержатся переданные в метод слова, например “python”
    def get_vacancies_with_keyword(self, keyword):
        # Выполняем SQL-запрос к таблицам employers и vacancies, используя объединение таблиц по полю employer_id и условие для выборки только тех вакансий, у которых название содержит заданное слово
        self.cur.execute("""
            SELECT e.name AS company_name, v.name AS vacancy_name, v.salary_from, v.salary_to, v.salary_currency, v.url AS vacancy_url
            FROM employers e
            JOIN vacancies v ON e.id = v.employer_id
            WHERE LOWER(v.name) LIKE %s
            ORDER BY company_name, vacancy_name
        """, ('%' + keyword.lower() + '%',))
        # Получаем результат запроса в виде списка кортежей
        result = self.cur.fetchall()
        # Возвращаем результат
        return result