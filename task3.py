import os
import re
import csv

from task2 import logger


""" Описание примера

Возьмем в качестве примера решение ДЗ по регулярным выражениям.

Условия ДЗ:
https://github.com/netology-code/py-homeworks-advanced/tree/master/5.Regexp

Решение ДЗ:
https://github.com/maxter9595/regexp_hw/blob/main/homework.py

Алгоритм работы с примером:
1. Подставляем решение ДЗ в виде функции
2. Вызываем logger, полученный в результате решения задания №2 текущего ДЗ
3. Применяем logger относительно решения ДЗ "Регулярные выражения"

"""


def test_3(log_path, read_path):
    
    if os.path.exists(log_path):
        os.remove(log_path)

    @logger(log_path)
    def open_csv(read_path, encoding='utf-8'):
        with open(read_path, encoding=encoding) as f:
            rows = csv.reader(f, delimiter=",")
            contacts_list = list(rows)
        return contacts_list
    
    @logger(log_path)
    def modify_name(contacts_list:list):
        for i, contact_list in enumerate(contacts_list[1:], start=1):
            name_str = contact_list[:3]
            name_list = " ".join(name_str).strip(" ").split()
            name_list.extend([""]*(len(name_str)-len(name_list)))
            contacts_list[i] = name_list+contact_list[3:]
        return contacts_list
    
    @logger(log_path)
    def modify_telephone(contacts_list):
        pattern=r"(\+7|8)?(\s*|\s*\()?(\d{3})(\)\s*|\s*|-)?(\d{3})(\s*|-)?"\
                "(\d{2})(\s*|-)?(\d{2})\s*(\w+.|\(\w+.)?\s*(\d+)?(\))?"
        for contact_list in contacts_list[1:]:
            telephone = contact_list[5]
            result = re.sub(pattern,r"+7(\3)\5-\7-\9 доб.\11",telephone)
            if result:
                if result.endswith("доб."):
                    idx_loc = result.index('доб.')
                    contact_list[5] = result[:idx_loc-1]
                else:
                    contact_list[5] = result
            else:
                contact_list[5] = ''
        return contacts_list
    
    @logger(log_path)
    def correct_similar_name(contacts_list):
        dict_data, col_list = {}, contacts_list[0]
        for contact_list in contacts_list[1:]:
            name = ' '.join(contact_list[:3])
            similarity_list = [n for n in dict_data.keys() 
                                if name in n or n in name]
            if similarity_list:
                for my_col, val in zip(col_list, contact_list):
                    if val:
                        dict_data[similarity_list[0]][my_col] = val
            else:
                dict_data[name] = dict(zip(col_list, contact_list))
        return [col_list] + [list(dict_data.get(k).values()) 
                            for k in dict_data.keys()]
    
    @logger(log_path)
    def write_csv(write_path, contacts_list, encoding="utf-8"):
        with open(write_path, "w", encoding=encoding) as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerows(contacts_list)    
    
    contacts_list = open_csv(read_path)
    contacts_list = modify_name(contacts_list)    
    contacts_list = modify_telephone(contacts_list)    
    contacts_list = correct_similar_name(contacts_list)
    write_path = os.path.join(os.path.abspath('task3_materials'),
                                'phonebook.csv')
    write_csv(write_path, contacts_list)


if __name__ == '__main__':
    read_path = os.path.join(os.path.abspath('task3_materials'),
                            'phonebook_raw.csv')
    test_3('log_task3.log', read_path)