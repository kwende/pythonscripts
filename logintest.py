import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

conn = sqlite3.connect('coupons')
cursor = conn.cursor()

cursor.execute('delete from coupon')
conn.commit()

browser = webdriver.PhantomJS()
browser.implicitly_wait(10) # wait if not readily available

def HandlePage(toInsert, browser, link):

	# get the root coupon divs
        couponItemsList = browser.find_elements_by_xpath(\
                "//div[@class='coupons-list']/div")

	# for each div get the information, append it to the array. 
        for couponItem in couponItemsList:
                idOfCouponItem = couponItem.get_attribute('id').replace('ItemHdr_','')
                couponFields = list(couponItem.find_elements_by_xpath(".//div[@class='inner-coupon-div']/*[2]/div"))

                title = couponFields[0].text
                save = couponFields[1].text
                description = couponFields[2].text
                expires = couponFields[3].text
	
		toInsert.append([title, save, description, expires, link, int(idOfCouponItem)])

if browser is not None: 
	browser.get('https://secure3.mywebgrocer.com/UMA/RegisterSignIn.aspx?uc=AEEAF106')

	emailAddress = browser.find_element_by_id('EmailAddressSignIn')
	password = browser.find_element_by_id('Password')
	loginForm = browser.find_element_by_id('frmSignIn')

	emailAddress.send_keys('ben@ben-rush.net')
	password.send_keys('###')

	loginForm.submit()
	
	allCouponLinks = []
	toInsert = []

	mainPageLink = 'http://super-saver.mywebgrocer.com/Coupons.aspx'

	# get the main coupon page. load the links to the other coupon pages. 
	browser.get(mainPageLink)
	allCouponLinkElements = browser.find_elements_by_xpath(\
		"//div[@class='coupons-pages ui-corner-all']/*[1]/a[@class='coupons-nav']")
	for couponLink in allCouponLinkElements:
		allCouponLinks.append(couponLink.get_attribute('href'))
	
	# get the coupon records on this page
	HandlePage(toInsert, browser, mainPageLink)

	# for each subsequent coupon page, load it and pull down the coupon records
	for couponLink in allCouponLinks:
		print('Navigating to ' + couponLink)
		# load
		browser.get(couponLink)
		# handle
		HandlePage(toInsert, browser, mainPageLink)
	
	# write to the database		
	cursor.executemany('insert into coupon values (?,?,?,?,?,?)', toInsert)
else:
	print('failed')

conn.commit()
conn.close()
