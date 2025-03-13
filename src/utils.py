import re
import time
import pandas as pd

from src.connecting_api import EmployersInfoHHAPI, EmployerVacancies
from src.db_manager import DBManager
from src.file_processing import SaveEmpInfoJSON, SaveVacanciesJSON, ReadCompaniesList
from src.processing_vacancies import VacancyProcessing


def data_to_insert() -> tuple[list, list]:
    """
    Функция для подключения к APi и обработки
    данных в пригодный формат.
    :return:
    """
    print("Данные обрабатываются.")
    query_insert_employer = []
    query_insert_vacancies = []
    companies_list = ReadCompaniesList().read_data_json

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


def user_interface(db_manager: DBManager) -> str:
    """
    Интерфейс для взаимодействия пользователя
    с программой.
    :param db_manager: Объект класса DBManager для взаимодействия с БД.
    """
    mes1, mes2, mes3 = program_message()
    print(mes1)
    print(mes2)
    cycle_true = True
    try:
        while cycle_true:
            user_answer = input("Введите число(а) от 1 до 5: \n")
            print("-------------------------------")
            user_answer = re.findall(r"[12345]", user_answer)
            if not user_answer or user_answer == []:
                print(f"Я не знаю такой команды. \nДоступны следующие команды:\n{mes2}")
                continue
            else:
                print(f'Вы ввели: {", ".join(set(user_answer))}\n')
                for value in set(user_answer):
                    if value == "1":
                        print(db_manager.get_companies_and_vacancies_count)
                    elif value == "2":
                        print(db_manager.get_all_vacancies)
                    elif value == "3":
                        print(db_manager.get_avg_salary)
                    elif value == "4":
                        print(db_manager.get_vacancies_with_higher_salary)
                    elif value == "5":
                        keyword = input("Введите ключевое слово для поиска вакансий: ")
                        keyword = re.findall(r"\w+", keyword)
                        keyword = " ".join(keyword)
                        get_vacancies = db_manager.get_vacancies_with_keyword(keyword.strip())
                        (print(get_vacancies) if isinstance(get_vacancies, pd.DataFrame)
                                         else print("\nЯ таких слов не знаю.. (-_-) "))
                print(mes3)
    except KeyboardInterrupt:
        return "\nПрограмма завершена пользователем."
    except Exception as err:
        print(f"Возникла ошибка: {err}")


def program_message() -> tuple[str, str, str]:
    """
    Сообщения для пользовательского интерфейса
    :return:
    """
    mes1 = ("Добро пожаловать в программу для взаимодействия с базой данных!\n"
           "Пожалуйста, введите одну или несколько команд представленных ниже:\n")
    time.sleep(1)
    mes2 = (">> `1` -Получить список всех компаний и количество вакансий у каждой компании.\n"
          ">> `2` -Получить информацию о всех вакансиях в сжатом виде.\n"
          ">> `3` -Получить среднюю зарплату по вакансиям.\n"
          ">> `4` -Получить список всех вакансий, у которых зарплата выше средней.\n"
          ">> `5` -Получить список всех вакансий по ключевому слову.\n")
    mes3 = ("\n--------------------------------------------------------------------------------------------"
      "\nДля выхода из программы (TERMINAL) зажмите/нажимайте `Ctrl + C` (В `RUN` кликни на `STOP`)\n"
      "--------------------------------------------------------------------------------------------\n")
    return mes1, mes2, mes3


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
