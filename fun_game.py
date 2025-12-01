# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Matthew Fertitta
#               Raj Khanal
#               Hitesh Vijay
#               Darsh Patel
# Section:      467
# Assignment:   Team lab 13 Game
# Date:         29/11/2025	(dd/mm/yyyy)

import pygame
import random

# ======================== CARD CLASS ========================

class Card:
    """ Information about a single card """

    def __init__(self, card_name: str, card_type: str, value=None, ability_effect=None):
        """
        Constructor for the Card Class
        
        Arguments:
        card_name -- Name of the card
        card_type -- Type of card (number, modifier, ability)
        value -- Point value of card
        ability_effect -- Description of card ability
        """
        self.card_name = card_name
        self.card_type = card_type
        self.value = value
        self.ability_effect = ability_effect
        self.rect = None  # holds position and size

        # colors
        self.BLACK = pygame.Color("black")
        self.WHITE = pygame.Color("white")
        self.CARD_COLOR = (200, 200, 200)

        # card specifications
        self.CARD_WIDTH = 80
        self.CARD_HEIGHT = 120
        self.CARD_SPACING = 10
        self.BORDER_COLOR = self.BLACK
        
    def draw_card_to_screen(self, surface: pygame.Surface, x, y):
        """
        Draws a card at a specified position
        
        Arguments:
        surface -- An instance of pygame's surface class
        x -- X position on screen
        y -- Y position on screen
        """
        self.rect = pygame.Rect(x, y, self.CARD_WIDTH, self.CARD_HEIGHT)

        # draws card background
        pygame.draw.rect(surface, self.CARD_COLOR, self.rect)
        pygame.draw.rect(surface, self.BORDER_COLOR, self.rect, 2)  # border

        # draws card text
        self.draw_text(surface, x, y)

    def draw_text(self, surface, x, y):
        """
        Helper method that handles multiline text and draws to the screen
        
        Arguments:
        surface -- An instance of pygame's surface class
        x -- X position on screen
        y -- Y position on screen
        """
        font = pygame.font.Font(None, 24)
        lines = self.card_name.split("\n")  # handles multi line text
        
        line_height = font.get_height()
        total_text_height = len(lines) * line_height

        # vertically center the text
        start_y = y + (self.CARD_HEIGHT - total_text_height) // 2

        # render text
        for i, line in enumerate(lines):
            label = font.render(line, True, self.BLACK)
            text_x = x + self.CARD_WIDTH // 2 - label.get_width() // 2
            text_y = start_y + i * line_height
            surface.blit(label, (text_x, text_y))

    def get_card_width(self):
        """ Getter method for CARD_WIDTH """
        return self.CARD_WIDTH
    
    def get_card_height(self):
        """ Getter method for CARD_HEIGHT """
        return self.CARD_HEIGHT
    
    def get_card_spacing(self):
        """ Getter method for CARD_SPACING """
        return self.CARD_SPACING

    def get_card_name(self):
        """ Getter method for card_name """
        return self.card_name
    
    def get_card_type(self):
        """ Getter method for card_type """
        return self.card_type
    
    def get_value(self):
        """ 
        Getter method for card value 
        
        Raises:
        NotImplementedError -- If value is None
        """
        if self.value == None:
            raise NotImplementedError
        return self.value
    
    def get_ability_effect(self):
        """ 
        Returns the description of an ability card 
        
        Raises:
        NotImplementedError -- If card is not an ability card
        """
        if not self.isAnAbilityCard():
            raise NotImplementedError
        return self.ability_effect

    def isAnAbilityCard(self):
        """ Boolean for checking if a card is an ability card or not """
        return self.ability_effect != None
    
    def isARegularCard(self):
        """ Boolean for checking if a card is a regular number card or not """
        return self.card_type == "number"

    def __str__(self):
        """ Python's version of Java's toString (used for debugging) """
        return self.card_name


# ======================== DECK CLASS ========================

