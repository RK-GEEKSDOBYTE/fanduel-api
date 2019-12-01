# import packages
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# import custom packages

# define static variables

# define dynamic variables


class BET:

    def __init__(self, driver, screen_load_wait):
        self.driver = driver
        self.screen_load_wait = screen_load_wait
        self.event_categories_xpath = '//div[@class="live-event-container"]/descendant::span[@class="coupontitle"]'
        self.teams_xpath_placeholder = '//div[@class="live-event-container"][{}]/descendant::section[@class="eventTitleWrapper"]/descendant::span[@class="name"]'
        self.bet_type_button_xpath_placeholder = '//div[@class="live-event-container"][{}]/descendant::div[contains(@class, "big3-event")][{}]/descendant::div[@class="{}"]/descendant::div[contains(@class, "selection-wapper selection-data")][{}]'
        self.betslip_empty_xpath = '//div[@class="empty-betslip REGULAR"]'
        self.betslip_populated_xpath = '//div[@class="singles REGULAR"]'
        self.bet_amount_field_xpath = '//div[@class="singles REGULAR"]/descendant::span[@class="stake"]/div[@class="money-input"]/input'
        self.place_bet_button_xpath = '//*[@id="SBbetSlip"]/div[7]/div[2]/div[2]/div[2]/div[2]/button'
        self.bet_confirmation_receipt_xpath = '//div[@class="your_receipt_desktop"]'
        self.bet_confirmation_exit_button_xpath = '//div[@class="betPlacement"]/descendant::div[@class="column column-left"]/button[@class="btn secondary"]'
        self.bet_refernce_id_xpath = '//div[@class="reference"]/span[@class="value"]'
        self.odds_changed_banner_xpath = '//div[@class="singles REGULAR"]/descendant::div[@class="header-changed msg info"]'
        self.delete_all_bets_xpath = '//div[@class="betslip_actions"]/descendant::button[@class="delALL btn"]'
        self.types = ['less', 'more', 'equal', 'any']
        self.current_value_xpath = ''
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


	# removes characters not allowed with float type (allows periods and negative characters)
    def float_regex(self, input):

        return re.sub('[^0-9^.^-]','', input)


	# removes characters not allowed with integer type (allows negative characters)
    def int_regex(self, input):

        return re.sub('[^0-9^-]','', input)


	# check if float type
    def is_float(self, input):

        try:
            num = float(input)
        except:
            return False

        return True


    # check if integer type
    def is_int(self, input):

        try:
            num = int(input)
        except:
            return False

        return True


    # delete all bets from betslip
    def delete_bets(self):

        # check if delete bets button xpath exists
        if self.driver.find_element_by_xpath(self.delete_all_bets_xpath):

            try:
                # wait for delete bets button to be cliackable
                WebDriverWait(self.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.delete_all_bets_xpath)))

            except TimeoutException:
                print('Betslip Delete Bets Error: Unable To Locate Clickable Button')

                return

            try:
                # create delete bets button object
                # click login form exit image
                # wait for login link to be cliackable
                delete_bets_button = self.driver.find_element_by_xpath(self.delete_all_bets_xpath)
                delete_bets_button.click()
                WebDriverWait(self.driver, self.screen_load_wait).until(EC.presence_of_element_located((By.XPATH, self.betslip_empty_xpath)))
                print('Betslip Delete Bets Successful')

            except TimeoutException:
                print('Betslip Delete Bets Error: Submission Exceeded Time Limit')

                return


    # submit bet
    def submit(self, bet_amount, league, team_name, compare_bet_type_value, bet_type='moneyline', type='equal'):

        # create default variables
        event_category_id = None
        event_team_builder_id = None

        # check if bet_type and type parameter inputs exist
        if bet_type in self.bet_types and type in self.types:

            # find live event categories
            event_categories = self.driver.find_elements_by_xpath(self.event_categories_xpath)

            # loop through event categories
            for i in range(0, len(event_categories)):

                # check if league event category exists
                # update event_category_id with additional increment since selenium starts with index 1
                if event_categories[i].text == league:
                    event_category_id = i + 1
                    break

            # check if event category id found
            if event_category_id:

                # dynamically build teams_xpath
                # find all teams currently playing in event category
                teams_xpath = self.teams_xpath_placeholder.format(event_category_id)
                team_names = self.driver.find_elements_by_xpath(teams_xpath)

                # cloop through teams starting from 1 since selenium starts with index 1
                for i in range(1, len(team_names) + 1):

                    # check if team exists
                    # update event_team_builder
                    if team_names[i-1].text == team_name:
                        event_team_builder_id = i
                        break

                # check if event/team div builder id exists
                # dynamically assign event and team div ids
                # dynamically build moneyline xpath
                if event_team_builder_id:
                    event_div_id = round((i / 2) + .01)
                    team_div_id = 2 if i % 2 == 0 else 1
                    bet_type_button_xpath = self.bet_type_button_xpath_placeholder.format(event_category_id, event_div_id, self.bet_types[bet_type]['xpath_class'], team_div_id)

                    try:
                        # check if bet type button exists
                        WebDriverWait(self.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, bet_type_button_xpath)))

                    except TimeoutException:
                        print('Bet Type Button Error: Unable To Locate Clickable {} Button'.format(bet_type.title()))

                        return False

                    try:
                        # dynamically assign bet type button value
                        bet_type_value = self.driver.find_element_by_xpath(bet_type_button_xpath).text

                        # check if bet type should be a float value
                        # convert bet type value to float
                        if self.bet_types[bet_type]['type'] == 'float':
                            bet_type_value = self.float_regex(input=bet_type_value)
                            bet_type_value  = float(bet_type_value) if self.is_float(input=bet_type_value) else bet_type_value

                        # check if bet_type should be an int value
                        # convert bet type value to int
                        elif self.bet_types[bet_type]['type'] == 'int':
                            bet_type_value = self.int_regex(input=bet_type_value)
                            bet_type_value = int(bet_type_value) if self.is_int(input=bet_type_value) else bet_type_value

                        if not self.is_int(input=bet_type_value) and not self.is_float(input=bet_type_value):
                            print('Bet Type Value Error: Value Is Not Int Or Float')

                            return False

                    except:
                        print('Bet Type Value Error: Unable To Prepare Bet Value')

                        return False

                    # create object to store bet rules
                    bet_rules = [type == 'less' and compare_bet_type_value > bet_type_value, type == 'equal' and compare_bet_type_value == bet_type_value,
                    		         type == 'more' and compare_bet_type_value < bet_type_value, type == 'any']

                    # check if any rules met to try to trigger bet
                    if any(bet_rules):

                        try:
                            # create bet type button object
                            # click bet type button
                            # wait for betslip bet amount field to be clickable
                            bet_type_button = self.driver.find_element_by_xpath(bet_type_button_xpath)
                            bet_type_button.click()
                            WebDriverWait(self.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.bet_amount_field_xpath)))
                            print('BetSlip Load Successful')

                        except TimeoutException:
                            print('Betslip Load Error: Form Load Exceeded Time Limit')

                            return False

                        try:
                            # create bet amount field object
                            # populate bet amount field
                            # wait for odds changed banner to appear or place bet button to become clickable
                            bet_amount_field = self.driver.find_element_by_xpath(self.bet_amount_field_xpath)
                            bet_amount_field.send_keys(bet_amount)
                            print('Betslip Population Successful')
                            WebDriverWait(self.driver, self.screen_load_wait).until(
                                lambda driver: driver.find_elements(By.XPATH, self.odds_changed_banner_xpath) or driver.find_elements(By.XPATH, self.place_bet_button_xpath))

                            # check if odds changed banner appeared
                            # delete all bets
                            if self.driver.find_elements_by_xpath(self.odds_changed_banner_xpath):
                                print("Betslip Error: Odds Changed")
                                self.delete_bets()

                                return False

                        except TimeoutException:
                            # delete all bets
                            print('Betslip Population Error: Field Population Exceeded Time Limit')
                            self.delete_bets()

                            return False

                        try:
                            # create bet button object
                            # click bet button button
                            # wait for odds changex to appear or bet confirmation button to become clickable
                            bet_button = self.driver.find_element_by_xpath(self.place_bet_button_xpath)
                            bet_button.click()
                            WebDriverWait(self.driver, self.screen_load_wait).until(
                                lambda driver: driver.find_elements(By.XPATH, self.odds_changed_banner_xpath) or driver.find_elements(By.XPATH, self.bet_confirmation_receipt_xpath))

                            # check if odds changed banner appeared
                            # delete all bets
                            if self.driver.find_elements_by_xpath(self.odds_changed_banner_xpath):
                                print("Betslip Error: Odds Changed")
                                self.delete_bets()

                                return False

                            else:
                                print('Betslip Submission Successful')

                        except TimeoutException:
                            print('Betslip Submission Error: Submission Exceeded Time Limit')
                            self.delete_bets()

                            return False

                        try:
                            # get bet refernce id
                            # create bet confirmation button object
                            # click bet confirmation button button
                            # wait for betslip to be empty
                            bet_refernce_id = self.driver.find_element_by_xpath(self.bet_refernce_id_xpath).text
                            bet_confirmation_button = self.driver.find_element_by_xpath(self.bet_confirmation_exit_button_xpath)
                            bet_confirmation_button.click()
                            WebDriverWait(self.driver, self.screen_load_wait).until(EC.presence_of_element_located((By.XPATH, self.betslip_empty_xpath)))
                            print('Betslip Reference #: {}'.format(bet_refernce_id))
                            print('Betslip Emptied Successful')

                            return bet_refernce_id

                        except TimeoutException:
                            print('Betslip Empty Error: Submission Exceeded Time Limit')

                            return False

                    else:
                        print('Betslip Load Error: Desired Bet Not Available')
                else:
                    print('Betslip Load Error: Unable To Locate Event ID')
            else:
                print('Betslip Load Error: Unable To Locate Event Category ID')
        elif bet_type not in self.bet_types:
            print('Bet Error: Parameter Input {} Not Valid'.format(bet_type))
        elif type not in self.types:
            print('Bet Error: Parameter Input {} Not Valid'.format(type))

        return False


    # sell bet
    def sell(self, reference_id, bet_comparision_value, type='equal'):
        print("TEST")


    def __repr__(self):

        return '{}'.format(vars(self))
