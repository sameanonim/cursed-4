import psycopg2
import json
from main_postgres import main

# запускает программу из main_postgres.py и затем открываем файл data_list.json и загружаем данные в переменную vacancies
main()
with open("data_list.json", "r", encoding='utf-8') as f:
    vacancies = json.load(f)

# создаём соединение с БД
conn = psycopg2.connect(dbname='hh', user='postgres', password='26111989', host='localhost', port='5433')
# создаём курсор для выполнения SQL-запросов
cur = conn.cursor()

# Создаем таблицу employers с полями: id, name, url, description
cur.execute("""
    CREATE TABLE employers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        url VARCHAR(255) NOT NULL,
        description TEXT
    )
""")


# Создаем таблицу vacancies с полями: id, name, url, description, remote_work, salary
# Поле employer_id ссылается на поле id таблицы employers
cur.execute("""
    CREATE TABLE vacancies (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        company_name VARCHAR(255) NOT NULL,
        url VARCHAR(255) NOT NULL,
        description TEXT,
        remote_work TEXT,
        salary INTEGER
    )
""")

# Для каждого словаря в списке
for vacancy in vacancies:
    # Получаем данные о вакансии из словаря
    vacancy_name = vacancy['name']
    vacancy_company_name = vacancy['company_name']
    vacancy_url = vacancy['url']
    vacancy_description = vacancy['description']
    if vacancy['remote_work']:
        vacancy_remote_work = vacancy['remote_work']
    else:
        vacancy_remote_work = None
    # Если в словаре есть данные о зарплате, то получаем их, иначе присваиваем None
    if vacancy['salary']:
        vacancy_salary = vacancy['salary']
    else:
        vacancy_salary = None

    # Проверяем, есть ли работодатель с таким именем в таблице employers
    cur.execute("""
        SELECT id FROM employers WHERE name = %s
    """, (vacancy_company_name,))

    # Получаем результат выборки или None, если такого работодателя нет
    employer_id = cur.fetchone()

    # Если такого работодателя нет, то добавляем его в таблицу employers и получаем его идентификатор
    if employer_id is None:
        cur.execute("""
            INSERT INTO employers (name, url)
            VALUES (%s, %s)
            RETURNING id
        """, (vacancy_company_name, vacancy_url))

        employer_id = cur.fetchone()

    # Добавляем запись в таблицу vacancies с данными о вакансии и ссылкой на работодателя по его идентификатору
    cur.execute("""
    INSERT INTO vacancies (name, company_name, url, description, remote_work, salary)
    VALUES (%s, %s, %s, %s, %s, %s)
""", (vacancy_name, vacancy_company_name, vacancy_url, vacancy_description,
      vacancy_remote_work, vacancy_salary))

# Сохраняем изменения в БД
conn.commit()
# Закрываем соединение с БД
conn.close()