import pandas as pd
import numpy as np
import random

import src.state_action_reward as sar
from src.randomgame import RandomGame
from src.cards import Card, Deck


class Agent(object):
    def __init__(self, agent_info:dict):
        """Initializes the agent to get parameters and create an empty q-tables."""

        self.epsilon     = agent_info["epsilon"]
        self.step_size   = agent_info["step_size"]
        self.states      = sar.states()
        self.actions     = sar.actions()
        self.R           = sar.rewards(self.states, self.actions)        

        self.q = pd.DataFrame(
            data    = np.zeros((len(self.states), len(self.actions))), 
            columns = self.actions, 
            index   = self.states
        )
        
        self.visit = self.q.copy()

#Tavie and Josh's implemented agent
#basically uses trial and error at every step
#to pick the card most likely to win
class StatelessMonteCarloAgent(Agent):
    def __init__(self, agent_info:dict):        
        print("in stateless monte carlo init")
        super().__init__(agent_info)
        self.prev_state  = 0
        self.prev_action = 0
        #self.hand = our_hand
        #self.opp_hand = opp_hand #integer value
        #self.open_card = open_card #current open card
        #self.played_cards = played_cards #cards discarded
        
    def step(self, state_dict, actions_dict, open_card, hand, num_opp_hand, played_cards):
        print("in step, hand is: ", type(hand))
        ACTION_ITERS = 500
        actions_possible = [key for key,val in actions_dict.items() if val != 0]
        win_tracker = np.zeros((len(actions_possible)), dtype = int)
        if len(actions_possible) == 1: #if only one feasible action
            return actions_possible[0] #play it
        for action in range(len(actions_possible)):
            for i in range(ACTION_ITERS):
                
                #play action. For opponent...
                #make new deck
                #draw opponent_card_num cards
                #check that none are in player.cards_seen
                #play game with this hand playing randomly
                #and player 1 playing randomly as well?
                #record who won in win_loss_tracker based on action (first card played) 
                
                won = RandomGame(open_card, hand, num_opp_hand, played_cards).winner
                 #TODO: num_opp_hand does not update (change from 7)
                print("player: ", won, "won the simulated battle")
                if won == 1:
                    win_tracker[action] += 1
        #calculate win_loss_proportions based on tracker -> tracker[0] / tracker.sum of column
        max_win = 0
        index = 0
        for i in range(len(win_tracker)):
            if max_win < win_tracker[i]:
                max_win = win_tracker[i]
                index = i
        
        #play action with highest likelihood of winning
                      
        return actions_possible[index]
    

    def assumeHand(played_cards): #returns a list of cards
        opp_cards = Deck().discardList(our_hand) #need to code for our_hand
        opp_cards.discardList(played_cards)
        opp_cards.discard(open_card)
        length = len(opp_cards)
        for i in range(length - opp_hand):
            num = random.randint(0, len(opp_cards))
            opp_cards.discard(opp_cards[num])
        
        return opp_cards.cards #returns just a list, not of the deck object class
    
    def update(self, state_dict, action):
        return 0
    
class QLearningAgent(Agent):
    
    def __init__(self, agent_info:dict):        
        
        super().__init__(agent_info)
        self.prev_state  = 0
        self.prev_action = 0
    
    def step(self, state_dict, actions_dict, open_card, hand, num_opp_hand, played_cards=None):
        """
        Choose the optimal next action according to the followed policy.
        Required parameters:
            - state_dict as dict
            - actions_dict as dict
        """
        
        # (1) Transform state dictionary into tuple
        state = [i for i in state_dict.values()]
        state = tuple(state)
        
        # (2) Choose action using epsilon greedy
        # (2a) Random action
        if random.random() < self.epsilon:
            
            actions_possible = [key for key,val in actions_dict.items() if val != 0]         
            action = random.choice(actions_possible)
        
        # (2b) Greedy action
        else:
            actions_possible = [key for key,val in actions_dict.items() if val != 0]
            random.shuffle(actions_possible)
            val_max = 0
            
            for i in actions_possible:
                val = self.q.loc[[state],i][0]
                if val >= val_max: 
                    val_max = val
                    action = i
        
        return action
    
    def update(self, state_dict, action):
        """
        Updating Q-values according to Belman equation
        Required parameters:
            - state_dict as dict
            - action as str
        """
        state = [i for i in state_dict.values()]
        state = tuple(state)
        
        # (1) Set prev_state unless first turn
        if self.prev_state != 0:
            prev_q = self.q.loc[[self.prev_state], self.prev_action][0]
            this_q = self.q.loc[[state], action][0]
            reward = self.R.loc[[state], action][0]
            
            print ("\n")
            print (f'prev_q: {prev_q}')
            print (f'this_q: {this_q}')
            print (f'prev_state: {self.prev_state}')
            print (f'this_state: {state}')
            print (f'prev_action: {self.prev_action}')
            print (f'this_action: {action}')
            print (f'reward: {reward}')
            
            # Calculate new Q-values
            if reward == 0:
                self.q.loc[[self.prev_state], self.prev_action] = prev_q + self.step_size * (reward + this_q - prev_q) 
            else:
                self.q.loc[[self.prev_state], self.prev_action] = prev_q + self.step_size * (reward - prev_q)
                
            self.visit.loc[[self.prev_state], self.prev_action] += 1
            
        # (2) Save and return action/state
        self.prev_state  = state
        self.prev_action = action
    
        
class MonteCarloAgent(Agent):

    def __init__(self, agent_info:dict):

        super().__init__(agent_info)
        self.state_seen  = list()
        self.action_seen = list()
        self.q_seen      = list()
    
    def step(self, state_dict, actions_dict, open_card, hand, num_opp_hand, played_cards=None):
        """
        Choose the optimal next action according to the followed policy.
        Required parameters:
            - state_dict as dict
            - actions_dict as dict
        """
        
        # (1) Transform state dictionary into tuple
        state = [i for i in state_dict.values()]
        state = tuple(state)
        
        # (2) Choose action using epsilon greedy
        # (2a) Random action
        if random.random() < self.epsilon:
            
            actions_possible = [key for key,val in actions_dict.items() if val != 0]         
            action = random.choice(actions_possible)
        
        # (2b) Greedy action
        else:
            actions_possible = [key for key,val in actions_dict.items() if val != 0]
            random.shuffle(actions_possible)
            val_max = 0
            
            for i in actions_possible:
                val = self.q.loc[[state],i][0]
                if val >= val_max: 
                    val_max = val
                    action = i
        
        # (3) Add state-action pair if not seen in this simulation
        if ((state),action) not in self.q_seen:
            self.state_seen.append(state)
            self.action_seen.append(action)
        
        self.q_seen.append(((state),action))
        self.visit.loc[[state], action] += 1
        
        return action
    
    def update(self, state_dict, action):
        """
        Updating Q-values according to Belman equation
        Required parameters:
            - state_dict as dict
            - action as str
        """
        
        state  = [i for i in state_dict.values()]
        state  = tuple(state)
        reward = self.R.loc[[state], action][0]
        
        # Update Q-values of all state-action pairs visited in the simulation
        for s,a in zip(self.state_seen, self.action_seen): 
            self.q.loc[[s], a] += self.step_size * (reward - self.q.loc[[s], a])
            print (self.q.loc[[s],a])
        
        self.state_seen, self.action_seen, self.q_seen = list(), list(), list()