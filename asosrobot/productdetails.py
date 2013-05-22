if __name__ == "__main__":
	import sys
	sys.path.append("/usr/local/var/taskserver/")

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, WebDriverException

from asosexceptions import *
from abstract import AsosRobot

class AsosProductDetailsJob(AsosRobot):
	def __init__(self, arguments):
		self.pagelink = arguments["pagelink"]
		self._progress = (0, "Not Started")
		
	def selenium_script(self, b):
		self._progress = (1, "Started")
		
		self.open_product_link(b, self.pagelink)
		
		titleElement = b.find_element_by_id("ctl00_ContentMainPage_ctlSeparateProduct_lblProductTitle")
		
		try:
			colorElement = Select(b.find_element_by_id( "ctl00_ContentMainPage_ctlSeparateProduct_drpdwnColour" ))
			
		except NoSuchElementException:
			self.answer( "SUCCESS", "OutOfStockException", {"description": titleElement.text, "colors": [], "sizes": []} )
			return 0
		
		colors = [o.text for o in colorElement.options if o.get_attribute("value") !="-1"]
		sizes = []
		for color in colorElement.options:
			colorElement.select_by_visible_text( color.text )
			sizeElement = Select(b.find_element_by_id( "ctl00_ContentMainPage_ctlSeparateProduct_drpdwnSize" ))
			sizes += [o.text for o in sizeElement.options if o.get_attribute("value") !="-1"]
		
		self.answer( "SUCCESS", "", {"description": titleElement.text, "colors": colors, "sizes": sizes} )
		
		
		

if __name__ == "__main__":
	
	import unittest
	
	class AsosProductDetailsJobUnitTest(unittest.TestCase):
		def test_success(self):
			link = "http://www.asos.com/Ash/Ash-Sioux-Fringed-Wedge-Boots/Prod/pgeproduct.aspx?iid=2370292&SearchQuery=ash&sh=0&pge=0&pgesize=-1&sort=3&clr=Black"
			p = AsosProductDetailsJob({"pagelink": link})
			p.execute()
			notused, answer = p.progress()
			print p.progress()
			self.assertEqual( answer["result"], "SUCCESS" )
			
		def test_bad_link(self):
			link = """http://www.asos.com/Women/Sale/New-In-Clothing/Cat/pgecategory.aspx?cid=5524"""
			p = AsosProductDetailsJob({"pagelink": link})
			p.execute()
			notused, answer = p.progress()
			print p.progress()
			self.assertEqual( answer["result"], "FAIL" )
			self.assertEqual( answer["error_type"], "URLNotValidException" )
			
		def test_out_of_stock(self):
			link = """http://www.asos.com/pgeproduct.aspx?iid=2478339"""
			p = AsosProductDetailsJob({"pagelink": link})
			p.execute()
			notused, answer = p.progress()
			print p.progress()
			self.assertEqual( answer["result"], "SUCCESS" )
			self.assertEqual( answer["error_type"], "OutOfStockException" )
		
	unittest.main(verbosity=2)
