from __future__ import print_function
# from sklearn.cross_validation import train_test_split
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
np.random.seed(1337)  # for reproducibility
from keras.preprocessing import sequence
# from keras.utils import np_utils
from tensorflow.keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding
from keras.layers import LSTM, SimpleRNN, GRU
from keras.datasets import imdb
# from keras.utils.np_utils import to_categorical
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import (precision_score, recall_score,f1_score, accuracy_score,mean_squared_error,mean_absolute_error)
from sklearn import metrics
from sklearn.preprocessing import Normalizer
import h5py
from keras import callbacks
from keras.callbacks import CSVLogger
import keras
import keras.preprocessing.text
import itertools
from keras.callbacks import CSVLogger
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, CSVLogger
from keras import callbacks
from sklearn import feature_extraction
import sklearn

# trainlabels = pd.read_csv('dgcorrect/trainlabel.csv', header=None)
trainlabels = pd.read_csv('../dataset/dgcorrect/trainlabel-binary.csv', header=None, sep=';')
trainlabel = trainlabels.iloc[:,1:2]
# print(trainlabel)

# testlabels = pd.read_csv('dgcorrect/test1label.csv', header=None)
testlabels = pd.read_csv('../dataset/dgcorrect/test1label.txt', header=None)
testlabel = testlabels.iloc[:,0:1]
# print(testlabel)

# testlabels1 = pd.read_csv('dgcorrect/test2label.csv', header=None)
testlabels1 = pd.read_csv('../dataset/dgcorrect/test2label.txt', header=None)
testlabel1 = testlabels1.iloc[:,0:1]
# print(testlabel1)

# train = pd.read_csv('dgcorrect/train.txt', header=None)
train = pd.read_csv('../dataset/dgcorrect/trainlabel-binary.csv', header=None, sep=';')
train = train.iloc[:,0:1]
# print(train)

# test = pd.read_csv('dgcorrect/test1.txt', header=None)
test = pd.read_csv('../dataset/dgcorrect/test1.txt', header=None)
# print(test)

# test1 = pd.read_csv('dgcorrect/test2.txt', header=None)
test1 = pd.read_csv('../dataset/dgcorrect/test2.txt', header=None)
# print(test1)

X = train.values.tolist()
X = list(itertools.chain(*X))

T = test.values.tolist()
T = list(itertools.chain(*T))

T1 = test1.values.tolist()
T1 = list(itertools.chain(*T1))

print("vectorizing data")
ngram_vectorizer = feature_extraction.text.CountVectorizer(analyzer='char', ngram_range=(2, 2))
X_train = ngram_vectorizer.fit_transform(X)
y_train = np.array(trainlabel)

print("vectorizing data")
ngram_vectorizer1 = feature_extraction.text.CountVectorizer(analyzer='char', ngram_range=(2, 2))
X_test1 = ngram_vectorizer1.fit_transform(T)
y_test1 = np.array(testlabel)

print("vectorizing data")
ngram_vectorizer2 = feature_extraction.text.CountVectorizer(analyzer='char', ngram_range=(2, 2))
X_test = ngram_vectorizer2.fit_transform(T1)
y_test = np.array(testlabel1)

max_features = X_train.shape[1]

#
X_train = X_train.todense()
X_train = sequence.pad_sequences(X_train, maxlen=max_features)

X_test = sequence.pad_sequences(X_test, maxlen=max_features)
X_test1 = sequence.pad_sequences(X_test1, maxlen=max_features)


print(y_test.shape)
print(X_test.shape)

model = Sequential()
model.add(Dense(1, input_dim=max_features, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam',metrics=['accuracy'])

model.load_weights("logs/bigram/checkpoint-01.hdf5")
y_proba = model.predict_proba(X_test.todense())
np.savetxt('res/bigram.csv', y_proba)

y_pred = model.predict_classes(X_train.todense())
accuracy = accuracy_score(y_train, y_pred)
recall = recall_score(y_train, y_pred , average="binary")
precision = precision_score(y_train, y_pred , average="binary")
f1 = f1_score(y_train, y_pred, average="binary")

print("----------------------------------------------")
print("accuracy")
print("%.3f" %accuracy)
print("racall")
print("%.3f" %recall)
print("precision")
print("%.3f" %precision)
print("f1score")
print("%.3f" %f1)
#

print(X_train.shape)
x = X_train.todense()
print(x.shape)

print(X_test.shape)
x = X_test.todense()
print(x.shape)

X_test = sequence.pad_sequences(x, 1450)

