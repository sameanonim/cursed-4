import json

class Vacancy:
    __slots__ = ('name', 'url', 'description', 'salary', 'date_published', 'remote_work')

    def __init__(self, name, company, url, description, salary, date_published, remote_work, *args):
        self.name = name
        self.company = company
        self.url = url
        self.description = description
        self.salary = salary
        self.date_publised = date_published
        self.remote_work = remote_work

    def __repr__(self):
        return f'Наименование вакансии: {self.name}\nРаботодатель: {self.company_name}\nСсылка на вакансию:' \
               f' {self.url}\nОписание вакансии: {self.description}\nМесто работы: {self.remote_work}\nЗарплата:' \
               f' {self.salary}\n'

    def __gt__(self, other):
        return self.salary > other.salary

class CountMixin:

    def __init__(self, file_name=None):
        self.file_name = file_name

    @property
    def get_count_of_vacancy(self):

        with open(self.file_name, 'r', encoding="UTF-8") as file:
            data = json.load(file)
            count = 0
            for i in data:
                count += 1
        return count