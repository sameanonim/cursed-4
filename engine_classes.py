from abc import ABC, abstractmethod
import os
import requests

class Engine(ABC):
    @abstractmethod
    def get_request(self):
        pass

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        pass


class HH(Engine):
    def __init__(self):
        pass

    def get_request(self):
        """
        парсим данные с ресурса HeadHunter
        """
        my_auth_data = {'X-Api-App-Id': os.environ['HH_API_KEY']}
        url = 'https://api.hh.ru/vacancies?text=' + self.word
        vacancies_list_hh = []
        for item in range(1):
            requests_hh = requests.get(url, headers=my_auth_data,
                                       params={"keywords": self.word, 'page': item}).json()['items']
            for item2 in requests_hh:
                if item2["salary"] is None:
                    item2["salary"] = {}
                    item2["salary"]["from"] = 0
                    item2["salary"]["to"] = 0
                if item2["salary"]["from"] is None:
                    item2["salary"]["from"] = 0
                if item2["salary"]["to"] is None:
                    item2["salary"]["to"] = 0
                if item2["salary"]["from"] > item2["salary"]["to"]:
                    tnp = item2["salary"]["from"]
                    item2["salary"]["from"] = item2["salary"]["to"]
                    item2["salary"]["to"] = tnp
                vacancies_list_hh.append(item2)
        return vacancies_list_hh

class SuperJob(Engine):
    def __init__(self, api_key):
        self.api_key = api_key

    def get_request(self):
        my_auth_data = {'X-Api-App-Id': os.environ['SJ_API_KEY']}
        url = 'https://api.superjob.ru/2.0/vacancies'
        vacancies_list_sj = []
        for item in range(1):
            requests_sj = requests.get(url, headers=my_auth_data,
                                       params={"keywords": self.word, 'page': item}).json()['objects']
            for item2 in requests_sj:
                if item2['payment_from'] is None:
                    item2['payment_from'] = 0
                if item2['payment'] is None:
                    item2['payment'] = 0
                if item2['payment_from'] > item2['payment_to']:
                    tmp = item2['payment_from']
                    item2['payment_from'] = item2['payment_to']
                    item2['payment_to'] = tmp
                vacancies_list_sj.append(item2)
        return vacancies_list_sj

class Connector(Engine):
    pass