# import packages

# import custom packages

# define static variables

# define dynamic variables


class NAVIGATE:

    def __init__(self, driver):
        self.driver = driver
        self.modal_initial_close_xpath = '//div[@class="q-close-template-overlay"]'
        self.modal_signin_close_xpath = '//button[@class="close"]'
        self.plugin_required_close_xpath = '//div[@class="close"]/descendant::i'
        self.cashout_toggle_xpath = '//button[contains(@class, "stmnt-tgl filterbbtgl")]'
        self.cashout_toggle_on_xpath = '//button[contains(@class, "stmnt-tgl filterbbtgl on")]'
        self.tab_type_xpaths =  {
                                'event_group': '//div[contains(@class, "tabs_home")]/descendant::a[contains(@class, "tabs__item") and text()="{}"]',
                                'bet_status': '//div[contains(@class, "betslip-page-header")]/descendant::a[@class="a-link-" and contains(., "{}")]',
                                'bet_type': '//div[contains(@class, "betslip_scroll")]/descendant::a[contains(@class, "a-link") and contains(., "{}")]'
                                }


    # close notification to download geo-location plugin required to bet
    def close_plugin(self):

        # check if plugin xpath exists
        # create plugin object
        if self.driver.driver.find_elements_by_xpath(self.plugin_required_close_xpath):
            plugin = self.driver.driver.find_element_by_xpath(self.plugin_required_close_xpath)

			# check if plugin can be closed (clicked)
            # close plugin
            if plugin.is_enabled() and plugin.is_displayed():
                plugin.click()
                self.driver.logging.info('Closed The Geo-Location Plugin Notification')

                return True

            else:
                self.driver.logging.error('Unable To Close The Active Geo-Location Plugin Notification')

                return False

        return True


	# close modal window that appears when first visiting webpage, refreshing webpage, or logging in
    def close_modal_window(self):

        # create list of modal window objects
        modal_window_objects = self.driver.driver.find_elements_by_xpath(self.modal_initial_close_xpath) + self.driver.driver.find_elements_by_xpath(self.modal_signin_close_xpath)

        # loop through modal window objects
        for modal_window in modal_window_objects:

			# check if modal window can be closed (clicked)
            # close modal window
            if modal_window.is_enabled() and modal_window.is_displayed():
                modal_window.click()
                self.driver.logging.info('Closed A Modal Window')

        return True


	# activate tab
    def click_tab(self, tab_type='event_group', tab_name='Live'):

        # check if tab_group parameter input is valid
        # create tab xpath
        if tab_type in self.tab_type_xpaths:
            tab_xpath = self.tab_type_xpaths[tab_type].format(tab_name)

            # check if tab xpath exists
            # create tab object
            if self.driver.driver.find_elements_by_xpath(tab_xpath):
                tab = self.driver.driver.find_element_by_xpath(tab_xpath)

                # check if tab can be activated (clicked)
                # activate tab
                if tab.is_enabled() and tab.is_displayed():
                    tab.click()
                    self.driver.logging.info('Clicked The {} Tab'.format(tab_name))

                    return True

                else:
                    self.driver.logging.error('Unable To Click The {} Tab'.format(tab_name))
            else:
                self.driver.logging.error('Unable To Locate A Tab Labeled {}'.format(tab_name))
        else:
            self.driver.logging.error('Unable To Click The {} Tab Because Invalid Parameter Inputs Were Provided'.format(tab_name))

        return False


    # toggle cashout on active tab
    def toggle_cashout(self, active=True):

        # check if active parameter input is valid
        # click active tab
        if active in [True, False]:
            self.click_tab(tab_type='bet_status', tab_name='Active')

            # check if toggle exists that only appears when user is logged in
            # create toggle object
            # create object to check if toggle is active
            if self.driver.driver.find_elements_by_xpath(self.cashout_toggle_xpath):
                toggle = self.driver.driver.find_element_by_xpath(self.cashout_toggle_xpath)
                toggle_on = self.driver.driver.find_elements_by_xpath(self.cashout_toggle_on_xpath)

                # check if toggle is already set to user input (active/inactive)
                if (active and toggle_on) or (not active and not toggle_on):
                    self.driver.logging.info('Confirmed The Cashout Toggle Is Already Set To {}'.format(active))

                    return True

                # check if toggle is clickable
                # click toggle
                if toggle.is_enabled() and toggle.is_displayed():
                    toggle.click()
                    self.driver.logging.info('Switched The Cashout Toggle To {}'.format(active))

                    return True

                else:
                    self.driver.logging.error('Unable To Locate The Clickable Cashout Toggle')
            else:
                self.driver.logging.error('Unable To Access The Cashout Toggle Because A User Is Not Logged In')
        else:
            self.driver.logging.error('Unable To Interact With The Cashout Toggle Because Invalid Parameter Input Provided')

        return False


    def __repr__(self):

        return '{}'.format(vars(self))
