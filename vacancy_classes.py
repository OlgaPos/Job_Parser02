class Vacancy:
    """Организация информации, полученной из вакансии в короткий и удобный вывод для пользователя"""
    __slots__ = ('source', 'position', 'requirements', 'position_description', 'city', 'salary', 'currency',
                 'employer', 'url')

    def __init__(self, source, position, requirements, position_description, city, salary, currency, employer, url):
        self.source = source
        self.position = position
        self.requirements = requirements
        self.position_description = position_description
        self.city = city
        self.salary = salary
        self.currency = currency
        self.employer = employer
        self.url = url

    def __str__(self):
        return f'{self.source}\nПозиция - {self.position}, \nзарплата от- {self.salary} {self.currency}/мес'

    def __repr__(self):
        return f'\n{self.source}: \nПозиция: {self.position}, \nРаботодатель: {self.employer}, \nЗарплата от: ' \
               f'{self.salary} {self.currency}/мес \n{self.url}'


class SJVacancy(Vacancy):
    """ SuperJob ShortVacancy """

    def __init__(self, source, position, requirements, position_description, city, salary, currency, employer, url):
        super().__init__(source, position, requirements, position_description, city, salary, currency, employer, url)

    def __str__(self):
        return f'\n{self.source}: Позиция: {self.position}, зарплата от: {self.salary} {self.currency}/мес'

    def __repr__(self):
        return f'\n{self.source}: \nПозиция: {self.position}, \nРаботодатель: {self.employer}, \nЗарплата от: ' \
               f'{self.salary} {self.currency}/мес \n{self.url}'


class HHVacancy(Vacancy):
    """ HeadHunter Vacancy """

    def __init__(self, source, position, requirements, position_description, city, salary, currency, employer, url):
        super().__init__(source, position, requirements, position_description, city, salary, currency, employer, url)

    def __str__(self):
        return f'{self.source}: Позиция: {self.position}, зарплата от: {self.salary} {self.currency}/мес'

    def __repr__(self):
        if self.currency == "":
            currency = ""
        currency = f'{self.currency}/мес'
        return f'\n{self.source}: \nПозиция: {self.position}, \nРаботодатель: {self.employer}, \nЗарплата от: ' \
               f'{self.salary} {currency} \n{self.url}'


def sorting(vacancies_list: list) -> list:
    """ Сортирует список всех вакансий по ежемесячной оплате (gt, lt magic methods) """
    return sorted(vacancies_list, key=lambda x: x.salary, reverse=True)


def get_vacancies_top_salary(vacancies_list: list, top_count: int) -> list:
    """
    Возвращает топ-n вакансий с сортировкой по уменьшению заработной платы.
    :param vacancies_list: список экземпляров класса Vacancy,
    :param top_count: сколько вакансий выводить
    :return: отсортированный список экземпляров класса Vacancy
    """
    return sorted(vacancies_list, key=lambda x: x.salary, reverse=True)[:top_count]


def get_vacancies_by_city(vacancies_list: list, city: str) -> list:
    """
    Возвращает список вакансий в указанном городе.
    :param vacancies_list: список экземпляров класса Vacancy
    :param city: город РФ
    :return: список экземпляров класса Vacancy
    """
    filtered_by_city = list(filter(lambda x: x.city == city, vacancies_list))
    if filtered_by_city:
        return filtered_by_city
    return []


def get_vacancies_by_employer(vacancies_list: list, employer: str) -> list:
    """
    Возвращает список вакансий в указанном городе.
    :param vacancies_list: список экземпляров класса Vacancy
    :param employer: город РФ
    :return: список экземпляров класса Vacancy
    """
    filtered_by_employer = list(filter(lambda x: x.employer == employer, vacancies_list))
    if filtered_by_employer:
        return filtered_by_employer
    return []
