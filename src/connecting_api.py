import json
import requests
from abc import ABC, abstractmethod


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

    def connecting_api(self, keyword="It"):
        """
        :param keyword:
        :return:
        """
        self.__params['text'] = keyword
        response = requests.get(
            url=self.__url, params=self.__params, headers=self.__headers
        )
        result = response.json()
        return result


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
        print(".")
        return current_emp_info


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
        return vacancies
