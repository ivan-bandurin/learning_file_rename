# python3.9
# file_renamer.py - предназначен для переименования файлов в папке courses

import os
import shelve
import pandas as pd

# Получение переменной с путем к папке с материалами курсов
shelfFile = shelve.open('directory_path')
courses_path = shelfFile['courses_path']
shelfFile.close()

files_df = pd.read_excel('test.xlsx')

def new_file_name(row):
    return (row['material_type'] + '_' + 
            str(row['course_number']) + '_' +
            str(row['theme_number']) + '_' +
            row['english_theme_name'].lower().replace(' ', '_'))

files_df['new_file_name'] = files_df.apply(new_file_name, axis=1)

# writer = pd.ExcelWriter('test_2.xlsx')
# files_df.to_excel(writer, 'Лист1', index=False)
# writer.save()
# writer.close()

file_list = list(files_df['file_name'].unique())

for f in file_list:
    folder = files_df[files_df['file_name'] == f]['folder'].values[0]
    new = files_df[files_df['file_name'] == f]['new_file_name'].values[0]
    old_name = courses_path +'\\' + folder + '\\' + f
    new_name = courses_path +'\\' + folder + '\\' + new + '.pdf'
    os.rename(old_name,new_name)
