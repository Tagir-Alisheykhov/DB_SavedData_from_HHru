import psycopg2


class DBManager:
    """
    Интерфейс для взаимодействия с базой данных.
    """

    params: dict
    db_name: str

    def __init__(self, params, dbname):
        """
        :param params: Параметры для подключения к БД.
        """
        self.params = params
        self.dbname = dbname
        self.conn = psycopg2.connect(**self.params, database=self.dbname)
        self.autocommit = self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def close(self) -> None:
        """
        Отключение от базы данных.
        """
        self.cur.close()
        self.conn.close()

    def create(self, new_db_name):
        """
        Создание базы данных.
        :return:
        """
        try:
            self.end_sessions(new_db_name)
            self.cur.execute(f"DROP DATABASE IF EXISTS {new_db_name}")
            self.cur.execute(f"CREATE DATABASE {new_db_name}")
            self.close()
            self.conn = psycopg2.connect(**self.params, database=new_db_name)
            self.autocommit = self.conn.autocommit = True
            self.cur = self.conn.cursor()
            print(f"Подключение к базе данных {new_db_name} установлено.")
        except Exception as err:
            print(f"Ошибка при создании базы данных: {err}")

    def design(self, request=None, close=True):
        """
        Проектирование базы данных.
        :return:
        """
        self.cur.execute(request)
        print("Таблицы созданы.")
        if close:
            self.close()

    def end_sessions(self, dat_name: str) -> None:
        """
        Модуль для завершения открытых сессий в БД.
        :param dat_name: Название базы данных.
        """
        try:
            self.cur.execute(
                f"SELECT pg_terminate_backend(pg_stat_activity.pid) "
                f"FROM pg_stat_activity "
                f"WHERE pg_stat_activity.datname = '{dat_name}'"
                f"AND pid <> pg_backend_pid();"
            )
            print(f"Все активные сеансы для базы данных {dat_name} прерваны.")
        except Exception as err:
            print(f"Возникла ошибка при завершении сеансов db_name: {dat_name}, ERROR {err}")

    def insert(self, request):
        """
        Вставка данных в базу данных.
        :return:
        """
        pass

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        pass

    def get_all_vacancies(self):
        """
         Получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию.
        :return:
        """
        pass

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        :return:
        """
        pass

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return:
        """
        pass

    def get_vacancies_with_keyword(self):
        """
        Получает список всех вакансий, в названии которых содержатся
        переданные в метод слова, например python.
        :return:
        """
        pass


# Спроектировать таблицы в БД PostgreSQL для хранения полученных данных
# о работодателях и их вакансиях. Для работы с БД используйте библиотеку psycopg2.

# Реализовать код, который заполняет созданные в БД PostgreSQL
# таблицы данными о работодателях и их вакансиях.

# Создать класс DBManager для работы с данными в БД. Класс DBManager




# class CreateDB:
#     """
#     Класс для создания базы данных.
#     """
#
#     def __init__(self, params=None):
#         """
#         :param params:
#         """
#         self.params = params
#
#     def connect(self):
#         """
#         :return:
#         """
#         conn = psycopg2.connect(self.params)
#
#
# class InsertDB:
#     """
#     Класс для загрузки данных в базу данных.
#     """
#
#     def __init__(self):
#         pass
