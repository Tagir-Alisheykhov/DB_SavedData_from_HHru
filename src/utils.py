import json
import os

from src.db_manager import DBManager

from src.config import config
from src.data_from_api import SearchEmployersHHAPI, EmployersInfoHHAPI, EmployerVacancies


companies_list = [
    {"name": "IT-компания Xpage", "id": "702774"},
    # {"name": "IT-Компания АБС", "id": "740349"},
    # {"name": "IT-компания ДиалогСофт", "id": "1800345"},
    # {"name": "IT-компания Рациональные Решения", "id": "90010"},
    # {"name": "IT курсы EasyUM", "id": "3901159"},
    # {"name": "IT-Лидер", "id": "3487796"},
    # {"name": "IT-парк Питерский мостик", "id": "2570550"},
    # {"name": "IT-Сервис", "id": "3735331"},
    # {"name": "Компьютерная Академия IT STEP", "id": "3666820"},
    # {"name": "ИнтерКом IT", "id": "8958190"}
]


def data_for_interface():
    """

    :return:
    """
    employer_info = ""
    vacancies_list_info = ""
    avg_salary_vacancies = ""

    for emp_id in companies_list:
        # api_key = os.getenv('HH_API_KEY')
        # list_companies = list()

        # search_emp = SearchEmployersHHAPI()
        # print(search_emp.connecting_api())
        #     ----------------------------------------
        # Следующая логика обрабатывает только одного работодателя.
        print()
        print("-----------------------------------------------")
        print()
        data_from_api = EmployersInfoHHAPI(emp_id["id"])
        employer_data = data_from_api.connecting_api()
        employer_data, vacancies_url = employer_data
        # employer_info = employer_data
        # print(json.dumps(employer_data, indent=2, ensure_ascii=False))
        # print()

        #     ----------------------------------------
        # Здесь нужно вывести все вакансии (и желательно avg_salary)
        vacancies = EmployerVacancies(vacancies_url=vacancies_url)
        vacancies_list = vacancies.connecting_api()
        vacancies_list_info = vacancies_list
        # print(json.dumps(vacancies_list, indent=4, ensure_ascii=False))
        # print()

        #     ----------------------------------------
        vacancies.avg_salary_vacancies = vacancies_list
        avg_salary = vacancies.avg_salary_vacancies
        avg_salary_vacancies = avg_salary
        # print(avg_salary)

    return employer_info, vacancies_list_info, avg_salary_vacancies


# def connecting_db():
#     """
#     Соединение с базой данных PostgreSQL
#     :return:
#     """
#     params = config()
#
#     create_db = CreateDB()
