import json
from abc import ABC, abstractmethod


class SaveToFile(ABC):
    """
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def saving_data_json(self):
        pass

    @abstractmethod
    def read_data_json(self):
        pass


class SaveEmpInfoJSON:
    """
    """
    def __init__(self):
        pass

    def saving_data_json(self):
        """
        :return:
        """
        pass

    def read_data_json(self):
        pass


class SaveVacanciesJSON:
    """
    """
    def __init__(self):
        pass

    def saving_data_json(self):
        """
        :return:
        """
        pass

    def read_data_json(self):
        pass