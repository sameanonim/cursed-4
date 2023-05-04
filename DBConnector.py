# импортируем модули для работы с конфигурационным файлом и базой данных
import configparser
import psycopg2

# создаем класс для чтения конфигурационного файла
class ConfigReader:
    # конструктор класса принимает имя файла
    def __init__(self, filename):
        # создаем объект для чтения конфигурационного файла
        self.config = configparser.ConfigParser()
        # читаем файл
        self.config.read(filename)

    # метод для получения данных подключения из секции [database]
    def get_connection_data(self):
        # возвращаем словарь с данными подключения
        return self.config['database']
    
class Database:
    # конструктор класса принимает словарь с данными подключения
    def __init__(self, connection_data):
        # формируем строку подключения к базе данных
        conn_string = f"host={connection_data['host']} port={connection_data['port']} dbname={connection_data['dbname']} user={connection_data['user']} password={connection_data['password']}"
        # подключаемся к базе данных
        self.conn = psycopg2.connect(conn_string)
        # создаем объект для выполнения SQL-запросов
        self.cur = self.conn.cursor()
    
    def __del__(self):
        self.cur.close()
        self.conn.close()

class ConnectDatabase(ConfigReader, Database):
    # конструктор класса принимает имя файла
    def __init__(self, filename):
        # вызываем конструктор ConfigReader для чтения файла
        ConfigReader.__init__(self, filename)
        # получаем данные подключения из файла
        connection_data = self.get_connection_data()
        # вызываем конструктор Database для подключения к базе данных
        Database.__init__(self, connection_data)

config_db = ConnectDatabase('config.ini')