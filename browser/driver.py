# import packages
import os
import time
import datetime
import requests
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# import custom packages

# define static variables

# define dynamic variables


class DRIVER:

	def __init__(self, browser_refresh_int, driver_headless, driver_location, log_file_path, debug, url):
		self.browser_refresh_int = browser_refresh_int
		self.driver_headless = driver_headless
		self.driver_location = driver_location
		self.log_file_path = log_file_path
		self.debug = debug
		self.url = url

		# create webdriver instance
		# setup logging configuration
		# log initial time to track browser refresh requirement
		self.setup_logging()
		self.connect()
		self.browser_refresh_complete_time = time.time()


	# setup logging
	def setup_logging(self):

		# set logging configuration variables
		format = '%(asctime)s.%(msecs)03d [%(levelname)s] :: %(message)s [%(filename)s:%(lineno)d]'
		datefmt = '%Y-%m-%d %H:%M:%S'
		formatter = logging.Formatter(fmt=format, datefmt=datefmt)

		# create root logger
		self.logging = logging.getLogger()
		self.logging.setLevel(logging.INFO)

		fh = logging.FileHandler(filename=self.log_file_path)
		fh.setLevel(logging.INFO)
		fh.setFormatter(formatter)
		self.logging.addHandler(fh)

		if self.debug:
			sh = logging.StreamHandler()
			sh.setLevel(logging.DEBUG)
			sh.setFormatter(formatter)
			self.logging.addHandler(sh)


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
		self.logging.info('Initialized Web Driver Instance')


	# check internet connection
	def check_internet_connection(self):

		try:
			# attempt to access website
			requests.get('https://www.google.com', timeout=10)
			self.logging.info('Confirmed Internet Connection Available')

			return True

		except:
			self.logging.error('Internet Connection Not Available')

		return False


	# refresh browser to ensure client-side continues updating webpage through API calls
	def browser_refresh(self):

		try:
			# refresh browser
			# log browser refresh completed time
			self.driver.refresh()
			self.browser_refresh_complete_time = time.time()
			self.logging.info('Refreshed Driver Instance Browser')

			return True

		except:
			self.logging.error('Unable To Refresh Driver Instance Browser')

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
