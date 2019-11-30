# import packages

# import custom packages

# define static variables

# define dynamic variables


class NAVIGATE:

    def __init__(self, driver):
        self.driver = driver
        self.modal_window_close_xpath = '//div[@class="q-close-template-overlay"]'
        self.plug_required_close_xpath = '//div[@class="close"]/descendant::i'
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

        # check if modal window xpath exists
        # create modal window object
        if self.driver.find_elements_by_xpath(self.modal_window_close_xpath):
            modal_window = self.driver.find_element_by_xpath(self.modal_window_close_xpath)

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
        if tab_type not in self.tab_type_xpaths:
            print('Tab Click Error: Parameter Input {} Not Valid'.format(tab_type))

            return False

        # dynamically create group tab xpath
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

        return False


    def __repr__(self):

        return '{}'.format(vars(self))
