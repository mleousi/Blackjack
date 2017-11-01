# Mini-project - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
q = False

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    # create Hand object
    def __init__(self):
        self.hand = []
        
    # return a string representation of a hand
    def __str__(self):
        #hand_str = "Hand contains "
        for i in range(len(self.hand)):
            hand_str = hand_str + (self.hand[i].suit + self.hand[i].rank)
            hand_str = hand_str + " "
        return hand_str
            
    # add a card object to a hand
    def add_card(self, card):
        self.hand.append(card)
            
    # compute the value of the hand, see Blackjack video
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust 
        hand_value = 0
        
        for i in range(len(self.hand)):
            hand_value += VALUES[self.hand[i].rank]
            
            if self.hand[i] == "A":
                if hand_value +10 <=21:
                    hand_value += 10
                else:
                    hand_value += VALUES[self.hand[i].rank]
        return hand_value 
  
    # draw a hand on the canvas, use the draw method for cards   
    def draw(self, canvas, pos):
        pos2 = pos[0]
        for c in range(len(self.hand)):
            self.hand[c].draw(canvas, [pos[0] + pos2, pos[1]])
            pos2 = pos2 + 80
        

# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck=[]
        for suit in range(len(SUITS)):
            for rank in range(len(RANKS)):
                card = Card(SUITS[suit], RANKS[rank])
                self.deck.append(card)	

    # shuffle the deck            
    def shuffle(self):
        random.shuffle(self.deck)	 

    # deal a card object from the deck
    def deal_card(self):
        return self.deck.pop(0)	
    
    # return a string representing the deck
    def __str__(self):
        deck_str = "Deck contains "
        for i in range(len(self.deck)):
            deck_str = deck_str + (self.deck[i].suit + self.deck[i].rank)
            deck_str = deck_str + " "
        return deck_str    	 


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player, dealer, q
    # your code goes here
    player = Hand()
    dealer = Hand()
    deck = Deck()
    in_play = True
    q = False
    
    deck.shuffle()
    i = 0
    while i<2:								#for i in range(2):
        player.add_card(deck.deal_card())	#	player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())	#	dealer.add_card(deck.deal_card())
        i+=1
    #The resulting hands should be printed
    #print "player.__str__()"
    outcome = "Hit or Stand?"
    
def hit():
    global player, deck, outcome, score, in_play, q

    q = False    
    # if the hand is in play, hit the player
    if in_play == True and player.get_value() < 21:
        player.add_card(deck.deal_card())
    # if busted, assign a message to outcome, update in_play and score
    else:
        outcome = "Player busted!"
        in_play = False
        score -= 1
        
def stand():
    global dealer, player, deck, outcome, in_play, score,q
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    #if in_play == False:
    #    outcome = "Player busted!"
    #    in_play = False
    #    score -= 1
    #else:
    while dealer.get_value()<=17:
        dealer.add_card(deck.deal_card())
    if dealer.get_value() > 21:
        outcome = "Dealer busted!Player wins!"
        score += 1
    elif player.get_value() > 21:
        outcome = "Player busted!"
        score -= 1
    else:
        if player.get_value() <= dealer.get_value():
            outcome = "Dealer wins.Player looses."
            score -= 1
        else:
            outcome = "Player wins!"
            score += 1 
    q = True
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    #card = Card("S", "A")
    canvas.draw_text(outcome, (250,400), 30, "Black")
    canvas.draw_text("Score = " + str(score), (350,200), 30, "Black")
    canvas.draw_text("Blackjack", (50,140), 50, "Blue")
    canvas.draw_text("Dealer", (50,200), 30, "Black")
    canvas.draw_text("Player", (50,400), 30, "Black")
    if in_play == True:
        player.draw(canvas,(25,420))
        dealer.draw(canvas, (25,220))
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                          [50 + CARD_BACK_CENTER[0], 220 + CARD_BACK_CENTER[1]] , CARD_SIZE)                
        if q == True:
            canvas.draw_image(card_images, CARD_BACK_CENTER, CARD_BACK_SIZE,
                            [50 + CARD_BACK_CENTER[0], 220 + CARD_BACK_CENTER[1]] , CARD_SIZE)                

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
