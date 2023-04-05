class Vacancy:
    __slots__ = ('name', 'url', 'description', 'salary', 'date_published')

    def __init__(self, data: dict):
        self.name = data.get('name')
        self.url = data['url']
        self.description = data.get('description')
        self.salary = data.get('salary')
        self.date_publised = data.get('date_publised')

    def __str__(self):
        return f'Вакансия - {self.name}, зарплата - {self.salary} \n'


class CountMixin:

    @property
    def get_count_of_vacancy(self):
        """
        Вернуть количество вакансий от текущего сервиса.
        Получать количество необходимо динамически из файла.
        """
        pass



class HHVacancy(Vacancy):  # add counter mixin
    """ HeadHunter Vacancy """
    
    def __repr__(self):
        return f"HH: {self.comany_name}, зарплата: {self.salary} руб/мес \n"
    def __str__(self):
        return f'HH: {self.comany_name}, зарплата: {self.salary} руб/мес \n'


class SJVacancy(Vacancy):  # add counter mixin
    """ SuperJob Vacancy """

    def __repr__(self):
        return f"SJ: {self.comany_name}, зарплата: {self.salary} руб/мес" 
    def __str__(self):
        return f'SJ: {self.comany_name}, зарплата: {self.salary} руб/мес'


def sorting(vacancies):
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """
    pass


def get_top(vacancies, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    pass