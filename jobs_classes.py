import json


class Vacancy:
    '''Вывод информации, полученной из вакансии, в удобном для пользователя формате'''
    __slots__ = ('name', 'company_name', 'url', 'description', 'remote_work', 'salary')

    def __init__(self, name: str, company_name: str, url: str, description: str, remote_work: bool, salary: str, *args):
        """
        Initialize the class

        :param name:
        :param company_name:
        :param url:
        :param description:
        :param remote_work:
        :param salary:
        :param args:
        """
        self.name = name
        self.company_name = company_name
        self.url = url
        if type(description) == str:
            self.description = description[:200]
        else:
            self.description = description
        self.remote_work = remote_work
        self.salary = salary
        super().__init__(*args)

    def __repr__(self):
        return f'Наименование вакансии: {self.name}\nРаботодатель: {self.company_name}\nСсылка на вакансию:' \
               f' {self.url}\nОписание вакансии: {self.description}\nМесто работы: {self.remote_work}\nЗарплата:' \
               f' {self.salary}\n'

    def __gt__(self, other) -> bool:
        """
        Compare two employees by salary.

        Args:
            other: The other employee to compare to.

        Returns:
            True if the salary of this employee is greater than the salary of the other employee.
        """
        return self.salary > other.salary


class CountMixin:
    """Возвращает количество вакансий из файла с вакансиями"""

    def __init__(self, file_name: str = None) -> None:
        """
        Initialize the file name

        :param file_name: The name of the file
        :type file_name: str
        """
        self.file_name = file_name

    def get_count_of_vacancy(self) -> int:
        """
        This function returns the number of vacancies in the file
        :return: int
        """

        with open(self.file_name, "r", encoding="UTF-8") as file:
            data = json.load(file)
            count = 0
            for i in data:
                count += 1
        return count
