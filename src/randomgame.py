import time
print("here")
from src.randomplay import randomPlay
from src.players import Player
from src.turn import Turn
from src.cards import Card, Deck
from src.utils import check_win, block_print, enable_print, bold
import config as conf

class RandomGame(object):
    """
    Randomly plays feasible moves from the two hands and returns a winner. 
    Create two plays and set_hand to our_hand and opp_hand
    1. start with opponent
    while no winner:
    """
    
    def __init__ (self, open_card, our_hand, num_opp_hand, played_cards):
        print("top of randomgame")
        self.player_1 = Player(1, agent=randomPlay)
        self.player_2 = Player(2, agent=randomPlay)
        self.player_1.set_hand(our_hand)
        deck = Deck() #TODO: figure out how to use remove_list(played_cards) to remove discarded cards
        deck.discardList(played_cards)
        deck.discardList(our_hand)
        self.player_2.set_hand_num(num_opp_hand, deck)
        self.card_open = open_card
        #TODO: need to evaluate hands based on open card? functionality note done in draw
        self.turn = Turn(
            deck=deck, 
            player_1=self.player_1, 
            player_2=self.player_2, 
            agent=randomPlay
        )
        self.turn_no = 0
        self.winner = 0 #will be 1 if player 1 wins, and 2 if opponent wins
        
        print("top of randomgame loop")
        while self.winner == 0:
            print("inside randomgame loop")
            self.turn_no += 1
            if (self.turn_no == 1):
                card_open = open_card
            else:
                card_open = self.turn.card_open
            
            if self.turn_no%2 == 1: player_act, player_pas = self.player_1, self.player_2
            else:                   player_act, player_pas = self.player_2, self.player_1
            
            player_act.show_hand()
            player_act.show_hand_play(card_open)
            self.turn.action(
                player=player_act, 
                opponent=player_pas, 
                agent=randomPlay,
                algorithm=None
            )
            
            if check_win(player_act) == True:
                self.winner = player_act.name
                print (f'{player_act.name} has won!')
                break
                
            if check_win(player_pas) == True:
                self.winner = player_pas.name
                print (f'{player_pas.name} has won!')
                break
                
            if player_act.card_play.value in ["REV", "SKIP"]:
                print (f'{player_act.name} has another turn')
                self.turn_no = self.turn_no-1
                
            if (self.turn.count > 0) and (self.turn.count %2 == 0):
                print (f'Again it is {player_act.name}s turn')
                self.turn_no = self.turn_no-1
        

        self.player_1.identify_state(card_open)