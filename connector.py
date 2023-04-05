from datetime import datetime

import json
import os


class JSONOldException(Exception):
    '''Класс обработки ошибки при устаревании файла'''

    def __init__(self, *args):
        self.message = args[0] if args else 'Файл устарел'

    def __str__(self) -> str:
        """
        Return the message of the exception.
        """
        return self.message


class Connector:
    '''Класс коннектор к файлу в json формате'''

    __data_file = None

    def __init__(self, filename: str) -> None:
        """
        Initialize the class with the filename
        :param filename: The name of the file to read
        """
        self.__data_file = filename

    @property
    def data_file(self) -> str:
        """
        Returns the data file.

        :return: The data file.
        """
        return self.__data_file

    @data_file.setter
    def data_file(self, value: str) -> None:
        """
        Set the data file and connect to the database.

        :param value: The data file to use.
        """
        self.__data_file = value
        self.__connect()

    def __connect(self):
        '''Проверка на существование файла с данными и создание его при необходимости. Проверка на устаревание'''
        with open(self.__data_file, 'a+', encoding='utf8') as f:
            f.seek(0)
            first_line = f.readline()
            if first_line:
                try:
                    f.seek(0)
                    data = json.load(f)
                    assert type(data) == list
                    for i in data:
                        assert type(i["name"]) == str
                        assert type(i["company_name"]) == str
                        assert type(i["url"]) == str
                        assert type(i["remote_work"]) == str
                        assert type(i["salary"]) == int
                except:
                    raise JSONOldException()
            else:
                json.dump([], f)
        #Проверка на актуальность файла по времени
        if (datetime.now() - datetime.fromtimestamp(os.path.getmtime(self.__data_file))).days >= 1:
            raise JSONOldException()

    def insert(self, data):
        '''Запись данных в файл, если файл пустой. Добавление данных в файл, если в нем есть данные'''
        with open(self.__data_file, 'r', encoding='utf8') as f:
            file_data = json.load(f)

        if type(data) == dict:
            file_data.append(data)
        elif type(data) == list:
            file_data.extend(data)

        with open(self.__data_file, 'w', encoding='utf8') as f:
            json.dump(file_data, f, ensure_ascii=False, indent=4)

    def select(self, query):
        '''Выбор данных из файла с применением фильтрации'''
        search_key, search_value = query.items()[0]

        with open(self.__data_file, 'r', encoding='utf8') as f:
            file_data = json.load(f)

        result = []
        for vacancy in file_data:
            if vacancy[search_key] == search_value:
                result.append(vacancy)
        return result

    def delete(self, query):
        '''Удаление записей из файла, которые соответствуют запросу'''
        if not query:
            return

        del_key, del_value = list(query.items())[0]

        with open(self.__data_file, 'r', encoding='utf8') as f:
            file_data = json.load(f)

        non_del = []
        for vacancy in file_data:
            if vacancy[del_key] == del_value:
                pass
            else:
                non_del.append(vacancy)

        with open(self.__data_file, 'w', encoding='utf8') as f:
            json.dump(non_del, f, ensure_ascii=False, indent=4)