class Deck:
    """ A class that holds the data for the deck """

    def __init__(self):
        """ Constructor for the Deck Class """
        # int number to letter number dict
        num_words = {
            0: "Zero",
            1: "One",
            2: "Two",
            3: "Three",
            4: "Four",
            5: "Five",
            6: "Six",
            7: "Seven",
            8: "Eight",
            9: "Nine",
            10: "Ten",
            11: "Eleven",
            12: "Twelve",
        }
        # initialize deck
        self.deck = [Card(num_words[0], "number", 0)]
        # generate number cards
        for num in range(13):
            for i in range(num):
                self.deck.append(Card(num_words[num], "number", num))
        # add score modifiers
        self.deck.append(Card("+2", "modifier", 2))
        self.deck.append(Card("+4", "modifier", 4))
        self.deck.append(Card("+6", "modifier", 6))
        self.deck.append(Card("+8", "modifier", 8))
        self.deck.append(Card("+10", "modifier", 10))
        self.deck.append(Card("x2", "modifier", 2))
        # add action cards
        for i in range(3):
            self.deck.append(Card("Freeze", "ability", 0, "Skips turn of affected player"))
            self.deck.append(Card("Flip\nThree", "ability", 0, "Draws 3 cards on affected player, if you bust early stop"))
            self.deck.append(Card("Second\nChance", "ability", 0, "Saves you when you bust"))

        # shuffle list
        random.shuffle(self.deck)

    def shuffle_deck(self):
        """ Shuffles the deck """
        random.shuffle(self.deck)

    def get_deck(self):
        """ Returns the deck list """
        return self.deck
    
    def set_deck(self, deck):
        """
        Sets deck to a new list
        
        Arguments:
        deck -- A list of Card objects
        """
        self.deck = deck

    def add_card(self, card: Card):
        """ 
        Adds a card back into the deck 
        
        Arguments:
        card -- An instance of the Card class
        """
        self.deck.append(card)

    def draw_card(self):
        """ 
        Takes a card out of the deck, reshuffles if empty
        
        Returns:
        Card -- A Card object from the top of the deck
        """
        if not len(self.deck) == 0:
            return self.deck.pop()
        else:
            self.__init__()
            return self.deck.pop()


# ======================== PLAYER CLASS ========================

class Player():
    """ Represents a player in the game """
    
    def __init__(self, player_num):
        """
        Constructor for Player Class
        
        Arguments:
        player_num -- The player's number
        """
        self.hand = []
        self.points = 0
        self.total_score = 0  # cumulative score across rounds
        self.hand_count = len(self.hand)
        self.InGame = True
        self.player_num = player_num
        self.default_player_locations = {1: "bottom", 2: "top"}
        self.standing = False  # track if player is standing this round
        self.busted = False    # track if player busted this round
        self.has_second_chance = False  # track if player has second chance card

    def draw_cards_on_screen(self, surface: pygame.Surface, SCREEN_WIDTH, SCREEN_HEIGHT, loc=None):
        """
        Draws cards at a location on the screen
        
        Arguments:
        surface -- An instance of pygame's Surface class
        SCREEN_WIDTH -- The screen width of the pygame window
        SCREEN_HEIGHT -- The screen height of the pygame window
        loc -- Which side of the screen to draw the cards on (optional)
        """
        # handle empty hands
        if not self.hand:
            return
        
        # use player num to set loc
        loc = self.default_player_locations[self.get_player_num()]
        # use first card in player's hand as reference
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
        """
        Draws a card from the given deck and adds it to the player's hand
        
        Arguments:
        deck -- An instance of the Deck class
        
        Returns:
        Card/str/bool -- The drawn card, "second_chance_used" string, or False if busted
        """
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
        """ Getter method for player_num """
        return self.player_num

    def get_hand_size(self):
        """ Getter method for length of hand """
        return len(self.hand)
    
    def get_number_card_count(self):
        """ 
        Getter method for the count of only number cards 
        
        Returns:
        int -- Count of number cards in hand
        """
        count = 0
        for card in self.hand:
            if card.isARegularCard():
                count += 1
        return count
    
    def get_hand(self):
        """ Getter method for the list of the player's hand """
        return self.hand
    
    def set_hand(self, hand: list):
        """
        Setter method for the hand list
        
        Arguments:
        hand -- A list of Card objects representing the player's hand
        """
        self.hand = hand

    def reset_hand(self):
        """ Resets the player's hand and status, called after every round """
        self.set_hand([])
        self.standing = False
        self.busted = False
        self.has_second_chance = False
    
    def set_standing(self, value: bool):
        """
        Setter method to set the player's standing status
        
        Arguments:
        value -- True or False value representing if player is standing
        """
        self.standing = value
    
    def is_standing(self):
        """ Boolean for checking if the player is standing """
        return self.standing
    
    def is_busted(self):
        """ Boolean for checking if the player is busted """
        return self.busted
    
    def is_active(self):
        """ 
        Returns True if player can still take actions this round 
        
        Returns:
        bool -- True if player is not standing and not busted
        """
        return not self.standing and not self.busted
    
    def calculate_round_score(self):
        """ 
        Calculates score for this round based on hand 
        
        Returns:
        int -- The calculated score for the round
        """
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
        """
        Adds points to the cumulative total score
        
        Arguments:
        points -- Point value to add to total score
        """
        self.total_score += points
    
    def get_total_score(self):
        """ Getter method for the total score """
        return self.total_score


