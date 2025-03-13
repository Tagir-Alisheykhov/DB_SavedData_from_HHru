import json
import os

from src.connecting_api import EmployersInfoHHAPI, EmployerVacancies
from src.file_processing import SaveEmpInfoJSON, SaveVacanciesJSON
from src.processing_vacancies import VacancyProcessing


companies_list = [
    {"name": "MediaNation", "id": "584898"},
    {"name": "Multilogin Software Ltd.", "id": "5034722"},
    {"name": "IT-компания Xpage", "id": "702774"},
    {"name": "IT-Компания АБС", "id": "740349"},
    {"name": "IT-компания Рациональные Решения", "id": "90010"},
    {"name": "IT курсы EasyUM", "id": "3901159"},
    {"name": "IT-Лидер", "id": "3487796"},
    {"name": "IT-парк Питерский мостик", "id": "2570550"},
    {"name": "IT-Сервис", "id": "3735331"},
    {"name": "ИП Храмшин Тимур Раисович", "id": "9074163"},
]


query_design = (
    """CREATE TABLE employers
           (
           employer_id INT,
           name VARCHAR(50),
           accredited_it_employer BOOL NOT NULL ,
           area VARCHAR NOT NULL,
           open_vacancies INT NOT NULL,
           description TEXT,
           CONSTRAINT pk_employers_employer_id PRIMARY KEY (employer_id)
           );
           CREATE TABLE vacancies 
           (
           vacancy_id INT,
           employer_id INT NOT NULL,
           type VARCHAR(40) NOT NULL,
           published_at_date DATE,
           published_at_time TIME,
           city VARCHAR(40),
           address VARCHAR(50),
           experience VARCHAR(25),
           professional_roles VARCHAR(60),
           schedule VARCHAR(25),
           salary INT,
           work_format VARCHAR(25),
           working_hours VARCHAR(40),
           work_schedule_by_days VARCHAR(40),
           url TEXT,
           description TEXT,
           CONSTRAINT pk_vacancies_vacancy_id PRIMARY KEY (vacancy_id)
           );
           ALTER TABLE vacancies 
           ADD CONSTRAINT fk_vacancies_vacancy_id 
           FOREIGN KEY(employer_id) REFERENCES employers(employer_id);
           """
)


def data_to_insert() -> tuple[list, list]:
    """
    Функция для подключения к APi и обработки
    данных в пригодный формат.
    :return:
    """
    print("Данные обрабатываются.")
    query_insert_employer = []
    query_insert_vacancies = []

    for emp_id in companies_list:
        # -----------------------------
        # Подключение к API (EMPLOYERS)
        data_from_api = EmployersInfoHHAPI(emp_id["id"])
        employer_data = data_from_api.connecting_api()
        # Записываем данные о работодателе в файл
        save_emp_info = SaveEmpInfoJSON(employer_data)
        save_emp_info.write_data_json()
        # Чтение данных о работодателе.
        employer_data = save_emp_info.read_data_json
        # Запись обработанных данных в переменные
        employer_data, vacancies_url = employer_data
        query_insert_employer.append(tuple(employer_data.values()))
        # -----------------------------
        # Подключение к API (VACANCIES)
        vacancies = EmployerVacancies(vacancies_url=vacancies_url)
        # Записываем вакансии в файл
        vacancies = vacancies.connecting_api()
        # print(json.dumps(vacancies, indent=4, ensure_ascii=False))
        saved_vacancies = SaveVacanciesJSON(vacancies)
        saved_vacancies.write_data_json()
        # Чтение данных из файла
        read_vacancies = saved_vacancies.read_data_json
        # Форматирование списка вакансий
        formatted_vacancies = VacancyProcessing(read_vacancies, keyword=None)
        vacancies_list = formatted_vacancies.formatter_vacancies()
        for vacancy in vacancies_list:
            query_insert_vacancies.append(tuple(vacancy.values()))

    return query_insert_employer, query_insert_vacancies


def user_interface(
        get_companies_and_vacancies_count,
        get_all_vacancies,
        get_avg_salary,
        get_vacancies_with_higher_salary,
):

    pass
