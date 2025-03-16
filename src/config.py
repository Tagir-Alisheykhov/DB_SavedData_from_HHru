import os
from configparser import ConfigParser

from dotenv import load_dotenv

path_to_data = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/")


def sensitive_env() -> dict:
    """
    Вывод чувствительных данных для
    подключения к БД.
    :return: Пароль и название БД.
    """
    load_dotenv()
    db_password = os.getenv("PASSWORD_DB")
    db_name = os.getenv("DBNAME")

    sensitive_data = {"password": db_password, "database": db_name}
    return sensitive_data


def config(
    filename: str = path_to_data + "database.ini", section: str = "postgresql"
) -> dict:
    """
    Вывод нечувствительных данных для подключения к БД.
    :param filename: Путь до конфигурационных данных.
    :param section: Секция внутри файла.
    :return: Host, User, Port.
    """
    parser = ConfigParser()
    parser.read(filename)

    db_data = dict()
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_data[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} is not found in the {1} file.".format(section, filename)
        )
    return db_data
