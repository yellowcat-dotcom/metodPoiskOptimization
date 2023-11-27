#-*- coding: utf-8 -*-

import pybee
import beeexamples

#import pylab


#Без графики - графика будет в отдельном модуле для всех лаб

'''
Пчелиный алгоритм
Параметры:
1. Номер оптимизируемой функции
   0 - сферичрская
   2 - Голдштейна
   3 - Розенброка
2. Количество пчёл-разведчиков
3. Количество пчел, отправляемые на лучшие участки
4. Количество пчел, отправляемых на выбранные, но не лучшие участки
5. Количество выбранных, но не лучших, участков
6. Количество лучших участков
7. Количество запусков алгоритма
8. Максимальное количество итераций
9. Через такое количество итераций без нахождения лучшего решения уменьшим область поиска
'''
def bee_algorithm(num_funct,scoutbeecount,bestbeecount,selectedbeecount,selsitescount,
                  bestsitescount,runcount, maxiteration, max_func_counter):

	
	###################################################
	##                     Параметры алгоритма
	###################################################
	
	# Класс пчел, который будет использоваться в алгоритме
	
	if num_funct==0:
		beetype = beeexamples.rosenbrockbee
	elif num_funct==1:
		beetype = beeexamples.rastriginbee
		# NEW !!!!!!
	elif num_funct==2:
		beetype = beeexamples.himmelblaubee
	elif num_funct==3:
		beetype = beeexamples.dejongbee



	# Во столько раз будем уменьшать область поиска
	koeff = beetype.getrangekoeff()
	
	###################################################
		
	for runnumber in range(runcount):		
		currhive = pybee.hive (scoutbeecount, selectedbeecount, bestbeecount, \
							   selsitescount, bestsitescount, \
							   beetype.getstartrange(), beetype)
		
		# Начальное значение целевой функции
		best_func = -1.0e9
		
		# Количество итераций без улучшения целевой функции
		func_counter = 0
		
		#stat.add (runnumber, currhive)
		
		for n in range (maxiteration):
			currhive.nextstep ()

			
			if currhive.bestfitness != best_func:
				# Найдено место, где целевая функция лучше
				best_func = currhive.bestfitness
				func_counter = 0


			else:
				func_counter += 1
				if func_counter == max_func_counter:
					# Уменьшим размеры участков
					currhive.range = [currhive.range[m] * koeff[m] for m in range ( len (currhive.range) ) ]
					func_counter = 0
					

	return [currhive.bestposition,-currhive.bestfitness]

