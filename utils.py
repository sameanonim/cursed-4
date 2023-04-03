import requests

responce = requests.get("https://api.hh.ru/vacancies?text=python&area=ru&sort=popularity&per_page=100")
print(responce.text)