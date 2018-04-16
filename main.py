import threading

from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen


sm = ScreenManager()


class CustomDataHandler():

	def __init__(self):
		self.isActive = False

	def startAutoUpdate(self):
		self.isActive = True
		threading.Timer(0.75, self.executeCommand).start()

	def stopAutoUpdate(self):
		self.isActive = False

	def executeCommand(self):
		if self.isActive:
			print "Hello, World!"
			threading.Timer(0.75, self.executeCommand).start()


class MainView(Screen):

	def showConfig(self):
		sm.switch_to(ShowConfigView())
		pass

	def setConfig(self):
		sm.switch_to(SetConfigView())
		pass


class ShowConfigView(Screen):

	def returnToMainMenu(self):
		sm.switch_to(MainView())
		pass


class SetConfigView(Screen):

	def doNothing(self):
		pass


class MainApp(App):

	myDataHandler = CustomDataHandler()

	def build(self):
		self.myDataHandler.startAutoUpdate()
		self.title = 'Nutzlastkonfigurator'
		sm.add_widget(MainView(name="MainView"))
		return sm

	def on_stop(self):
		print("Application is about to close...")
		self.myDataHandler.stopAutoUpdate()


if __name__ == "__main__":
	Config.set('graphics', 'fullscreen', False)
	Config.set('graphics', 'width', '480')
	Config.set('graphics', 'height', '320')
	Config.write()
	MainApp().run()
