import pygame

class Card:
    """ Information about a single card """

    def __init__(self, card_name: str, card_type: str, value=None, ability_effect=None):
        self.card_name = card_name
        self.card_type = card_type
        self.value = value
        self.ability_effect = ability_effect
        self.rect = None # holds position and size

        # colors
        self.BLACK = pygame.Color("black")
        self.WHITE = pygame.Color("white")
        self.CARD_COLOR = (200, 200, 200)

        # card specifications
        self.CARD_WIDTH = 80
        self.CARD_HEIGHT = 120
        self.CARD_SPACING = 10
        self.BORDER_COLOR = self.BLACK

    @classmethod
    def empty(cls):
        """ Used to get constant values from other classes """
        return cls("EMPTY", "NONE")
        

    def draw_card_to_screen(self, surface: pygame.Surface, x, y):
        """ Draws a card at a specified position """
        self.rect = pygame.Rect(x, y, self.CARD_WIDTH, self.CARD_HEIGHT)

        # draws card background
        pygame.draw.rect(surface, self.CARD_COLOR, self.rect)
        pygame.draw.rect(surface, self.BORDER_COLOR, self.rect, 2) # border

        # draws card text
        self.draw_text(surface, x, y) # draw one image onto another

    def draw_text(self, surface, x, y):
        font = pygame.font.Font(None, 24)
        lines = self.card_name.split("\n") # handles multi line text
        
        line_height = font.get_height()
        total_text_height = len(lines) * line_height

        # veritcally center the text
        start_y = y + (self.CARD_HEIGHT - total_text_height) // 2

        # render text
        for i, line in enumerate(lines):
            label = font.render(line, True, self.BLACK)
            text_x = x + self.CARD_WIDTH // 2 - label.get_width() // 2
            text_y = start_y + i * line_height
            surface.blit(label, (text_x, text_y)) # draw one image onto another

    def get_card_width(self):
        return self.CARD_WIDTH
    
    def get_card_height(self):
        return self.CARD_HEIGHT
    
    def get_card_spacing(self):
        return self.CARD_SPACING

    def get_card_name(self):
        return self.card_name
    
    def get_card_type(self):
        return self.card_type
    
    def get_value(self):
        if self.value == None:
            raise NotImplementedError
        return self.value
    
    def get_ability_effect(self):
        if not self.isAnAbilityCard():
            raise NotImplementedError
        return self.ability_effect

    def isAnAbilityCard(self):
        return self.ability_effect != None
    
    def isARegularCard(self):
        return self.card_type == "number"
    
    def use(self):
        pass

    def __str__(self):
        """ Python's version of Java's toString (used for debugging) """
        return self.card_name
