# import packages
from datetime import datetime
from bs4 import BeautifulSoup

# import custom packages
from . import helper

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


	# get event information
	def get_event_info_html(self, event_html):

		# get core betting information
		self.game_info = event_html.find('section', {'class': 'single-coupon-footer'})
		self.team_name_info = event_html.find_all('span', {'class': 'name'})
		self.team_score_info = event_html.find_all('td', {'class': 'score-value'})

		# check if no betting options (markets) are available
		if not event_html.find('section', {'class': 'nomarkets'}):

			# check if spread information is available
			if event_html.find('div', {'class': 'market points'}):
				self.spread_info = event_html.find('div', {'class': 'market points'}).find_all('div', {'class': 'currenthandicap'})

				# check if spread information found
				# delete excess elements captured (need to identify better identifier)
				if self.spread_info:
					del self.spread_info[3]
					del self.spread_info[1]

			# check if moneyline information is available
			if event_html.find('div', {'class': 'market money'}):
				self.moneyline_info = event_html.find('div', {'class': 'market money'}).find_all('div', {'class': 'selectionprice'})

			# check if over/under information is available
			if event_html.find('div', {'class': 'market total'}):
				self.over_under_info = event_html.find('div', {'class': 'market total'}).find_all('div', {'class': 'uo-currenthandicap'})

			# check if spread odds information is available and not suspended
			if event_html.find('div', {'class': 'market points'}):

				# check if spread odds information is not suspended
				if not event_html.find('div', {'class': 'market points'}).find('div', {'class': 'selectionprice suspended'}):
					self.spread_info_odds = event_html.find('div', {'class': 'market points'}).find_all('div', {'class': 'selectionprice'})

			# check if over/under odds information is available
			if event_html.find('div', {'class': 'market total'}):

				# check if over/under odds information is not suspended
				if not event_html.find('div', {'class': 'market total'}).find('div', {'class': 'selectionprice suspended'}):
					self.over_under_info_odds =  event_html.find('div', {'class': 'market total'}).find_all('div', {'class': 'selectionprice'})

			# check if result odds information is available and not suspended
			if event_html.find('div', {'class': 'three-and-more-selections'}):

				# check if result odds information is not suspended
				if not event_html.find('div', {'class': 'suspended three-and-more-selections'}):
					self.result_info_odds = event_html.find_all('div', {'class': 'selectionprice'})


	# get event time information
	def get_time_info(self):

		# check if period/quarter/half information exists
		# use regex to remove non-numeric characters
		# convert to int type if possible
		if self.game_info.find('span', {'class': 'live-time'}):
			period = self.game_info.find('span', {'class': 'live-time'}).text
			period = helper.int_regex(period)
			self.period = int(period) if helper.is_int(period) else self.period

		# check if time information exists
		# use regex to remove non-numeric characters
		# convert to int type if possible
		if self.game_info.find('span', {'class': 'match-time'}):
			minute = self.game_info.find('span', {'class': 'match-time'}).text
			minute = helper.int_regex(minute)
			self.minute = int(minute) if helper.is_int(minute) else self.minute


	# get team and betting options information
	def get_team_info(self):

		# check if team name information exists
		if self.team_name_info:
			self.away_team_name = self.team_name_info[0].text
			self.home_team_name = self.team_name_info[1].text

		# check if team score information exists
		# use regex to remove non-numeric characters
		# convert to int type if possible
		if self.team_score_info:
			away_team_score = helper.int_regex(self.team_score_info[0].text)
			home_team_score = helper.int_regex(self.team_score_info[1].text)
			self.away_team_score = int(away_team_score) if helper.is_int(away_team_score) else self.away_team_score
			self.home_team_score = int(home_team_score) if helper.is_int(home_team_score) else self.home_team_score

		# check if team spread information exists
		# use regex to remove nun-numeric characters (allow decimals)
		# convert to float type if possible
		if self.spread_info:
			away_team_spread = helper.float_regex(self.spread_info[0].text)
			home_team_spread = helper.float_regex(self.spread_info[1].text)
			self.away_team_spread = float(away_team_spread) if helper.is_float(away_team_spread) else self.away_team_spread
			self.home_team_spread = float(home_team_spread) if helper.is_float(home_team_spread) else self.home_team_spread

		# check if team spread odds information exists
		# use regex to remove non-numeric characters
		# convert to int type if possible
		if self.spread_info_odds:
			away_team_spread_odds = helper.int_regex(self.spread_info_odds[0].text)
			home_team_spread_odds = helper.int_regex(self.spread_info_odds[1].text)
			self.away_team_spread_odds = int(away_team_spread_odds) if helper.is_int(away_team_spread_odds) else self.away_team_spread_odds
			self.home_team_spread_odds = int(home_team_spread_odds) if helper.is_int(home_team_spread_odds) else self.home_team_spread_odds

		# check if team moneyline information exists
		# check if tie moneyline exists to assign values
		# use regex to remove non-numeric characters
		# convert to int type if possible
		if self.moneyline_info or self.result_info_odds:
			away_team_moneyline = helper.int_regex(self.moneyline_info[0].text) if not self.result_info_odds else helper.int_regex(self.result_info_odds[0].text)
			home_team_moneyline = helper.int_regex(self.moneyline_info[1].text) if not self.result_info_odds else helper.int_regex(self.result_info_odds[2].text)
			tie_moneyline = None if not self.result_info_odds else helper.int_regex(self.result_info_odds[1].text)
			self.away_team_moneyline = int(away_team_moneyline) if helper.is_int(away_team_moneyline) else self.away_team_moneyline
			self.tie_moneyline = int(tie_moneyline) if helper.is_int(tie_moneyline) else self.tie_moneyline
			self.home_team_moneyline = int(home_team_moneyline) if helper.is_int(home_team_moneyline) else self.home_team_moneyline


	# get total score over/under betting information
	def get_over_under_info(self):

		# check if over/under information exists
		# use regex to remove nun-numeric characters (allow decimals)
		# convert to float type if possible
		if self.over_under_info:
			over = helper.float_regex(self.over_under_info[0].text)
			under = helper.float_regex(self.over_under_info[1].text)
			self.over = float(over) if helper.is_float(over) else self.over
			self.under = float(under) if helper.is_float(under) else self.under

		# check if over/under odds information exists
		# use regex to remove non-numeric characters
		# convert to int type if possible
		if self.over_under_info_odds:
			over_odds = helper.int_regex(self.over_under_info_odds[0].text)
			under_odds = helper.int_regex(self.over_under_info_odds[1].text)
			self.over_odds = int(over_odds) if helper.is_int(over_odds) else self.over_odds
			self.under_odds = int(under_odds) if helper.is_int(under_odds) else self.under_odds


	def __repr__(self):

		return '{}'.format(vars(self))


