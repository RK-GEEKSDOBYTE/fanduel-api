# import packages
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# import custom packages

# define static variables

# define dynamic variables


class DRIVER:

	def __init__(self, browser_refresh_int, driver_headless, driver_location, url):
		self.browser_refresh_int = browser_refresh_int
		self.driver_headless = driver_headless
		self.driver_location = driver_location
		self.url = url

		# create webdriver instance
		# log initial time to track browser refresh requirement
		self.connect()
		self.browser_refresh_complete_time = time.time()


	# create webdriver instance
	def connect(self):

		# set headless attribute
		# set window size attribute to ensure consistency across devices
		options = Options()
		options.headless = self.driver_headless
		options.add_argument('window-size=1200,1100')

		# create webdriver object
		# navigate to webpage
		self.driver = webdriver.Chrome(self.driver_location, chrome_options=options)
		self.driver.get(self.url)
		print('Driver API Success: Created Web Driver')


	# check internet connection
	def check_internet_connection(self):

		try:
			# attempt to access website
			requests.get('https://www.google.com', timeout=10)
			print('Driver API Success: Internet Connection Exists')

			return True

		except:
			print('Driver API Error: No Internet Connection')

		return False


	# refresh browser to ensure client-side continues updating webpage through API calls
	def browser_refresh(self):

		try:
			# refresh browser
			# log browser refresh completed time
			self.driver.refresh()
			self.browser_refresh_complete_time = time.time()
			print('Driver API Success: Refreshed Browser')

			return True

		except:
			print('Drive API Error: Unable To Refresh Browser')

		return False


	# check if browser refresh is required
	def check_browser_refresh_required(self):

		# calculate time elapsed since driver creation or last refresh
		time_elapsed = time.time() - self.browser_refresh_complete_time

		# check if time elapsed is greater than browser refresh interval
		# refresh webpage
		if time_elapsed > self.browser_refresh_int:
			return True

		return False


	def __repr__(self):

		return '{}'.format(vars(self))
