from bs4 import BeautifulSoup as bs
import requests
# url = 'http://problems.ru/view_problem_details_new.php?id=30320'
# page = urllib2.urlopen(quote_page)

def clean_tags(s):
	s_new = ''

	state = 'Closed'
	for char in s:
		if char == '<':
			state = 'Open'
		elif char == '>':
			state = 'Closed'
		elif state == 'Closed':
			s_new += char
	return s_new



n = 61419

r = requests.get('http://problems.ru/view_problem_details_new.php?id=' + str(n))
soup = bs(r.content, 'html5lib')
all_info = str(soup)
cut_1 = all_info.find('<h3>Условие</h3>')
cut_2 = all_info.find('<h3>Подсказка</h3>')
cut_3 = all_info.find('<h3>Решение</h3>')
cut_4 = all_info.find('<h3>Ответ</h3>')
cut_5 = all_info.find('<h3>Источники')


if (cut_4 == -1):
	cut_4 = cut_5

if (cut_3 == -1):
	cut_3 = cut_4

if (cut_2 == -1):
	cut_2 = cut_3

task = clean_tags(all_info[cut_1:cut_2])
hint = clean_tags(all_info[cut_2:cut_3])
solution = clean_tags(all_info[cut_3:cut_4])
answer = clean_tags(all_info[cut_4:cut_5])




print(task)
print('------------------------')
print(hint)
print('------------------------')
print(solution)
print('------------------------')
print(answer)

''' УБРАТЬ КЛЮЧЕВЫЕ СЛОВА, ДОБАВИТЬ ФОТО, ДОБАВИТЬ КЛАССЫ, СЛОЖНОСТЬ, ТЕМЫ, НОМЕР
ПРОЙТИСЬ ПО ВСЕМ ЗАДАЧАМ, МАССИВ КЛАССОВ ЗАДАЧ, УДОБНО СОХРАНИТЬ ИХ
СОЗДАТЬ КАЖДОМУ ПОЛЬЗОВАТЕЛЮ УРОВЕНЬ, обдумать эту систему... за правильно решенные задачи добавлять баллы , давать levelup
отформатировать ответ (если есть пункты а б в...)
