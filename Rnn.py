import tensorflow as tf
import random
import json
import numpy

class RNNConfig():
    input_size=1
    num_steps=120
    lstm_size=128*2
    num_layers=1
    keep_prob=0.8
    batch_size = 64
    init_learning_rate = 0.001
    learning_rate_decay = 0.99
    init_epoch = 5
    max_epoch = 100

config = RNNConfig()

tf.reset_default_graph()
lstm_graph = tf.Graph()
with lstm_graph.as_default():
    inputs = tf.placeholder(tf.float32, [None, config.num_steps, config.input_size])
    targets = tf.placeholder(tf.float32, [None, config.input_size])
    learning_rate = tf.placeholder(tf.float32, None)
    def _create_one_cell():
        lstm_cell = tf.contrib.rnn.LSTMCell(config.lstm_size, state_is_tuple=True)
        return tf.contrib.rnn.DropoutWrapper(lstm_cell, output_keep_prob=config.keep_prob)
    cell = tf.contrib.rnn.MultiRNNCell(
        [_create_one_cell() for _ in range(config.num_layers)], 
        state_is_tuple=True
    )

    val, _ = tf.nn.dynamic_rnn(cell, inputs, dtype=tf.float32)
    val = tf.transpose(val, [1, 0, 2])
    print(val.get_shape())
    last = tf.gather(val, int(val.get_shape()[0]) - 1, name="last_lstm_output")

    weight = tf.Variable(tf.truncated_normal([config.lstm_size, config.input_size]))
    bias = tf.Variable(tf.constant(0.1, shape=[config.input_size]))
    prediction = tf.matmul(last, weight) + bias

    loss = tf.reduce_mean(tf.square(prediction - targets))
    optimizer = tf.train.RMSPropOptimizer(learning_rate)
    minimize = optimizer.minimize(loss)

def getbatches(ins,outs,amount,train):
    a = []
    o = []
    for i in range(amount):
        o.append([])
        a.append([])
        for b in range(config.batch_size):
            if(train):
                x = random.randrange(0,len(ins)/2)
            else:
                x = random.randrange(len(ins)/2,len(ins))
            o[i].append(outs[x][0])
            a[i].append(ins[x])
    return a, o

#aas = [[[int(i-6+random.randrange(12))] for i in range(config.num_steps)] for _ in range(config.batch_size)]
#ts = [[int(300-6+random.randrange(12))] for _ in range(config.batch_size)]
with open("train.json","r") as file:
    data = json.load(file)
    #print(data["inputs"])
    act = data["actual"]
    aas, ts = getbatches(data["inputs"], data["outputs"],config.max_epoch,True)
    aastest, tstest = data["inputs"], data["outputs"]


with tf.Session(graph=lstm_graph) as sess:
    tf.global_variables_initializer().run()
    learning_rates_to_use = [
    config.init_learning_rate * (
        config.learning_rate_decay ** max(float(i + 1 - config.init_epoch), 0.0)
    ) for i in range(config.max_epoch)]
    for epoch_step in range(config.max_epoch):
        current_lr = learning_rates_to_use[epoch_step]
        feed_dict={
            inputs: aas[epoch_step],
            targets: ts[epoch_step],
            learning_rate:current_lr
        }
        train_loss, _ = sess.run([loss, minimize], feed_dict)
        if epoch_step % 10 == 0:
            test_loss, _pred = sess.run([loss, prediction], feed_dict)
            print("pred",_pred,test_loss)
    print("------------------------------------------------------")
    predictedtargets = []
    for epoch_step in range(len(aastest)):
        feed_dict={
            inputs: [aastest[epoch_step]],
            targets: tstest[epoch_step]
        }
        pred = sess.run([prediction], feed_dict)
        predictedtargets.append(pred)

for i,a in enumerate(predictedtargets):
    predictedtargets[i][0]*=act[i+120]
for i,a in enumerate(predictedtargets):
    print(a[0],act[i])

        

predsjson = {actual:actualtargets,predicted:predictedtargets}
for i in range(len(actualtargets)):
    if(i>=120):
        print(actualtargets[i],predictedtargets[i-120])

with open("predictions.json","w") as file:
    data = json.dump(file,predsjson)

        

    


    
