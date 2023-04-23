import json
import os
from abc import ABC, abstractmethod
from connector import Connector
import requests


class Engine(ABC):
    @abstractmethod
    def get_request(self, keyword):
        """Запрашивает вакансии, в том числе через API"""
        pass

    @staticmethod
    def get_connector(file_name: str) -> Connector:
        """Возвращает экземпляр класса Connector"""
        pass

    @staticmethod
    def create_json(data, path):
        """Сохраняем файл json в проекте, чтобы не загружать каждый раз с сайта"""
        with open(path, 'w', encoding="UTF-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)


class SuperJob(Engine):
    HEADERS = {"X-Api-App-Id": os.environ["SuperJob_API_KEY"]}
    URL = 'https://api.superjob.ru/2.0/vacancies/'

    def get_request(self, keyword):
        """Возвращает список из 500 вакансий, найденных по ключевому слову через API"""
        sj_vacancies = []
        for page_number in range(5):
            response = requests.get(url=self.URL, headers=self.HEADERS,
                                    params={"keywords": keyword, "count": 100,
                                            "page": page_number})
            # print(response.status_code)  # mozhno ubrat' ili peredelat' test
            data = response.json()
            if response.status_code == 200:
                for vacancy in data['objects']:
                    sj_vacancies.append(vacancy)
            else:
                print("Что-то пошло не так")  # mozhno ubrat' ili peredelat' test
        return sj_vacancies

    @staticmethod
    def get_vacancies(data: dict) -> list:
        """Возвращает список с короткими вакансиями"""
        sj_vacancies = []
        count = 0
        for i in data:
            if i["client"].get('staff_count') is None:
                i["client"]["staff_count"] = "Нет данных"
            i["client"]["staff_count"] = i["client"]["staff_count"]
            sj_vacancy = {"source": "SJ", "position": i["profession"], "requirements": i["candidat"],
                          "position_description": "same", "city": i["town"]["title"],
                          "salary": i["payment_from"], "currency": i["currency"], "employer": i["firm_name"],
                          "url": i["link"]}
            count += 1
            # print(sj_vacancy)
            sj_vacancies.append(sj_vacancy)
        # print(count)
        return sj_vacancies


class HeadHunter(Engine):
    URL = 'https://api.hh.ru/vacancies'

    def get_request(self, keyword) -> list:
        hh_vacancies = []
        for page_number in range(5):
            response = requests.get(url=self.URL, params={"text": f"{keyword}", "per_page": 100, "page": 0})
            # print(response.status_code)  # mozhno ubrat' ili peredelat' test
            data = response.json()
            if response.status_code == 200:
                for vacancy in data['items']:
                    hh_vacancies.append(vacancy)
            else:
                print("Что-то пошло не так")  # mozhno ubrat' ili peredelat' test
        return hh_vacancies

    @staticmethod
    def get_vacancies(data: dict) -> list:
        """Возвращает список с короткими вакансиями"""
        hh_vacancies = []
        count = 0
        requirements = ''
        description = ''
        for i in data:
            if i["snippet"]["requirement"] is None:
                description = "Нет деталей"
            elif "<highlighttext>" and "</highlighttext>" in i["snippet"]["requirement"]:
                requirements = i["snippet"]["requirement"].replace("<highlighttext>", "")\
                    .replace("</highlighttext>", "")
            if i["snippet"]["responsibility"] is None:
                description = "Нет деталей"
            elif "<highlighttext>" and "</highlighttext>" in i["snippet"]["responsibility"]:
                description = i["snippet"]["responsibility"].replace("<highlighttext>", "")\
                    .replace("</highlighttext>", "")
            if i["salary"] is None:
                salary_from = 0
                salary_currency = ""
            elif i["salary"].get('from') is None:
                salary_from = 0
                salary_currency = ""
            else:
                salary_from = i["salary"].get('from')
                salary_currency = i["salary"].get('currency')
            hh_vacancy = {"source": "HH", "position": i["name"], "requirements": requirements,
                          "position_description": description, "city": i["area"]["name"], "salary": salary_from,
                          "currency": salary_currency, "employer": i["employer"]["name"], "url": i["url"]}
            count += 1
            # print(hh_vacancy)
            hh_vacancies.append(hh_vacancy)
        # print(count)
        return hh_vacancies

