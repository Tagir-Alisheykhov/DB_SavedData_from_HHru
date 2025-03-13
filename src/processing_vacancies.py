from datetime import datetime
from typing import Any

import pandas as pd


class VacancyProcessing:
    """
    Обработка данных о вакансиях, полученных из API `HH.ru`
    """

    vacancies: list

    def __init__(self, vacancies):
        """
        :param vacancies: Данные о вакансиях
        """
        self.raw_vacancies = vacancies

    def formatter_vacancies(self) -> list:
        """
        Обработка полученных данных о вакансиях.
        :return: Готовые данные для записи в БД.
        """
        vacancies_list = list()
        for vacancy in self.raw_vacancies:
            published_at = datetime.strptime(
                vacancy["published_at"], "%Y-%m-%dT%H:%M:%S%z"
            )
            new_dict = dict()
            new_dict["vacancy_id"] = vacancy["id"]
            new_dict["employer_id"] = vacancy["employer"]["id"]
            new_dict["type"] = vacancy["type"]["id"]
            new_dict["published_at_date"] = published_at.strftime("%d-%m-%Y")
            new_dict["published_at_time"] = published_at.strftime("%H:%M:%S")
            new_dict["city"] = (
                vacancy["address"]["city"] if vacancy["address"] else None
            )
            new_dict["address"] = (
                f'{vacancy["address"]["street"]} {vacancy["address"]["building"]}'
                if vacancy["address"]
                else None
            )
            new_dict["experience"] = vacancy["experience"]["id"]
            new_dict["professional_roles"] = vacancy["professional_roles"][0]["name"]
            new_dict["schedule"] = vacancy["schedule"]["id"]
            new_dict["salary"] = self.detect_salary(vacancy["salary"])
            new_dict["work_format"] = (
                vacancy["work_format"][0]["name"]
                if vacancy["work_format"] != []
                else "Не указано"
            )
            new_dict["working_hours"] = vacancy["working_hours"][0]["name"]
            working_schedule = self.processing_key_work_schedule_by_days(
                vacancy["work_schedule_by_days"]
            )
            new_dict["work_schedule_by_days"] = working_schedule
            new_dict["url"] = vacancy["alternate_url"]
            new_dict["description"] = vacancy["snippet"]["requirement"]
            vacancies_list.append(new_dict)
        return vacancies_list

    @staticmethod
    def processing_key_work_schedule_by_days(work_schedule_by_days: str) -> str:
        """
        Форматирование ключа work_schedule_by_days.
        :return: Готовые данные.
        """
        df_schedule = pd.DataFrame(work_schedule_by_days)
        work_schedule = "-".join([x for x in df_schedule["name"]])
        return work_schedule

    @staticmethod
    def detect_salary(salary: dict) -> Any:
        """
        Выявление зарплаты из массива
        :return: Готовая информация о зарплате.
        """
        if salary:
            if salary["from"] and salary["to"]:
                salary = salary["to"]
            elif salary["from"] and not salary["to"]:
                salary = salary["from"]
            elif not salary["from"] and salary["to"]:
                salary = salary["to"]
            elif not salary["from"] and not salary["to"]:
                return 0
            return salary
        else:
            return 0
