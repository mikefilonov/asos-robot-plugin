import sys, traceback


if __name__ == "__main__":
	import sys
	sys.path.append("/usr/local/var/taskserver/")

import time, json, os.path
from urlparse import urlparse


from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, WebDriverException

from asosexceptions import *
from task import Task

class AsosRobot(Task):
	"""Abstract class and example of implementation
	
	Takes two arguments and logs in to the asos site.
	Illustrates the use of arguments, selenium_script and addititonal functions in child-classes
	"""
	def __init__(self, arguments):
		self._login = arguments["login"]
		self._password = arguments["password"]
		self._progress = (0, "Not finished")
		
	def progress(self):
		return self._progress
	
	def answer( self, result, error_type="", message="" ):
		self._progress = (100, {"result": result, "error_type": error_type, "message": message})
	
	def execute(self):
		firefoxProfile = FirefoxProfile()
		firefoxProfile.set_preference('permissions.default.stylesheet', 2)
		firefoxProfile.set_preference('permissions.default.image', 2)
		firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
		b = webdriver.Firefox(firefoxProfile)
		#b = webdriver.Firefox()
		
		try:
			self.selenium_script(b)
			
		except Exception, ex:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			traceback.print_exception( exc_type, exc_value, exc_traceback, limit=2, file=sys.stderr)
			self.answer("FAIL", ex.__class__.__name__, ex.message)
		
		finally:
			b.quit()

		
	def selenium_script(self, b):
		b.get( "http://www.asos.com/pgeproduct.aspx?iid=2370304" )
		self.login(b)
		self.answer( "SUCCESS" )
		
	def login(self, b):
		b.get( "https://www.asos.com" )
		
		
		attempt=0
		while True:
			try:
				b.find_element_by_id("_ctl0_ContentBody_txtEmail")
				break
			except NoSuchElementException:
				attempt+=1
				time.sleep(0.1)
				if attempt > 20:
					raise
			
		attempt=0
		while b.find_element_by_id("_ctl0_ContentBody_txtEmail").get_attribute( "value" ) != self._login and attempt < 20:
			b.find_element_by_id("_ctl0_ContentBody_txtEmail").clear()
			b.find_element_by_id("_ctl0_ContentBody_txtEmail").send_keys( self._login )
			b.find_element_by_id("_ctl0_ContentBody_txtPassword").clear()
			b.find_element_by_id("_ctl0_ContentBody_txtPassword").send_keys( self._password )
			attempt+=1
			time.sleep(0.1)
			
		b.find_element_by_id("_ctl0_ContentBody_btnLogin").click()
		if b.current_url == "https://www.asos.com/":
			raise LoginFailedException()

	def open_product_link(self, b, url):
		pr = urlparse(url)
		if not all([pr.scheme=="http" or pr.scheme=="https", pr.netloc=="www.asos.com", os.path.basename(pr.path)=="pgeproduct.aspx"]):
			raise URLNotValidException()
		b.get( url )

if __name__ == "__main__":
	p = AsosRobot({"login": "mail@mikefilonov.ru", "password": "appleroid55"})
	p.execute()
	print p.progress()
	p.execute()
	print p.progress()
	p.execute()
	print p.progress()
	p.execute()
	print p.progress()
	p.execute()
	print p.progress()
	p.execute()
	print p.progress()
	p.execute()
	print p.progress()
	p.execute()
	print p.progress()

