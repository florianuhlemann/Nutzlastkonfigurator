import threading, random, os, glob

from kivy.app import App
from kivy.config import Config
from kivy.config import ConfigParser
from kivy.event import EventDispatcher
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.uix.accordion import Accordion
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.settings import SettingsPanel, Settings


sm = ScreenManager()


def callback(instance, value):
	print('My callback is call from {} and the a value changed to {}.'.format(instance, value))


class CustomDataHandler(EventDispatcher):

	a = NumericProperty(1.2)

	dataAgrarprodukt = StringProperty("")
	dataNutzlasttyp = StringProperty("")

	def __init__(self):
		self.isActive = False
		#self.bind(a=callback)
		self.bind(dataAgrarprodukt=callback)
		self.bind(dataNutzlasttyp=callback)

	def startAutoUpdate(self):
		self.isActive = True
		threading.Timer(0.75, self.executeCommand).start()

	def stopAutoUpdate(self):
		self.isActive = False

	def executeCommand(self):
		if self.isActive:
			self.a = round((random.randint(0,9999)) / 100.0, 2)
			threading.Timer(0.75, self.executeCommand).start()


myDataHandler = CustomDataHandler()


class MainView(Screen):

	def showConfig(self):
		sm.switch_to(ShowConfigView())

	def setConfig(self):
		sm.switch_to(SetConfigView())


class ShowConfigView(Screen):

	def updateLabel(self):
		self.varOne = "testing"

	def returnToMainMenu(self):
		sm.switch_to(MainView())


class SetConfigView(Screen):

	def returnToMainMenu(self):
		sm.switch_to(MainView())


class SetConfigAccordion(Accordion):

	def setAgrarprodukt(self, Agrarprodukt):
		print("Setting Agrarprodukt to {}".format(Agrarprodukt))
		myDataHandler.dataAgrarprodukt = Agrarprodukt

	def setNutzlasttyp(self, Nutzlasttyp):
		print("Setting Nutzlasttyp to {}".format(Nutzlasttyp))
		myDataHandler.dataAgrarprodukt = Nutzlasttyp


class SetConfigRecycleView(RecycleView):

	def __init__(self, **kwargs):
		super(SetConfigRecycleView, self).__init__(**kwargs)
		os.chdir("Agrarprodukt")
		for file in glob.glob("*.csv"):
			self.data.append({"text" : "{}".format(file[:-4])})
		print(self.data)

	def returnToMainMenu(self):
		sm.switch_to(MainView())


class SetConfigAgrarproduktBoxLayout(BoxLayout):

	def returnText(self):
		return "myText"


class MainApp(App):

	def build(self):
		myDataHandler.startAutoUpdate()
		self.title = 'Nutzlastkonfigurator'
		sm.add_widget(MainView(name="MainView"))
		return sm

	def on_stop(self):
		print("Application is about to close...")
		myDataHandler.stopAutoUpdate()


if __name__ == "__main__":
	#Config.read('myconfig.ini')
	Config.set('graphics', 'fullscreen', 'False')
	Config.set('graphics', 'borderless', '0')
	Config.set('graphics', 'width', '480')
	Config.set('graphics', 'height', '320')
	Config.set('graphics', 'show_cursor', '1')
	Config.write()
	MainApp().run()





