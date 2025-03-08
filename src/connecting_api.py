import json
import re
from datetime import datetime
from time import time
import requests
from abc import ABC, abstractmethod
import pandas as pd


class ConnectingHHAPI(ABC):
    """
    Абстрактный метод для создания дочерних классов.
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def connecting_api(self):
        pass


class SearchEmployersHHAPI(ConnectingHHAPI):
    """
    Класс для подключения к API, сервиса HeadHunter.
    В данном классе реализуется поиск информации о работодателе,
    в основном для определения ID интересующих работодателей.
    ID работодателя необходим для последующего взаимодействия
    с информацией о работодателях.
    """

    def __init__(self):
        self.__url = 'https://api.hh.ru/employers'
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {
            "text": "",
            "name": "",
            "per_page": 100,
            "page": 1,
            "local": "RU",
            "host": "hh.ru",
            "only_with_vacancies": True
        }

    def connecting_api(self, keyword="IT"):
        list_companies = list()

        self.__params['text'] = keyword
        response = requests.get(
            url=self.__url, params=self.__params, headers=self.__headers
        )
        print(response.status_code)
        result = response.json()
        return json.dumps(result, indent=4, ensure_ascii=False)


class EmployersInfoHHAPI(ConnectingHHAPI):
    """
    """

    def __init__(self, employer_id):
        self.employer_id = employer_id
        self.__url = f'https://api.hh.ru/employers/{employer_id}'
        self.__headers = {"User-Agent": "HH-User-Agent"}

    def connecting_api(self):
        """
        Установка соединения с API `hh.ru`,
        для получения данных работодателе
        :return:
        """
        response = requests.get(
            url=self.__url, headers=self.__headers
        )
        current_emp_info = response.json()
        print(response.status_code)
        return current_emp_info
        # -----
        # OLD VERSION
        # formatted_data = self.formatter_data(current_emp_info)
        # end_time = time()
        # return formatted_data

    # @staticmethod
    # def formatter_data(data):
    #     """
    #     . . .
    #     :param data:
    #     :return:
    #     """
    #     vacancies_url = data["vacancies_url"]
    #     data["employer_id"] = data["id"]
    #     data["area"] = data["area"]["name"]
    #     data["industries_id"] = data["industries"][0]["id"] if data["industries"] else 0
    #     data["industries_name"] = data["industries"][0]["name"] if data["industries"] else 0
    #     if data["industries_name"]:
    #         data["description"] = data["industries_name"]
    #         del data["industries_name"]
    #     else:
    #         del data["industries_name"]
    #         data["description"] = data["description"]
    #     del (
    #         data["site_url"],
    #         data["id"],
    #         data["alternate_url"],
    #         data["vacancies_url"],
    #         data["relations"],
    #         data["industries"],
    #         data["insider_interviews"],
    #         data["branded_description"],
    #         data["logo_urls"],
    #         data["industries_id"],
    #         data["branding"]
    #     )
    #     return data, vacancies_url


class EmployerVacancies(ConnectingHHAPI):
    """
    Класс для вывода вакансий работодателя.
    """

    vacancies_url: str
    keyword: str | None

    def __init__(self, vacancies_url, keyword=None, currency="RUR"):
        """
        :param vacancies_url: Ссылка на вакансии работодателя.
        """
        self._avg_salaries = None
        self.keyword = keyword
        self.currency = currency
        self.vacancies_url = vacancies_url

    def connecting_api(self) -> [float, list]:
        """
        :return:
        """
        response = requests.get(url=self.vacancies_url)
        vacancies = response.json()["items"]

        with open("data/vacancies.json", "w", encoding="UTF-8") as file_write:
            json.dump(vacancies, file_write, indent=4, ensure_ascii=False)
        with open("data/vacancies.json", "r",  encoding="UTF-8") as file_read:
            vacancies = json.load(file_read)

        formatted_vacancies = self.formatter_vacancies(vacancies)
        return formatted_vacancies

    def formatter_vacancies(self, vacancies):
        """
        :param vacancies:
        :return:
        """
        vacancies_list = list()
        for vacancy in vacancies:
            if self.currency:
                vacancy["salary"] = \
                    {'from': 0, 'to': 0, 'currency': 'RUR'} if not vacancy["salary"] else vacancy["salary"]
            # print(json.dumps(vacancy, indent=2, ensure_ascii=False))
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

            df_hours = pd.DataFrame(vacancy["working_hours"])
            hours_list = [x if isinstance(x, int) else "0" for x in df_hours["name"]]
            work_hours = "-".join(list(map(lambda x: re.findall(r"\d+", x)[0], hours_list)))
            new_dict["working_hours"] = work_hours

            df_schedule = pd.DataFrame(vacancy["work_schedule_by_days"])
            work_schedule = "-".join([x for x in df_schedule["name"]])
            new_dict["work_schedule_by_days"] = work_schedule

            if not self.keyword:
                vacancies_list.append(new_dict)
            elif any(
                    isinstance(value, str)
                    and self.keyword
                    in value
                    for value in vacancy.values()):
                vacancies_list.append(new_dict)
        return vacancies_list

    @property
    def avg_salary_vacancies(self):
        """
        :return:
        """
        try:
            print("Средняя зарплата работодателя по вакансиям:")
            return round(self._avg_salaries, 2)
        except TypeError:
            print("-- Warning: Не удалось вывести среднее значение")
            print("   У данного работодателя нет вакансий по заданным параметрам.")

    @avg_salary_vacancies.setter
    def avg_salary_vacancies(self, vacancies):
        """
        :param vacancies:
        :return:
        """
        salary_list = list()
        print(f"Количество вакансий по заданным параметрам: \n{len(vacancies)}")
        if vacancies:
            salary_list = [vacancy["salary"] for vacancy in vacancies if vacancy["salary"] > 0]
            if salary_list:
                self._avg_salaries = sum(salary_list) / len(salary_list)
            else:
                self._avg_salaries = None

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



            # if vacancy.get("branding"):
            #     del vacancy["branding"]
            # if vacancy.get("show_logo_in_search"):
            #     del vacancy["show_logo_in_search"]
            # del (
            #     vacancy["url"],
            #     vacancy["id"],
            #     vacancy["internship"],
            #     vacancy["insider_interview"],
            #     vacancy["archived"],
            #     vacancy["premium"],
            #     vacancy["adv_context"],
            #     vacancy["professional_roles"],
            #     vacancy["is_adv_vacancy"],
            #     vacancy["accept_incomplete_resumes"],
            #     vacancy["employment_form"],
            #     vacancy["employment"],
            #     vacancy["alternate_url"],
            #     vacancy["apply_alternate_url"],
            #     vacancy["relations"],
            #     vacancy["working_days"],
            #     vacancy["fly_in_fly_out_duration"],
            #     vacancy["working_time_intervals"],
            #     vacancy["working_time_modes"],
            #     vacancy["has_test"],
            #     vacancy["night_shifts"],
            #     vacancy["response_url"],
            #     vacancy["sort_point_distance"],
            #     vacancy["adv_response_url"],
            #     vacancy["department"],
            #     vacancy["response_letter_required"],
            #     vacancy["published_at"],
            #     vacancy["created_at"],
            #     vacancy["area"],
            #     vacancy["snippet"],
            #     vacancy["employer"]
            # )