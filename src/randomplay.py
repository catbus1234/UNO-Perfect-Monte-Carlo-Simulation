import pandas as pd
import numpy as np
import random

import src.state_action_reward as sar
from src.cards import Card, Deck

class randomPlay():
    
    def step(state_dict, actions_dict, open_card, hand, num_opp_hand, played_cards):
        """
        Randomly plays a possible action
        """
        print("type actions_dict: ", type(actions_dict))
        actions_possible = [key for key,val in actions_dict.items() if val != 0]         
        action = random.choice(actions_possible)
        
        return action