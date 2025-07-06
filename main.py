from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# TODO 1: выполните пункты 1-3 ДЗ
# берем все данные, кроме заголовков
contacts_list1 = contacts_list[1:]
# новый список
cl = []
# проверяем список на дубликаты и склеиваем их в новом списке
for record in contacts_list1:
    # берем фамилию из оригинального списка
    fio = " ".join(record[:3])
    # по умолчанию считаем, что дубликатов нет
    is_double = False
    # для каждой записи в новом списке проверяем, совпадает ли она с текущей
    for r in cl:
        fio2 = " ".join(r[:3])
        if fio.split()[:2] == fio2.split()[:2]:
            # склеиваем данные из двух списков
            for i, zap in enumerate(record):
                if not r[i]:
                    r[i] = zap
            is_double = True
    # если не было дублирующихся записей, забираем в новый список запись
    # из старого целиком
    if not is_double:
        cl.append(record)

# распределяем ФИО по первым трем колонкам
for i, record in enumerate(cl):
    fio = " ".join(record[:3])
    cl[i][0] = fio.split()[0]
    cl[i][1] = fio.split()[1]
    cl[i][2] = fio.split()[2]

# заменяем телефон выбранным форматом
for record in cl:
    # если есть добавочный номер
    pattern = re.compile(r"(\+7|8)?\s*\((\d+)\)\s*(\d+)[-\s]*(\d+)[-\s]*(\d+)\s*(\(|\s)(доб\.)\s*(\d*)\)*")
    subst = r"+7(\2)\3-\4-\5 \7\8"
    s = r"\8"
    # ищем строку по паттерну в колонке с телефоном
    new, col = re.subn(pattern, subst, record[5])
    # заменяем телефон, если нашлась наша строка
    if col:
        record[5] = new
        continue
    else:
        # если нет добавочного номера
        pattern = re.compile(r"(\+7|8)?\s*\(?(\d{3})\)?(\s|-)?(\d{3})(\s|-)?(\d{2})(\s|-)?(\d{2})")
        subst = r"+7(\2)\4-\6-\8"
        # ищем строку по паттерну в колонке с телефоном
        new, col1 = re.subn(pattern, subst, record[5])
        # заменяем телефон, если нашлась наша строка
        if col1:
            record[5] = new
            continue
# склеиваем первую строку наименований столбцов с данными
contacts_list = [contacts_list[0]] + cl

# TODO 2: сохраните получившиеся данные в другой файл
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)