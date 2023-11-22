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
	##NNEEWW
	elif num_funct==1:
		beetype = beeexamples.rastriginbee
	elif num_funct==2:
		beetype = beeexamples.goldsteinbee
	elif num_funct==3:
		beetype = beeexamples.dejongbee




	#beetype = beeexamples.testbee
	#beetype = beeexamples.funcbee
	
	# Количество пчел-разведчиков
	#scoutbeecount = 300
	
	# Количество пчел, отправляемых на выбранные, но не лучшие участки
	#selectedbeecount = 10
	
	# Количество пчел, отправляемые на лучшие участки
	#bestbeecount = 30
	
	
	# Количество выбранных, но не лучших, участков
	#selsitescount = 15
	
	# Количество лучших участков
	#bestsitescount = 5

	
	# Количество запусков алгоритма
	#runcount = 1
	
	# Максимальное количество итераций
	#maxiteration = 2000
	
	# Через такое количество итераций без нахождения лучшего решения уменьшим область поиска
	#max_func_counter = 10	
	
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
			
			#stat.add (runnumber, currhive)
			
			if currhive.bestfitness != best_func:
				# Найдено место, где целевая функция лучше
				best_func = currhive.bestfitness
				func_counter = 0
				
				# Обновим рисунок роя пчел
				#beetestfunc.plotswarm (currhive, 0, 1)
				
				'''print ("\n*** iteration %d / %d" % (runnumber + 1, n))
				print ("Best position: %s" % (str (currhive.bestposition)))
				print ("Best fitness: %f" % currhive.bestfitness)'''
			else:
				func_counter += 1
				if func_counter == max_func_counter:
					# Уменьшим размеры участков
					currhive.range = [currhive.range[m] * koeff[m] for m in range ( len (currhive.range) ) ]
					func_counter = 0
					
					'''print ("\n*** iteration %d / %d (new range)" % (runnumber + 1, n))
					print ("New range: %s" % (str (currhive.range) ))
					print ("Best position: %s" % (str (currhive.bestposition) ))
					print ("Best fitness: %f" % currhive.bestfitness)'''
				
			#if n % 10 == 0:
				#beetestfunc.plotswarm (currhive, 2, 3)

	#beetestfunc.plotstat(stat)
	'''print ("Best position: %s" % (str (currhive.bestposition) ))
	print ("Best fitness: %f" % currhive.bestfitness)'''	
	return [currhive.bestposition,-currhive.bestfitness]

