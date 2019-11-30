# import packages
from datetime import datetime
from bs4 import BeautifulSoup
import re

# import custom packages

# define static variables

# define dynamic variables


class EVENT:

	def __init__(self):
		self.game_info = None
		self.team_name_info = None
		self.team_score_info = None
		self.spread_info = None
		self.spread_info_odds = None
		self.moneyline_info = None
		self.over_under_info = None
		self.over_under_info_odds = None
		self.result_info_odds = None
		self.period = None
		self.minute = None
		self.time_left = None
		self.away_team_name = None
		self.away_team_score = None
		self.away_team_spread = None
		self.away_team_spread_odds = None
		self.away_team_moneyline = None
		self.home_team_name = None
		self.home_team_score = None
		self.home_team_spread = None
		self.home_team_spread_odds = None
		self.home_team_moneyline = None
		self.over = None
		self.over_odds = None
		self.under = None
		self.under_odds = None
		self.tie_moneyline = None

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


	# get data for event
	def get_event_info_html(self, soup):

		# get core betting data (should always exist)
		self.game_info = soup.find('section', {'class': 'single-coupon-footer'})
		self.team_name_info = soup.find_all('span', {'class': 'name'})
		self.team_score_info = soup.find_all('td', {'class': 'score-value'})

		# check if no markets (betting options) are available and store data in database to track scores (even if missing)
		if not soup.find('section', {'class': 'nomarkets'}):

			# check if spread data is available
			if soup.find('div', {'class': 'market points'}):
				self.spread_info = soup.find('div', {'class': 'market points'}).find_all('div', {'class': 'currenthandicap'})

				# check if spread information is available
				if self.spread_info:
					del self.spread_info[3]
					del self.spread_info[1]

			# check if moneyline information is available
			if soup.find('div', {'class': 'market money'}):
				self.moneyline_info = soup.find('div', {'class': 'market money'}).find_all('div', {'class': 'selectionprice'})

			# check if over/under information is available
			if soup.find('div', {'class': 'market total'}):
				self.over_under_info = soup.find('div', {'class': 'market total'}).find_all('div', {'class': 'uo-currenthandicap'})

			# check if spread odds information is available and not suspended
			if soup.find('div', {'class': 'market points'}):
				if not soup.find('div', {'class': 'market points'}).find('div', {'class': 'selectionprice suspended'}):
					self.spread_info_odds = soup.find('div', {'class': 'market points'}).find_all('div', {'class': 'selectionprice'})

			# check if over/under odds information is available and not suspended
			if soup.find('div', {'class': 'market total'}):
				if not soup.find('div', {'class': 'market total'}).find('div', {'class': 'selectionprice suspended'}):
					self.over_under_info_odds =  soup.find('div', {'class': 'market total'}).find_all('div', {'class': 'selectionprice'})

			# check if result odds information is available and not suspended
			if soup.find('div', {'class': 'three-and-more-selections'}):
				if not soup.find('div', {'class': 'suspended three-and-more-selections'}):
					self.result_info_odds = soup.find_all('div', {'class': 'selectionprice'})


	# get event logistics information
	def get_time_info(self):

		# check if period/quarter/half information exists
		# use regular expressions (regex) to remove non-numeric characters
		# convert values scraped to int if int type
		if self.game_info.find('span', {'class': 'live-time'}):
			period = self.game_info.find('span', {'class': 'live-time'}).text
			period = self.int_regex(period)
			self.period = int(period) if self.is_int(period) else self.period

		# check if time information exists
		# use regular expressions (regex) to remove non-numeric characters
		# convert values scraped to int if int type
		if self.game_info.find('span', {'class': 'match-time'}):
			minute = self.game_info.find('span', {'class': 'match-time'}).text
			minute = self.int_regex(minute)
			self.minute = int(minute) if self.is_int(minute) else self.minute


	# get team and betting options information
	def get_team_info(self):

		# check if team name information exists
		if self.team_name_info:
			self.away_team_name = self.team_name_info[0].text
			self.home_team_name = self.team_name_info[1].text

		# check if team score information exists
		# use regular expressions (regex) to remove non-numeric characters
		# convert values scraped to int if int type
		if self.team_score_info:
			away_team_score = self.int_regex(self.team_score_info[0].text)
			home_team_score = self.int_regex(self.team_score_info[1].text)
			self.away_team_score = int(away_team_score) if self.is_int(away_team_score) else self.away_team_score
			self.home_team_score = int(home_team_score) if self.is_int(home_team_score) else self.home_team_score

		# check if team spread information exists
		# use regular expressions (regex) to remove nun-numeric characters (allow decimals)
		# convert values scraped to int if int type
		if self.spread_info:
			away_team_spread = self.float_regex(self.spread_info[0].text)
			home_team_spread = self.float_regex(self.spread_info[1].text)
			self.away_team_spread = float(away_team_spread) if self.is_float(away_team_spread) else self.away_team_spread
			self.home_team_spread = float(home_team_spread) if self.is_float(home_team_spread) else self.home_team_spread

		# check if team spread odds information exists
		if self.spread_info_odds:

			# use regular expressions (regex) to remove nun-numeric characters
			# convert values scraped to int if int type
			away_team_spread_odds = self.int_regex(self.spread_info_odds[0].text)
			home_team_spread_odds = self.int_regex(self.spread_info_odds[1].text)
			self.away_team_spread_odds = int(away_team_spread_odds) if self.is_int(away_team_spread_odds) else self.away_team_spread_odds
			self.home_team_spread_odds = int(home_team_spread_odds) if self.is_int(home_team_spread_odds) else self.home_team_spread_odds

		# check if team moneyline information exists
		if self.moneyline_info or self.result_info_odds:

			# check if tie moneyline exists
			# use regular expressions (regex) to remove nun-numeric characters
			# convert values scraped to int if int type
			if not self.result_info_odds:
				away_team_moneyline = self.int_regex(self.moneyline_info[0].text)
				home_team_moneyline = self.int_regex(self.moneyline_info[1].text)
				tie_moneyline = None

			else:
				away_team_moneyline = self.int_regex(self.result_info_odds[0].text)
				tie_moneyline = self.int_regex(self.result_info_odds[1].text)
				home_team_moneyline = self.int_regex(self.result_info_odds[2].text)

			self.away_team_moneyline = int(away_team_moneyline) if self.is_int(away_team_moneyline) else self.away_team_moneyline
			self.tie_moneyline = int(tie_moneyline) if self.is_int(tie_moneyline) else self.tie_moneyline
			self.home_team_moneyline = int(home_team_moneyline) if self.is_int(home_team_moneyline) else self.home_team_moneyline


	# get total score over/under betting information
	def get_over_under_info(self):

		# check if over/under information exists
		# use regular expressions (regex) to remove nun-numeric characters (allow decimals)
		# convert values scraped to float if float type
		if self.over_under_info:
			over = self.float_regex(self.over_under_info[0].text)
			under = self.float_regex(self.over_under_info[1].text)
			self.over = float(over) if self.is_float(over) else self.over
			self.under = float(under) if self.is_float(under) else self.under

		# check if over/under odds information exists
		# use regular expressions (regex) to remove nun-numeric characters
		# check values scraped to int if int type
		if self.over_under_info_odds:
			over_odds = self.int_regex(self.over_under_info_odds[0].text)
			under_odds = self.int_regex(self.over_under_info_odds[1].text)
			self.over_odds = int(over_odds) if self.is_int(over_odds) else self.over_odds
			self.under_odds = int(under_odds) if self.is_int(under_odds) else self.under_odds


	def __repr__(self):

		return '{}'.format(vars(self))