# ======================== CARDGAME CLASS ========================

class CardGame:
    """ Main class that runs everything """
    
    def __init__(self):
        """ Constructor for the CardGame Class """
        # initialize pygame
        pygame.init()
        # set window size
        screen_size = (800, 600)
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        # set window name
        pygame.display.set_caption("Flip 7")

        # set framerate & time
        self.time = pygame.time
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        # initialize the deck
        self.deck = Deck()

        # initialize font
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        # colors
        self.BLACK = pygame.Color("black")
        self.WHITE = pygame.Color("white")
        self.RED = pygame.Color("red")
        self.GREEN = pygame.Color("green")

        # game log
        self.gamelog = "=== FLIP 7 GAME LOG ===\n\n"
        
        # game state
        self.paused = False

    def log(self, message):
        """ 
        Add a message to the game log 
        
        Arguments:
        message -- String message to add to the log
        """
        self.gamelog += message + "\n"
        print(message)  # Also print to console for debugging
    
    def show_rules_screen(self):
        """
        Display rules before game starts
        
        Returns:
        bool -- True if player started game, False if quit
        """
        self.screen.fill(self.WHITE)
        title = self.font.render("=== FLIP 7 RULES ===", True, self.BLACK)
        title_rect = title.get_rect(center=(self.SCREEN_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)
        
        rules = [
            "GOAL: Be first to 7 number cards OR highest score after 3 rounds",
            "",
            "CONTROLS:",
            "  D = Draw Card",
            "  S = Stand (lock in for round)",
            "  ESC = Options Menu",
            "",
            "BUST: Drawing a duplicate number card ends your round",
            "",
            "ABILITY CARDS:",
            "  Freeze - Forces opponent to stand",
            "  Flip Three - Opponent draws 3 cards",
            "  Second Chance - Saves you from one bust",
            "",
            "SCORING: (Number cards) x (Multipliers) + (Additions)",
            "Busted players get 0 points for that round",
            "",
            "Press SPACE to start"
        ]
        
        y = 130
        for line in rules:
            text = self.small_font.render(line, True, self.BLACK)
            rect = text.get_rect(center=(self.SCREEN_WIDTH // 2, y))
            self.screen.blit(text, rect)
            y += 25
        
        pygame.display.update()
        
        # Wait for space
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False
                elif event.type == pygame.QUIT:
                    return False
        return True
    
    def show_options_menu(self, players):
        """
        Display options menu during game
        
        Arguments:
        players -- List of Player objects
        
        Returns:
        str -- "resume" to continue game or "quit" to exit
        """
        menu_active = True
        selected_option = 0
        options = ["Resume Game", "View Rules", "View Scores", "Quit Game"]
        
        while menu_active:
            self.screen.fill(self.WHITE)
            
            # Title
            title = self.font.render("=== OPTIONS MENU ===", True, self.BLACK)
            title_rect = title.get_rect(center=(self.SCREEN_WIDTH // 2, 100))
            self.screen.blit(title, title_rect)
            
            # Menu options
            y = 200
            for i, option in enumerate(options):
                if i == selected_option:
                    color = self.GREEN
                    text = f"> {option} <"
                else:
                    color = self.BLACK
                    text = f"  {option}"
                
                option_text = self.font.render(text, True, color)
                rect = option_text.get_rect(center=(self.SCREEN_WIDTH // 2, y))
                self.screen.blit(option_text, rect)
                y += 50
            
            # Instructions
            instructions = self.small_font.render("Use UP/DOWN arrows, ENTER to select, ESC to resume", True, self.BLACK)
            inst_rect = instructions.get_rect(center=(self.SCREEN_WIDTH // 2, 450))
            self.screen.blit(instructions, inst_rect)
            
            pygame.display.update()
            
            # Handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:  # Resume Game
                            return "resume"
                        elif selected_option == 1:  # View Rules
                            self.show_rules_display()
                        elif selected_option == 2:  # View Scores
                            self.show_scores_display(players)
                        elif selected_option == 3:  # Quit Game
                            return "quit"
                    elif event.key == pygame.K_ESCAPE:
                        return "resume"
        
        return "resume"
    
    def show_rules_display(self):
        """ Display rules from options menu """
        self.screen.fill(self.WHITE)
        
        title = self.font.render("=== GAME RULES ===", True, self.BLACK)
        title_rect = title.get_rect(center=(self.SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)
        
        rules = [
            "OBJECTIVE: Get 7 number cards first OR highest score after 3 rounds",
            "",
            "GAMEPLAY:",
            "- Draw cards on your turn (D key) or Stand (S key)",
            "- Drawing a duplicate number card = BUST (0 points for round)",
            "- Number cards count toward the 7-card win",
            "- Ability and modifier cards don't count toward 7",
            "",
            "ABILITY CARDS (auto-activate):",
            "  Freeze: Forces opponent to stand for the round",
            "  Flip Three: Opponent must draw 3 cards",
            "  Second Chance: Held until you bust, then saves you",
            "",
            "SCORING:",
            "- Sum all number card values",
            "- Multiply by x2 cards (if any)",
            "- Add +2, +4, +6, +8, +10 modifiers",
            "",
            "Press ESC to return"
        ]
        
        y = 90
        for line in rules:
            text = self.small_font.render(line, True, self.BLACK)
            rect = text.get_rect(center=(self.SCREEN_WIDTH // 2, y))
            self.screen.blit(text, rect)
            y += 23
        
        pygame.display.update()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False
                elif event.type == pygame.QUIT:
                    waiting = False
    
    def show_scores_display(self, players):
        """
        Display current scores from options menu
        
        Arguments:
        players -- List of Player objects
        """
        self.screen.fill(self.WHITE)
        
        title = self.font.render("=== CURRENT SCORES ===", True, self.BLACK)
        title_rect = title.get_rect(center=(self.SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        y = 200
        for p in players:
            score_text = f"Player {p.get_player_num()}: {p.get_total_score()} points"
            status = ""
            if p.is_busted():
                status = " (BUSTED)"
            elif p.is_standing():
                status = " (STANDING)"
            elif p.has_second_chance:
                status = " (Second Chance Active)"
            
            text = self.font.render(score_text + status, True, self.BLACK)
            rect = text.get_rect(center=(self.SCREEN_WIDTH // 2, y))
            self.screen.blit(text, rect)
            
            # Show current hand
            if p.get_hand():
                hand_str = ", ".join([c.get_card_name() for c in p.get_hand()])
                hand_text = self.small_font.render(f"Hand: {hand_str}", True, self.BLACK)
                hand_rect = hand_text.get_rect(center=(self.SCREEN_WIDTH // 2, y + 25))
                self.screen.blit(hand_text, hand_rect)
                y += 50
            
            y += 60
        
        instructions = self.small_font.render("Press ESC to return", True, self.BLACK)
        inst_rect = instructions.get_rect(center=(self.SCREEN_WIDTH // 2, 500))
        self.screen.blit(instructions, inst_rect)
        
        pygame.display.update()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False
                elif event.type == pygame.QUIT:
                    waiting = False

    def deal_cards(self, players: list):
        """ 
        Deals cards to all players at the start of each round 
        
        Arguments:
        players -- List of Player objects
        """
        for p in players:
            card = self.deck.draw_card()
            while not card.isARegularCard():
                self.deck.add_card(card)  # add card back into deck
                self.deck.shuffle_deck()
                card = self.deck.draw_card()

            p.set_hand([card])
            self.log(f"  Player {p.get_player_num()} dealt: {card.get_card_name()}")
    
    def display_action(self, action):
        """ 
        Displays text to the action bar in the middle of the screen 
        
        Arguments:
        action -- String message to display
        """
        action_bar = self.font.render(action, True, self.BLACK)
        rect = action_bar.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self.screen.blit(action_bar, rect)
    
    def display_scores(self, players):
        """ 
        Display player names and scores in corners 
        
        Arguments:
        players -- List of Player objects
        """
        for p in players:
            if p.get_player_num() == 1:
                # Player 1 on bottom
                name_label = self.small_font.render(f"Player {p.get_player_num()}", True, self.BLACK)
                score_label = self.small_font.render(f"Score: {p.get_total_score()}", True, self.BLACK)
                self.screen.blit(name_label, (10, self.SCREEN_HEIGHT - 40))
                self.screen.blit(score_label, (self.SCREEN_WIDTH - 100, self.SCREEN_HEIGHT - 40))
            elif p.get_player_num() == 2:
                # Player 2 on top
                name_label = self.small_font.render(f"Player {p.get_player_num()}", True, self.BLACK)
                score_label = self.small_font.render(f"Score: {p.get_total_score()}", True, self.BLACK)
                self.screen.blit(name_label, (10, 10))
                self.screen.blit(score_label, (self.SCREEN_WIDTH - 100, 10))
    
    def display_player_status(self, player: Player):
        """ 
        Display if player is standing, busted, or has second chance 
        
        Arguments:
        player -- A Player object
        """
        status_text = ""
        color = self.BLACK
        
        if player.is_busted():
            status_text = "BUSTED"
            color = self.RED
        elif player.is_standing():
            status_text = "STANDING"
            color = self.GREEN
        elif player.has_second_chance:
            status_text = "Second Chance Active"
            color = self.GREEN
        
        if status_text:
            status_label = self.small_font.render(status_text, True, color)
            
            if player.get_player_num() == 1:
                # Bottom player
                rect = status_label.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 160))
            else:
                # Top player
                rect = status_label.get_rect(center=(self.SCREEN_WIDTH // 2, 160))
            
            self.screen.blit(status_label, rect)
    
    def get_other_player(self, players, current_player):
        """ 
        Returns the other player 
        
        Arguments:
        players -- List of Player objects
        current_player -- The current Player object
        
        Returns:
        Player -- The other player, or None if not found
        """
        for p in players:
            if p.get_player_num() != current_player.get_player_num():
                return p
        return None
    
    def handle_ability_card(self, card, current_player, other_player):
        """ 
        Handles the automatic use of ability cards 
        
        Arguments:
        card -- The ability Card object
        current_player -- The Player who drew the card
        other_player -- The other Player affected by the card
        
        Returns:
        str -- Message describing what happened
        """
        card_name = card.get_card_name()
        
        if card_name == "Freeze":
            # Freeze the other player (force them to stand)
            other_player.set_standing(True)
            message = f"Player {current_player.get_player_num()} used Freeze! Player {other_player.get_player_num()} is frozen!"
            self.log(f"  ACTION: {message}")
            return message
        
        elif card_name == "Flip\nThree":
            # Force other player to draw 3 cards
            message = f"Player {current_player.get_player_num()} used Flip Three! Player {other_player.get_player_num()} draws 3 cards!"
            self.log(f"  ACTION: {message}")
            cards_drawn = 0
            for i in range(3):
                result = other_player.draw_card(self.deck)
                if result == False:
                    # Other player busted
                    bust_msg = f"Player {other_player.get_player_num()} busted on card {i+1}!"
                    message += f" {bust_msg}"
                    self.log(f"    {bust_msg}")
                    break
                elif result == "second_chance_used":
                    sc_msg = f"Player {other_player.get_player_num()} used Second Chance on card {i+1}!"
                    message += f" {sc_msg}"
                    self.log(f"    {sc_msg}")
                    continue
                else:
                    if hasattr(result, 'get_card_name'):
                        self.log(f"    Player {other_player.get_player_num()} drew: {result.get_card_name()}")
                cards_drawn += 1
            return message
        
        return ""
    
    def check_round_end(self, players):
        """ 
        Check if round should end 
        
        Arguments:
        players -- List of Player objects
        
        Returns:
        tuple -- (bool, str) True/False for round ended, and end message
        """
        # Check if any player has 7 number cards
        for p in players:
            if p.get_number_card_count() >= 7:
                return True, f"Player {p.get_player_num()} wins with 7 cards!"
        
        # Check if all players are either standing or busted
        all_inactive = True
        for p in players:
            if p.is_active():
                all_inactive = False
                break
        
        if all_inactive:
            return True, "All players standing or busted!"
        
        return False, ""
    
    def end_round(self, players, round_number):
        """ 
        Handle end of round scoring 
        
        Arguments:
        players -- List of Player objects
        round_number -- Current round number
        """
        self.log(f"\n--- ROUND {round_number} RESULTS ---")
        
        for p in players:
            round_score = p.calculate_round_score()
            p.add_to_total_score(round_score)
            
            # Log hand details
            hand_str = ", ".join([c.get_card_name() for c in p.get_hand()])
            status = "BUSTED" if p.is_busted() else "STANDING" if p.is_standing() else "ACTIVE"
            self.log(f"Player {p.get_player_num()} ({status}):")
            self.log(f"  Hand: [{hand_str}]")
            self.log(f"  Number cards: {p.get_number_card_count()}")
            self.log(f"  Round score: {round_score} points")
            self.log(f"  Total score: {p.get_total_score()} points")
        
        # Display round results on screen
        self.screen.fill(self.WHITE)
        y_pos = 200
        for p in players:
            round_score = p.calculate_round_score()
            result_text = f"Player {p.get_player_num()}: {round_score} points this round (Total: {p.get_total_score()})"
            result_label = self.font.render(result_text, True, self.BLACK)
            rect = result_label.get_rect(center=(self.SCREEN_WIDTH // 2, y_pos))
            self.screen.blit(result_label, rect)
            y_pos += 40
        
        pygame.display.update()
        self.time.wait(3000)
     
    def main(self):
        """ 
        Main Function 
        
        Handles all processes: game logging, menus, game logic, etc
        """
        if __name__ == "__main__":

            ############## INITIALIZATION #####################

            self.log("GAME START")
            self.log("Number of players: 2")
            self.log("Number of rounds: 3")
            self.log("")

            # initialize players
            num_players = 2
            players = []
            for i in range(num_players):
                player_num = i + 1
                players.append(Player(player_num))

            # set round num
            max_rounds = 3
            round_number = 1
            
            # Show rules screen at start
            if not self.show_rules_screen():
                self.log("\nGAME ABORTED BY USER")
                return

            # initialize screen
            self.screen.fill(self.WHITE)
            
            # deal initial cards
            self.log(f"=== ROUND {round_number} START ===")
            self.log("Dealing initial cards:")
            self.deal_cards(players)
            
            # initial draw players
            for p in players:
                p.draw_cards_on_screen(self.screen, 
                                       self.SCREEN_WIDTH, 
                                       self.SCREEN_HEIGHT)
            
            # display initial scores
            self.display_scores(players)
            # initial screen update
            pygame.display.update()

            ################ MAIN GAME LOOP ####################
            
            current_player_index = 0
            waiting = True
            running = True
            action_message = ""
            
            while running:
                # frame timing
                self.clock.tick(self.FPS)
                
                # get current player
                current_player = players[current_player_index]
                
                # skip if current player is not active
                if not current_player.is_active() and waiting:
                    # move to next player
                    current_player_index += 1
                    if current_player_index >= len(players):
                        current_player_index = 0
                    continue
                
                # event handler
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting = False
                        self.log("\nGAME ABORTED BY USER")
                    # check if key is pressed
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            # Open options menu
                            menu_result = self.show_options_menu(players)
                            if menu_result == "quit":
                                running = False
                                waiting = False
                                self.log("\nGAME QUIT FROM OPTIONS MENU")
                        elif waiting and current_player.is_active():
                            if event.key == pygame.K_d:
                                drew_card = True
                                waiting = False
                                self.log(f"\nPlayer {current_player.get_player_num()}'s turn: DRAW")
                            elif event.key == pygame.K_s:
                                # player stands
                                current_player.set_standing(True)
                                action_message = f"Player {current_player.get_player_num()} stands!"
                                self.log(f"\nPlayer {current_player.get_player_num()}'s turn: STAND")
                                waiting = False
                                drew_card = False
                
                ########## GAME LOGIC ####################
                if not waiting:
                    
                    if drew_card:
                        result = current_player.draw_card(self.deck)
                        other_player = self.get_other_player(players, current_player)
                        
                        # handle ability cards
                        if result and hasattr(result, 'isAnAbilityCard') and result.isAnAbilityCard():
                            if result.get_card_name() == "Second\nChance":
                                action_message = f"Player {current_player.get_player_num()} drew Second Chance!"
                                self.log(f"  Drew: Second Chance (saved for later)")
                            else:
                                action_message = self.handle_ability_card(result, current_player, other_player)
                        elif result == "second_chance_used":
                            action_message = f"Player {current_player.get_player_num()} used Second Chance and survived!"
                            self.log(f"  BUST AVOIDED: Used Second Chance")
                        elif result == False:
                            action_message = f"Player {current_player.get_player_num()} Busted!"
                            self.log(f"  BUSTED: Drew duplicate card")
                        elif result and hasattr(result, 'get_card_name'):
                            # Regular or modifier card
                            self.log(f"  Drew: {result.get_card_name()}")
                            self.log(f"  Current number cards: {current_player.get_number_card_count()}/7")
                    
                    # check for round end
                    round_ended, end_message = self.check_round_end(players)
                    
                    if round_ended:
                        self.log(f"\nROUND END: {end_message}")
                        
                        # display end message
                        self.screen.fill(self.WHITE)
                        self.display_action(end_message)
                        for p in players:
                            p.draw_cards_on_screen(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                        self.display_scores(players)
                        pygame.display.update()
                        self.time.wait(2000)
                        
                        # end round and calculate scores
                        self.end_round(players, round_number)
                        
                        # check if game is over
                        if round_number >= max_rounds:
                            # display final winner
                            self.screen.fill(self.WHITE)
                            winner = max(players, key=lambda p: p.get_total_score())
                            winner_text = f"Game Over! Player {winner.get_player_num()} wins with {winner.get_total_score()} points!"
                            winner_label = self.font.render(winner_text, True, self.BLACK)
                            rect = winner_label.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
                            self.screen.blit(winner_label, rect)
                            
                            # Log final results
                            self.log("\n" + "="*50)
                            self.log("GAME OVER - FINAL RESULTS")
                            self.log("="*50)
                            for p in players:
                                self.log(f"Player {p.get_player_num()}: {p.get_total_score()} points")
                            self.log(f"\nWINNER: Player {winner.get_player_num()} with {winner.get_total_score()} points!")
                            self.log("="*50)
                            
                            pygame.display.update()
                            self.time.wait(5000)
                            running = False
                            continue
                        
                        # start new round
                        round_number += 1
                        self.log(f"\n=== ROUND {round_number} START ===")
                        self.screen.fill(self.WHITE)
                        self.display_action(f"Round: {round_number}")
                        pygame.display.update()
                        self.time.wait(1500)
                        self.deck = Deck()
                        for p in players:
                            p.reset_hand()
                        self.log("Dealing initial cards:")
                        self.deal_cards(players)
                        current_player_index = 0
                        action_message = ""
                        waiting = True
                        continue

                    # move to the next player
                    current_player_index += 1
                    if current_player_index >= len(players):
                        current_player_index = 0
                    
                    # next turn is ready
                    waiting = True

                # draw screen
                self.screen.fill(self.WHITE)

                for p in players:
                    p.draw_cards_on_screen(
                        self.screen,
                        self.SCREEN_WIDTH,
                        self.SCREEN_HEIGHT
                    )
                    self.display_player_status(p)

                self.display_scores(players)
                
                # display current turn
                if current_player.is_active():
                    turn_text = f"Player {current_player.get_player_num()}'s Turn (D=Draw, S=Stand)"
                else:
                    turn_text = f"Player {current_player.get_player_num()} is inactive"
                
                self.display_action(turn_text)
                
                # display action message if any
                if action_message:
                    msg_label = self.small_font.render(action_message, True, self.BLACK)
                    rect = msg_label.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 30))
                    self.screen.blit(msg_label, rect)
                
                pygame.display.update()

            # Write game log to file
            try:
                with open("GameLog.txt", "w") as gameLogFile:
                    gameLogFile.write(self.gamelog)
                print("\nGame log saved to GameLog.txt")
            except IOError as e:
                print(f"\nError saving game log: {e}")
                print("Game log could not be saved to file.")
            except Exception as e:
                print(f"\nUnexpected error while saving game log: {e}")


# ======================== MAIN EXECUTION ========================

if __name__ == "__main__":
    game = CardGame()
    game.main()
    pygame.quit()