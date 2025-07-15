from time import time

from src.config import config, sensitive_env
from src.db_manager import DBManager
from src.utils import data_to_insert, query_design, user_interface


def main() -> str:
    """
    Основная функция для объединения и вызова
    всего функционала программы.

    """
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
    result = user_interface(db_manager)
    return result


if __name__ == "__main__":
    start_time = time()
    print("Подключение к API\n.")
    # -----------------
    print(main())
    # -----------------
    end_time = time()
    def_time = end_time - start_time
    print(f"\nВремя выполнения программы: \n{def_time}")
