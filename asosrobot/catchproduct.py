if __name__ == "__main__":
	import sys
	sys.path.append("/usr/local/var/taskserver/")

import time
import json

import difflib


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
					print "SizeNotAvailable or NoSize for: ", c
				raise SizeNotAvailableException()
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
	
	
	def color_element(self,b):
		try:
			return Select(b.find_element_by_id("ctl00_ContentMainPage_ctlSeparateProduct_drpdwnColour"))
		except NoSuchElementException:
			raise OutOfStockException()

	def size_element(self,b):
		try:
			return Select(b.find_element_by_id("ctl00_ContentMainPage_ctlSeparateProduct_drpdwnSize"))
		except NoSuchElementException:
			raise OutOfStockException()

	
	
	def available_colors(self, b):
		colorElement = self.color_element(b)
		return [o.text for o in colorElement.options if o.get_attribute("value") != "-1"]

	def available_sizes(self, b):
		sizeElement = self.size_element(b)
		return [o.text for o in sizeElement.options if o.get_attribute("value") != "-1"]

	def select_color(self, b, color_name):
		try:
			self.color_element(b).select_by_visible_text(color_name)
		except NoSuchElementException:
			colors = self.available_colors(b)
			raise NoColorException(colors)


	def distance(self, s1, s2):
		def f(a,b):
			return 1 if a==b else 0
		l = min( len(s1), len(s2) )
		return sum( map( lambda a,b: int(a==b),s1[:l],s2[:l]) ) 

	def get_close_matches(self, candidate, available):
		r = difflib.get_close_matches(candidate, [a[:len(candidate)] for a in available])
		if r:
			best = r[0]
			for a in available:
				if a.startswith(best):
					return a
		return candidate


	def select_size(self, b, size_name):
		sizeElement = self.size_element(b)
		
		try:
			if size_name == "*":
				for size in self.available_sizes(b):
					sizeElement.select_by_visible_text(size)
					if not self.size_not_available_alert(b): break
				else:
					raise SizeNotAvailableException()
			else:
				best_size = self.get_close_matches( size_name, self.available_sizes(b))
				print size_name, best_size
				print 'options: ', sizeElement.first_selected_option.get_attribute("value")
				sizeElement.select_by_visible_text(best_size)
				if self.size_not_available_alert(b): raise SizeNotAvailableException()
				print "ok"
		except NoSuchElementException:
			raise NoSizeException( self.available_sizes(b) )


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
		mini_bag = b.find_element_by_id("miniBasketAdded")
		countdown = 10
		while not mini_bag.is_displayed():
			print "attempt ", countdown
			if countdown <=0:
				raise BagNotWorkingException( "Can't put item to bag" )
			countdown -= 0.1
			time.sleep(0.1)
		print "ok"

		
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