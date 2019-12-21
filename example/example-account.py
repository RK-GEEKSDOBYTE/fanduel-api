# import packages
import sys
import time

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
lfp = config.log_file_path
dbg = config.debug
url = config.url


def main():

    # create driver object
    driver = dri.DRIVER(browser_refresh_int=bri, driver_headless=dh, driver_location=dl, log_file_path=lfp, debug=dbg, url=url)
    navigate = nav.NAVIGATE(driver=driver)
    account = act.ACCOUNT(driver=driver, screen_load_wait=slw)

    try:

		# check if internet connection exists
        if not driver.check_internet_connection():
            raise Exception('No Internet Connection')

        # wait a second for the modal window to load
		# close modal window
        time.sleep(1)
        navigate.close_modal_window()

        # login to account
        # close modal window
        # close plugin
        account.login(username=username, password=password)
        navigate.close_modal_window()
        navigate.close_plugin()

        # click Live group event tab
        navigate.click_tab(tab_type='event_group', tab_name='Live')

        # get account information
        last_login = account.get_user_information(information_type='last_login')
        session_time = account.get_user_information(information_type='session_time')
        available_funds = account.get_user_information(information_type='available_funds')

        # print account information
        print('Last Login: {}'.format(last_login))
        print('Session Time: {}'.format(session_time))
        print('Avaiable Funds: {}'.format(available_funds))

        # toggle active bets that can be cashed out
        navigate.click_tab(tab_type='bet_status', tab_name='Active')
        navigate.toggle_cashout(active=True)
        navigate.toggle_cashout(active=False)
        navigate.toggle_cashout(active=False)

        # toggle active bets that can be cashed out
        navigate.click_tab(tab_type='bet_status', tab_name='Betslip')
        navigate.toggle_cashout(active=True)
        navigate.toggle_cashout(active=False)
        navigate.toggle_cashout(active=False)

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
