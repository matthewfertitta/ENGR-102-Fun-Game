from card import Card
from deck import Deck
import pygame

class Player():
    
    def __init__(self, player_num):
        super().__init__()
        self.hand = []
        self.points = 0
        self.hand_count = len(self.hand)
        self.InGame = True
        self.player_num = player_num

    def draw_cards_on_screen(self, surface: pygame.Surface, SCREEN_WIDTH, SCREEN_HEIGHT, loc):
        """ Draws cards at a location on the screen """
        card_data = Card.empty()
        
        if loc == "bottom":
            total_width = len(self.hand) * card_data.get_card_width() + (len(self.hand) - 1) * card_data.get_card_spacing()
            start_x = (SCREEN_WIDTH - total_width) // 2
            start_y = SCREEN_HEIGHT - card_data.get_card_height() - 20  # 20 pixels from bottom
    
            for i, card in enumerate(self.hand):
                x = start_x + i * (card_data.get_card_width() + card_data.get_card_spacing())
                card.draw(surface, x, start_y)

    def draw_card(self, deck: Deck):
        """ Draws a card from the given deck and adds it to the player's hand """
        # draw card from deck
        card = deck.draw_card()
        # check for bust
        for c in self.hand:
            c: Card # define c of type card
            # check for equality excluding ablities and score modifiers
            if c.get_card_name() == card.get_card_name() and card.isARegularCard():
                # player busted
                print(f"{self.player_num} Busted!")
                return False
        # player got a unique card
        self.hand.append(card)
        


    def get_hand_size(self):
        return len(self.hand)

