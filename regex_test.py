import re

course_regex = re.compile(r'course(\d+)')

file_name = 'praktikum_data_scientist_takeaways_course8_theme4.pdf'
print(int(course_regex.findall(file_name)[0]))