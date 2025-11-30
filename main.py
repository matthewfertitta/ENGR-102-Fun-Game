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

        # set framerate
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        # initialze the deck
        self.deck = Deck()

    def deal_cards(self, players: list):
        for p in players:
            p: Player # define p of type Player
            p.draw_card(self.deck)
    
    def main(self):
        if __name__ == "__main__":
            # initalize players
            num_players = 1
            players = []
            for i in range(num_players):
                player_num = i + 1
                players.append(Player(player_num))

            # set round num
            round_number = 0

            # intialize screen
            self.screen.fill((255, 255, 255))
            # deal inital cards
            self.deal_cards(players)
            # intial draw players
            for p in players:
                p: Player # p is of typer Player
                p.draw_cards_on_screen(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, loc="bottom")
            # intial screen update
            pygame.display.update()

            running = True
            while running:
                # loop through players
                for i, current_player in enumerate(players):
                    current_player: Player # defines player as the player class
                    # refresh screen
                    self.screen.fill((255, 255, 255))



                    current_player.draw_cards_on_screen(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, loc="bottom")

                    waiting = True
                    # waiting event handler for each player
                    while waiting:
                        for event in pygame.event.get():
                            key = pygame.key.get_pressed()
                            if event.type == pygame.QUIT:
                                running = False
                                waiting = False
                            if event.type == pygame.KEYDOWN:
                                if key[pygame.K_d] == True:
                                    current_player.draw_card(self.deck)
                                    waiting = False



                    # how to recognize key presses
                    #key = pygame.key.get_pressed()
                    #if key[pygame.K_a] == True:
                    #    rectangle.move_ip(-1, 0)
                    #elif key[pygame.K_d] == True:
                    #    rectangle.move_ip(1, 0)

                    # auto win condition
                    if current_player.get_hand_size() == 7:
                        print(f"Player {i + 1} wins!") # TODO: print to gui instead of console
                        running = False
                        break

                    # update display
                    pygame.display.update()
                    self.clock.tick(self.FPS)


                round_number += 1

game = CardGame()
game.main()

pygame.quit()