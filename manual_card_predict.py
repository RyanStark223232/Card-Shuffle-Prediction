from card_shuffle import Cards
import matplotlib.pyplot as plt
import random
import math
import numpy as np

class Agent:
    def __init__(self, style, time, target):
        self.style = style
        self.time = time
        self.target = target
        
    def guess (self):
        correct = 0
        guesses = []
        if self.style == 1:
            cards = list(range(1, 53))
            step = 0
            guess = 0
            while cards:
                if step == 0: guess = 1
                else:
                    i = 0
                    while i < len(cards):
                        if cards[i] > self.target[step - 1]:
                            guess = cards[i]
                            break
                        i += 1
                    if i == len(cards): guess = random.choice(cards)                        
                if guess == self.target[step]: correct += 1
                guesses.append(guess)
                cards.remove(self.target[step])
                step += 1
        elif self.style == 5:
            cards = list(range(1, 53))
            inc_seq = []
            step = 0
            guess = 0
            while cards:
                valid_inc_seq = []
                for i in range(len(inc_seq)):
                    if (inc_seq[i]+1) < 53 and (inc_seq[i]+1) in cards:
                        valid_inc_seq.append(inc_seq[i]+1)
                if len(valid_inc_seq) == 0:
                    guess = cards[0]
                else: 
                    guess = random.choice(valid_inc_seq)
                if guess == self.target[step]:
                    correct += 1
                if self.target[step]-1 in inc_seq:
                    inc_seq_ind = inc_seq.index(self.target[step]-1)
                    inc_seq[inc_seq_ind] = self.target[step]
                else:
                    inc_seq.append(self.target[step])
                guesses.append(guess)
                cards.remove(self.target[step])
                step += 1
        return correct, guesses
        
if __name__ == "__main__":
    style = 5 #5: riffle shuffle 1: overhand shuffle
    max_times = 20
    iters = 100000
    win_times = []
    for times in range(10, max_times+1):
        total_win = 0
        doc_cards = []
        doc_guess = []
        for _ in range(iters):
            cards = Cards(5, times).get_cards()
            agent = Agent(5, times, cards)
            num_correct, guesses = agent.guess()
            doc_cards.append(cards)
            doc_guess.append(guesses)
            total_win += num_correct
        print("Number of Correct for {} shuffle:".format(times), total_win/iters)
        win_times.append(total_win/iters)
        doc_cards = np.array(doc_cards)
        doc_guess = np.array(doc_guess)
        doc_win = np.equal(doc_cards, doc_guess)
        doc_avg = np.average(doc_win, axis = 0)
        doc_avg_ai = np.array([0.0395, 0.0362, 0.0404, 0.0418, 0.038 , 0.0389, 0.0432, 0.0448,
                               0.0442, 0.0466, 0.0472, 0.0445, 0.0486, 0.0534, 0.0503, 0.0507,
                               0.0494, 0.0513, 0.0599, 0.0601, 0.0568, 0.0611, 0.0657, 0.0666,
                               0.0678, 0.0696, 0.0706, 0.071 , 0.0733, 0.0781, 0.0854, 0.0824,
                               0.0907, 0.0886, 0.0909, 0.1014, 0.1017, 0.1047, 0.1168, 0.119 ,
                               0.1209, 0.1345, 0.1377, 0.151 , 0.1607, 0.1744, 0.2005, 0.2246,
                               0.2756, 0.3466, 0.5143, 0.9997])
        plt.plot(doc_avg, label = "Algorithm")
        plt.plot(doc_avg_ai, label = "Neural")
        plt.legend(loc = 'upper left')
#        plt.plot([27.01, 14.86, 9.12, 6.58, 5.43], label = "Algorithm")
#        plt.plot([26.67, 15.09, 9.33, 6.83, 5.86], label = "Neural")
        plt.legend(loc = 'upper left')
        plt.show()
    plt.axhline(y = 4.538, color = 'r', linestyle = '--')
    win_times_log = [math.log(x) for x in win_times]
    win_times_prob = [x for x in win_times]
#    AI_times_plot = [48, 41.283, 33.53, 28.532, 23.336]
#    plt.plot(win_times_plot)
#    plt.plot(AI_times_plot)
#    plt.xlabel([1, 5, 10, 15, 20])
#    plt.show()
    plt.plot(win_times_prob)