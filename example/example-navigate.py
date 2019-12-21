# import packages
import sys
import time

# import custom packages
sys.path.append('..')

from config import config as cfg
from browser import driver as dri
from browser import navigate as nav

# define static variables

# define dynamic variables
config = cfg.CONFIG
bri = config.browser_refresh_int
dci = config.data_collection_int
dh = config.driver_headless
dl = config.driver_location
lfp = config.log_file_path
dbg = config.debug
url = config.url


def main():

    # create driver object
    driver = dri.DRIVER(browser_refresh_int=bri, driver_headless=dh, driver_location=dl, log_file_path=lfp, debug=dbg, url=url)
    navigate = nav.NAVIGATE(driver=driver)

    try:

		# check if internet connection exists
        if not driver.check_internet_connection():
            raise Exception('No Internet Connection')

        # wait a second for the modal window to load
		# close modal window
        time.sleep(1)
        navigate.close_modal_window()

		# click event group tabs
        navigate.click_tab(tab_type='event_group', tab_name='Live')
        navigate.click_tab(tab_type='event_group', tab_name='Popular')
        navigate.click_tab(tab_type='event_group', tab_name='Odds Boosts')

        # click best status tabs (Active/Settled only available when logged in)
        navigate.click_tab(tab_type='bet_status', tab_name='Settled')
        navigate.click_tab(tab_type='bet_status', tab_name='Active')
        navigate.click_tab(tab_type='bet_status', tab_name='Betslip')

        # click bet type tabs
        navigate.click_tab(tab_type='bet_type', tab_name='Round Robin')
        navigate.click_tab(tab_type='bet_type', tab_name='Standard')
        navigate.click_tab(tab_type='bet_type', tab_name='Teaser')

    except Exception as e:
        print(str(e))

	# check if driver instance exists
	# close current driver instance windows
    if driver.driver:
        driver.driver.quit()


if __name__ == '__main__':
	main()
