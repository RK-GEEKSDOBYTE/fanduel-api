# import packages
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# import custom packages
from . import helper

# define static variables

# define dynamic variables


class SELL:

    def __init__(self, driver, screen_load_wait):
        self.driver = driver
        self.screen_load_wait = screen_load_wait
        self.active_bet_reference_ids_xpath = '//div[@class="betrefs"]'
        self.active_bet_current_moneyline_xpath = '//div[@class="stmnt-bets"]/div[contains(@class, "stmnt-bet")][{}]/descendant::span[@class="leginfo-odds pricetype-CP"]'
        self.sell_button_xpath = '//div[@class="stmnt-bets"]/descendant::div[@class="block buyback"][{}]/button[@class="stmnt-btn sb-green"]'
        self.sell_confirmation_button_xpath = '//div[@class="block buyback"]/button[@class="stmnt-btn sb-blue"]'
        self.sold_confirmation_xpath = '//div[@class="legribbon legribbon-boughtback"]'
        self.types = ['less', 'more', 'equal', 'any']


    # create selling/betting rules
    def get_bet_rules(self, type, compare_value, current_value):

        # build ruleset any results if criteria met for each
        rules = [type == 'less' and compare_value > current_value,
                    type == 'equal' and compare_value == current_value,
                    type == 'more' and compare_value < current_value,
                    type == 'any']

        return rules


    # sell bet
    def sell(self, reference_id, compare_moneyline_value, type='equal'):

        # create default variable
        active_bet_order = None

        # check if type parameter input is valid
        if type in self.types:

            try:
                # wait for active bets to exist
                WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.presence_of_element_located((By.XPATH, self.active_bet_reference_ids_xpath)))

            except TimeoutException:
                self.driver.logging.error('Unable To Locate Any Active Bets')

                return False

            active_bet_ids = self.driver.driver.find_elements_by_xpath(self.active_bet_reference_ids_xpath)

            # loop through active bets
            for i, item in enumerate(active_bet_ids):

                # check if active bet has reference id
                # update active_bet_order variable (increment by 1 since selenium starts with index 1)
                if str(reference_id) in item.text:
                    active_bet_order = i + 1
                    self.driver.logging.info('Located Bet #{} Requested To Sell'.format(reference_id))

                    break

            # check if reference # found
            # build current moneyline xpath
            # build sell button xpath
            if active_bet_order:
                self.active_bet_current_moneyline_xpath = self.active_bet_current_moneyline_xpath.format(active_bet_order)
                self.sell_button_xpath = self.sell_button_xpath.format(active_bet_order)

                try:
                    # wait for active bet current moneyline to exist
                    # get active bet current moneyline
                    WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.presence_of_element_located((By.XPATH, self.active_bet_current_moneyline_xpath)))
                    current_moneyline = self.driver.driver.find_element_by_xpath(self.active_bet_current_moneyline_xpath).text
                    self.driver.logging.info('Located Current Moneyline Value Required To Sell')

                    # convert to int type if possible
                    current_moneyline = helper.int_regex(input=current_moneyline)
                    current_moneyline = int(current_moneyline) if helper.is_int(input=current_moneyline) else current_moneyline

                except TimeoutException:
                    self.driver.logging.error('Unable To Locate Current Moneyline Value Required To Sell')

                    return False

                # check if current moneyline was converted to an int
                if helper.is_int(input=current_moneyline):

                    try:
                        # wait for sell button to become clickable
                        # create sell button object
                        WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.sell_button_xpath)))
                        sell_button = self.driver.driver.find_element_by_xpath(self.sell_button_xpath)

                    except TimeoutException:
                        self.driver.logging.error('Unable To Locate Clickable Sell Button')

                        return False

                    # create object of rules on selling a bet based on parameter inputs
                    bet_rules = self.get_bet_rules(type=type, compare_value=compare_moneyline_value, current_value=current_moneyline)

                    # check if any trigger rules met
                    if any(bet_rules):

                        try:
                            # click sell button
                            # wait for sell confirmation button to appear
                            sell_button.click()
                            WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.sell_confirmation_button_xpath)))
                            self.driver.logging.info('Clicked Sell Button')

                        except TimeoutException:
                            self.driver.logging.error('Unable To Complete Process After Clicking Sell Button')

                            return False

                        try:
                            # create sell confirmation button object
                            # click sell confirmation button
                            sell_confirmation_button = self.driver.driver.find_element_by_xpath(self.sell_confirmation_button_xpath)
                            sell_confirmation_button.click()
                            WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.sold_confirmation_xpath)))
                            self.driver.logging.info('Sold Bet #{}'.format(reference_id))

                            return True

                        except TimeoutException:
                            self.driver.logging.error('Unable To Complete Process After Clicking Sell Confirmation Button')

                            return False

                    else:
                        self.driver.logging.error('Desired Bet Based On Parameters Is Not Available')
                        print('Bet API Error: Desired Bet Based On Parameters Is Not Available')
                else:
                    self.driver.logging.error('Current Moneyline Value Required To Sell Not A Number')
            else:
                self.driver.logging.error('Unable To Locate Bet #'.format(reference_id))
        elif type not in self.types:
            self.driver.logging.error('Unable To Sell Because Invalid Parameter Input Provided')

        return False


    def __repr__(self):

        return '{}'.format(vars(self))
