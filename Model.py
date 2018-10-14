from random import shuffle
from Notifiable import Notifiable
import time


class Model:
    BUTTON_DICT = {'retry': True, 'hit': False, 'stand': False, 'split': False}

    def __init__(self, window: Notifiable):
        self.suits = ['C', 'D', 'S', 'H']
        self.values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.deck = []
        self.playerhand = []
        self.dealerhand = []
        self.observer = window
        self.player = 0
        self.is_hidden = True  # Dealer first card hidden?
        self.cash = 100
        self.bet = 25

    def create_deck(self):
        for suit in self.suits:
            for value in self.values:
                self.deck.append([value, suit])
        shuffle(self.deck)

    def draw_card(self, hand):
        hand.append(self.deck[0])
        self.observer.notify('Draw card')
        self.deck.pop(0)

    def dealer_card_choice(self):
        self.is_hidden = False
        Model.button_changer('stand')
        Model.button_changer('hit')
        while self.card_value_check(self.dealerhand) < 16:
            self.draw_card(self.dealerhand)
            self.observer.notify("Dealer thinking")
        self.end_game()

    def blackjack_check(self, hand):
        if self.card_value_check(hand) == 21 and len(hand) == 2:
            return True
        return False


    def blackjack_logic(self):  #Checks who has blackjack and if both then bets are returned and game over
        if self.blackjack_check(self.playerhand) or self.blackjack_check(self.dealerhand):
            return True
        else:
            return False


    def push(self):
        self.cash += self.bet
        self.bet = 0

    @classmethod
    def button_changer(cls, button):
        Model.BUTTON_DICT[button] = not Model.BUTTON_DICT[button]  # Changes BUTTON_DICT values based on choice.

    '''
    def _player_or_dealer(func):
        def wrapper(*args):
            runner = func(*args)
            print('Function: {0} ran with parameters: {1} giving result {2}.'.format(func.__name__, args, runner))
            return runner
        return wrapper
    '''

    # @_player_or_dealer
    @staticmethod
    def card_value_check(hand):
        total = 0
        num_of_aces = 0
        for number in list(hand):
            if number[0] == 'A':
                num_of_aces += 1
                total += 11

            elif number[0] == 'J' or number[0] == 'Q' or number[0] == 'K':
                total += 10

            else:
                total += int(number[0])
        while num_of_aces > 0 and total > 21:
            num_of_aces -= 1
            total -= 10
        return total

    def end_game(self):
        playerscore = self.card_value_check(self.playerhand)
        dealerscore = self.card_value_check(self.dealerhand)
        self.observer.notify("You have {}, Dealer has {}".format(playerscore, dealerscore))

        if Model.BUTTON_DICT['stand'] and Model.BUTTON_DICT['hit']:# Change to hide buttons and flip card if
            Model.button_changer('stand')                          # blackjack happens on first cards
            Model.button_changer('hit')
            self.is_hidden = False

        if playerscore == dealerscore:
            self.push()
            self.observer.notify("Draw, bets pushed.")
            return 0

        elif self.blackjack_check(self.dealerhand):  # Blackjack
            self.observer.notify('Blackjack, you lose!')
            return 0

        elif self.blackjack_check(self.playerhand):  # Blackjack
            self.observer.notify('Blackjack, you win!')
            return 0

        elif playerscore > 21:  # Player bust

            if dealerscore > 21:  # Player bust, Dealer bust
                print('No winners here')
                self.observer.notify('No winners here')
                return 0

            else:  # Player bust, dealer <= 21
                print('Bust, you lose')
                self.observer.notify('Bust, you lose')
                return 0

        elif dealerscore > 21 and playerscore < 21:
            self.observer.notify('Dealer bust, You win')
            return 0

        elif playerscore > dealerscore:
            self.observer.notify('You win')
            return 0

        else:
            self.observer.notify('You lose')
            return 0

    def notify(self, choice=0):
        if choice == 'retry':
            # Model.button_changer('double')
            if not Model.BUTTON_DICT['stand'] and not Model.BUTTON_DICT['hit']:
                Model.button_changer('stand')
                Model.button_changer('hit')
            self.deck = []
            self.playerhand = []
            self.dealerhand = []
            self.is_hidden = True

            self.create_deck()
            self.draw_card(self.playerhand)
            self.draw_card(self.playerhand)
            self.draw_card(self.dealerhand)
            self.draw_card(self.dealerhand)
            self.observer.notify("cards dealt")
            if self.blackjack_logic():  # One person with blackjack
                self.end_game()
            self.player = 0

        # if self.playerhand[0][0] == self.playerhand[0][1]:
        #    Model.button_changer('split')

        if self.player == 0:
            # Model.button_changer('double')
            if choice == 'split':
                pass

            elif choice == 'double':
                pass

            elif choice == 'surrender':
                pass

            elif choice == 'stand':
                self.dealer_card_choice()

            elif choice == 'hit':
                self.draw_card(self.playerhand)
                if self.card_value_check(self.playerhand) > 21:
                    self.observer.notify("Bust")
                    self.dealer_card_choice()

        self.observer.notify("")
