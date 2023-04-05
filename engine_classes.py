from abc import ABC, abstractmethod
from connector import Connector
import requests
import os

my_api_key: str = os.getenv('SJ_API_KEY')


class Engine(ABC):
    @abstractmethod
    def get_request(self, keyword: str) -> str:
        """
        This function makes a request to the API and returns the response.

        Args:
            keyword: The keyword to search for.

        Returns:
            The response from the API.
        """
        pass

    @staticmethod
    def get_connector(file_name: str) -> Connector:
        """
        Get a connector for the given file name.

        Args:
            file_name: The name of the file to get a connector for.

        Returns:
            A connector for the given file name.
        """
        connector = Connector(file_name)
        return connector

    def rec_vacancies(self, file_name: str, vacancies: list) -> None:
        """
        The function records vacancies in the file

        :param file_name: name of the file
        :param vacancies: list of vacancies
        :return: None
        """
        connector = self.get_connector(file_name)
        connector.insert(vacancies)

class HH(Engine):

    @staticmethod
    def _get_salary(salary_info: dict) -> int:
        """
        Get salary from salary_info dict

        :param salary_info: dict with salary info
        :return: int salary
        """
        if salary_info:
            if salary_info.get('to'):
                return salary_info['to']
            if salary_info.get('from'):
                return salary_info['from']
        return 0

    @staticmethod
    def _get_remote_work(remote_work_info: dict) -> str:
        """
        Get remote work type from remote work info.

        Args:
            remote_work_info: Remote work info.

        Returns:
            Remote work type.
        """
        if remote_work_info:
            if remote_work_info['id'] == 'fullDay':
                return 'В офисе'
            if remote_work_info['id'] == 'remote':
                return 'Удаленно'
        return 'Другое'

    def get_request(self, keyword: str) -> list:
        """
        Get vacancies from hh.ru

        :param keyword: search keyword
        :return: list of vacancies
        """
        vacancies = []
        for page in range(5):
            response = requests.get(f'https://api.hh.ru/vacancies?text={keyword}', params={'per_page': 100, 'page': page}).json()
            for vacancy in response['items']:
                vacancies.append({
                    'name': vacancy['name'],
                    'company_name': vacancy['employer']['name'],
                    'url': vacancy['alternate_url'],
                    'description': vacancy['snippet']['requirement'],
                    'remote_work': self._get_remote_work(vacancy.get('schedule', {})),
                    'salary': self._get_salary(vacancy.get('salary', {})),
                })
        return vacancies


class SuperJob(Engine):

    @staticmethod
    def _get_salary(salary_info: dict):
        if salary_info.get('payment_to'):
            return salary_info['payment_to']
        if salary_info.get('payment_from'):
            return salary_info['payment_from']
        return 0

    @staticmethod
    def _get_remote_work(remote_work_info: dict) -> str:
        """
        Get remote work info

        :param remote_work_info: remote work info
        :return: remote work info
        """
        if remote_work_info:
            if remote_work_info['id'] == 1:
                return 'В офисе'
            if remote_work_info['id'] == 2:
                return 'Удаленно'
        return 'Другое'

    def get_request(self, keyword: str) -> list:
        """
        Get vacancies from SuperJob API

        :param keyword: search keyword
        :return: list of vacancies
        """
        vacancies = []
        for page in range(5):
            response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers={'X-Api-App-Id': my_api_key},
                                    params={'keywords': keyword, 'count': 100,
                                            'page': page}).json()
            for vacancy in response['objects']:
                vacancies.append({
                    'name': vacancy['profession'],
                    'company_name': vacancy['firm_name'],
                    'url': vacancy['link'],
                    'description': vacancy['candidat'],
                    'remote_work': self._get_remote_work(vacancy.get('place_of_work', {})),
                    'salary': self._get_salary(vacancy),
                })
        return vacancies