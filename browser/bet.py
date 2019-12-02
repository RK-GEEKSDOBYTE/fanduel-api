# import packages
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# import custom packages
from . import helper

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
        self.bet_reference_id_xpath = '//div[@class="reference"]/span[@class="value"]'
        self.odds_changed_banner_xpath = '//div[@class="singles REGULAR"]/descendant::div[@class="header-changed msg info"]'
        self.delete_all_bets_xpath = '//div[@class="betslip_actions"]/descendant::button[@class="delALL btn"]'
        self.active_bet_reference_ids_xpath = '//div[@class="betrefs"]'
        self.active_bet_current_moneyline_xpath = '//div[@class="stmnt-bets"]/div[contains(@class, "stmnt-bet")][{}]/descendant::span[@class="leginfo-odds pricetype-CP"]'
        self.sell_button_xpath = '//div[@class="stmnt-bets"]/descendant::div[@class="block buyback"][{}]/button[@class="stmnt-btn sb-green"]'
        self.sell_confirmation_button_xpath = '//div[@class="block buyback"]/button[@class="stmnt-btn sb-blue"]'
        self.sold_confirmation_xpath = '//div[@class="legribbon legribbon-boughtback"]'
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
        if self.driver.find_elements_by_xpath(self.delete_all_bets_xpath):

            try:
                # wait for delete all bets button to be cliackable
                WebDriverWait(self.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.delete_all_bets_xpath)))

            except TimeoutException:
                print('Bet API Error: Unable To Locate Clickable Delete All Bets Button')

                return

            try:
                # create delete all bets button object
                # click delete all bets button
                # wait for empty betslip xpath to exist
                delete_all_bets_button = self.driver.find_element_by_xpath(self.delete_all_bets_xpath)
                delete_all_bets_button.click()
                WebDriverWait(self.driver, self.screen_load_wait).until(EC.presence_of_element_located((By.XPATH, self.betslip_empty_xpath)))
                print('Bet API Success: Deleted All Bets')

            except TimeoutException:
                print('Bet API Error: Delete All Bets Submission Exceeded Time Limit')

                return


    # submit bet
    def submit(self, bet_amount, league, team_name, compare_bet_type_value, bet_type='moneyline', type='equal'):

        # create default variables
        event_category_id = None
        event_team_builder_id = None

        # check if bet_type and type parameter inputs are valid
        if bet_type in self.bet_types and type in self.types:

            # get live event categories
            event_categories = self.driver.find_elements_by_xpath(self.event_categories_xpath)

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
                team_names = self.driver.find_elements_by_xpath(teams_xpath)

                # loop through teams
                for i, item in enumerate(team_names):

                    # check if team exists
                    # update event_team_builder variable (increment by 1 since selenium starts with index 1)
                    if team_names[i].text == team_name:
                        event_team_builder_id = i + 1
                        break

                # check if event/team div builder id exists
                # assign event and team div ids
                # create moneyline xpath
                if event_team_builder_id:
                    event_div_id = round((i / 2) + .01)
                    team_div_id = 2 if i % 2 == 0 else 1
                    bet_type_button_xpath = self.bet_type_button_xpath_placeholder.format(event_category_id, event_div_id, self.bet_types[bet_type]['xpath_class'], team_div_id)

                    try:
                        # check if bet type button is clickable
                        WebDriverWait(self.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, bet_type_button_xpath)))

                    except TimeoutException:
                        print('Bet API Error: Unable To Locate Clickable {} Button'.format(bet_type.title()))

                        return False

                    try:
                        # get bet type button value
                        bet_type_value = self.driver.find_element_by_xpath(bet_type_button_xpath).text

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
                            print('Bet API Error: Unable To Convert {} Button Value To Int/Float'.format(bet_type.title()))

                            return False

                    except:
                        print('Bet API Error: Unable To Extract {} Button Value'.format(bet_type.title()))

                        return False

                    # create object of rules on triggering a bet based on parameter inputs
                    bet_rules = self.get_bet_rules(type=type, compare_value=compare_bet_type_value, current_value=bet_type_value)

                    # check if any trigger rules met
                    if any(bet_rules):

                        try:
                            # create bet type button object
                            # click bet type button
                            # wait for betslip bet amount field to be clickable
                            bet_type_button = self.driver.find_element_by_xpath(bet_type_button_xpath)
                            bet_type_button.click()
                            WebDriverWait(self.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.bet_amount_field_xpath)))
                            print('Bet API Success: Loaded Betslip Form To Initiate Bet')

                        except TimeoutException:
                            print('Bet API Error: Betslip Form Load To Initiate Bet Exceeded Time Limit')

                            return False

                        try:
                            # create bet amount field object
                            # populate bet amount field
                            # wait for odds changed banner or place bet button to exist
                            bet_amount_field = self.driver.find_element_by_xpath(self.bet_amount_field_xpath)
                            bet_amount_field.send_keys(bet_amount)
                            print('Bet API Success: Populated Bet Amount Field')
                            WebDriverWait(self.driver, self.screen_load_wait).until(
                                lambda driver: driver.find_elements(By.XPATH, self.odds_changed_banner_xpath) or driver.find_elements(By.XPATH, self.place_bet_button_xpath))

                            # check if odds changed banner appeared
                            # delete all bets
                            if self.driver.find_elements_by_xpath(self.odds_changed_banner_xpath):
                                print("Bet API Error: Unable To Process Bet Because The Odds Changed")
                                self.delete_bets()

                                return False

                        except TimeoutException:
                            # delete all bets
                            print('Bet API Error: Bet Amount Field Population Exceeded Time Limit')
                            self.delete_bets()

                            return False

                        try:
                            # create bet button object
                            # click bet button button
                            # wait for odds changed banner or place bet button to exist
                            bet_button = self.driver.find_element_by_xpath(self.place_bet_button_xpath)
                            bet_button.click()
                            WebDriverWait(self.driver, self.screen_load_wait).until(
                                lambda driver: driver.find_elements(By.XPATH, self.odds_changed_banner_xpath) or driver.find_elements(By.XPATH, self.bet_confirmation_receipt_xpath))

                            # check if odds changed banner appeared
                            # delete all bets
                            if self.driver.find_elements_by_xpath(self.odds_changed_banner_xpath):
                                print("Bet API Error: Unable To Process Bet Because The Odds Changed")
                                self.delete_bets()

                                return False

                            else:
                                print('Bet API Success: Bet Submission Processed')

                        except TimeoutException:
                            print('Bet API Error: Bet Submission Exceeded Time Limit')
                            self.delete_bets()

                            return False

                        try:
                            # create default variable
                            # wait for bet reference to be available
                            # update variable
                            bet_reference_id = None
                            WebDriverWait(self.driver, self.screen_load_wait).until(EC.presence_of_element_located((By.XPATH, self.bet_reference_id_xpath)))
                            bet_reference_id = self.driver.find_element_by_xpath(self.bet_reference_id_xpath).text
                            print('Bet API Success: Extracted Bet Reference ID ({})'.format(bet_reference_id))

                        except TimeoutException:
                            print('Bet API Error: Unable To Extract Bet Reference ID')

                        try:
                            # create bet confirmation button object
                            # click bet confirmation button
                            # wait for betslip to be empty
                            bet_confirmation_button = self.driver.find_element_by_xpath(self.bet_confirmation_exit_button_xpath)
                            bet_confirmation_button.click()
                            WebDriverWait(self.driver, self.screen_load_wait).until(EC.presence_of_element_located((By.XPATH, self.betslip_empty_xpath)))
                            print('Bet API Success: Betslip Emptied After Purchase')

                        except TimeoutException:
                            print('Bet API Error: Emptying Betslip After Purchase Exceeded Time Limit')

                        return bet_reference_id

                    else:
                        print('Bet API Error: Desired Bet Based On Parameters Is Not Available')
                else:
                    print('Bet API Error: Unable To Locate Event ID')
            else:
                print('Bet API Error: Unable To Locate Event Category ID')
        elif bet_type not in self.bet_types:
            print('Bet API Error: Parameter Input {} For "bet_type" Not Valid'.format(bet_type))
        elif type not in self.types:
            print('Bet API Error: Parameter Input {} For "type" Not Valid'.format(type))

        return False


    # sell bet
    def sell(self, reference_id, compare_moneyline_value, type='equal'):

        # create default variable
        active_bet_order = None

        # check if type parameter input is valid
        if type in self.types:

            try:
                # wait for active bets to exist
                WebDriverWait(self.driver, self.screen_load_wait).until(EC.presence_of_element_located((By.XPATH, self.active_bet_reference_ids_xpath)))

            except TimeoutException:
                print('Bet API Error: Unable To Locate Any Active Bets')

                return False

            active_bet_ids = self.driver.find_elements_by_xpath(self.active_bet_reference_ids_xpath)

            # loop through active bets
            for i, item in enumerate(active_bet_ids):

                # check if active bet has reference id
                # update active_bet_order variable (increment by 1 since selenium starts with index 1)
                if str(reference_id) in item.text:
                    active_bet_order = i + 1
                    print('Bet API Success: Located Bet #{} Requested To Sell'.format(reference_id))

            # check if reference # found
            # build current moneyline xpath
            # build sell button xpath
            if active_bet_order:
                self.active_bet_current_moneyline_xpath = self.active_bet_current_moneyline_xpath.format(active_bet_order)
                self.sell_button_xpath = self.sell_button_xpath.format(active_bet_order)

                try:
                    # wait for active bet current moneyline to exist
                    # get active bet current moneyline
                    WebDriverWait(self.driver, self.screen_load_wait).until(EC.presence_of_element_located((By.XPATH, self.active_bet_current_moneyline_xpath)))
                    current_moneyline = self.driver.find_element_by_xpath(self.active_bet_current_moneyline_xpath).text
                    print('Bet API Success: Located Current Moneyline Value Required To Sell')

                    # convert to int type if possible
                    current_moneyline = helper.int_regex(input=current_moneyline)
                    current_moneyline = int(current_moneyline) if helper.is_int(input=current_moneyline) else current_moneyline

                except TimeoutException:
                    print('Bet API Error: Unable To Locate Current Moneyline Value Required To Sell')

                    return False

                # check if current moneyline was converted to an int
                if helper.is_int(input=current_moneyline):

                    try:
                        # wait for sell button to become clickable
                        # create sell button object
                        WebDriverWait(self.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.sell_button_xpath)))
                        sell_button = self.driver.find_element_by_xpath(self.sell_button_xpath)

                    except TimeoutException:
                        print('Bet API Error: Unable To Locate Clickable Sell Button')

                        return False

                    # create object of rules on selling a bet based on parameter inputs
                    bet_rules = self.get_bet_rules(type=type, compare_value=compare_moneyline_value, current_value=current_moneyline)

                    # check if any trigger rules met
                    if any(bet_rules):

                        try:
                            # click sell button
                            # wait for sell confirmation button to appear
                            sell_button.click()
                            WebDriverWait(self.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.sell_confirmation_button_xpath)))
                            print('Bet API Success: Clicked Sell Button')

                        except TimeoutException:
                            print('Bet API Error: Unable To Complete Process After Clicking Sell Button')

                            return False

                        try:
                            # create sell confirmation button object
                            # click sell confirmation button
                            sell_confirmation_button = self.driver.find_element_by_xpath(self.sell_confirmation_button_xpath)
                            sell_confirmation_button.click()
                            WebDriverWait(self.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.sold_confirmation_xpath)))
                            print('Bet API Success: Sold Bet #{}'.format(reference_id))

                        except TimeoutException:
                            print('Bet API Error: Unable To Complete Process After Clicking Sell Confirmation Button')

                            return False

                    else:
                        print('Bet API Error: Desired Bet Based On Parameters Is Not Available')
                else:
                    print('Bet API Error: Current Moneyline Value Required To Sell Not A Number')
            else:
                print('Bet API Error: Unable To Locate Bet #'.format(reference_id))
        elif type not in self.types:
            print('Bet API Error: Parameter Input {} For "type" Not Valid'.format(type))


    def __repr__(self):

        return '{}'.format(vars(self))
