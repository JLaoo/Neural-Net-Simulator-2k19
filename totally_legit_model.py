import random
import time
import numpy as np
import os

pid = os.getpid()

with open('SETTINGS.txt', 'r') as f:
	raw_settings = [line.strip() for line in f.readlines()]
settings = [s.split(': ')[1] for s in raw_settings]

def visuals(current_epoch, epochs):
	print('Epoch '+ str(current_epoch) + '/' + str(epochs))
	bars = ''
	starting_bar = '------------------------------'
	loading_bar = starting_bar
	num = 0
	times = []
	block_len = round(30/int(settings[2]))
	block = ''
	add_count = 0
	while add_count < block_len:
		block += '='
		add_count += 1
	bars = ''
	while True:
		if num < 10:
			spaces = '  '
		elif num < 100:
			spaces = ' '
		else:
			spaces = ''
		print(str(num) + '/'+ '240 ' + spaces + '['+loading_bar+']', end="\r")
		bars += block
		starting_bar = starting_bar[block_len:]
		loading_bar = bars + starting_bar
		num += round(240/int(settings[2]))
		if len(bars) > 30:
			break
		avg_sleep_time = float(settings[3])
		if settings[4] == 'High':
			variance = avg_sleep_time/2
		elif settings[4] == 'Medium':
			variance = avg_sleep_time/4
		else:
			variance = avg_sleep_time/8	
		sleep_time = random.uniform(avg_sleep_time-variance, avg_sleep_time+variance)
		times.append(sleep_time)
		time.sleep(sleep_time)
	return np.mean(times)
def simulate_epoch(epochs):
	epoch_count = 1
	start_accuracy = float(settings[0])/100
	start_loss = float(settings[1])
	accuracy = start_accuracy
	loss = start_loss
	learn_speed = settings[6]
	while epoch_count <= epochs:
		distance = 1 - accuracy
		if learn_speed == 'Low':
			acc_denom = random.uniform(15, 20)
			loss_denom = random.uniform(15, 20)
		elif learn_speed == 'Medium':
			acc_denom = random.uniform(10, 15)
			loss_denom = random.uniform(10, 15)
		else:
			acc_denom = random.uniform(5, 10)
			loss_denom = random.uniform(5, 10)
		accuracy_increment = distance/acc_denom
		loss_increment = loss/loss_denom
		avg_time = visuals(epoch_count, epochs)
		avg_time = str('%.3f'%(avg_time))
		bar_str = '240/240 [==============================] - '
		time_str = str(avg_time) + 's/sample - '
		loss_acc_str = 'loss: ' + str('%.4f'%(loss)) + ' - acc: ' + str('%.4f'%(accuracy))
		print(bar_str + time_str + loss_acc_str)
		epoch_count += 1
		accuracy += accuracy_increment
		loss -= loss_increment

simulate_epoch(int(settings[5]))
print('Model Trained!')
