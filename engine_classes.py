from abc import ABC, abstractmethod
import os
import requests
import json
from connector import Connector

class Engine(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_request(self):
        pass

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        return Connector(file_name)


class HH(Engine):
    URL = 'https://api.hh.ru/vacancies'

    def __init__(self, search_keyword):
        super().__init__()
        self.params = {
            'text': f'{search_keyword}',
            'per_page': 100,
            'area': 113,
            'page': 0
        }
        

    def get_request(self):
        """
        парсим данные с ресурса HeadHunter
        """
        responce = requests.get(self.URL, params=self.params)
        data = responce.content.decode('utf-8')
        responce.close()

        js_hh = json.load(data)
        return js_hh

    def get_info_vacancy(self, data):
        info = {
            'from': 'Headhunter',
            'name': data.get('name'),
            'url': data.get('alternate_url'),
            'description': data.get('sniplet').get('responsibility'),
            'salary': data.get('salary'),
            'date_published': data.get('published_at'),
            'expirience': data.get('expirience'),
            'page_number': data.get('page')
        }

    @property
    def get_vacancies(self):
        """
        получаем вакансии
        """
        vacancies = []
        while len(vacancies) <= 500:
            data = self.get_request()
            items = data.get('items')
            if not items:
                break
            for vacancy in items:
                if vacancy.get('salary') is not None and vacancy.get('salary').get('currency') == 'RUB':
                    vacancies.append(self.get_info_vacancy(vacancy))
        return vacancies


class SuperJob(Engine):
    URL = 'https://api.superjob.ru/2.0/vacancies/'

    def __init__(self, search_keyword):
        super().__init__()
        self.params = {'keywords': f'{search_keyword}', 'count': 100, 'page': 0}


    def get_request(self):
        self.HEADERS = {
            'Host': 'api.superjob.ru',
            'X-Api-App-Id': os.getenv('SJ_API_KEY'),
            'Authorization': 'Bearer r.000000010000001.example.access_token',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.get(self.URL, headers=self.HEADERS, params=self.params)  # .json()
        data = response.content.decode()
        response.close()
        js_sj = json.loads(data)
        return js_sj

    def get_info_vacancy(self, data):
        info = {
            'from': 'SuperJob',
            'name': data['profession'],
            'url': data['link'],
            'description': data.get('client').get('description'),
            'salary': data['currency'],
            'date_published': data['date_published']

        }
        return info

    @property
    def get_vacancies(self):
        """Записывает информацию о вакансии в список при наличии сведений о ЗП в рублях"""
        vacancies = []
        while len(vacancies) <= 500:
            data = self.get_request()
            objects = data['objects']
            if not objects:  # Если нет вакансий на странице, выход из цикла
                break
            for vacancy in objects:
                if vacancy.get('payment_from') is not None and vacancy.get('currency') == 'rub':
                    vacancies.append(self.get_info_vacancy(vacancy))

            self.params['page'] += 1  # Увеличиваем значение параметра 'page' после обработки всех вакансий на текущей странице

        print(len(vacancies))
        return vacancies

class Connector(Engine):
    pass