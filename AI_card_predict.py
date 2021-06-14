import tensorflow as tf
import CNN_Tools as ct
from tensorflow.contrib import rnn
from card_shuffle import Cards
import numpy as np
from matplotlib.pyplot import plot, show

train = 0
deck_size = 52
embedding_size = 128
if train:
    iteration = 2000
    batch_size = 500
else:
    iteration = 10000
    batch_size = 1
hidden_size = 1024
layers = 3

tf.reset_default_graph()
sess = tf.InteractiveSession()

x = tf.placeholder(tf.int32, [batch_size, deck_size])
y = tf.placeholder(tf.int32, [batch_size, deck_size])
embedding = tf.Variable(tf.random_normal([deck_size+1, embedding_size]))
card_embed = tf.nn.embedding_lookup(embedding, x)

cell = rnn.MultiRNNCell([rnn.LSTMCell(hidden_size) for _ in range(layers)]+
                        [rnn.LSTMCell(deck_size)])
fc, state = tf.nn.dynamic_rnn(cell, card_embed, dtype = tf.float32)

Loss = tf.nn.sparse_softmax_cross_entropy_with_logits(labels = y, logits = fc)
out_loss = tf.reduce_mean(Loss)
opt = tf.train.AdamOptimizer(1e-4).minimize(Loss)

acc = ct.get_acc(fc, y)
argmax = ct.get_max(fc)

#sess.run(tf.global_variables_initializer())
saver, _ = ct.training_progress(sess, "C:\\Users\\wongh\\.spyder-py3\\Shuffle_5_6", train)
if not train:
    saver.restore(sess, "C:\\Users\\wongh\\.spyder-py3\\Shuffle_5_6")

print("Starts...")
correct = []
doc_true = []
frequency = [0 for _ in range(52)]
for it in range(0, iteration):
    train_input = []
    train_target = []
    for _ in range(batch_size):
        deck = Cards(times = 6, style = 5).get_cards()
        train_input.append([0]+deck[:-1])
        train_target.append(deck)
    train_input = np.array(train_input)
    train_target = np.array(train_target)-1
    train_dict = {x:train_input, y:train_target}
    if train:
        inf, loss, _ = sess.run([argmax, out_loss, opt], train_dict)
        accuracy = np.equal(inf, train_target)
        correct_guess = sum(sum(accuracy))/batch_size
        print("Iteration:{} Loss:{} Cards:{}".format(it+1, loss, correct_guess))
        if it % 20 == 0:
            correct.append(correct_guess)
            print("Infere:", sess.run(argmax, train_dict)[0])
            print("Target:", train_target[0])
            plot(correct)
            show()
    else:   
        output_value = sess.run(argmax, train_dict)
        trueness = np.equal(output_value, train_target)
        number_correct = output_value[trueness]
        for n in number_correct:
            frequency[n] += 1
        doc_true.append(trueness[0])
        correct.append(sum(sum(trueness))/batch_size)
doc_avg = np.average(np.array(correct), axis = 0)
plot(doc_avg)
show()

saver.save(sess, "C:\\Users\\wongh\\.spyder-py3\\Shuffle_5_6")
if not train:
    print("Cards Guessed Correctly on Average after 1000 epochs of Training: {} Cards".format(sum(correct)/len(correct)))