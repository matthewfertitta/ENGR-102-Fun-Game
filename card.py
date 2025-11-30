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
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
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
        

    def draw(self, surface, x, y):
        """ Draws a card at a specified position """
        self.rect = pygame.Rect(x, y, self.CARD_WIDTH, self.CARD_HEIGHT)

        # draws card background
        pygame.draw.rect(surface, self.CARD_COLOR, self.rect)
        pygame.draw.rect(surface, self.BORDER_COLOR, self.rect, 2) # border

        # draws card text
        font = pygame.font.Font(None, 24)
        name_text = font.render(self.card_name, True, self.BLACK)
        name_rect = name_text.get_rect(center=(x + self.CARD_WIDTH//2, y + self.CARD_HEIGHT//2))
        surface.blit(name_text, name_rect)

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
        return self.card_type == "regular"
    
    def use(self):
        pass