class SCRAPE():


	def __init__(self, driver, sports_active={}, sports_html_classes={}, sports_minute_logged={}):
		self.driver = driver
		self.sports_active = sports_active
		self.sports_html_classes = sports_html_classes
		self.sports_minute_logged = sports_minute_logged


	# get category (sport) HTML
	def get_event_category_html(self, soup, sport, sport_html_class):

		# create empty BeautifulSoup object (future requirements if nothing found)
		# find live event categories
		sport_live_event_category_html = BeautifulSoup('', 'html.parser')
		live_event_categories_html = soup.find_all('div', {'class': 'live-event-container'})

		# iterate through live event categories
		# check if desired sport found
		for live_event_category_html in live_event_categories_html:
			if live_event_category_html.header.section.h4('span')[2].text == sport:
				sport_live_event_category_html = live_event_category_html

		# return events within event category
		return sport_live_event_category_html.find_all('div', {'class': sport_html_class})


	# get information for events
	def get_all_events_info(self):

		soup = BeautifulSoup(self.driver.page_source, 'html.parser')

		# create empty list to store data
		# identify active sports to scrape (specified in the configuration file)
		data = []
		sports_active = [k for k, v in self.sports_active.items() if v == True]
		sports_html_classes = {k: v for k, v in self.sports_html_classes.items() if k in sports_active}
		sports_minute_logged = {k: v for k, v in self.sports_minute_logged.items() if k in sports_active}

		# loop through all active sports
		for key in sports_active:

			# define sport variables
			# create live event class object
			sport = key
			sport_html_class = sports_html_classes[key]
			sport_minute_logged = sports_minute_logged[key]
			live_event_info = EVENT()

			# iterate through all live events of a sport
			for live_event_html in self.get_event_category_html(soup=soup, sport=sport, sport_html_class=sport_html_class):

				# gets live event information
				live_event_info.get_event_info_html(live_event_html)
				live_event_info.get_time_info()
				live_event_info.get_team_info()
				live_event_info.get_over_under_info()

				# default minute to 0
				if not sport_minute_logged:
					live_event_info.minute = None

				# create object to store event logistics information
				log_rules = [
							live_event_info.period,
							live_event_info.away_team_name,
							live_event_info.home_team_name,
							live_event_info.away_team_score is not None,
							live_event_info.home_team_score is not None,
							(sport_minute_logged and live_event_info.minute) or sport_minute_logged == False,
							]

				# check if rules met to log data
				# add data to list
				if all(log_rules):
					data.append([datetime.now().strftime('%Y-%m-%d'), datetime.now(), sport_html_class, sport, live_event_info.period, live_event_info.minute,
									live_event_info.away_team_name, live_event_info.home_team_name, live_event_info.away_team_score, live_event_info.home_team_score,
									live_event_info.away_team_spread, live_event_info.away_team_spread_odds, live_event_info.home_team_spread,
									live_event_info.home_team_spread_odds, live_event_info.away_team_moneyline, live_event_info.home_team_moneyline,
									live_event_info.over, live_event_info.over_odds, live_event_info.under, live_event_info.under_odds, live_event_info.tie_moneyline])

		return data


	def __repr__(self):

		return '{}'.format(vars(self))
