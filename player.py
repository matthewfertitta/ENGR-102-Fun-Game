from card import Card
from deck import Deck
import pygame

class Player():
    
    def __init__(self, player_num):
        self.hand = []
        self.points = 0
        self.total_score = 0  # cumulative score across rounds
        self.hand_count = len(self.hand)
        self.InGame = True
        self.player_num = player_num
        self.default_player_locations = {1:"bottom", 2:"top"}
        self.standing = False  # track if player is standing this round
        self.busted = False    # track if player busted this round
        self.has_second_chance = False  # track if player has second chance card

    def draw_cards_on_screen(self, surface: pygame.Surface, SCREEN_WIDTH, SCREEN_HEIGHT, loc=None):
        """ Draws cards at a location on the screen """
        
        # handle empty hands
        if not self.hand:
            return
        
        # use player num to set loc
        loc = self.default_player_locations[self.get_player_num()]
        # use first card in player's hand a reference
        ref_card = self.hand[0]
        card_width = ref_card.get_card_width()
        card_height = ref_card.get_card_height()
        spacing = ref_card.get_card_spacing()

        # get total width of all cards with spacing
        total_width = len(self.hand) * card_width + (len(self.hand) - 1) * spacing
        start_x = (SCREEN_WIDTH - total_width) // 2

        # vertical location
        if loc == "bottom":
            start_y = SCREEN_HEIGHT - card_height - 20
        elif loc == "top":
            start_y = 20
        else:
            raise NotImplementedError

        # draw cards
        for i, card in enumerate(self.hand):
            x = start_x + i * (card_width + spacing)
            card.draw_card_to_screen(surface, x, start_y)

    def draw_card(self, deck: Deck):
        """ Draws a card from the given deck and adds it to the player's hand """
        # draw card from deck
        card = deck.draw_card()
        
        # handle ability cards
        if card.isAnAbilityCard():
            if card.get_card_name() == "Second\nChance":
                # hold onto second chance card
                self.has_second_chance = True
                return card  # return the card for tracking
            else:
                # other ability cards are used immediately
                return card
        
        # handle modifiers - add to hand but don't count for bust
        if card.get_card_type() == "modifier":
            self.hand.append(card)
            return card
        
        # check for bust (only for number cards)
        for c in self.hand:
            c: Card # define c of type card
            # check for equality excluding abilities and score modifiers
            if c.get_card_name() == card.get_card_name() and card.isARegularCard():
                # player busted
                self.hand.append(card)
                
                # check if player has second chance
                if self.has_second_chance:
                    self.has_second_chance = False
                    return "second_chance_used"  # special return value
                else:
                    self.busted = True
                    return False
        
        # player got a unique card
        self.hand.append(card)
        # player didn't bust, return card gotten
        return card
        
    def get_player_num(self):
        return self.player_num

    def get_hand_size(self):
        return len(self.hand)
    
    def get_number_card_count(self):
        """ Returns count of only number cards """
        count = 0
        for card in self.hand:
            if card.isARegularCard():
                count += 1
        return count
    
    def get_hand(self):
        return self.hand
    
    def set_hand(self, hand: list):
        self.hand = hand

    def reset_hand(self):
        self.set_hand([])
        self.standing = False
        self.busted = False
        self.has_second_chance = False
    
    def set_standing(self, value: bool):
        self.standing = value
    
    def is_standing(self):
        return self.standing
    
    def is_busted(self):
        return self.busted
    
    def is_active(self):
        """ Returns True if player can still take actions this round """
        return not self.standing and not self.busted
    
    def calculate_round_score(self):
        """ Calculates score for this round based on hand """
        if self.busted:
            return 0
        
        # sum up number cards
        base_score = 0
        multiplier = 1
        addition = 0
        
        for card in self.hand:
            if card.isARegularCard():
                base_score += card.get_value()
            elif card.get_card_type() == "modifier":
                if card.get_card_name() == "x2":
                    multiplier *= 2
                else:
                    # addition modifiers
                    addition += card.get_value()
        
        # apply multiplier first, then addition
        final_score = (base_score * multiplier) + addition
        return final_score
    
    def add_to_total_score(self, points):
        """ Adds points to the cumulative total score """
        self.total_score += points
    
    def get_total_score(self):
        return self.total_score