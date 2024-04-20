import os, shutil, json, tarfile, sys
from pathlib import Path
os.environ['KIVY_NO_CONSOLELOG'] = '1'

args = None
if '-c' in sys.argv:
	flag = sys.argv.index('-c')
	args = sys.argv[flag+1:]
if '--console' in sys.argv:
	flag = sys.argv.index('-console')
	args = sys.argv[flag+1:]

if args:
	if len(args) != 4:
		print('Usage: pmkInstanceCreator wwiseIntegrationPath wwiseSDKPath palworldModdingKitPath newInstancePath', flush=True)

	wwiseIntegration, wwiseSDK, palworldModdingKit, newInstance = list(map(Path, args))

	conds = {
		"Please provide a path for the WWise integration files, it cannot be the same folder as this program": wwiseIntegration == Path(),
		"Please provide a path for the WWise SDK, it cannot be the same folder as this program": wwiseSDK == Path(),
		"Please provide a path for the PalWorld Modding Kit, it cannot be the same folder as this program": palworldModdingKit == Path(),
		"please provide a path to save the new instance to, it cannot be the same folder as this program": newInstance == Path()
	}
	
	for message, cond in conds.items():
		if cond:
			print(f'Error: {message}', flush=True)
			sys.exit()

	if os.path.exists(newInstance):
		if len(os.listdir(newInstance)) > 0:
			print(f"Error: new instance folder ({newInstance}) must be empty", flush=True)
			sys.exit()

	print('creating new instance of the palworld modding kit', flush=True)
	shutil.copytree(palworldModdingKit, newInstance, dirs_exist_ok=True)

	print('extracting wwise integration files', flush=True)
	with tarfile.open(Path(wwiseIntegration) / 'Unreal.5.0.tar.xz') as f:
		f.extractall(newInstance / 'Plugins')

	thirdPartyFolder = newInstance / 'Plugins' / 'Wwise' / 'ThirdParty'
	os.mkdir(thirdPartyFolder)

	print('copying wwise Win32_vc170', flush=True)
	shutil.copytree(wwiseSDK / 'Win32_vc170', thirdPartyFolder / 'Win32_vc170')

	print('creating wwise Win32_vc160', flush=True)
	shutil.copytree(wwiseSDK / 'Win32_vc170', thirdPartyFolder / 'Win32_vc160')


	print('copying wwise x64_vc170', flush=True)
	shutil.copytree(wwiseSDK / 'x64_vc170', thirdPartyFolder / 'x64_vc170')

	print('creating wwise x64_vc160', flush=True)
	shutil.copytree(wwiseSDK / 'x64_vc170', thirdPartyFolder / 'x64_vc160')

	print('copying wwise include', flush=True)
	shutil.copytree(wwiseSDK / 'include', thirdPartyFolder / 'include')


	print('changing WWise.uplugin \"EngineVersion\" to \"5.1\"', flush=True)
	uplugin = {}
	with open(newInstance / 'plugins' / 'WWise' / 'WWise.uplugin', 'r') as f:
		uplugin = json.load(f)

	uplugin['EngineVersion'] = '5.1'

	with open(newInstance / 'plugins' / 'WWise' / 'WWise.uplugin', 'w') as f:
		json.dump(uplugin, f, indent = 4)

	print(f'new instance created at {newInstance}', flush=True)
	sys.exit()

import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock, mainthread
from kivy.resources import resource_add_path, resource_find

from threading import Thread

import tkinter as tk
from tkinter import filedialog as tkFileDialog

