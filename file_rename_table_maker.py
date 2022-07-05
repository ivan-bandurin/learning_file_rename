# python3.9
# file_rename_table_maker.py - предназначен для создания таблицы для переименования файлов в папке courses

import os
import shelve
import re
import pandas as pd
import fitz 
from googletrans import Translator
translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.co.kr',
    ])

# Функция получения типа материала
def mat_type(row):
    if 'abstract' in row['file_name']:
        return 'abstract'
    elif 'takeaways' in row['file_name']:
        return 'takeaways'
    else:
        return 'something'

# Функция получения номера курса
def course_num(row):
    course_regex = re.compile(r'course(\d+)')
    try:
        file_course_num = int(course_regex.findall(row['file_name'])[0])
        folder_course_num = int(row['folder'].split('_')[0])
        if file_course_num == folder_course_num:
            return file_course_num
        else:
            return 'mistake'
    except IndexError:
        return 'mistake_2'

# Функция получения номера темы
def theme_num(row):
    course_regex = re.compile(r'theme(\d+)')
    try:
        file_course_num = int(course_regex.findall(row['file_name'])[0])
        return file_course_num

    except IndexError:
        return 'mistake'

# Функция получения русского названия темы
def theme(row):
    th_name_regex = re.compile(r'Конспект по теме [«"](.+)[»"]')
    file_name = courses_path + '\\' + row['folder'] + '\\' + row['file_name']
    doc_1 = fitz.open(file_name)
    text = doc_1.load_page(0).get_text().split('\n')[0]
    if len(th_name_regex.findall(text)) == 0:
        return text
    else:
        return th_name_regex.findall(text)[0]

def english_th_name(row):
    return translator.translate(row['theme_name']).text

# Получение переменной с путем к папке с материалами курсов
shelfFile = shelve.open('directory_path')
courses_path = shelfFile['courses_path']
shelfFile.close()

# Получение списка файлов во всех папках папки courses и создание базового датафрейма
file_list = []
for f, s, fls in os.walk(courses_path):
    folder_name = os.path.basename(f)
    for fl in fls:
        inner_list = []
        inner_list.append(fl)
        inner_list.append(folder_name)
        file_list.append(inner_list)
files_df=pd.DataFrame(file_list,columns=['file_name', 'folder'])

# Добавление столбца с типом материала
files_df['material_type'] = files_df.apply(mat_type, axis=1)

# Добавление столбца с номером курса
files_df['course_number'] = files_df.apply(course_num, axis=1)

# Добавление столбца с номером темы
files_df['theme_number'] = files_df.apply(theme_num, axis=1)

# Добавление столбца с названием темы
files_df['theme_name'] = files_df.apply(theme, axis=1)

# Добавление столбца с английским названием темы
files_df['english_theme_name'] = files_df.apply(english_th_name, axis=1)

writer = pd.ExcelWriter('test.xlsx')
files_df.to_excel(writer, 'Лист1', index=False)
writer.save()
writer.close()
# print(files_df[files_df['course_number'] == 'mistake_2'])