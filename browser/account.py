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

        # check if xpath that only appears when user is logged in exists
        if self.driver.find_elements_by_xpath(self.logged_in_xpath):
            return True

        return False


    # close login form
    def close_login_form(self):

        # check if login form exit xpath exists
        if self.driver.find_elements_by_xpath(self.login_form_exit_xpath):

            try:
                # wait for login form exit image to be cliackable
                WebDriverWait(self.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.login_form_exit_xpath)))

            except TimeoutException:
                print('Login Error: Unable To Locate Login Form Exit Image')

                return

            try:
                # create login form exit image object
                # click login form exit image
                # wait for login link to be cliackable
                login_form_exit_image = self.driver.find_element_by_xpath(self.login_form_exit_xpath)
                login_form_exit_image.click()
                WebDriverWait(self.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.login_link_xpath)))

            except TimeoutException:
                print('Login Error: Login Link Render (After Closing Login Form) Exceeded Time Limit')

                return


    # log user into account
    def login(self, username, password):

        # check if user has provied provided credentials and if user is not already logged in
        if username and password and not self.check_logged_in():

            try:
                # wait for login link to be cliackable
                WebDriverWait(self.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.login_link_xpath)))

            except TimeoutException:
                print('Login Error: Unable To Locate Clickable Login Link')

                return False

            try:
                # create login link object
                # click link
                # wait for username/password field to be cliackable
                login_link = self.driver.find_element_by_xpath(self.login_link_xpath)
                login_link.click()
                WebDriverWait(self.driver, self.screen_load_wait).until(EC.presence_of_element_located((By.XPATH, self.login_form_xpath)))

            except TimeoutException:
                print('Login Error: Form Render Exceeded Time Limit')

                return False

            try:
                # wait for username/password field to be cliackable
                WebDriverWait(self.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.login_username_field_xpath)))
                WebDriverWait(self.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.login_password_field_xpath)))

            except TimeoutException:
                print('Login Error: Unable To Locate Clickable Username/Password Fields')
                self.close_login_form()

                return False

            try:
                # create user/password field objects
                # populate form fields
                # wait for submit button to become enabled
                username_field = self.driver.find_element_by_xpath(self.login_username_field_xpath)
                password_field = self.driver.find_element_by_xpath(self.login_password_field_xpath)
                username_field.send_keys(username)
                password_field.send_keys(password)
                WebDriverWait(self.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.login_submit_button_xpath)))

            except TimeoutException:
                print('Login Error: Unable To Locate Clickable Submit Button')
                self.close_login_form()

                return False

            try:
                # create login submit button
                # click login submit button
                login_submit_button = self.driver.find_element_by_xpath(self.login_submit_button_xpath)
                login_submit_button.click()
                WebDriverWait(self.driver, self.screen_load_wait).until(
                    lambda driver: driver.find_elements(By.XPATH, self.logged_in_xpath) or driver.find_elements(By.XPATH, self.invalid_credentials_xpath))

            except TimeoutException:
                print('Login Error: Submission Exceeded Time Limit')
                self.close_login_form()

                return False

            # check if invalid credentials xpath exists
            if self.driver.find_elements_by_xpath(self.logged_in_xpath):
                print('Login Successful')

                return True

            elif self.driver.find_elements_by_xpath(self.invalid_credentials_xpath):
                print('Login Error: Invalid Credentials')
                self.close_login_form()

                return False

        elif not username or not password:
            print('Login Error: Username And/Or Password Not Provided')
        elif self.check_logged_in():
            print('Login Error: User Already Logged In')

        return False


    # log user out of account
    def logout(self):

        # check if user is logged in
        if self.check_logged_in():

            try:
                # wait for account menu button to be cliackable
                WebDriverWait(self.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.account_menu_xpath)))

            except TimeoutException:
                print('Login Error: Unable To Locate Clickable Account Menu')

                return False

            try:
                # create account menu object
                # click account menu
                # wait for account menu items to become available
                account_menu = self.driver.find_element_by_xpath(self.account_menu_xpath)
                account_menu.click()
                WebDriverWait(self.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.logout_link_xpath)))

            except:
                print('Logout Error: Unable To Locate Clickable Logout Account Menu Item')
                account_menu.click()

                return False

            try:
                # create logout link object
                # click logout link
                # wait for logout confirmation button to become available
                logout_link = self.driver.find_element_by_xpath(self.logout_link_xpath)
                logout_link.click()
                WebDriverWait(self.driver, self.screen_load_wait).until(EC.element_to_be_clickable((By.XPATH, self.logout_confirmation_button_xpath)))

            except:
                print('Logout Error: Unable To Locate Clickable Logout Confirmation Button')

                return False

            try:
                # create logout confirmation button object
                # click logout confirmation button
                # wait for login button to become available
                logout_confirmation_button = self.driver.find_element_by_xpath(self.logout_confirmation_button_xpath)
                logout_confirmation_button.click()
                WebDriverWait(self.driver, self.screen_load_wait).until(EC.presence_of_element_located((By.XPATH, self.login_link_xpath)))
                print('Logout SuccessFul')

            except:
                print('Logout Error: Unable To Locate Clickable Login Link')

                return False

        else:
            print('Logout Error: User Not Logged In')

        return False


    # get user information
    def get_user_information(self, information_type='available_funds'):

        # check if information_type parameter input exists and if user logged in
        # get information type xpath
        # get information type label to remove
        if information_type in self.information_type_xpaths and self.check_logged_in():
            information_type_xpath = self.information_type_xpaths[information_type]['xpath']
            information_type_label_remove = self.information_type_xpaths[information_type]['label_remove']

		    # check if information xpath xpath exists
            # find information with label
            # remove label from information
            if self.driver.find_elements_by_xpath(information_type_xpath):
                label_information = self.driver.find_element_by_xpath(information_type_xpath).text
                information = label_information[len(information_type_label_remove) + 1: ]
                print('{} Information Retrieval Successful'.format(information_type.replace('_', ' ').title()))

                return information

            else:
                print('User Information Error: Unable To Locate Information')

        elif information_type not in self.information_type_xpaths:
            print('User Information Error: Need To Provide Valid Information Type')
        elif not self.check_logged_in():
            print('User Information Error: User Not Logged In')

        return None


    def __repr__(self):

        return '{}'.format(vars(self))
