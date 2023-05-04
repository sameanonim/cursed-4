import json
from engine_classes import HH
from jobs_classes import Vacancy

# Константы для имени файла и количества вакансий
FILE_NAME = 'data_list.json'
TOP_COUNT = 10

# Класс для основной логики программы
class DownloadDatafromHH:
    def __init__(self):
        # Получаем от пользователя ключевое слово для поиска вакансий
        self.key_word = input('Введите вакансию для поиска: ').strip()
        self.hh = HH()
        self.response = self.hh.get_request(self.key_word)
        self.into_file_hh = self.hh.rec_vacancies(FILE_NAME, self.response)
        # Открываем файл с данными
        with open(FILE_NAME, 'r', encoding='utf8') as f:
            vacancies_from_json = json.load(f)
            # Создаем список объектов класса Vacancy
            self.vacancy_subjects = [Vacancy(vac["name"], vac["company_name"], vac["url"], vac["description"], vac["remote_work"], vac["salary"]) for vac in vacancies_from_json]

    def print_end(self):
        print('Завершение программы')

# Создаем объект класса Main и вызываем его метод print_end()
main = DownloadDatafromHH()
main.print_end()