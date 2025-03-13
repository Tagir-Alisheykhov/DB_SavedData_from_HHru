import json
import os
from abc import ABC, abstractmethod
from typing import Any

path_to_data = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/")


class SaveToFile(ABC):
    """ """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def write_data_json(self):
        pass

    @abstractmethod
    def read_data_json(self):
        pass


class SaveEmpInfoJSON(SaveToFile):
    """
    Сохранение информации о работодателе в json-файл.
    """

    emp_data: str

    def __init__(self, emp_data):
        """
        :param emp_data: Данные о работодателе.
        """
        self.emp_data = emp_data

    def write_data_json(self) -> None:
        """
        Запись данных в файл.
        """
        with open("data/employer.json", "w", encoding="UTF-8") as file_writing:
            json.dump(self.emp_data, file_writing, indent=4, ensure_ascii=False)

    @property
    def read_data_json(self) -> Any:
        """
        Чтение данных из файла.
        :return: Данные о работодателе.
        """
        with open(
            path_to_data + "employer.json", "r", encoding="UTF-8"
        ) as file_reading:
            reading_data = json.load(file_reading)
            reading_data = self.formatter_data(reading_data)
            return reading_data

    @staticmethod
    def formatter_data(raw_emp_data) -> tuple[dict, str]:
        """
        Форматирование данных о работодателе.
        :return: Готовы данные для записи в БД.
        """
        new_data = dict()
        vacancies_url = raw_emp_data["vacancies_url"]
        new_data["employer_id"] = raw_emp_data["id"]
        new_data["name"] = raw_emp_data["name"]
        new_data["accredited_it_employer"] = raw_emp_data["accredited_it_employer"]
        new_data["area"] = raw_emp_data["area"]["name"]
        new_data["open_vacancies"] = raw_emp_data["open_vacancies"]
        industries = raw_emp_data.get("industries")
        if industries and len(industries) > 0:
            new_data["description"] = industries[0]["name"]
        else:
            new_data["description"] = raw_emp_data.get("description", "")
        return new_data, vacancies_url


class SaveVacanciesJSON:
    """
    Сохранение информации о вакансии в json-файл.
    """

    vacancies: str

    def __init__(self, vacancies):
        """
        :param vacancies: Данные о вакансиях.
        """
        self.vacancies = vacancies

    def write_data_json(self) -> None:
        """
        Запись данных в файл.
        :return: Данные о вакансии.
        """
        with open(path_to_data + "vacancies.json", "w", encoding="UTF-8") as file_write:
            json.dump(self.vacancies, file_write, indent=4, ensure_ascii=False)

    @property
    def read_data_json(self) -> dict:
        """
        Вывод данных из файла.
        :return: Данные о вакансии.
        """
        with open("data/vacancies.json", "r", encoding="UTF-8") as file_read:
            vacancies = json.load(file_read)
            return vacancies


class ReadCompaniesList:
    """
    Чтение списка работодателей для
    последующего вывода информации о них.
    """

    @property
    def read_data_json(self) -> dict:
        """
        Чтение данных из json-файла.
        :return: Названия и id работодателей.
        """
        with open(
            path_to_data + "companies_list.json", "r", encoding="UTF-8"
        ) as read_file:
            return json.load(read_file)