class SCRAPE():


	def __init__(self, driver):
		self.driver = driver


	# get information for events
	def get_all_events_info(self, sports_active, sports_html_classes, sports_minute_logged):

		# convert html to BeautifulSoup object
		# find live event categories
		# get scrape time
		# create empty list to store data
		html = BeautifulSoup(self.driver.driver.page_source, 'html.parser')
		live_event_categories_html = html.find_all('div', {'class': 'live-event-container'})
		scrape_time = datetime.now()
		data = []

		# loop through active sports
		for sport in sports_active:

			# create default variables
			# get html class associated to active sport
			# get minute logged flag associated to active sport
			events_html = None
			sport_html_class = sports_html_classes[sport]
			sport_minute_logged = sports_minute_logged[sport]

			# loop through live event categories
			for live_event_category_html in live_event_categories_html:

				# check if desired sport found
				if live_event_category_html.header.section.h4('span')[2].text == sport:
					events_html = live_event_category_html.find_all('div', {'class': sport_html_class})
					break

			# check if live events exist for sport
			if events_html:

				# loop through live events of a sport
				for event_html in events_html:

					# create live event class object
					# gets live event information
					event_info = EVENT()
					event_info.get_event_info_html(event_html=event_html)
					event_info.get_time_info()
					event_info.get_team_info()
					event_info.get_over_under_info()

					# default minute to 0 if minute not logged in sport
					event_info.minute = None if not sport_minute_logged else event_info.minute

					# create rules to decide on whether to track event information
					log_rules = [event_info.period, event_info.away_team_name, event_info.home_team_name, event_info.away_team_score is not None,
								event_info.home_team_score is not None, (sport_minute_logged and event_info.minute) or sport_minute_logged == False]

					# check if rules met
					if all(log_rules):

						# add data to list
						data.append([scrape_time.strftime('%Y-%m-%d'), scrape_time, sport_html_class, sport, event_info.period, event_info.minute,
										event_info.away_team_name, event_info.home_team_name, event_info.away_team_score, event_info.home_team_score,
										event_info.away_team_spread, event_info.away_team_spread_odds, event_info.home_team_spread,
										event_info.home_team_spread_odds, event_info.away_team_moneyline, event_info.home_team_moneyline,
										event_info.over, event_info.over_odds, event_info.under, event_info.under_odds, event_info.tie_moneyline])

		self.driver.logging.info('Scraped {} Records'.format(len(data)))

		return data


	def __repr__(self):

		return '{}'.format(vars(self))
