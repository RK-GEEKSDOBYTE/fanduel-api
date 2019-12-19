# import packages
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# import custom packages

# define static variables

# define dynamic variables


class ACCOUNT:

    def __init__(self, driver, screen_load_wait):
        self.driver = driver
        self.screen_load_wait = screen_load_wait
        self.logged_in_xpath = '//div[contains(@class, "user_logged_in")]'
        self.login_link_xpath = '//button[contains(@class, "login_btn")]'
        self.login_form_xpath = '//div[@class="login-component"]'
        self.login_form_exit_xpath = '//div[@class="login-component"]/div[@class="header"]/div[@class="layout logo"]/div[@class="flex float-right xs12"]/img'
        self.login_username_field_xpath = '//input[@id="username"]'
        self.login_password_field_xpath = '//input[@id="password"]'
        self.login_submit_button_xpath = '//button[@class="primary-btn-blue btn btn--block active-green" and not(@disabled)]'
        self.invalid_credentials_xpath = '//p[@class="error" and contains(text(), "Invalid credentials")]'
        self.account_menu_xpath = '//div[@class="menu__activator"]/button[@class="btn btn--flat"]'
        self.logout_link_xpath = '//div[@class="account_links"]/descendant::ul[@class="navigation"]/li/a[@href="/logout"]/parent::li'
        self.logout_form_exit_xpath = ''
        self.logout_confirmation_button_xpath = '//div[@class="card__actions"]/button[@class="primary-btn-blue btn"]'
        self.information_type_xpaths =  {
                                        'last_login':       {
                                                            'xpath': '//div[@class="flex float-right"]/span[@class="header-txt"]/span[1]',
                                                            'label_remove': 'Last login: '
                                                            },
                                        'session_time':     {
                                                            'xpath': '//div[@class="flex float-right"]/span[@class="header-txt"]/span[2]',
                                                            'label_remove': 'Session time: '
                                                            },
                                        'available_funds':  {
                                                            'xpath': '//span[@class="balance"]/span[@class="value"]',
                                                            'label_remove': '$'
                                                            }
                                        }


    # check if user logged in
    def check_logged_in(self):

        # check if user logged in xpath exists
        if self.driver.driver.find_elements_by_xpath(self.logged_in_xpath):
            return True

        return False


    # close login form
    def close_login_form(self):

        # check if login form exit xpath exists
        if self.driver.driver.find_elements_by_xpath(self.login_form_exit_xpath):

            try:
                # wait for login form exit to be cliackable
                WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.login_form_exit_xpath)))

            except TimeoutException:
                print('Account API Error: Unable To Locate Clickable Exit Button On Login Form')

                return False

            try:
                # create login form exit object
                # click login form exit
                # wait for login link to be cliackable
                login_form_exit_image = self.driver.driver.find_element_by_xpath(self.login_form_exit_xpath)
                login_form_exit_image.click()
                WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.login_link_xpath)))

                return True

            except TimeoutException:
                print('Account API Error: Unable To Locate Clickable Login Link After Closing Login Form')

                return False

        else:
            print('Account API Error: Unable To Locate Exit Button On Login Form')

        return False


    # log user into account
    def login(self, username, password):

        # check if user has provied provided credentials
        # check if user is already logged in
        if username and password and not self.check_logged_in():

            try:
                # wait for login link to be clickable
                WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.login_link_xpath)))

            except TimeoutException:
                print('Account API Error: Unable To Locate Clickable Login Link')

                return False

            try:
                # create login link object
                # click login link
                # wait for login form xpath to exist
                login_link = self.driver.driver.find_element_by_xpath(self.login_link_xpath)
                login_link.click()
                WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.presence_of_element_located((By.XPATH, self.login_form_xpath)))

            except TimeoutException:
                print('Account API Error: Login Form Render Exceeded Time Limit')

                return False

            try:
                # wait for username/password fields to be cliackable
                WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.login_username_field_xpath)))
                WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.login_password_field_xpath)))

            except TimeoutException:
                # close login form
                print('Account API Error: Unable To Locate Clickable Username/Password Fields On Login Form')
                self.close_login_form()

                return False

            try:
                # create username/password field objects
                # populate username/password fields
                # wait for submit button to be clickable
                username_field = self.driver.driver.find_element_by_xpath(self.login_username_field_xpath)
                password_field = self.driver.driver.find_element_by_xpath(self.login_password_field_xpath)
                username_field.send_keys(username)
                password_field.send_keys(password)
                WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.login_submit_button_xpath)))

            except TimeoutException:
                # close login form
                print('Account API Error: Unable To Locate Clickable Submit Button On Login Form')
                self.close_login_form()

                return False

            try:
                # create submit button
                # click submit button
                # wait for invalid credentials banner or logged in elements to appear
                login_submit_button = self.driver.driver.find_element_by_xpath(self.login_submit_button_xpath)
                login_submit_button.click()
                WebDriverWait(self.driver.driver, self.screen_load_wait).until(
                    lambda driver: driver.find_elements(By.XPATH, self.logged_in_xpath) or driver.find_elements(By.XPATH, self.invalid_credentials_xpath))

            except TimeoutException:
                # close login form
                print('Account API Error: Login Form Submission Exceeded Time Limit')
                self.close_login_form()

                return False

            # check if user successfuly logged in
            if self.driver.driver.find_elements_by_xpath(self.logged_in_xpath):
                print('Account API Success: Logged Into System As {}'.format(username))

                return True

            # check if invalid credentials banner exists
            # close login form
            elif self.driver.driver.find_elements_by_xpath(self.invalid_credentials_xpath):
                print('Account API Error: Invalid Credentials Provided For Username {}'.format(username))
                self.close_login_form()

                return False

        # check if username or password not provided
        elif not username or not password:
            print('Account API Error: Username And/Or Password Input Parameters Not Provided')

        # check if user is already logged in
        elif self.check_logged_in():
            print('Account API Error: User Already Logged In')

        return False


    # log user out of account
    def logout(self):

        # check if user is already logged in
        if self.check_logged_in():

            try:
                # wait for account menu button to be clickable
                WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.account_menu_xpath)))

            except TimeoutException:
                print('Account API Error: Unable To Locate Clickable Account Menu')

                return False

            try:
                # create account menu object
                # open account menu
                # wait for account menu items to become clickable
                account_menu = self.driver.driver.find_element_by_xpath(self.account_menu_xpath)
                account_menu.click()
                WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.logout_link_xpath)))

            except:
                # close account menu
                print('Account API Error: Unable To Locate Clickable Account Menu Logout Item')
                account_menu.click()

                return False

            try:
                # create logout link object
                # click logout link
                # wait for logout confirmation button to become clickable
                logout_link = self.driver.driver.find_element_by_xpath(self.logout_link_xpath)
                logout_link.click()
                WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.logout_confirmation_button_xpath)))

            except:
                print('Account API Error: Unable To Locate Clickable Logout Confirmation Button')

                return False

            try:
                # create logout confirmation button object
                # click logout confirmation button
                # wait for login button xpath to exist
                logout_confirmation_button = self.driver.driver.find_element_by_xpath(self.logout_confirmation_button_xpath)
                logout_confirmation_button.click()
                WebDriverWait(self.driver.driver, self.screen_load_wait).until(EC.presence_of_element_located((By.XPATH, self.login_link_xpath)))
                print('Account API Success: Logged Out Of System')

                return True

            except:
                print('Account API Error: Unable To Locate Clickable Login Link After Logging Out')

                return False

        else:
            print('Account API Error: Unable To Logout Because User Not Logged In')

        return False


    # get user information
    def get_user_information(self, information_type='available_funds'):

        # check if information_type parameter input is valid
        # check if user already logged in
        # get information type xpath based on parameter input
        # get information type label to remove based on parameter input
        if information_type in self.information_type_xpaths and self.check_logged_in():
            information_type_xpath = self.information_type_xpaths[information_type]['xpath']
            information_type_label_remove = self.information_type_xpaths[information_type]['label_remove']

		    # check if information xpath exists
            # find information with label
            # remove label from information
            if self.driver.driver.find_elements_by_xpath(information_type_xpath):
                label_information = self.driver.driver.find_element_by_xpath(information_type_xpath).text
                information = label_information[len(information_type_label_remove): ]
                print('Account API Success: Retrieved {} Information'.format(information_type.replace('_', ' ').title()))

                return information

            else:
                print('Account API Error: Unable To Locate {} Information'.format(information_type.replace('_', ' ').title()))

        # check if invalid parameter input provided
        elif information_type not in self.information_type_xpaths:
            print('Account API Error: Unable To Retrieve Information Because Invalid Input For Parameter Provided')

        # check if user logged in
        elif not self.check_logged_in():
            print('Account API Error: Unable To Retrieve {} Information Because User Not Logged In'.format(information_type.replace('_', ' ').title()))

        return False


    def __repr__(self):

        return '{}'.format(vars(self))
