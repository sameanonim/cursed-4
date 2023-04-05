import json
from engine_classes import SuperJob, HH
from jobs_classes import Vacancy

#Получаем от пользователя ключевое слово для поиска вакансий
key_word = input('Введите вакансию для поиска: ').strip()


hh = HH()
response = hh.get_request(key_word)
into_file_hh = hh.rec_vacancies('data_list.json', response)


s = SuperJob()
response = s.get_request(key_word)
into_file_sj = s.rec_vacancies('data_list.json', response)


print('По вашему запросу собрано 500 вакансий с сайта SuperJob и 500 вакансий с сайта HeadHunter.\nВыберите '
      "дальнейшее действие:\nВывести список всех вакансий: нажмите s\nВывести 10 самых высокооплачиваемых вакансий: "
      "введите top\nВывести вакансии с возможностью удаленной работы: нажмите n\nЕсли вы хотите завершить программу: "
      "нажмите q")


with open('data_list.json', 'r', encoding='utf8') as f:
    vacancies_from_json = json.load(f)
    vacancy_subjects = []
    for vac in vacancies_from_json:
        v = Vacancy(vac["name"], vac["company_name"], vac["url"], vac["description"], vac["remote_work"], vac["salary"])
        vacancy_subjects.append(v)


user_choice = input()

while user_choice != 'q':
    if user_choice == 's':
        for i in vacancy_subjects:
            print(i)
        user_choice = input('Введите следующую команду ')
    if user_choice == 'top':
        sorted_vacancies = sorted(vacancy_subjects, reverse=True)[:10]
        for i in sorted_vacancies:
            print(i)
        user_choice = input('Введите следующую команду ')
    if user_choice == 'n':
        remote_vacancies = []
        for i in vacancy_subjects:
            if i.remote_work == 'Удаленно':
                remote_vacancies.append(i)
        for rem in remote_vacancies:
            print(rem)
        user_choice = input('Введите следующую команду ')
    else:
        print('Команда не распознана. Попробуйте еще раз или нажмите q для завершения программы')
        user_choice = input()

print('Завершение программы')