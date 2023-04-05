import json
import os
import datetime

class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """
    __data_file = None

    def __init__(self, filename: str):
        self.data_file = filename

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