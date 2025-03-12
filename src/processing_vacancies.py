from datetime import datetime
import re
import pandas as pd


class VacancyProcessing:
    """
    """
    vacancies: list
    keyword: str
    currency: str

    def __init__(self, vacancies, keyword=None, currency="RUR"):
        """
        :param vacancies:
        :param keyword:
        :param currency:
        """
        self.keyword = keyword
        self.currency = currency
        self.raw_vacancies = vacancies
        # self._avg_salaries = None

    def formatter_vacancies(self):
        """
        :return:
        """
        vacancies_list = list()
        for vacancy in self.raw_vacancies:
            published_at = datetime.strptime(vacancy["published_at"], "%Y-%m-%dT%H:%M:%S%z")
            new_dict = dict()
            new_dict["vacancy_id"] = vacancy["id"]
            new_dict["published_at_date"] = published_at.strftime("%d-%m-%Y")
            new_dict["published_at_time"] = published_at.strftime("%H:%M:%S")
            new_dict["city"] = vacancy["address"]["city"] if vacancy["address"] else None
            new_dict["address"] = f'{vacancy["address"]["street"]} {vacancy["address"]["building"]}' \
                if vacancy["address"] else None
            new_dict["description"] = vacancy["snippet"]["requirement"]
            new_dict["employer_id"] = vacancy["employer"]["id"]
            new_dict["type"] = vacancy["type"]["id"]
            new_dict["experience"] = vacancy["experience"]["id"]
            new_dict["professional_roles"] = vacancy["professional_roles"][0]["name"]
            new_dict["schedule"] = vacancy["schedule"]["id"]
            new_dict["salary"] = self.detect_salary(vacancy["salary"])
            new_dict["work_format"] = vacancy["work_format"][0]["id"] if vacancy["work_format"] else None
            working_hours = self.processing_key_working_hours(vacancy["working_hours"])
            new_dict["working_hours"] = working_hours
            working_schedule = self.processing_key_work_schedule_by_days(vacancy["work_schedule_by_days"])
            new_dict["work_schedule_by_days"] = working_schedule

            if not self.keyword:
                vacancies_list.append(new_dict)
            elif any(
                    isinstance(value, str)
                    and self.keyword
                    in value
                    for value in vacancy.values()):
                vacancies_list.append(new_dict)
        return vacancies_list

    @staticmethod
    def processing_key_work_schedule_by_days(work_schedule_by_days):
        """
        :return:
        """
        df_schedule = pd.DataFrame(work_schedule_by_days)
        work_schedule = "-".join([x for x in df_schedule["name"]])
        return work_schedule

    @staticmethod
    def processing_key_working_hours(working_hours):
        """
        :return:
        """
        df_hours = pd.DataFrame(working_hours)
        hours_list = [x if isinstance(x, int) else "0" for x in df_hours["name"]]
        work_hours = "-".join(list(map(lambda x: re.findall(r"\d+", x)[0], hours_list)))
        return work_hours

    @staticmethod
    def detect_salary(salary):
        """
        Выявление зарплаты из массива
        :return: int
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

    def currency_validate(self, vacancy):
        """
        :return:
        """
        if self.currency:
            vacancy["salary"] = (
                {'from': 0, 'to': 0, 'currency': 'RUR'}
                if not vacancy["salary"] else vacancy["salary"])
            return vacancy["salary"]


class VacanciesSalaryAVG:
    """
    """

    def __init__(self, vacancies):
        """
        :param vacancies:
        """
        self.vacancies = vacancies
        self._avg_salaries = None

    def avg(self):
        """
        :return:
        """
        # print(f"Количество вакансий по заданным параметрам: \n{len(self.vacancies)}")
        if self.vacancies:
            salary_list = [vacancy["salary"] for vacancy in self.vacancies if vacancy["salary"] > 0]
            if salary_list:
                self._avg_salaries = sum(salary_list) / len(salary_list)
            else:
                self._avg_salaries = None
        return round(self._avg_salaries, 2)

