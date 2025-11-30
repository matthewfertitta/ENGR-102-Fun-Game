import random, card

class Deck:
    """ A class that holds the data for the deck """

    def __init__(self):
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
        # initalize deck
        self.deck = [card.Card("Zero", "number", 0)]
        # generate number cards
        for i in range(12):
            for num in range(i):
                self.deck.append(card.Card(num_words[num], "number", num))
        # add score modifiers
        self.deck.append([card.Card("+2", "modifier", 2),
                          card.Card("+4", "modifier", 4),
                          card.Card("+6", "modifier", 6),
                          card.Card("+8", "modifier", 8),
                          card.Card("+10", "modifier", 10),
                          card.Card("x2", "modifier", 2)])
        # add action cards
        for i in range(3):
            self.deck.append(card.Card("Freeze", "ability", 0, "Skips turn of affected player"))
            self.deck.append(card.Card("Flip\nThree", "ability", 0, "Draws 3 cards on affected player, if you bust early stop"))
            self.deck.append(card.Card("Second\nChance", "ability", 0, "Saves you when you bust"))
        # shuffle list
        random.shuffle(self.deck)

    def shuffle_deck(self):
        """ Shuffles Deck """
        random.shuffle(self.deck)

    def get_deck(self):
        """ Returns the deck """
        return self.deck
    
    def set_deck(self, deck):
        """ Sets deck to a new list """
        self.deck = deck

    def draw_card(self):
        """ Takes a card out of the deck """
        return self.deck.pop()