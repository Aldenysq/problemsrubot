from bs4 import BeautifulSoup as bs
import requests
# url = 'http://problems.ru/view_problem_details_new.php?id=30320'
# page = urllib2.urlopen(quote_page)

def clean_tags(s):
	s_new = ''
	image_string_array = []
	#find for images
	while s.find('<img') != -1:
		num_img = s.find('<img')
		image_string_array.append(s[num_img:s.find('>', num_img)+1])
		s = s[:num_img] + 'IMAGE' +s[s.find('>', num_img)+1:]

	#find for powers
	s = s.replace('<sup>', '^НВИ^') # начало верхнего индекса
	s = s.replace('</sup>', '^КВИ^') # конец верхнего индекса

	s = s.replace('<sub>', '^ННИ^') # начало нижнего индекса
	s = s.replace('</sub>', '^КНИ^') # конец нижнего индекса

	state = 'Closed'
	for char in s:
		if char == '<':
			state = 'Open'
		elif char == '>':
			state = 'Closed'
		elif state == 'Closed':
			s_new += char
	return s_new, image_string_array



n = 73734

r = requests.get('http://problems.ru/view_problem_details_new.php?id=' + str(n))
soup = bs(r.content, 'html5lib')
all_info = str(soup)
cut_1 = all_info.find('<h3>Условие</h3>')
cut_2 = all_info.find('<h3>Подсказка</h3>')
cut_3 = all_info.find('<h3>Решение</h3>')
cut_4 = all_info.find('<h3>Ответ</h3>')
cut_5 = all_info.find('<h3>Источники')




#THEMES

if all_info.find('Темы') != -1:
	cut_themes_start = all_info.find('Темы')
	cut_themes_end = all_info.find('Сложность:')
	themes = all_info[cut_themes_start: cut_themes_end]
	rofl = clean_tags(themes)[0]
	# print(rofl.find('\t'))
	themes_local = rofl.replace('\t', '')
	themes_local = themes_local.replace('\n', '')
	themes_local = themes_local.replace('\xa0', '')
	# themes_local = themes_local.split(' ')
	themes_local = themes_local[5:]
else:
	cut_themes_start = all_info.find('Тема')
	cut_themes_end = all_info.find('Сложность:')
	themes = all_info[cut_themes_start: cut_themes_end]
	rofl = clean_tags(themes)[0]
	# print(rofl.find('\t'))
	themes_local = rofl.replace('\t', '')
	themes_local = themes_local.replace('\n', '')
	themes_local = themes_local.replace('\xa0', '')
	# themes_local = themes_local.split(' ')
	themes_local = themes_local[5:]

array_of_themes = []
while len(themes_local)!=0:
	bracket_open_num = themes_local.find('[')
	bracket_close_num = themes_local.find(']', bracket_open_num)
	local_theme = themes_local[bracket_open_num+1:bracket_close_num]
	themes_local = themes_local[:bracket_open_num] + themes_local[bracket_close_num+1:]
	array_of_themes.append(local_theme)



#GET CLASSES
cut_classes_start = all_info.find('<nobr>Классы')
cut_classes_end = all_info.find('</nobr>', cut_classes_start)
classes_string = all_info[cut_classes_start+14: cut_classes_end]
classes = classes_string.split(',') ##массив классов

###GET LEVELS
cut_level_start = all_info.find('<nobr>Сложность')
cut_level_end = all_info.find('</nobr>', cut_level_start)
level = all_info[cut_level_start+17: cut_level_end] #уровень


#CUT FOR TASK,HINT,SOLUTION,ANSWER
if (cut_4 == -1):
	cut_4 = cut_5

if (cut_3 == -1):
	cut_3 = cut_4

if (cut_2 == -1):
	cut_2 = cut_3

task, task_images = clean_tags(all_info[cut_1:cut_2])
hint, hint_images = clean_tags(all_info[cut_2:cut_3])
solution, solution_images = clean_tags(all_info[cut_3:cut_4])
answer, answer_images = clean_tags(all_info[cut_4:cut_5])

task = task[7:]
hint = hint[9:]
solution = solution[7:]
answer = answer[5:]



print(task, task_images)
print('------------------------')
print(hint, hint_images)
print('------------------------')
print(solution,solution_images)
print('------------------------')
print(answer,answer_images)
print('-----------------------')
print(classes)
print(level)
print(n)
print(array_of_themes)



''' 
сделать что-то с КВИ и НВИ...
обдумать как считать правильный ли ответ
ПРОЙТИСЬ ПО ВСЕМ ЗАДАЧАМ, МАССИВ КЛАССОВ ЗАДАЧ, УДОБНО СОХРАНИТЬ ИХ
СОЗДАТЬ КАЖДОМУ ПОЛЬЗОВАТЕЛЮ УРОВЕНЬ, обдумать эту систему... за правильно решенные задачи добавлять баллы , давать levelup
отформатировать ответ (если есть пункты а б в...)'''
