# import packages
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# import custom packages
from . import helper

# define static variables

# define dynamic variables


class BUY:

    def __init__(self, driver, screen_load_wait):
        self.driver = driver
        self.screen_load_wait = screen_load_wait
        self.event_categories_xpath = '//div[@class="live-event-container"]/descendant::span[@class="coupontitle"]'
        self.teams_xpath_placeholder = '//div[@class="live-event-container"][{}]/descendant::section[@class="eventTitleWrapper"]/descendant::span[@class="name"]'
        self.bet_type_button_xpath_placeholder = '//div[@class="live-event-container"][{}]/descendant::div[contains(@class, "big3-event")][{}]/descendant::div[@class="{}"]/descendant::div[contains(@class, "selection-wapper selection-data")][{}]'
        self.betslip_empty_xpath = '//div[@class="empty-betslip REGULAR"]'
        self.bet_amount_field_xpath = '//div[@class="singles REGULAR"]/descendant::span[@class="stake"]/div[@class="money-input"]/input'
        self.place_bet_button_xpath = '//*[@id="SBbetSlip"]/div[7]/div[2]/div[2]/div[2]/div[2]/button'
        self.bet_confirmation_receipt_xpath = '//div[@class="your_receipt_desktop"]'
        self.bet_confirmation_exit_button_xpath = '//div[@class="betPlacement"]/descendant::div[@class="column column-left"]/button[@class="btn secondary"]'
        self.bet_reference_id_xpath = '//div[@class="reference"]/span[@class="value"]'
        self.odds_changed_banner_xpath = '//div[@class="singles REGULAR"]/descendant::div[@class="header-changed msg info"]'
        self.delete_all_bets_xpath = '//div[@class="betslip_actions"]/descendant::button[@class="delALL btn"]'
        self.types = ['less', 'more', 'equal', 'any']
        self.bet_types =    {
                            'spread':       {
                                            'xpath_class': 'market points',
                                            'type': 'float'
                                            },
                            'moneyline':    {
                                            'xpath_class': 'market money',
                                            'type': 'int'
                                            },
                            'total':        {
                                            'xpath_class': 'market total',
                                            'type': 'float'
                                            }
                            }


    # create selling/betting rules
    def get_bet_rules(self, type, compare_value, current_value):

        # build ruleset any results if criteria met for each
        rules = [type == 'less' and compare_value > current_value,
                    type == 'equal' and compare_value == current_value,
                    type == 'more' and compare_value < current_value,
                    type == 'any']

        return rules


    # delete all bets from betslip
    def delete_bets(self):

        # check if delete all bets button xpath exists
        if self.driver.driver.find_elements_by_xpath(self.delete_all_bets_xpath):

            try:
                # wait for delete all bets button to be cliackable
                WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.delete_all_bets_xpath)))

            except TimeoutException:
                self.driver.logging.error('Unable To Locate The Clickable Delete All Bets Button')

                return False

            try:
                # create delete all bets button object
                # click delete all bets button
                # wait for empty betslip xpath to exist
                delete_all_bets_button = self.driver.driver.find_element_by_xpath(self.delete_all_bets_xpath)
                delete_all_bets_button.click()
                WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.presence_of_element_located((By.XPATH, self.betslip_empty_xpath)))
                self.driver.logging.info('Deleted All Bets')

                return True

            except TimeoutException:
                self.driver.logging.error('Submission To Delete All Bets Exceeded Time Limit')

                return True

        else:
            self.driver.logging.error('Unable To Locate The Delete All Bets Button')

        return False


    # submit bet
    def buy(self, bet_amount, league, team_name, compare_bet_type_value, bet_type='moneyline', type='equal'):

        # create default variables
        event_category_id = None
        team_id = None

        # check if bet_type and type parameter inputs are valid
        if bet_type in self.bet_types and type in self.types:

            # get live event categories
            event_categories = self.driver.driver.find_elements_by_xpath(self.event_categories_xpath)

            # loop through event categories
            for i, item in enumerate(event_categories):

                # check if league event category exists
                # update event_category_id variable (increment by 1 since selenium starts with index 1)
                if event_categories[i].text == league:
                    event_category_id = i + 1
                    break

            # check if event_category_id updated
            if event_category_id:

                # create teams_xpath
                # find all teams currently playing within event category
                teams_xpath = self.teams_xpath_placeholder.format(event_category_id)
                team_names = self.driver.driver.find_elements_by_xpath(teams_xpath)

                # loop through teams
                for j, item in enumerate(team_names):

                    # check if team exists
                    # update event_team_builder variable (increment by 1 since selenium starts with index 1)
                    if team_names[i].text == team_name:
                        team_id = j + 1
                        break

                # check if event/team div builder id exists
                # assign event and team div ids
                # create moneyline xpath
                if team_id:
                    event_div_id = round((event_category_id / 2) + .01)
                    team_div_id = 2 if team_id % 2 == 0 else 1
                    bet_type_button_xpath = self.bet_type_button_xpath_placeholder.format(event_category_id, event_div_id, self.bet_types[bet_type]['xpath_class'], team_div_id)

                    try:
                        # check if bet type button is clickable
                        WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, bet_type_button_xpath)))

                    except TimeoutException:
                        self.driver.logging.error('Unable To Locate The Clickable Button Labeled {}'.format(bet_type.title()))

                        return False

                    try:
                        # get bet type button value
                        bet_type_value = self.driver.driver.find_element_by_xpath(bet_type_button_xpath).text

                        # check if bet type should be a float value
                        # convert bet type value to float
                        if self.bet_types[bet_type]['type'] == 'float':
                            bet_type_value = helper.float_regex(input=bet_type_value)
                            bet_type_value  = float(bet_type_value) if helper.is_float(input=bet_type_value) else bet_type_value

                        # check if bet_type should be an int value
                        # convert bet type value to int
                        elif self.bet_types[bet_type]['type'] == 'int':
                            bet_type_value = helper.int_regex(input=bet_type_value)
                            bet_type_value = int(bet_type_value) if helper.is_int(input=bet_type_value) else bet_type_value

                        if not helper.is_int(input=bet_type_value) and not helper.is_float(input=bet_type_value):
                            self.driver.logging.error('Unable To Convert The {} Button Value To Int/Float'.format(bet_type.title()))

                            return False

                    except:
                        self.driver.logging.error('Unable To Extract The {} Button Value'.format(bet_type.title()))

                        return False

                    # create object of rules on triggering a bet based on parameter inputs
                    bet_rules = self.get_bet_rules(type=type, compare_value=compare_bet_type_value, current_value=bet_type_value)

                    # check if any trigger rules met
                    if any(bet_rules):

                        try:
                            # create bet type button object
                            # click bet type button
                            # wait for betslip bet amount field to be clickable
                            bet_type_button = self.driver.driver.find_element_by_xpath(bet_type_button_xpath)
                            bet_type_button.click()
                            WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.bet_amount_field_xpath)))
                            self.driver.logging.info('Loaded Betslip Form')

                        except TimeoutException:
                            self.driver.logging.error('Betslip Form Load Exceeded Time Limit')

                            return False

                        try:
                            # create bet amount field object
                            # populate bet amount field
                            # wait for odds changed banner or place bet button to exist
                            bet_amount_field = self.driver.driver.find_element_by_xpath(self.bet_amount_field_xpath)
                            bet_amount_field.send_keys(bet_amount)
                            self.driver.logging.info('Populated Bet Amount Field')
                            WebDriverWait(self.driver.driver, self.screen_load_wait).until(
                                lambda driver: driver.find_elements(By.XPATH, self.odds_changed_banner_xpath) or driver.find_elements(By.XPATH, self.place_bet_button_xpath))

                            # check if odds changed banner appeared
                            # delete all bets
                            if self.driver.driver.find_elements_by_xpath(self.odds_changed_banner_xpath):
                                self.driver.logging.error('Unable To Process The Bet Because The Odds Changed')
                                self.delete_bets()

                                return False

                        except TimeoutException:
                            # delete all bets
                            self.driver.logging.error('Bet Amount Field Population Exceeded Time Limit')
                            self.delete_bets()

                            return False

                        try:
                            # create bet button object
                            # click bet button button
                            # wait for odds changed banner or place bet button to exist
                            bet_button = self.driver.driver.find_element_by_xpath(self.place_bet_button_xpath)
                            bet_button.click()
                            WebDriverWait(self.driver.driver, self.screen_load_wait).until(
                                lambda driver: driver.find_elements(By.XPATH, self.odds_changed_banner_xpath) or driver.find_elements(By.XPATH, self.bet_confirmation_receipt_xpath))

                            # check if odds changed banner appeared
                            # delete all bets
                            if self.driver.driver.find_elements_by_xpath(self.odds_changed_banner_xpath):
                                self.driver.logging.error('Unable To Process Bet Because The Odds Changed')
                                self.delete_bets()

                                return False

                            else:
                                self.driver.logging.info('Bet Submission Processed')

                        except TimeoutException:
                            self.driver.logging.error('Bet Submission Exceeded Time Limit')
                            self.delete_bets()

                            return False

                        try:
                            # create default variable
                            # wait for bet reference to be available
                            # update variable
                            bet_reference_id = None
                            WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.presence_of_element_located((By.XPATH, self.bet_reference_id_xpath)))
                            bet_reference_id = self.driver.driver.find_element_by_xpath(self.bet_reference_id_xpath).text
                            self.driver.logging.info('Extracted Bet Reference ID ({})'.format(bet_reference_id))

                        except TimeoutException:
                            self.driver.logging.error('Unable To Extract Bet Reference ID')

                        try:
                            # create bet confirmation button object
                            # click bet confirmation button
                            # wait for betslip to be empty
                            bet_confirmation_button = self.driver.driver.find_element_by_xpath(self.bet_confirmation_exit_button_xpath)
                            bet_confirmation_button.click()
                            WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.presence_of_element_located((By.XPATH, self.betslip_empty_xpath)))
                            self.driver.logging.info('Betslip Emptied After Purchase')

                        except TimeoutException:
                            self.driver.logging.error('Emptying Betslip After Purchase Exceeded Time Limit')

                        return bet_reference_id

                    else:
                        self.driver.logging.error('Desired Bet Based On Parameter Inputs Is Not Available')
                else:
                    self.driver.logging.error('Unable To Locate The Event ID')
            else:
                self.driver.logging.error('Unable To Locate The Event Category ID')
        elif bet_type not in self.bet_types:
            self.driver.logging.error('Unable To Trigger A Bet Because Invalid Parameter Inputs Were Provided')
        elif type not in self.types:
            self.driver.logging.error('Unable To Trigger A Bet Because Invalid Parameter Inputs Were Provided')

        return False


    def __repr__(self):

        return '{}'.format(vars(self))
