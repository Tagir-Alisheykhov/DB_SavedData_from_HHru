import json
import os
from time import time

from src.config import config
from src.db_manager import DBManager
from src.utils import data_to_insert, request1, request2
from src.config import config, sensitive_env


def main():
    """
    :return:
    """
    # API connecting...
    employer_info, vacancies_list_info, avg_salary_vacancies = data_to_insert()
    # . . .
    # print(json.dumps(vacancies_list_info, indent=4, ensure_ascii=False))
    # --------------------------------------

    # Загрузка параметров для подключения к БД.
    params = config() | sensitive_env()
    dbname = params["database"]
    del params["database"]

    # Подключение к менеджеру для работы с БД.
    db_manager = DBManager(params=params, dbname=dbname)
    db_manager.create(new_db_name="head_hunter")   # Создание БД.
    db_manager.design(request=request1, close=True)  # Проектирование БД.
    db_manager.insert(request=request2)


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

