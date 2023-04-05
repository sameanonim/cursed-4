import json
import os

import json
import os

class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """
    data_file = None

    def __init__(self, file_path: str):
        self.data_file = file_path
        self.__connect

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        # тут должен быть код для установки файла
        self.__data_file = value
        self.__connect()

    def __connect(self):
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        Также проверить на деградацию и возбудить исключение
        если файл потерял актуальность в структуре данных
        """
        if not os.path.isfile("../filename.json"):
            raise FileNotFoundError("File filename.json not found")
        try:
            with open(self.__data_file, 'r', enconding='windows-1251') as file:
                json_reader = json.load(file)
                print(len(json_reader))
                for i in json_reader:
                    if i.get('name') < 0:
                        print('error')
                    else:
                        raise Exception
        except Exception:
            print('файл filename.json поверждён')


    def insert(self, path, data):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        with open(path, 'a', enconding='UTF-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False, skipkeys=True, sort_keys=True)

    def select(self, query: dict):
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """
        result = []
        with open(self.__data_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        if not query:
            return data
        
        for item in data:
            for key, value in query.items():
                if item.get(key) == value:
                    result.append(item)
        return result

    def delete(self, query):
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        if not query:
            return
        
        with open(self.__data_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        result = []
        for item in data:
            match = True
            for key, value in query.items():
                if item.get(key) != value:
                    match = False
                    break
            if match:
                result.append(item)
        
        with open(self.__data_file, 'w', encoding='utf-8') as file:
            for item in data:
                if item not in result:
                    json.dump(item, file)
                    file.write('\n')