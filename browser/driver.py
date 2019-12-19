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

	def __init__(self, browser_refresh_int, driver_headless, driver_location, log_file_directory, debug, url):
		self.browser_refresh_int = browser_refresh_int
		self.driver_headless = driver_headless
		self.driver_location = driver_location
		self.log_file_directory = log_file_directory
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
		debug_level = logging.DEBUG
		log_level = logging.INFO
		format = '%(asctime)s.%(msecs)03d [%(levelname)s] :: %(message)s [%(filename)s:%(lineno)d]'
		datefmt = '%Y-%m-%d %H:%M:%S'
		log_file_name = 'sys_' + str(datetime.date.today()) + ".log"
		log_file_path = os.path.join(self.log_file_directory, log_file_name)

		# create logging object
		# set logging object configuration
		self.logging = logging
		self.logging.basicConfig(level=log_level, format=format, filename=log_file_path, datefmt=datefmt)

		# check if debug set to True to display logging on console
		# set up logging to console
		if self.debug:
			console = logging.StreamHandler()
			console.setLevel(logging.DEBUG)
			console.setFormatter(logging.Formatter(fmt=format, datefmt=datefmt))
			self.logging.getLogger().addHandler(console)


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
