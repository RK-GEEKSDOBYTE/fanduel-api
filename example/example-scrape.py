# import packages
import sys
from datetime import datetime
import time

# import custom packages
sys.path.append('..')

from config import config as cfg
from browser import driver as dri
from browser import scrape as scp
from browser import navigate as nav

# define static variables

# define dynamic variables
config = cfg.CONFIG
bri = config.browser_refresh_int
dci = config.data_collection_int
dh = config.driver_headless
dl = config.driver_location
url = config.url
sa = {k: v['active'] for k, v in config.sports.items() if v['active'] == True}
shc = {k: v['html_class'] for k, v in  config.sports.items() if k in sa}
sml = {k: v['minute_logged'] for k, v in  config.sports.items() if k in sa}
sa = {k: v for k, v in sa.items() if k in shc and k in sml}


def main():

	# create driver object
	driver = dri.DRIVER(browser_refresh_int=bri, driver_headless=dh, driver_location=dl, url=url)
	navigate = nav.NAVIGATE(driver=driver.driver)
	scrape = scp.SCRAPE(driver=driver.driver)

	try:
		# close modal window
		# click Live group event tab
		navigate.close_modal_window()
		navigate.click_tab(tab_type='event_group', tab_name='Live')

		while True:

			# check if internet connection exists
			if not driver.check_internet_connection():
				raise Exception('No Internet Connection')

			# check if browser needs to be refreshed (ensures client-side continues updating webpage through API calls)
			if driver.check_browser_refresh_required():

				# close modal window
				# click Live group event tab
				navigate.close_modal_window()
				navigate.click_tab(tab_type='event_group', tab_name='Live')

			# log time to start data collection
			# scrape webpage for active events
			data_collection_start_time = time.time()
			data = scrape.get_all_events_info(sports_active=sa, sports_html_classes=shc, sports_minute_logged=sml)
			print('{} --- Found {} record(s)'.format(datetime.now().time(), len(data)))

			# log time to finish data collection
			# calculate data collection interval
			data_collection_finish_time = time.time()
			cycle_duration = data_collection_finish_time - data_collection_start_time

			# check if duration was less time than data collection interval time
			# sleep for the difference (if less)
			if cycle_duration < dci:
				time.sleep(dci - cycle_duration)

        # close current driver instance windows
        driver.driver.quit()

	except Exception as e:
		print(str(e))

		# check if driver instance exists
		# close current driver instance windows
		if driver.driver:
			driver.driver.quit()


if __name__ == '__main__':
	main()
