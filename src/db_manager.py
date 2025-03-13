import pandas as pd
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
            self.dbname = new_db_name
            self.conn = psycopg2.connect(**self.params, database=self.dbname)
            self.autocommit = self.conn.autocommit = True
            self.cur = self.conn.cursor()
            print(f"Подключение к базе данных {new_db_name} установлено.\n")
        except Exception as err:
            print(f"Ошибка при создании базы данных: {err}")

    def design(self, query=None, close=False):
        """
        Проектирование базы данных.
        :return:
        """
        self.cur.execute(query)
        if close is True:
            self.close()

    def insert(self, employers=None, vacancies=None, close=False):
        """
        Вставка данных в базу данных.
        :return:
        """
        # conn = psycopg2.connect(**self.params, database=self.dbname)
        # with conn.cursor() as cur:
        if employers:
            self.cur.executemany("""
            INSERT INTO employers (
                employer_id, name, accredited_it_employer, area, open_vacancies, description
                ) VALUES (%s, %s, %s, %s, %s, %s)""",
                             employers)
        if vacancies:
            self.cur.executemany("""
            INSERT INTO vacancies (
                vacancy_id, employer_id, type, published_at_date, published_at_time,
                city, address, experience, professional_roles, schedule, salary,
                work_format, working_hours, work_schedule_by_days, url, description) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                             vacancies)
        if close is True:
            self.close()

    @property
    def get_companies_and_vacancies_count(self) -> pd.DataFrame:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        self.cur.execute("""
        SELECT DISTINCT(employers.name), COUNT(vacancies.vacancy_id) AS count_vacancies
        FROM vacancies
        JOIN employers USING(employer_id)
        GROUP BY employers.name
        """)
        df = pd.DataFrame(self.cur.fetchall())
        df.columns = ["Название компании", "Кол-во вакансий"]
        df.index = df.index + 1
        return df

    @property
    def get_all_vacancies(self) -> pd.DataFrame:
        """
         Получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию.
        :return:
        """
        self.cur.execute(
            """SELECT employers.name AS company_name, professional_roles, salary, url AS vacancy_url
            FROM vacancies
            JOIN employers USING(employer_id)
            ORDER BY salary DESC"""
        )
        df = pd.DataFrame(self.cur.fetchall())
        df.columns = ["Название компании", "Должность", "Зарплата", "Ссылка на вакансию"]
        df.index = df.index + 1
        return df

    @property
    def get_avg_salary(self) -> pd.DataFrame:
        """
        Получает среднюю зарплату по вакансиям.
        :return:
        """
        self.cur.execute("""SELECT ROUND(AVG(salary), 2) AS avg_salary FROM vacancies""")
        df = pd.DataFrame(self.cur.fetchone())
        df.columns = ["Средняя зарплата по вакансиям"]
        df.index = df.index + 1
        return df

    @property
    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых
        зарплата выше средней по всем вакансиям.
        :return:
        """
        self.cur.execute(
            """SELECT * FROM vacancies
                WHERE salary > (SELECT AVG(salary) FROM vacancies)"""
        )
        df = pd.DataFrame(self.cur.fetchall())
        df.columns = [
            "vacancy_id", "employer_id", "type", "published_at_date", "published_at_time",
            "city", "address", "experience", "professional_roles", "schedule", "salary",
            "work_format", "working_hours", "work_schedule_by_days", "url", "description"
        ]
        df.index = df.index + 1
        return df

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых
        содержатся переданные в метод слова, например python.
        :return:
        """
        self.cur.execute(
            f"""SELECT * FROM vacancies
            WHERE 
            LOWER(CONCAT(description, ' ', city, ' ', address, ' ', professional_roles,
            ' ', schedule, ' ',work_format, ' ', work_schedule_by_days, ' ', url, ' '))
            LIKE(LOWER('%{keyword}%'))"""
        )
        df = pd.DataFrame(self.cur.fetchall())
        df.columns = [
            "vacancy_id", "employer_id", "type", "published_at_date", "published_at_time",
            "city", "address", "experience", "professional_roles", "schedule", "salary",
            "work_format", "working_hours", "work_schedule_by_days", "url", "description"
        ]
        df.index = df.index + 1
        return df

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
        except Exception as err:
            print(f"Возникла ошибка при завершении сеансов db_name: {dat_name}, ERROR {err}")
