import json

from engine_classes import SuperJob, HeadHunter
from vacancy_classes import Vacancy, sorting, get_vacancies_top_salary, get_vacancies_by_city, \
    get_vacancies_by_employer

# Запрашивает у пользователя ключевое слово, по которому будет производиться поиск.
keyword = input('Введите ключевое слово для поиска вакансий: \n')

sj = SuperJob()
sj_data = sj.get_request(keyword)
sj.create_json(sj.get_vacancies(sj_data), "sj_vac.json")

hh = HeadHunter()
hh_data = hh.get_request(keyword)
hh.create_json(hh.get_vacancies(hh_data), "hh_vac.json")

# Открываем 2 JSON файла и сохраняем их объекты в переменные
with open("sj_vac.json", 'r', encoding="UTF-8") as f1:
    sj_vacancies = json.load(f1)
with open("hh_vac.json", 'r', encoding="UTF-8") as f2:
    hh_vacancies = json.load(f2)

# Складываем 2 объекта в переменную
all_vacancies = sj_vacancies + hh_vacancies
print(len(all_vacancies))
# print(all_vacancies)

# Записываем объединенный объект JSON в новый файл
with open("all_vacancies.json", 'w', encoding="UTF-8") as f3:
    json.dump(all_vacancies, f3, indent=2, ensure_ascii=False)

print(f"Всего было найдено {len(all_vacancies)} вакансий")

# Открываем JSON файл и сохраняем его объекты в список с экземплярами класса Vacancy
with open("all_vacancies.json", 'r', encoding="UTF-8") as f:
    data = json.load(f)
vacancies_list = []
for i in data:
    vacancy = Vacancy(i["source"], i["position"], i["requirements"], i["position_description"], i["city"],
                      i["salary"], i["currency"], i["employer"], i["url"])
    vacancies_list.append(vacancy)
# print(vacancies_list)


# Сортируем список всех вакансий по ежемесячной оплате
print(f"\nОтсортировать вакансии по заработной плате? Y/N")
user_answer = input()
if user_answer.upper() == "Y":
    print(sorting(vacancies_list))

print("\nЧто делать дальше? \n1 - Выбрать самые высокооплачиваемые вакансии\n2 - Выбрать вакансии в определённом "
      "городе\n3 - Выбрать вакансии одного работодателя\nЧтобы выйти нажмите любую клавишу\n")

user_input = input("Ваш выбор: \n")
if int(user_input) == 1:
    top_count = int(input("Сколько вакансий выводить? \n"))
    top_vacancies = get_vacancies_top_salary(vacancies_list, top_count)
    print(top_vacancies)
    print(f"\nСпасибо! Приходите ещё.")
elif int(user_input) == 2:
    city_input = input("\nВведите город: \n").title()
    vacancies_by_city = get_vacancies_by_city(vacancies_list, city=city_input)
    print(f"Найдено {len(vacancies_by_city)} вакансий удовлетворяющих вашему запросу")
    print(vacancies_by_city)
    print(f"\nСпасибо! Приходите ещё.")
elif int(user_input) == 3:
    employer_input = input("\nВведите название компании: \n")
    employers_vacancies = get_vacancies_by_employer(vacancies_list, employer=employer_input)
    print(f"Найдено {len(employers_vacancies)} вакансий удовлетворяющих вашему запросу")
    print(employers_vacancies)
    print(f"\nСпасибо! Приходите ещё.")
else:
    print(f"\nСпасибо! Приходите ещё.")
