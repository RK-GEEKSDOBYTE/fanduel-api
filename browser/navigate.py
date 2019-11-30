# import packages

# import custom packages

# define static variables

# define dynamic variables


class NAVIGATE:

    def __init__(self, driver):
        self.driver = driver
        self.modal_initial_close_xpath = '//div[@class="q-close-template-overlay"]'
        self.modal_signin_close_xpath = '//button[@class="close"]'
        self.plug_required_close_xpath = '//div[@class="close"]/descendant::i'
        self.cashout_toggle_xpath = '//button[contains(@class, "stmnt-tgl filterbbtgl")]'
        self.cashout_toggle_on_xpath = '//button[contains(@class, "stmnt-tgl filterbbtgl on")]'
        self.tab_type_xpaths =  {
                                'event_group': '//div[contains(@class, "tabs_home")]/descendant::a[contains(@class, "tabs__item") and text()="{}"]',
                                'bet_status': '//div[contains(@class, "betslip-page-header")]/descendant::a[@class="a-link-" and contains(., "{}")]',
                                'bet_type': '//div[contains(@class, "betslip_scroll")]/descendant::a[contains(@class, "a-link") and contains(., "{}")]'
                                }


    # close notification to download geo-location plugin required to bet
    def close_plugin(self):

        # check if modal window xpath exists
        # create modal window object
        if self.driver.find_elements_by_xpath(self.plug_required_close_xpath):
            plugin = self.driver.find_element_by_xpath(self.plug_required_close_xpath)

			# check if modal window can be clicked (closed)
            # click (close) modal window
            if plugin.is_enabled() and plugin.is_displayed():
                plugin.click()
                print('Plugin Close Successful')

                return True

        return False


	# close modal window that appears when first visiting webpage, refreshing webpage, or logging in
    def close_modal_window(self):

        # find modal window objects
        modal_window_objects = self.driver.find_elements_by_xpath(self.modal_initial_close_xpath) + self.driver.find_elements_by_xpath(self.modal_signin_close_xpath)

        # iterate through modal window objects
        for modal_window in modal_window_objects:

			# check if modal window can be clicked (closed)
            # click (close) modal window
            if modal_window.is_enabled() and modal_window.is_displayed():
                modal_window.click()
                print('Modal Window Close Successful')

                return True

        return False


	# activate tab
    def click_tab(self, tab_type='event_group', tab_name='Live'):

        # check if tab_group parameter input exists
        # dynamically create group tab xpath
        if tab_type in self.tab_type_xpaths:
            tab_xpath = self.tab_type_xpaths[tab_type].format(tab_name)

            # check if event group tab xpath exists
            # create tab object
            if self.driver.find_elements_by_xpath(tab_xpath):
                tab = self.driver.find_element_by_xpath(tab_xpath)

                # check if tab can be clicked (activate)
                # click (activate) tab
                if tab.is_enabled() and tab.is_displayed():
                    tab.click()
                    print('{} Tab Click Successful'.format(tab_name))

                    return True

                else:
                    print('Tab Click Error: Unable To Click {} Tab'.format(tab_name))
            else:
                print('Tab Click Error: Unable To Locate Clickable Tab Labeled {}'.format(tab_name))
        else:
            print('Tab Click Error: Parameter Input {} Not Valid'.format(tab_type))

        return False


    # toggle cashout active tab
    def toggle_cashout(self, active=True):

        self.click_tab(tab_type='bet_status', tab_name='Active')

        # check if toggle exists (user needs to be logged in)
        # create toggle object
        if self.driver.find_elements_by_xpath(self.cashout_toggle_xpath):
            toggle = self.driver.find_element_by_xpath(self.cashout_toggle_xpath)

            if active and self.driver.find_elements_by_xpath(self.cashout_toggle_on_xpath):
                print('Toggle Already Active Successful')

                return True

            elif not active and not self.driver.find_elements_by_xpath(self.cashout_toggle_on_xpath):
                print('Toggle Already Inactive Successful')

                return True

            if toggle.is_enabled() and toggle.is_displayed():
                toggle.click()
                print('Toggle Active Successful') if active else print('Toggle Inactive Successful')

                return True

            else:
                print('Toggle Click Error: Unable To Locate Clickable Toggle')
        else:
            print('Toggle Click Error: User Not Logged In')

        return False


    def __repr__(self):

        return '{}'.format(vars(self))
