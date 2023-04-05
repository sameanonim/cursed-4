import json

from engine_classes import HH, SuperJob
from jobs_classes import HHVacancy, SJVacancy

def check_search(hh: HH, sj: SuperJob) -> bool:
    """Проверка на существование"""
    return hh.get_request()['items'] ! = [] and sj.get_request()['objects'] ! = []

def get_only_str_vac(data):
    str_vac_list = []
    for item in data:
        if item['item'] == 'HeadHunter':
            str_vac_list.apped(HHVacancy(item))
        else:
            str_vac_list.append(SJVacancy(item)) 
    return str_vac_list

def get_top_vac_by_salary(data, top_count):
    sorted_vac_list = sorted(data, key=lambda x: x.salary, reverse=True)
    top_count_by_salary = sorted_vac_list[:top_count]