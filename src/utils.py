import json
import os

from src.db_manager import DBManager

from src.config import config
from src.connecting_api import SearchEmployersHHAPI, EmployersInfoHHAPI, EmployerVacancies
from src.file_processing import SaveEmpInfoJSON, SaveVacanciesJSON
from src.processing_vacancies import VacancyProcessing, VacanciesSalaryAVG

companies_list = [
    {"name": "IT-компания Xpage", "id": "702774"},
    {"name": "IT-Компания АБС", "id": "740349"},
    {"name": "IT-компания ДиалогСофт", "id": "1800345"},
    {"name": "IT-компания Рациональные Решения", "id": "90010"},
    {"name": "IT курсы EasyUM", "id": "3901159"},
    {"name": "IT-Лидер", "id": "3487796"},
    {"name": "IT-парк Питерский мостик", "id": "2570550"},
    {"name": "IT-Сервис", "id": "3735331"},
    {"name": "Компьютерная Академия IT STEP", "id": "3666820"},
    {"name": "ИнтерКом IT", "id": "8958190"}
]


def data_for_interface():
    """

    :return:
    """
    print("Данные обрабатываются.")
    employer_info = ""
    vacancies_list_info = ""
    avg_salary_vacancies = ""

    for emp_id in companies_list:
        # api_key = os.getenv('HH_API_KEY')
        # list_companies = list()

        # search_emp = SearchEmployersHHAPI()
        # print(search_emp.connecting_api())
        #     ----------------------------------------

        # Подключение к API
        data_from_api = EmployersInfoHHAPI(emp_id["id"])
        employer_data = data_from_api.connecting_api()
        # Записываем данные о работодателе в файл
        save_emp_info = SaveEmpInfoJSON(employer_data)
        save_emp_info.write_data_json()
        # Чтение данных о работодателе.
        employer_data = save_emp_info.read_data_json
        # Запись обработанных данных в переменные
        employer_data, vacancies_url = employer_data
        employer_info = employer_data
        # print(json.dumps(employer_data, indent=2, ensure_ascii=False))
        # print()
        #     ----------------------------------------
        # Подключение к API
        vacancies = EmployerVacancies(vacancies_url=vacancies_url)
        # Записываем вакансии в файл
        vacancies = vacancies.connecting_api()
        # print(json.dumps(vacancies, indent=4, ensure_ascii=False))
        saved_vacancies = SaveVacanciesJSON(vacancies)
        saved_vacancies.write_data_json()
        # Чтение данных из файла
        read_vacancies = saved_vacancies.read_data_json
        # Форматирование и фильтрация списка вакансий
        formatted_vacancies = VacancyProcessing(read_vacancies)
        vacancies_list = formatted_vacancies.formatter_vacancies()
        # print(json.dumps(vacancies_list, indent=4, ensure_ascii=False))
        vacancies_list_info = vacancies_list

    #     ----------------------------------------
    #   Определение средней зарплаты по вакансиям работодателя.
        detect_avg_salary = VacanciesSalaryAVG(vacancies_list)
        # print(detect_avg_salary.avg())


        # vacancies.avg_salary_vacancies = vacancies_list
        # avg_salary = vacancies.avg_salary_vacancies
        # avg_salary_vacancies = avg_salary
        # print(avg_salary)
    #
    return employer_info, vacancies_list_info, avg_salary_vacancies


# def connecting_db():
#     """
#     Соединение с базой данных PostgreSQL
#     :return:
#     """
#     params = config()
#
#     create_db = CreateDB()
