from task import Task
from selenium import webdriver
import time
import json

from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

class LoginFailedException(Exception): pass


class AsosRobot(Task):
	"""Abstract class and example of implementation
	
	Takes two arguments and logs in to the asos site.
	Illustrates the use of arguments, selenium_script and addititonal functions in child-classes
	"""
	def __init__(self, arguments):
		self._login = arguments["login"]
		self._password = arguments["password"]
		pass
		
	def execute(self):
		firefoxProfile = FirefoxProfile()
		firefoxProfile.set_preference('permissions.default.stylesheet', 2)
		firefoxProfile.set_preference('permissions.default.image', 2)
		firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
		b = webdriver.Firefox(firefoxProfile)
		#b = webdriver.Firefox()
		
		
		try:
			self.selenium_script(b)
		finally:
			b.quit()
		
	def selenium_script(self, b):
		self.login(b)
		
	def login(self, b):
		b.get( "https://www.asos.com" )
		b.find_element_by_id("_ctl0_ContentBody_txtEmail").send_keys( self._login )
		b.find_element_by_id("_ctl0_ContentBody_txtPassword").send_keys( self._password )
		b.find_element_by_id("_ctl0_ContentBody_btnLogin").click()
		if b.current_url == "https://www.asos.com/":
			raise LoginFailedException()
