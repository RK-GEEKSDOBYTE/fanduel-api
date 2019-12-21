class CONFIG:
	browser_refresh_int = 120
	data_collection_int = 4
	screen_load_wait = 10
	driver_headless = False
	driver_location = '/usr/lib/chromium-browser/chromedriver'
	log_file_path = '/home/ubuntu/Desktop/fanduel-api/log/sys.log'
	debug = False
	url = 'https://sportsbook.fanduel.com/sports'
	sports =	{
				'NBA': 					{
										'active': True,
										'html_class': 'BASKETBALL',
										'minute_logged': True
										},
				'NFL': 					{
										'active': True,
										'html_class': 'NFL',
										'minute_logged': False
										},
				'MLB': 					{
										'active': True,
										'html_class': 'BASEBALL',
										'minute_logged': False
										},
				'NHL': 					{
										'active': True,
										'html_class': 'HOCKEY',
										'minute_logged': False
										},
				'EPL': 					{
										'active': True,
										'html_class': 'SOCCER',
										'minute_logged': True
										}
				}
