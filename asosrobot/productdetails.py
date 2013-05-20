if __name__ == "__main__":
	import sys
	sys.path.append("/usr/local/var/taskserver/")

from task import Task
from selenium import webdriver
import time
import json
from selenium.webdriver.support.ui import Select

from abstract import AsosRobot

class AsosProductDetailsJob(AsosRobot):
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
	p = AsosProductDetailsJob( {"pagelink": "http://www.asos.com/Ash/Ash-Sioux-Fringed-Wedge-Boots/Prod/pgeproduct.aspx?iid=2370292&SearchQuery=ash&sh=0&pge=0&pgesize=-1&sort=3&clr=Black"})
	#p = AsosProductDetailsJob( {"pagelink": "http://www.asos.com/Goldie/Goldie-Floral-Tunic-Dress/Prod/pgeproduct.aspx?iid=2652191&SearchQuery=turquose&sh=0&pge=0&pgesize=-1&sort=3&clr=Turquoise"})
	
	p.execute()
	print p.progress()