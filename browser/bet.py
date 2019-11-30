# import packages

# import custom packages

# define static variables

# define dynamic variables


class BET:

    def __init__(self, driver):
        self.driver
        self.types = ['less', 'more', 'equal', 'any']
        self.bet_types = ['spread', 'moneyline', 'total']


    # submit bet
    def bet(self, bet_amount, league, team_name, bet_comparision_value, bet_type='moneyline', type='equal'):
        print("TEST")


    # sell bet
    def sell(self, reference_id, bet_comparision_value, type='equal'):
        print("TEST")


	def __repr__(self):

		return '{}'.format(vars(self))
