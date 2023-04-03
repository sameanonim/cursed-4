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
    def get_request(self):
        pass

class Connector(Engine):
