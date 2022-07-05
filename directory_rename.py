# python3.9
# directory_rename.py - предназначен для переименования папок в папке courses

import shelve
import os
from googletrans import Translator

# Получение переменной с путем к папке с материалами курсов
shelfFile = shelve.open('directory_path')
courses_path = shelfFile['courses_path']
shelfFile.close()

# Получение словаря из папок
dir_dict = {}
for folder_name in os.listdir(courses_path):
    dir_dict.setdefault(int(folder_name.split('. ')[0]), folder_name.split('. ')[1])

# Перевод названий папок и создание словаря
translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.co.kr',
    ])
new_dir_dict = {}
for v in dir_dict.values():
    new_dir_dict.setdefault(v, translator.translate(v).text.lower().replace(' ', '_'))
new_dir_dict['Временные ряды'] = 'time_series'
new_dir_dict['Обучение без учителя'] = 'unsupervised_learning'
new_dir_dict['Предобработка данных'] = 'data_preprocessing'
new_dir_dict['Исследовательский анализ данных'] = 'exploratory_data_analysis'
new_dir_dict['Обучение с учителем'] = 'supervised_learning'
new_dir_dict['Машинное обучение в бизнесе'] = 'machine_learning_in_business'

# Переименование папок
for folder_name in os.listdir(courses_path):
    new_name = str(folder_name.split('. ')[0]) + '_' + new_dir_dict[dir_dict[int(folder_name.split('. ')[0])]]
    os.rename(courses_path+'\\'+folder_name,courses_path+'\\'+new_name)

