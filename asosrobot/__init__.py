if __name__ == "__main__":
	import sys
	sys.path.append("/usr/local/var/taskserver/")

from task import Task
from selenium import webdriver
import time
import json


from selenium.webdriver.support.ui import Select



def register_plugin( pm ):
	pm.register("asosrobot", AsosGetSizeRobot)
	pm.register("details.asos", AsosProductDetailsPage)
	
	
	
class AsosRobot(Task):
	def __init__(self, arguments):
		self._login = arguments["login"]
		self._password = arguments["password"]
		pass
		
	def execute(self):
		b = webdriver.Firefox()
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
		
class AsosGetSizeRobot(AsosRobot):
	def __init__(self, arguments):
		super(AsosGetSizeRobot, self).__init__(arguments)
		self._page = arguments["page"]
		self._result = None
		
	def selenium_script(self, b):
		self.login(b)
		self.get_size(b)
		
	def progress(self):
		return (0, "Not finished") if not self._result else (100, self._result)
	
	def get_size(self, b):
		b.get(self._page)
		el = b.find_element_by_id( "ctl00_ContentMainPage_ctlSeparateProduct_drpdwnSize" )
		self._result = [option.text for option in el.find_elements_by_tag_name('option')]

class AsosProductDetailsPage(AsosRobot):
	def __init__(self, arguments):
		self.pagelink = arguments["pagelink"]
		self._progress = (0, "Not finished")
		
	def selenium_script(self, b):
		self._progress = (1, "Started")
		
		b.get( self.pagelink )
		titleElement = b.find_element_by_id("ctl00_ContentMainPage_ctlSeparateProduct_lblProductTitle")
		colorElement = Select(b.find_element_by_id( "ctl00_ContentMainPage_ctlSeparateProduct_drpdwnColour" ))
		colors = [(o.get_attribute("value"),o.text) for o in colorElement.options]
		sizes = []
		for color in colorElement.options:
			colorElement.select_by_visible_text( color.text )
			sizeElement = Select(b.find_element_by_id( "ctl00_ContentMainPage_ctlSeparateProduct_drpdwnSize" ))
			sizes += [(o.get_attribute("value"),o.text) for o in sizeElement.options]
		
		result = {"description": titleElement.text, "colors": dict(colors), "sizes": dict(sizes)}
		
		self._progress = (100, json.dumps(result))


	
	def progress(self):
		return self._progress
		
if __name__ == "__main__":
	p = AsosProductDetailsPage( {"pagelink": "http://www.asos.com/Ash/Ash-Sioux-Fringed-Wedge-Boots/Prod/pgeproduct.aspx?iid=2370292&SearchQuery=ash&sh=0&pge=0&pgesize=-1&sort=3&clr=Black"})
	#p = AsosProductDetailsPage( {"pagelink": "http://www.asos.com/Goldie/Goldie-Floral-Tunic-Dress/Prod/pgeproduct.aspx?iid=2652191&SearchQuery=turquose&sh=0&pge=0&pgesize=-1&sort=3&clr=Turquoise"})
	
	p.execute()
	print p.progress()