if __name__ == "__main__":
	import sys
	sys.path.append("/usr/local/var/taskserver/")

import time
import json


from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, WebDriverException


from asosexceptions import *
from abstract import AsosRobot


class AsosCatchProductJob(AsosRobot):
	def __init__(self, arguments):
		self._login = arguments[ "login" ]
		self._password = arguments[ "password" ]
		self._pagelink = arguments["pagelink"]
		self._size_name = arguments[ "size_name" ]
		self._color_name = arguments[ "color_name" ]
		self._progress = (0, "Not Started")
		
	def selenium_script(self, b):
		self._progress = (1, "Started")
		
		self.open_product_link(b, self._pagelink)
		self.ignore_popup(b)
		
		self._progress = (20, "Loaded Page")
		
		if self._color_name == "*":
			for c in self.available_colors(b):
				self.select_color(b, c)
				try:
					self.select_size(b, self._size_name)
					break;
				except SizeNotAvailableException, NoSizeException:
					print "- ", c
		else:
			self.select_color( b, self._color_name )
			self.select_size( b, self._size_name )
		self.put_in_bag(b)

		self._progress = (40, "Product fetched")
		self.login(b)
		
		self.answer("SUCCESS")

	def ignore_popup(self, b):
		try:
			b.find_element_by_xpath("""//div[@class="popup"]//a[@class="lightbox-close close"]""").click()
		except:
			print "WARNING ", self._pagelink, """NOT FOUND: //div[@class="popup"]//a[@class="lightbox-close close"]"""
	
	def available_colors(self, b):
		colorElement = Select(b.find_element_by_id("ctl00_ContentMainPage_ctlSeparateProduct_drpdwnColour"))
		return [o.text for o in colorElement.options if o.get_attribute("value") != "-1"]

	def available_sizes(self, b):
		sizeElement = Select(b.find_element_by_id("ctl00_ContentMainPage_ctlSeparateProduct_drpdwnSize"))
		return [o.text for o in sizeElement.options if o.get_attribute("value") != "-1"]

	def select_color(self, b, color_name):
		try:
			colorElement = Select(b.find_element_by_id("ctl00_ContentMainPage_ctlSeparateProduct_drpdwnColour"))
		except NoSuchElementException:
			raise OutOfStockException()
		try:
			colorElement.select_by_visible_text(color_name)
		except NoSuchElementException:
			colors = self.available_colors(b)
			raise NoColorException(colors)

	def select_size(self, b, size_name):
		try:
			sizeElement = Select(b.find_element_by_id("ctl00_ContentMainPage_ctlSeparateProduct_drpdwnSize"))
		except NoSuchElementException:
			raise OutOfStockException()
		try:
			if size_name == "*":
				for size in self.available_sizes(b):
					sizeElement.select_by_visible_text(size)
					if not self.size_not_available_alert(b): break
				else:
					raise SizeNotAvailableException()
			else:
				sizeElement.select_by_visible_text(size_name)
				if self.size_not_available_alert(b): raise SizeNotAvailableException()
		except NoSuchElementException:
			raise NoSizeException( self.available_sizes() )


	def size_not_available_alert(self, b):
		try: 
			alert_popup = b.switch_to_alert()
			alert_popup.accept()
			return True
		except WebDriverException:
			return False
			
			
	def put_in_bag(self, b):
		bag_button = b.find_element_by_id( "ctl00_ContentMainPage_ctlSeparateProduct_btnAddToBasket" )
		bag_button.click()
		
		mini_bag = b.find_element_by_id ("miniBasketAdded")
		countdown = 10
		while not mini_bag.is_displayed():
			if countdown <=0:
				raise BagNotWorkingException( "Can't put item to bag" )
			countdown -= 0.1
			time.sleep(0.1)

		
if __name__ == "__main__":

	"""
	p = AsosCatchProductJob({
		"login": "mail@mikefilonov.ru",
		"password":"appleroid55",
		"color":"Dark camel",
		"size":"2107",
		"pagelink": "http://www.asos.com/Ash/Ash-Sioux-Fringed-Wedge-Boots/Prod/pgeproduct.aspx?iid=2370292&SearchQuery=ash&sh=0&pge=0&pgesize=-1&sort=3&clr=Black",
		})
	"""
	
	"""
	#one color
	p = AsosCatchProductJob(  {
		"login": "mail@mikefilonov.ru",
		"password":"appleroid55",
		"color_name":"Print",
		"size_name": "UK 6",
		"pagelink": "http://www.asos.com/pgeproduct.aspx?iid=2798867&abi=1&clr=print&xr=1&xmk=na&xr=3&xr=1&mk=na&r=3"
		})
	"""

	
	# match
	p = AsosCatchProductJob( 
	    {
		"login": "mail@mikefilonov.ru",
		"password":"appleroid55",
		"color_name":"*",
		"size_name": "*",
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
		})
	"""

	"""#bad url
	p = AsosCatchProductJob( 
	    {
		"login": "mail@mikefilonov.ru",
		"password":"appleroid55",
		"color_name":"Denim",
		"size_name": "UK 8",
		"pagelink": "http://yandex.ru/pgeproduct.aspx?iid=2323803"
		})"""

	"""
	#bad url
	p = AsosCatchProductJob( 
	    {
		"login": "mail@mikefilonov.ru",
		"password":"appleroid55",
		"color_name":"Denim",
		"size_name": "UK 8",
		"pagelink": "http://www.asos.com/Fashion-Online-16/Cat/pgecategory.aspx?cid=13516&WT.ac=Women|HotPieces|Gladiators"
		})
	"""
	
	#Size not available
	p = AsosCatchProductJob( 
	    {
		"login": "mail@mikefilonov.ru",
		"password":"appleroid55",
		"color_name":"Vanilla",
		"size_name": "UK 10",
		"pagelink": "http://www.asos.com/Urban-Code/Urban-Code-Crop-Leather-Jacket/Prod/pgeproduct.aspx?iid=2475416&cid=10307&sh=0&pge=0&pgesize=-1&sort=3&clr=Vanilla"
		})
	


	p = AsosCatchProductJob( 
	    {
		"login": "mail@mikefilonov.ru",
		"password":"appleroid55",
		"color_name":"*",
		"size_name": "*",
		"pagelink": "http://www.asos.com/pgeproduct.aspx?iid=2370304" 
		})

	
	
	
	
	p.execute()
	print p.progress()