# import packages
import sys

# import custom packages
sys.path.append('..')

from config import config as cfg
from browser import driver as dri
from browser import navigate as nav
from browser import account as act

# define static variables
username = ''
password = ''

# define dynamic variables
config = cfg.CONFIG
bri = config.browser_refresh_int
dci = config.data_collection_int
slw = config.screen_load_wait
dh = config.driver_headless
dl = config.driver_location
url = config.url


def main():

    # create driver object
    driver = dri.DRIVER(browser_refresh_int=bri, driver_headless=dh, driver_location=dl, url=url)
    navigate = nav.NAVIGATE(driver=driver.driver)
    account = act.ACCOUNT(driver=driver.driver, screen_load_wait=slw)

    try:

		# check if internet connection exists
        if not driver.check_internet_connection():
            raise Exception('No Internet Connection')

		# close modal window
        navigate.close_modal_window()

        # login to account
        account.login(username=username, password=password)
        navigate.close_plugin()

        # click Live group event tab
        navigate.click_tab(tab_type='event_group', tab_name='Live')

        # get account information
        last_login = account.get_user_information(information_type='last_login')
        session_time = account.get_user_information(information_type='session_time')
        available_funds = account.get_user_information(information_type='available_funds')

        # logout of account
        account.logout()


    except Exception as e:
        print(str(e))

		# check if driver instance exists
		# close current driver instance windows
        if driver.driver:
            driver.driver.quit()


if __name__ == '__main__':
	main()
