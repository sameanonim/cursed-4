import json
from engine_classes import HH
from jobs_classes import Vacancy

# Константы для имени файла и количества вакансий
FILE_NAME = 'data_list.json'
TOP_COUNT = 10

# Функция для основной логики программы
def main():
    # Получаем от пользователя ключевое слово для поиска вакансий
    key_word = input('Введите вакансию для поиска: ').strip()

    hh = HH()
    response = hh.get_request(key_word)
    into_file_hh = hh.rec_vacancies(FILE_NAME, response)

    print(f'По вашему запросу собраны вакансии с HeadHunter.\nВыберите '
          f"дальнейшее действие:\nВывести список всех вакансий: нажмите s\nВывести {TOP_COUNT} самых высокооплачиваемых вакансий: "
          f"введите t\nВывести вакансии с возможностью удаленной работы: нажмите n\nЕсли вы хотите завершить программу: "
          f"нажмите q")

    # Открываем файл с данными
    with open(FILE_NAME, 'r', encoding='utf8') as f:
        vacancies_from_json = json.load(f)
        # Создаем список объектов класса Vacancy
        vacancy_subjects = [Vacancy(vac["name"], vac["company_name"], vac["url"], vac["description"], vac["remote_work"], vac["salary"]) for vac in vacancies_from_json]

    # Цикл для обработки ввода пользователя
    while True:
        user_choice = input().lower()

        if user_choice == 's':
            print('\n'.join(str(i) for i in vacancy_subjects))
            print('Введите следующую команду ')
        elif user_choice == 't':
            sorted_vacancies = sorted(vacancy_subjects, reverse=True)[:TOP_COUNT]
            print('\n'.join(str(i) for i in sorted_vacancies))
            print('Введите следующую команду ')
        elif user_choice == 'n':
            remote_vacancies = list(filter(lambda i: i.remote_work == 'Удаленно', vacancy_subjects))
            print('\n'.join(str(rem) for rem in remote_vacancies))
            print('Введите следующую команду ')
        elif user_choice == 'q':
            break
        else:
            print('Команда не распознана. Попробуйте еще раз или нажмите q для завершения программы')

    print('Завершение программы')

# Вызываем функцию main()
if __name__ == '__main__':
    main()