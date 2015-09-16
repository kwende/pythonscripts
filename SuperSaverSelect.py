import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

conn = sqlite3.connect('coupons')
cursor = conn.cursor()

cursor.execute('select * from ToSelect')
toSelects = cursor.fetchall()

browser = webdriver.PhantomJS()
browser.implicitly_wait(10) # wait if not readily available

if browser is not None: 
	browser.get('https://secure3.mywebgrocer.com/UMA/RegisterSignIn.aspx?uc=AEEAF106')

	emailAddress = browser.find_element_by_id('EmailAddressSignIn')
	password = browser.find_element_by_id('Password')
	loginForm = browser.find_element_by_id('frmSignIn')

	fin = open('../supersaverpassword.txt', 'r')
	clearTextPassword = fin.read().replace('\n','')
	fin.close()

	#print('Logging in with password "' + clearTextPassword + '"')
	emailAddress.send_keys('ben@ben-rush.net')
	password.send_keys(clearTextPassword)

	loginForm.submit()
	
	allCouponLinks = []
	toInsert = []

	for toSelect in toSelects:
		idToSelect = toSelect[0]

		cursor.execute('select link from coupon where id = ' + str(idToSelect))
		result = cursor.fetchone()

		print('Need to navigate to page ' + result[0])

		print(str(idToSelect)) 

else:
	print('failed')

conn.commit()
conn.close()
