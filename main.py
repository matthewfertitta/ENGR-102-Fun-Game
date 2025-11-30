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
from deck import Deck
from player import Player

class CardGame:
    """ Main class that runs everything """
    
    def __init__(self):
        # initalize pygame
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
        
        # initialze the deck
        self.deck = Deck()

        # initalize font
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        # colors
        self.BLACK = pygame.Color("black")
        self.WHITE = pygame.Color("white")
        self.RED = pygame.Color("red")
        self.GREEN = pygame.Color("green")

    def deal_cards(self, players: list):
        for p in players:
            p: Player # define p of type Player
            card = self.deck.draw_card()
            while not card.isARegularCard():
                self.deck.add_card(card) # add card back into deck
                self.deck.shuffle_deck()
                card = self.deck.draw_card()

            p.set_hand([card])
    
    def display_action(self, action):
        action_bar = self.font.render(
            action,
            True,
            self.BLACK
        )
        rect = action_bar.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self.screen.blit(action_bar, rect)
    
    def display_scores(self, players):
        """ Display player names and scores in corners """
        for p in players:
            p: Player
            
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
        """ Display if player is standing, busted, or has second chance """
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
        """ Returns the other player """
        for p in players:
            if p.get_player_num() != current_player.get_player_num():
                return p
        return None
    
    def handle_ability_card(self, card, current_player, other_player):
        """ Handles the automatic use of ability cards """
        card_name = card.get_card_name()
        
        if card_name == "Freeze":
            # Freeze the other player (force them to stand)
            other_player.set_standing(True)
            return f"Player {current_player.get_player_num()} used Freeze! Player {other_player.get_player_num()} is frozen!"
        
        elif card_name == "Flip\nThree":
            # Force other player to draw 3 cards
            message = f"Player {current_player.get_player_num()} used Flip Three! Player {other_player.get_player_num()} draws 3 cards!"
            cards_drawn = 0
            for i in range(3):
                result = other_player.draw_card(self.deck)
                if result == False:
                    # Other player busted
                    message += f" Player {other_player.get_player_num()} busted on card {i+1}!"
                    break
                elif result == "second_chance_used":
                    message += f" Player {other_player.get_player_num()} used Second Chance on card {i+1}!"
                    continue
                cards_drawn += 1
            return message
        
        return ""
    
    def check_round_end(self, players):
        """ Check if round should end """
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
        """ Handle end of round scoring """
        for p in players:
            round_score = p.calculate_round_score()
            p.add_to_total_score(round_score)
        
        # Display round results
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
        if __name__ == "__main__":

            ############## INITALIZATION #####################

            # initalize players
            num_players = 2
            players = []
            for i in range(num_players):
                player_num = i + 1
                players.append(Player(player_num))

            # set round num
            max_rounds = 3
            round_number = 1

            # intialize screen
            self.screen.fill(self.WHITE)
            # deal inital cards
            self.deal_cards(players)
            # intial draw players
            for p in players:
                p: Player # p is of typer Player
                p.draw_cards_on_screen(self.screen, 
                                       self.SCREEN_WIDTH, 
                                       self.SCREEN_HEIGHT)
            
            # display initial scores
            self.display_scores(players)
            # intial screen update
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
                    # check if key is pressed
                    elif event.type == pygame.KEYDOWN and waiting and current_player.is_active():
                        if event.key == pygame.K_d:
                            drew_card = True
                            waiting = False
                        elif event.key == pygame.K_s:
                            # player stands
                            current_player.set_standing(True)
                            action_message = f"Player {current_player.get_player_num()} stands!"
                            waiting = False
                            drew_card = False
                
                ########## GAME LOGIC ####################
                if not waiting:
                    
                    if drew_card:
                        result = current_player.draw_card(self.deck)
                        other_player = self.get_other_player(players, current_player)
                        
                        # handle ability cards
                        if result and hasattr(result, 'isAnAbilityCard') and result.isAnAbilityCard():
                            if result.get_card_name() != "Second\nChance":
                                action_message = self.handle_ability_card(result, current_player, other_player)
                        elif result == "second_chance_used":
                            action_message = f"Player {current_player.get_player_num()} used Second Chance and survived!"
                        elif result == False:
                            action_message = f"Player {current_player.get_player_num()} Busted!"
                    
                    # check for round end
                    round_ended, end_message = self.check_round_end(players)
                    
                    if round_ended:
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
                            pygame.display.update()
                            self.time.wait(5000)
                            running = False
                            continue
                        
                        # start new round
                        round_number += 1
                        self.screen.fill(self.WHITE)
                        self.display_action(f"Round: {round_number}")
                        pygame.display.update()
                        self.time.wait(1500)
                        self.deck = Deck()
                        for p in players:
                            p.reset_hand()
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

game = CardGame()
game.main()
pygame.quit()