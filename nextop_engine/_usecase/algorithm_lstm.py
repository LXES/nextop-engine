import os
import sys
path_name= os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path_name)

from _element.feature_control import *
from _element.calculations import minMaxNormalizer, minMaxDeNormalizer

import tensorflow as tf
import numpy as np
from datetime import datetime
import pandas as pd

def LSTM(txs, forecastDay, features):
    tf.reset_default_graph()
    tf.set_random_seed(77)
    # Add basic date related features to the table
    year = lambda x: datetime.strptime(x, "%Y-%m-%d").year
    dayOfWeek = lambda x: datetime.strptime(x, "%Y-%m-%d").weekday()
    month = lambda x: datetime.strptime(x, "%Y-%m-%d").month
    weekNumber = lambda x: datetime.strptime(x, "%Y-%m-%d").strftime('%V')
    txs['year'] = txs['ds'].map(year)
    txs['month'] = txs['ds'].map(month)
    txs['weekNumber'] = txs['ds'].map(weekNumber)
    txs['dayOfWeek'] = txs['ds'].map(dayOfWeek)

    # Add non-basic date related features to the table
    seasons = [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 0]  # dec - feb is winter, then spring, summer, fall etc
    season = lambda x: seasons[(datetime.strptime(x, "%Y-%m-%d").month - 1)]
    day_of_week01s = [0, 0, 0, 0, 0, 1, 1]
    day_of_week01 = lambda x: day_of_week01s[(datetime.strptime(x, "%Y-%m-%d").weekday())]
    txs['season'] = txs['ds'].map(season)
    txs['dayOfWeek01'] = txs['ds'].map(day_of_week01)

    # Backup originalSales
    originalSales = list(txs['y'])
    sales = list(txs['y'])

    # week number는 경계부분에서 약간 오류가 있다.
    if features is 'DayOfWeek_WeekNumber_Month_Season':
        tempxy = [list(txs['dayOfWeek']), list(txs['weekNumber']), list(txs['month']), list(txs['season']), sales]
    elif features is 'DayOfWeek01_WeekNumber_Month_Season':
        tempxy = [list(txs['dayOfWeek01']), list(txs['weekNumber']), list(txs['month']), list(txs['season']), sales]

    elif features is 'WeekNumber_Month_Season_Year':
        tempxy = [list(txs['weekNumber']), list(txs['month']), list(txs['season']), list(txs['year']), sales]

    xy = np.array(tempxy).transpose().astype(np.float)

    # Backup originalXY for denormalize
    originalXY = np.array(tempxy).transpose().astype(np.float)
    xy = minMaxNormalizer(xy)

    # TRAIN PARAMETERS
    # data_dim은 y값 도출을 위한 feature 가지수+1(독립변수 가지수 +1(y포함))
    data_dim = 5
    # data_dim크기의 data 한 묶음이 seq_length만큼 input으로 들어가
    seq_length = 10
    # output_dim(=forecastDays)만큼의 다음날 y_data를 예측
    output_dim = forecastDay
    # hidden_dim은 정말 임의로 설정
    hidden_dim = 100
    # learning rate은 배우는 속도(너무 크지도, 작지도 않게 설정)
    learning_rate = 0.001
    iterations = 1000
    # Build a series dataset(seq_length에 해당하는 전날 X와 다음 forecastDays에 해당하는 Y)
    x = xy
    y = xy[:, [-1]]
    dataX = []
    dataY = []
    for i in range(0, len(y) - seq_length - forecastDay + 1):
        _x = x[i:i + seq_length]
        _y = y[i + seq_length:i + seq_length + forecastDay]
        _y = np.reshape(_y, (forecastDay))
        dataX.append(_x)
        dataY.append(_y)

    train_size = int(len(dataY) - forecastDay)
    # train_size = int(len(dataY) * 0.7)
    test_size = len(dataY) - train_size

    trainX, testX = np.array(dataX[0:train_size]), np.array(dataX[train_size:])

    trainY, testY = np.array(dataY[0:train_size]), np.array(dataY[train_size:])

    X = tf.placeholder(tf.float32, [None, seq_length, data_dim])
    Y = tf.placeholder(tf.float32, [None, forecastDay])

    cell = tf.contrib.rnn.BasicLSTMCell(num_units=hidden_dim, state_is_tuple=True, activation=tf.tanh)
    outputs, _states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)
    Y_pred = tf.contrib.layers.fully_connected(outputs[:, -1], output_dim, activation_fn=None)
    loss = tf.reduce_sum(tf.square(Y_pred - Y))  # sum of the squares
    optimizer = tf.train.AdamOptimizer(learning_rate)
    train = optimizer.minimize(loss)

    denormalizedTestY = originalSales[train_size + seq_length:]
    #     denormalizedTestY_feed=np.array([[i] for i in denormalizedTestY])

    targets = tf.placeholder(tf.float32, [None, 1])
    predictions = tf.placeholder(tf.float32, [None, 1])

    count = 0
    with tf.Session() as sess:

        # 초기화
        init = tf.global_variables_initializer()
        sess.run(init)

        # Training step
        for i in range(iterations):
            _, step_loss = sess.run([train, loss], feed_dict={X: trainX, Y: trainY})
            print("[step: {}] loss: {}".format(i, step_loss))

        # Test step
        test_predict = minMaxDeNormalizer(sess.run(Y_pred, feed_dict={X: testX}), originalXY)
        realSale = minMaxDeNormalizer(testY[-1], originalXY)
    return np.square(test_predict[-1]).tolist()

# TODO : 엘에스티엠 개선
