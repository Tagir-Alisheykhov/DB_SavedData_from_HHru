import json
from time import time

import pandas as pd

from src.connecting_api import SearchEmployersHHAPI
from src.db_manager import DBManager
from src.utils import data_to_insert, query_design, user_interface
from src.config import config, sensitive_env


def main() -> None:
    """
    Основная функция для объединения и вызова
    всего функционала программы.
    :return:
    """
    # # Отладка
    # search = SearchEmployersHHAPI()
    # result = search.connecting_api()
    # print(json.dumps(result, indent=4, ensure_ascii=False))


    # ------------------------------------------
    # Подключение к API и обработка данных.
    employers, vacancies = data_to_insert()

    # Загрузка параметров для подключения к БД.
    params = config() | sensitive_env()
    dbname = params["database"]
    del params["database"]

    # Подключение к менеджеру для работы с БД.
    db_manager = DBManager(params=params, dbname=dbname)
    db_manager.create(new_db_name="head_hunter")
    db_manager.design(query=query_design)
    db_manager.insert(employers=employers, vacancies=vacancies)
    # ------------------------------------------


    # user_interface(
    #     db_manager.get_companies_and_vacancies_count,
    #     db_manager.get_all_vacancies,
    #     db_manager.get_avg_salary,
    #     db_manager.get_vacancies_with_higher_salary,
    # )
    # print(db_manager.get_companies_and_vacancies_count)
    # print()
    # print(db_manager.get_all_vacancies)
    # print()
    # print(db_manager.get_avg_salary)
    # print()
    # print(db_manager.get_vacancies_with_higher_salary)
    # print()
    # print(db_manager.get_vacancies_with_keyword("PHP"))
    # db_manager.close()

#   Проблема с корректной валютой (проще всего будет сменить компании на Российские)


if __name__ == '__main__':
    start_time = time()
    print("Подключение к API\n.")
    # -----------------
    main()
    # -----------------
    end_time = time()
    def_time = end_time - start_time
    print(f'\nВремя выполнения программы: \n{def_time}')







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

