import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

conn = sqlite3.connect('coupons')
cursor = conn.cursor()

browser = webdriver.PhantomJS()
browser.implicitly_wait(10) # wait if not readily available

if browser is not None: 
	browser.get('https://secure3.mywebgrocer.com/UMA/RegisterSignIn.aspx?uc=AEEAF106')

	emailAddress = browser.find_element_by_id('EmailAddressSignIn')
	password = browser.find_element_by_id('Password')
	loginForm = browser.find_element_by_id('frmSignIn')

	emailAddress.send_keys('ben@ben-rush.net')
	password.send_keys('###')

	loginForm.submit()

	browser.get('http://super-saver.mywebgrocer.com/Coupons.aspx')

	allCouponLinkElements = browser.find_elements_by_xpath(\
		"//div[@class='coupons-pages ui-corner-all']/*[1]/a[@class='coupons-nav']")

	allCouponLinks = []

	for couponLink in allCouponLinkElements:
		allCouponLinks.append(couponLink.get_attribute('href'))

	toInsert = []

	for couponLink in allCouponLinks:
		print('Navigating to ' + couponLink)

		browser.get(couponLink)
	
		allCouponDivs = browser.find_elements_by_xpath(\
			"//div[@class='coupon-description-container float-right']")	

		for couponDiv in allCouponDivs:
			titleDiv = couponDiv.find_element_by_xpath(".//*[1]/div")
			saveDiv = couponDiv.find_element_by_xpath(".//*[2]/div")			
			descriptionDiv = couponDiv.find_element_by_xpath(".//*[3]/div")
			expiresDiv = couponDiv.find_element_by_xpath(".//*[4]/span")			

			title = titleDiv.text
			save = saveDiv.text
			description = descriptionDiv.text
			expires = expiresDiv.text.replace("Coupon expires: ","")

			toInsert.append([title, save, description, expires])
	
	cursor.executemany('insert into coupon values (?,?,?,?)', toInsert)
else:
	print('failed')

conn.commit()
conn.close()
