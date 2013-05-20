if __name__ == "__main__":
	import sys
	sys.path.append("/usr/local/var/taskserver/")

from task import Task
from selenium import webdriver
import time
import json
from selenium.webdriver.support.ui import Select

from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, WebDriverException

from abstract import AsosRobot

from urlparse import urlparse
import os.path


class URLNotValidException(Exception):
	pass


class AsosCatchProductJob(AsosRobot):
	def __init__(self, arguments):
		self._login = arguments[ "login" ]
		self._password = arguments[ "password" ]
		self._pagelink = arguments["pagelink"]
		self._size_name = arguments[ "size_name" ]
		self._color_name = arguments[ "color_name" ]
		self._progress = (0, "Not finished")
		
	
	def open_product_link(self, webdriver, url):
		pr = urlparse(url)
		if not all([pr.scheme=="http" or pr.scheme=="https", pr.netloc=="www.asos.com", os.path.basename(pr.path)=="pgeproduct.aspx"]):
			raise URLNotValidException()
		webdriver.get( url )
	
	def answer( self, result, message ):
		self._progress = (100, {"result": result, "message": message})
		
	def selenium_script(self, b):
		self._progress = (1, "Started")
		
		self.open_product_link(b, self._pagelink)
		
		try:
			b.find_element_by_xpath("""//div[@class="popup"]//a[@class="lightbox-close close"]""").click()
		except:
			print "WARNING ", self._pagelink, """NOT FOUND: //div[@class="popup"]//a[@class="lightbox-close close"]"""
		
		self._progress = (20, "Loaded Page")
		
		try:
			colorElement = Select(b.find_element_by_id("ctl00_ContentMainPage_ctlSeparateProduct_drpdwnColour"))
			colorElement.select_by_visible_text(self._color_name)
			
			sizeElement = Select(b.find_element_by_id("ctl00_ContentMainPage_ctlSeparateProduct_drpdwnSize"))
			sizeElement.select_by_visible_text(self._size_name)
			
			#ignore alert
			try: 
				alert_popup = b.switch_to_alert()
				alert_popup.accept()
			except WebDriverException:
				pass
			
			item_available = sizeElement.first_selected_option.text == self._size_name and colorElement.first_selected_option.text == self._color_name

		except NoSuchElementException, ex:
			raise
			item_available = False
		
		if item_available:
			bag_button = b.find_element_by_id( "ctl00_ContentMainPage_ctlSeparateProduct_btnAddToBasket" )
			bag_button.click()
			time.sleep(2)
			
			self.login(b)
			self._progress = (100, {"result": "SUCCESS"})
		else:
			self._progress = (100, {"result": "FAIL"})

	def progress(self):
		return self._progress
		
if __name__ == "__main__":

	"""p = AsosCatchProductJob( 
	    {
		"login": "mail@mikefilonov.ru",
		"password":"appleroid55",
		"color":"Dark camel",
		"size":"2107",
		"pagelink": "http://www.asos.com/Ash/Ash-Sioux-Fringed-Wedge-Boots/Prod/pgeproduct.aspx?iid=2370292&SearchQuery=ash&sh=0&pge=0&pgesize=-1&sort=3&clr=Black",
		})"""
	
	#one color
	p = AsosCatchProductJob( 
	    {
		"login": "mail@mikefilonov.ru",
		"password":"appleroid55",
		"color_name":"Print",
		"size_name": "UK 6",
		"pagelink": "http://www.asos.com/pgeproduct.aspx?iid=2798867&abi=1&clr=print&xr=1&xmk=na&xr=3&xr=1&mk=na&r=3"
		})


	# match
	p = AsosCatchProductJob( 
	    {
		"login": "mail@mikefilonov.ru",
		"password":"appleroid55",
		"color_name":"Black",
		"size_name": "UK 12",
		"pagelink": "http://www.asos.com/Urban-Code/Urban-Code-Crop-Leather-Jacket/Prod/pgeproduct.aspx?iid=2475416&cid=10307&sh=0&pge=0&pgesize=-1&sort=3&clr=Vanilla"
		})
	"""
	#out of stock
	p = AsosCatchProductJob( 
	    {
		"login": "mail@mikefilonov.ru",
		"password":"appleroid55",
		"color_name":"Denim",
		"size_name": "UK 8",
		"pagelink": "http://www.asos.com/pgeproduct.aspx?iid=2323803"
		})"""


	"""#bad url
	p = AsosCatchProductJob( 
	    {
		"login": "mail@mikefilonov.ru",
		"password":"appleroid55",
		"color_name":"Denim",
		"size_name": "UK 8",
		"pagelink": "http://yandex.ru/pgeproduct.aspx?iid=2323803"
		})"""


	"""#bad url
	p = AsosCatchProductJob( 
	    {
		"login": "mail@mikefilonov.ru",
		"password":"appleroid55",
		"color_name":"Denim",
		"size_name": "UK 8",
		"pagelink": "http://www.asos.com/Fashion-Online-16/Cat/pgecategory.aspx?cid=13516&WT.ac=Women|HotPieces|Gladiators"
		})
	"""
	
		
	
	p.execute()
	print p.progress()