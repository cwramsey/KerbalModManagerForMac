#!/usr/bin/python
import getpass
import os
import shutil

from Tkinter import *
from ConfigParser import SafeConfigParser

class ModManager:
	master = None
	kerbal_locations = {}
	frames = {}
	buttons = {}
	labels = {}
	mod_list = None
	
	def __init__(self, frameObject):
		self.master = frameObject
		#Parse ini file
		parser = SafeConfigParser()
		parser.read('config.ini')
		self.kerbal_locations.update({'Steam': parser.get('kerbal_locations', 'steam').replace('{user}', getpass.getuser())})
		
	def add_elements(self):
		#Title
		self.master.wm_title("Kerbal Mod Manager For Mac")
		
		 #Create frames and buttons
		self.frames.update({'app_name': Frame(self.master,
			width=768,
			height=50)})
		self.frames['app_name'].pack()
		
		#Add app label
		self.appName = Label(
			self.frames['app_name'],
			text="Kerbal Mod Manager For Mac")
		self.appName.pack()
		
		self.frames.update({'install_location': Frame(self.master) })
		self.frames['install_location'].pack()
		
		#loop through locations from config.ini and find the application
		found_install = FALSE
		for key in self.kerbal_locations:
			if os.path.isdir(self.kerbal_locations[key]):
				#Create labels
				self.labels.update({'location': Label(
					self.frames['install_location'],
					text="Looks like you're using " + key)})
				self.labels['location'].pack(side=LEFT)
				
				self.labels.update({'mod_count': Label(
					self.frames['install_location'],
					text=self.count_mods(self.kerbal_locations[key]) + ' Mods found')})
				self.labels['mod_count'].pack(side=LEFT)
				
				#Make list of mods
				self.frames.update({'mod_list': Frame(self.master)})
				self.frames['mod_list'].pack()
				
				self.mod_list = Listbox(self.frames['mod_list'],
					selectmode=EXTENDED)
				self.mod_list.pack()
				
				#Add mods to list
				for mod in os.walk(self.kerbal_locations[key]).next()[1]:
					if mod != "Squad":
						self.mod_list.insert(END, mod)
				
				#add delete mod button
				self.buttons.update({'delete_mod': Button(
					self.frames['mod_list'],
					text="Delete Mod(s)",
					command=self.delete_mod)})
				self.buttons['delete_mod'].pack(side=BOTTOM)
				
				found_install = TRUE
				
		if found_install == FALSE:
			self.location = Label(
			self.frames['install_location'],
					text="Sorry, we couldn't find the installation.")
			self.location.pack(side=LEFT)
				
		self.frames.update({'controls': Frame(self.master) })
		self.frames['controls'].pack()
		
		self.quit = Button(
			self.frames['controls'],
			text="QUIT",
			command=self.frames['app_name'].quit)
		self.quit.pack(side=LEFT)
		
	def count_mods(self, directory):
		mods = os.walk(directory).next()[1]
		mod_count = 0
		for mod in mods:
			if mod != 'Squad':
				mod_count += 1
				
		return str(mod_count)
		
	def delete_mod(self):
		selected = map(int, self.mod_list.curselection())
		for mod in selected:
			shutil.rmtree(self.kerbal_locations['Steam'] + '/' + self.mod_list.get(mod))
			self.mod_list.delete(mod)
		
		
				
		
root = Tk()
app = ModManager(root)
app.add_elements()
root.mainloop()