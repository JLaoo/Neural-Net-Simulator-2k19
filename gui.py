#Gui Libraries
import kivy
from kivy.app import App 
from kivy.config import Config 
from kivy.core.window import Window
from kivy.uix.label import Label 
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.slider import Slider
from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput 
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
import subprocess
from subprocess import check_call
import sys
import os
import platform
if platform.system() == 'Darwin':
	import appscript

class gui(GridLayout):
	initial_accuracy = StringProperty('Starting Accuracy: 50.0000')
	initial_loss = StringProperty('Starting Loss: 5.0000')
	initial_samples = StringProperty('Number of Samples: 5')
	def __init__(self, **kwargs):
		super(gui, self).__init__(**kwargs)
		#Window Setup
		self.cols = 2
		Config.set('graphics', 'resizable', False)
		Window.size = (670, 240)
		#Starting Accuracy Slider
		self.starting_accuracy = Slider(min=0, max=100, value=50, step=0.0001, 
										size_hint_x=1, size_hint_y=None, height=30)
		self.starting_accuracy.fbind('value', self.on_acc_val)
		self.acc_label = Label(text=str(self.initial_accuracy), 
								size_hint_x=1, size_hint_y=None, height=30)
		self.add_widget(self.acc_label)
		self.add_widget(self.starting_accuracy)
		#Starting Loss Slider
		self.starting_loss = Slider(min=1, max=10, value=5, step=0.0001,
									size_hint_x=1, size_hint_y=None, height=30)
		self.starting_loss.fbind('value', self.on_loss_val)
		self.loss_label = Label(text=str(self.initial_loss),
								size_hint_x=1, size_hint_y=None, height=30)
		self.add_widget(self.loss_label)
		self.add_widget(self.starting_loss)
		#Number of Samples Slider
		self.samples = Slider(min=3, max=10, value=5, step=1,
								size_hint_x=1, size_hint_y=None, height=30)
		self.samples.fbind('value', self.on_sample)
		self.sample_label = Label(text=str(self.initial_samples),
									size_hint_x=1, size_hint_y=None, height=30)
		self.add_widget(self.sample_label)
		self.add_widget(self.samples)
		#Average Training Time Text Input
		self.avg_train_time_label = Label(text='Average Training Time per Sample (In Seconds):',
										size_hint_x=1, size_hint_y=None, height=30)
		self.avg_train_time = TextInput(multiline=False, input_filter='float', hint_text='Default: 1',
										size_hint_x=1, size_hint_y=None, height=30)
		self.add_widget(self.avg_train_time_label)
		self.add_widget(self.avg_train_time)
		#Training Time Variance Dropdown Menu
		self.spinner = Spinner(text='Low', values=('High', 'Medium', 'Low'), sync_height=True,
								size_hint_x=1, size_hint_y=None, height=30)
		self.variance_label = Label(text='Training Time Variance:',
									size_hint_x=1, size_hint_y=None, height=30)
		self.add_widget(self.variance_label)
		self.add_widget(self.spinner)
		#Learning Speed Dropdown Menu
		self.spinner2 = Spinner(text='Low', values=('High', 'Medium', 'Low'), sync_height=True,
								size_hint_x=1, size_hint_y=None, height=30)
		self.speed_label = Label(text='Learning Speed:',
									size_hint_x=1, size_hint_y=None, height=30)
		self.add_widget(self.speed_label)
		self.add_widget(self.spinner2)
		#Number of Epochs Text Input
		self.epochs_label = Label(text='Number of Epochs:',
									size_hint_x=1, size_hint_y=None, height=30)
		self.epochs = TextInput(multiline=False, input_filter='int', hint_text='Default: 10',
								size_hint_x=1, size_hint_y=None, height=30)
		self.add_widget(self.epochs_label)
		self.add_widget(self.epochs)
		#Go!
		inputs = [self.starting_accuracy]
		self.go = Button(text='Go!', on_press=self.begin_simulation,
							size_hint_x=1, size_hint_y=None, height=30)
		self.add_widget(self.go)
		#Stop!
		self.stop = Button(text='Stop!', on_press=self.end_simulation,
							size_hint_x=1, size_hint_y=None, height=30)
		self.add_widget(self.stop)

	def on_acc_val(self, instance, val):
		self.acc_label.text = 'Starting Accuracy: ' + str('%.4f'%(val))

	def on_loss_val(self, instance, val):
		self.loss_label.text = 'Starting Loss: ' + str('%.4f'%(val))

	def on_sample(self, instance, val):
		self.sample_label.text = 'Number of Samples: ' + str(val)

	def begin_simulation(self, btn):
		if self.avg_train_time.text == '':
			train_time = '1'
		else:
			train_time = self.avg_train_time.text
		if self.epochs.text == '':
			num_epochs = '10'
		else:
			num_epochs = self.epochs.text
		lst = [self.starting_accuracy.value, self.starting_loss.value, self.samples.value,
				train_time, self.spinner.text, num_epochs, self.spinner2.text]
		#Initialize Settings
		cwd = os.getcwd()
		with open(cwd + '/SETTINGS.txt', 'w') as outfile:
			outfile.write('STARTING ACCURACY: ' + str(lst[0]) + '\n')
			outfile.write('STARTING LOSS: ' + str(lst[1]) + '\n')
			outfile.write('NUM SAMPLES: ' + str(lst[2]) + '\n')
			outfile.write('AVG TRAIN TIME: ' + str(lst[3]) + '\n')
			outfile.write('TRAIN VARIANCE: ' + str(lst[4]) + '\n')
			outfile.write('NUM EPOCHS: ' + str(lst[5]) + '\n')
			outfile.write('LEARN SPEED: ' + str(lst[6]) + '\n')
		if platform.system() == 'Linux':
			subprocess.call(['gnome-terminal', '-x', 'python3', 'totally_legit_model.py'])
		elif platform.system() == 'Darwin':
			appscript.app('Terminal').do_script('python3 ' + cwd + '/totally_legit_model.py')

	def end_simulation(self, btn):
		subprocess.call(['pkill', '-9', '-f', 'totally_legit_model.py'])

class App(App):
	def build(self):
		self.title = 'Totally Legit Machine Learning'
		return gui()

if __name__ == '__main__':
	App().run()
	subprocess.call(['pkill', '-9', '-f', 'totally_legit_model.py'])
