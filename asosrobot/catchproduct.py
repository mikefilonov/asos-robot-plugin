if __name__ == "__main__":
	import sys
	sys.path.append("/usr/local/var/taskserver/")

from task import Task
from selenium import webdriver
import time
import json
from selenium.webdriver.support.ui import Select

from selenium.common.exceptions import NoAlertPresentException

from abstract import AsosRobot

class AsosCatchProductJob(AsosRobot):
	def __init__(self, arguments):
		self._login = arguments[ "login" ]
		self._password = arguments[ "password" ]
		self._pagelink = arguments["pagelink"]
		self._size = arguments[ "size" ]
		self._color = arguments[ "color" ]
		self._progress = (0, "Not finished")
		
	def selenium_script(self, b):
		self._progress = (1, "Started")
		
		b.get( self._pagelink )
		
		
		el = b.find_element_by_xpath("""//div[@class="popup"]//a[@class="lightbox-close close"]""")
		el.click()
		
		
		self._progress = (20, "Loaded Page")
		
		colorElement = Select(b.find_element_by_id( "ctl00_ContentMainPage_ctlSeparateProduct_drpdwnColour" ))
		colorElement.select_by_value(self._color)
		
		sizeElement = Select(b.find_element_by_id( "ctl00_ContentMainPage_ctlSeparateProduct_drpdwnSize" ))
		sizeElement.select_by_value(self._size)
		
		item_available = False
		
		
		
		
		try:
			a = b.switch_to_alert()
			a.accept()
			time.sleep(1)
			item_available = False
			
		except:
			item_available = sizeElement.first_selected_option.get_attribute("value") == self._size
			
		if item_available:
			bag_button = b.find_element_by_id( "ctl00_ContentMainPage_ctlSeparateProduct_btnAddToBasket" )
			bag_button.click()
			time.sleep(10)
			
			self.login(b)
			dir(b.current_url)
			
			time.sleep(10)
			
			
			self._progress = (100, {"result": "SUCCESS"})
		
		else:
			self._progress = (100, {"result": "FAIL"})
		
		

	def progress(self):
		return self._progress
		
if __name__ == "__main__":
	p = AsosCatchProductJob( 
	    {
		"login": "mail@mikefilonov.ru",
		"password":"appleroid55",
		"color":"Dark camel",
		"size":"2107",
		"pagelink": "http://www.asos.com/Ash/Ash-Sioux-Fringed-Wedge-Boots/Prod/pgeproduct.aspx?iid=2370292&SearchQuery=ash&sh=0&pge=0&pgesize=-1&sort=3&clr=Black",
		
		
		})
	#p = AsosProductDetailsPage( {"pagelink": "http://www.asos.com/Goldie/Goldie-Floral-Tunic-Dress/Prod/pgeproduct.aspx?iid=2652191&SearchQuery=turquose&sh=0&pge=0&pgesize=-1&sort=3&clr=Turquoise"})
	
	p.execute()
	print p.progress()