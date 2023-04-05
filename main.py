from engine_classes import Engine, HH, SuperJob
from jobs_classes import Vacancy, HHVacancy, SJVacancy
from utils import check_search, get_only_str_vac, get_top_vac_by_salary
from operator import itemgetter
import os

# Получение вакансий с разных платформ
def main():

    path = os.path.join('.filename.json')
    connector = Engine.get_connector(path)  # создаем экземпляр класса Connector функцией get_connector из класса Engine

    search_keyword = input('Введите ключевое слово поиска')

    hh = HH(search_keyword)
    sj = SuperJob(search_keyword)
    if check_search(hh, sj):
        all_vacancies = hh.get_vacancies + sj.get_vacancies
        connector.insert(path, all_vacancies)
        print(type(all_vacancies))
        print(all_vacancies[0])
        sorted(all_vacancies, key=itemgetter('date_published'))

if __name__ == '__main__':
    main()