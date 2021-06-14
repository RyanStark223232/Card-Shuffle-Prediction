import random
import numpy as np
import matplotlib.pyplot as plt

class Cards:
    def __init__(self, style = 1, times = 1):
        self.cards = list(range(1, 53))
        self.style = style
        self.times = times
        
    def shuffle(self):
        if self.style == 1:
            a = random.randint(1, 51)
            b = random.randint(a+1, 52)
            self.cards = self.cards[a:b+1] + self.cards[:a] + self.cards[b+1:]
        elif self.style == 2:
            new_cards = []
            deck1 = self.cards[0:26]
            deck2 = self.cards[26:52]
            while (len(deck1) and len(deck2)):
                flip = random.randint(0, 1)
                if (flip):
                    new_cards.append(deck1.pop())
                else:
                    new_cards.append(deck2.pop())
            if (len(deck1)):
                new_cards = new_cards+deck1
            else:
                new_cards = new_cards+deck2
            self.cards = new_cards
        elif self.style == 3:
            for i in range(len(self.cards)):
                j = random.randint(i, 51)
                temp = self.cards[i]
                self.cards[i] = self.cards[j]
                self.cards[j] = temp
        elif self.style == 4:
            random.shuffle(self.cards)
        elif self.style == 5:
            coin_flips = []
            for i in range(len(self.cards)):
                coin_flips.append(random.randint(0, 1))                    
            heads = coin_flips.count(1)                    
            left_packet = self.cards[:heads]
            right_packet = self.cards[heads:]                            
            result = []
            for coin in coin_flips:
                if coin == 1:
                    result.append(left_packet[0])
                    left_packet = left_packet[1:]
                else:
                    result.append(right_packet[0])
                    right_packet = right_packet[1:]                            
            self.cards = result
                
    def get_cards(self):
        for _ in range(self.times):
            self.shuffle()
        return self.cards
    
if __name__ == "__main__":    
    epoch = 10000
    freq = np.zeros([52, 52])
    for _ in range(epoch):
        deck = Cards(style = 4, times = 1).get_cards()
        for i in range(len(deck)):
            freq[i][deck[i]-1] += 1
    freq = freq
    plt.imshow(freq, interpolation='nearest')
    plt.show()
    print(np.std(freq))