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


class URLNotValidException(Exception): pass
class OutOfStockException(Exception): pass
class NoColorException(Exception): pass
class NoSizeException(Exception): pass
class SizeNotAvailableException(Exception): pass
from abstract import LoginFailedException

class UnknownException(Exception): pass

class AsosCatchProductJob(AsosRobot):
	def __init__(self, arguments):
		self._login = arguments[ "login" ]
		self._password = arguments[ "password" ]
		self._pagelink = arguments["pagelink"]
		self._size_name = arguments[ "size_name" ]
		self._color_name = arguments[ "color_name" ]
		self._progress = (0, "Not finished")
		

	def progress(self):
		return self._progress
	
	def answer( self, result, error_type="", message="" ):
		self._progress = (100, {"result": result, "error_type": error_type, "message": message})
		
	def selenium_script(self, b):
		try:
			self.catch_item(b)
		except Exception, ex:
			self.answer("FAIL", ex.__class__.__name__, ex.message)

	def catch_item(self, b):
		self._progress = (1, "Started")
		
		self.open_product_link(b, self._pagelink)
		self.ignore_popup(b)
		
		self._progress = (20, "Loaded Page")

		self.select_color( b, self._color_name )
		self.select_size( b, self._size_name )
		self.put_in_bag(b)
		self.login(b)
		
		self.answer("SUCCESS")


	def open_product_link(self, webdriver, url):
		pr = urlparse(url)
		if not all([pr.scheme=="http" or pr.scheme=="https", pr.netloc=="www.asos.com", os.path.basename(pr.path)=="pgeproduct.aspx"]):
			raise URLNotValidException()
		webdriver.get( url )

		
	def ignore_popup(self, b):
		try:
			b.find_element_by_xpath("""//div[@class="popup"]//a[@class="lightbox-close close"]""").click()
		except:
			print "WARNING ", self._pagelink, """NOT FOUND: //div[@class="popup"]//a[@class="lightbox-close close"]"""


	def select_color(self, b, color_name):
		try:
			colorElement = Select(b.find_element_by_id("ctl00_ContentMainPage_ctlSeparateProduct_drpdwnColour"))
		except NoSuchElementException:
			raise OutOfStockException()
		try:
			colorElement.select_by_visible_text(color_name)
		except NoSuchElementException:
			colors = [o.text for o in colorElement.options  if o.get_attribute("value") != "-1"]
			raise NoColorException(colors)

	def select_size(self, b, size_name):
		try:
			sizeElement = Select(b.find_element_by_id("ctl00_ContentMainPage_ctlSeparateProduct_drpdwnSize"))
		except NoSuchElementException:
			raise OutOfStockException()
		try:
			sizeElement.select_by_visible_text(self._size_name)
		except NoSuchElementException:
			size = [o.text for o in sizeElement.options if o.get_attribute("value") != "-1"]
			raise NoSizeException(size)

		#ignore alert
		try: 
			alert_popup = b.switch_to_alert()
			alert_popup.accept()
			raise SizeNotAvailableException()
		except WebDriverException:
			pass
			

	def put_in_bag(self, b):
		bag_button = b.find_element_by_id( "ctl00_ContentMainPage_ctlSeparateProduct_btnAddToBasket" )
		bag_button.click()
		
		mini_bag = b.find_element_by_id ("miniBasketAdded")
		countdown = 30
		while not mini_bag.is_displayed():
			countdown -= 1
			if countdown <=0:
				raise UnknownException( "Can't put item to bag" )
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
	
	#one color
	p = AsosCatchProductJob(  {
		"login": "mail@mikefilonov.ru",
		"password":"appleroid55",
		"color_name":"Print",
		"size_name": "UK 6",
		"pagelink": "http://www.asos.com/pgeproduct.aspx?iid=2798867&abi=1&clr=print&xr=1&xmk=na&xr=3&xr=1&mk=na&r=3"
		})


	
	"""# match
	p = AsosCatchProductJob( 
	    {
		"login": "mail@mikefilonov.ru",
		"password":"appleroid55",
		"color_name":"Black",
		"size_name": "UK 12",
		"pagelink": "http://www.asos.com/Urban-Code/Urban-Code-Crop-Leather-Jacket/Prod/pgeproduct.aspx?iid=2475416&cid=10307&sh=0&pge=0&pgesize=-1&sort=3&clr=Vanilla"
		})"""
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
	"""
	#Size not available
	p = AsosCatchProductJob( 
	    {
		"login": "mail@mikefilonov.ru",
		"password":"appleroid55",
		"color_name":"Vanilla",
		"size_name": "UK 4",
		"pagelink": "http://www.asos.com/Urban-Code/Urban-Code-Crop-Leather-Jacket/Prod/pgeproduct.aspx?iid=2475416&cid=10307&sh=0&pge=0&pgesize=-1&sort=3&clr=Vanilla"
		})
	"""
	
	
	p.execute()
	print p.progress()