class palworldModdingKitInstanceCreator(App):
	def build(self):
		Window.size = (600, 330)
		Window.minimum_height = 330
		Window.minimum_width = 600
		self.icon = 'favicon.ico'
		self.title = 'PMK Instance Creator'
		self.lastPopup = None
		return Builder.load_file('main.kv')

	def browse(self, tinput, title):
		root = tk.Tk()
		root.withdraw()
		root.iconbitmap(os.path.join(sys._MEIPASS, 'favicon.ico'))

		path = tkFileDialog.askdirectory(title=title)

		tinput.text = str(Path(path))

	def popupDismissed(self, p):
		if self.lastPopup == p:
			self.lastPopup = None

	
	def getAllButtonsAndTextInputs(self):
		wids = []
		for widget in self.root.walk():
			if isinstance(widget, Button):
				wids.append(widget)
			if isinstance(widget, TextInput):
				wids.append(widget)

		return wids

	@mainthread
	def createPopup(self, title, message):
		popup = Popup(title=title, content=Label(text=message, halign='center', valign='center'), size_hint=(0.8, 0.4))

		popup.content.bind(size = lambda lab, size: setattr(lab, 'text_size', size))

		popup.bind(on_touch_down=lambda pop, _: pop.dismiss())
		popup.bind(on_dismiss=self.popupDismissed)

		popup.open()
		if self.lastPopup:
			self.lastPopup.dismiss()
			self.lastPopup = None

		self.lastPopup = popup

	def createNewInstanceThread(self, wwiseIntegration, wwiseSDK, palworldModdingKit, newInstance):
		for wid in self.getAllButtonsAndTextInputs():
			wid.disabled = True

		wwiseIntegration = Path(wwiseIntegration)
		wwiseSDK = Path(wwiseSDK)
		palworldModdingKit = Path(palworldModdingKit)
		newInstance = Path(newInstance)

		try:
			conds = {
				"Please provide a path for the WWise integration files, it cannot be the same folder as this program": wwiseIntegration == Path(),
				"Please provide a path for the WWise SDK, it cannot be the same folder as this program": wwiseSDK == Path(),
				"Please provide a path for the PalWorld Modding Kit, it cannot be the same folder as this program": palworldModdingKit == Path(),
				"please provide a path to save the new instance to, it cannot be the same folder as this program": newInstance == Path()
			}
			
			for message, cond in conds.items():
				if cond:
					self.createPopup('Error', message)
					return

			if os.path.exists(newInstance):
				if len(os.listdir(newInstance)) > 0:
					self.createPopup('Error', f"new instance folder ({newInstance}) must be empty")
					return

			self.createPopup('Progress', 'creating new instance of the palworld modding kit')
			shutil.copytree(palworldModdingKit, newInstance, dirs_exist_ok=True)

			self.createPopup('Progress', 'extracting wwise integration files')
			with tarfile.open(Path(wwiseIntegration) / 'Unreal.5.0.tar.xz') as f:
				f.extractall(newInstance / 'Plugins')

			thirdPartyFolder = newInstance / 'Plugins' / 'Wwise' / 'ThirdParty'
			os.mkdir(thirdPartyFolder)

			self.createPopup('Progress', 'copying wwise Win32_vc170')
			shutil.copytree(wwiseSDK / 'Win32_vc170', thirdPartyFolder / 'Win32_vc170')

			self.createPopup('Progress', 'creating wwise Win32_vc160')
			shutil.copytree(wwiseSDK / 'Win32_vc170', thirdPartyFolder / 'Win32_vc160')

			self.createPopup('Progress', 'copying wwise x64_vc170')
			shutil.copytree(wwiseSDK / 'x64_vc170', thirdPartyFolder / 'x64_vc170')

			self.createPopup('Progress', 'creating wwise x64_vc160')
			shutil.copytree(wwiseSDK / 'x64_vc170', thirdPartyFolder / 'x64_vc160')

			self.createPopup('Progress', 'copying wwise include')
			shutil.copytree(wwiseSDK / 'include', thirdPartyFolder / 'include')

			self.createPopup('Progress', 'changing WWise.uplugin \"EngineVersion\" to \"5.1\"')
			uplugin = {}
			with open(newInstance / 'plugins' / 'WWise' / 'WWise.uplugin', 'r') as f:
				uplugin = json.load(f)

			uplugin['EngineVersion'] = '5.1'

			with open(newInstance / 'plugins' / 'WWise' / 'WWise.uplugin', 'w') as f:
				json.dump(uplugin, f, indent = 4)

			self.createPopup('Progress', f'new instance created at {newInstance}')

		except Exception as e:
			self.createPopup('Unhandled Exception', str(e))

		finally:
			for wid in self.getAllButtonsAndTextInputs():
				wid.disabled = False

	def createNewInstance(self, wwiseIntegration, wwiseSDK, palworldModdingKit, newInstance):
		Thread(target=self.createNewInstanceThread, args=(wwiseIntegration, wwiseSDK, palworldModdingKit, newInstance), daemon=True).start()

if __name__ == '__main__':
	if hasattr(sys, '_MEIPASS'):
		resource_add_path(os.path.join(sys._MEIPASS))
	palworldModdingKitInstanceCreator().run()
