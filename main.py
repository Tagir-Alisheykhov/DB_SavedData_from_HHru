import json
import os
from time import time

from src.db_manager import DBManager
from src.data_from_api import SearchEmployersHHAPI, EmployersInfoHHAPI, EmployerVacancies
from src.utils import data_for_interface

if __name__ == '__main__':
    start_time = time()
    # -----------------

    employer_info, vacancies_list_info, avg_salary_vacancies = data_for_interface()

    # -----------------
    end_time = time()
    def_time = end_time - start_time
    print(f'Время выполнения программы: \n{def_time}')




#
#
#
#
#     # api_key = os.getenv('HH_API_KEY')
#     # list_companies = list()
#
#     # search_emp = SearchEmployersHHAPI()
#     # print(search_emp.connecting_api())
#
#     # Следующая логика обрабатывает только одного работодателя.
#     # (Нужно будет использовать цикл для всех работодателей)
#     #     ----------------------------------------
#     # Выводим данные каждого работодателя
#     # data_from_api = EmployersInfoHHAPI()
#     # employer_data = data_from_api.connecting_api()
#     # employer_data, vacancies_url = employer_data
#     # print(json.dumps(employer_data, indent=2, ensure_ascii=False))
#     # print()
#
# #     ----------------------------------------
#     # # Здесь нужно вывести все вакансии (и желательно avg_salary)
#     # vacancies = EmployerVacancies(vacancies_url=vacancies_url)
#     # vacancies_list = vacancies.connecting_api()
#     # print(json.dumps(vacancies_list, indent=4, ensure_ascii=False))
#     # print()
#
# #     ----------------------------------------
#     # vacancies.avg_salary_vacancies = vacancies_list
#     # avg_salary = vacancies.avg_salary_vacancies
#     # print(avg_salary)
#

#
#
#
#
#
#     # ЧТО НУЖНО СДЕЛАТЬ: ДОФО



# OPEN QUESTIONS
# ------------------------------------------------------------------------------
#       Исходя из условия, нужно выводить также список вакансий каждого работодателя
#       связывать их можно в Postgres по ID.
#       Видимо все таки нужно вывести отдельный класс, т.к.
#       возможно нужен будет класс наследник для вывода вакансий.
#       А среднее значение можно добавлять в main или utils.
#       Для связки ID также в main или utils, можно функцию (в utils будет корректней)
#
# ------------------------------------------------------------------------------
#      Необходимо сделать условие, если есть industries_name, то выводим его,
#      если нет, то выводим description.
#      - description - использовать регулярные выражения
#      Необходимо захватить информацию, только которая внутри <p>

# ------------------------------------------------------------------------------
#      Возможно нужно не удалять, а просто создать новый массив с данными.
#      для эффективности нужно вычислить время выполнения

# ------------------------------------------------------------------------------
#      А среднее значение можно добавлять в main или utils.
#      Для связки ID также в main или utils, можно функцию (в utils будет корректней)
#
# ------------------------------------------------------------------------------
#      Файл database.ini нужно добавить в .gitignore
#
# ------------------------------------------------------------------------------

