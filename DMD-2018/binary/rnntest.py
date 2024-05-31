from __future__ import print_function
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
np.random.seed(1337) 
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding
from keras.layers import LSTM, SimpleRNN, GRU
from keras.datasets import imdb
from sklearn.metrics import (precision_score, recall_score,f1_score, accuracy_score,mean_squared_error,mean_absolute_error)
from sklearn import metrics
from sklearn.preprocessing import Normalizer
import h5py
from keras import callbacks
from keras.callbacks import CSVLogger
import keras
from tensorflow.keras.preprocessing import text
import itertools
from keras.callbacks import CSVLogger
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, CSVLogger
from keras import callbacks
from keras.layers import Convolution1D, GlobalMaxPooling1D

trainlabels = pd.read_excel('../dataset/detect/training/training.xlsx', header=None)
trainlabel = trainlabels.iloc[:,1:2]
print(trainlabel)

testlabel = pd.read_csv('../dataset/detect/testing/first/test1label.txt', header=None)
print(testlabel)

testlabel1 = pd.read_csv('../dataset/detect/testing/second/test2label.txt', header=None)
print(testlabel1)

train = trainlabels.iloc[:,0:1]
print(train)

test = pd.read_csv('../dataset/detect/testing/first/test1.txt', header=None)
print(test)

test1 = pd.read_csv('../dataset/detect/testing/second/test2.txt', header=None)
print(test1)

X = train.values.tolist()
X = list(itertools.chain(*X))


T = test.values.tolist()
T = list(itertools.chain(*T))

T1 = test1.values.tolist()
T1 = list(itertools.chain(*T1))

# Convert all elements to strings and join them into a single string
X_str = ''.join(map(str, X + T + T1))

# Create a dictionary mapping each unique character to a unique integer
def create_char_to_int_mapping(data):
    unique_chars = sorted(set(data))  # Get unique characters and sort them
    char_to_int_mapping = {char: idx for idx, char in enumerate(unique_chars)}
    return char_to_int_mapping

# Create the mapping for the training data
valid_chars = create_char_to_int_mapping(X_str)
print(valid_chars)

max_features = len(valid_chars) + 1

# Ensure elements are strings before calculating their lengths
maxlen = np.max([len(str(x)) for x in X])
print(maxlen)


# Convert X, T, and T1 to lists of strings
X_str_list = [str(x) for x in X]
T_str_list = [str(x) for x in T]
T1_str_list = [str(x) for x in T1]

# Map each character in X_str_list to its corresponding integer value using valid_chars
X1 = [[valid_chars[char] for char in x] for x in X_str_list]

# Map each character in T_str_list to its corresponding integer value using valid_chars
T11 = [[valid_chars[char] for char in x] for x in T_str_list]

# Map each character in T1_str_list to its corresponding integer value using valid_chars
T12 = [[valid_chars[char] for char in x] for x in T1_str_list]


X_train = sequence.pad_sequences(X1, maxlen=maxlen)

X_test = sequence.pad_sequences(T11, maxlen=maxlen)

X_test1 = sequence.pad_sequences(T12, maxlen=maxlen)

y_train = np.array(trainlabel)
y_test = np.array(testlabel)
y_test1 = np.array(testlabel1)


embedding_vecor_length = 128

model = Sequential()
model.add(Embedding(max_features, embedding_vecor_length, input_length=maxlen))
model.add(SimpleRNN(128))
model.add(Dropout(0.1))
model.add(Dense(1))
model.add(Activation('sigmoid'))

# Build the model
input_dim = X_train.shape[1]  # assuming X_train is a 2D tensor
model.build((None, input_dim))

# Now load the weights
model.load_weights("logs/rnn/checkpoint-01.keras")

# Predict probabilities
y_pred_prob = model.predict(X_test)

# Convert probabilities into class labels
y_pred = np.where(y_pred_prob > 0.5, 1, 0)
accuracy = accuracy_score(y_test, y_pred)
recall = recall_score(y_test, y_pred , average="binary")
precision = precision_score(y_test, y_pred , average="binary")
f1 = f1_score(y_test, y_pred, average="binary")

print("confusion matrix")
print("----------------------------------------------")
print("accuracy")
print("%.3f" %accuracy)
print("racall")
print("%.3f" %recall)
print("precision")
print("%.3f" %precision)
print("f1score")
print("%.3f" %f1)

# Predict probabilities
y_pred_prob = model.predict(X_test1)

# Convert probabilities into class labels
y_pred = np.where(y_pred_prob > 0.5, 1, 0)
accuracy = accuracy_score(y_test1, y_pred)
recall = recall_score(y_test1, y_pred , average="binary")
precision = precision_score(y_test1, y_pred , average="binary")
f1 = f1_score(y_test1, y_pred, average="binary")

print("confusion matrix")
print("----------------------------------------------")
print("accuracy")
print("%.3f" %accuracy)
print("racall")
print("%.3f" %recall)
print("precision")
print("%.3f" %precision)
print("f1score")
print("%.3f" %f1)

'''
cm = metrics.confusion_matrix(y_test, y_pred)
print("==============================================")
print(cm)
tp = cm[0][0]
fp = cm[0][1]
tn = cm[1][1]
fn = cm[1][0]
print("tp")
print(tp)
print("fp")
print(fp)
print("tn")
print(tn)
print("fn")
print(fn)

print("LSTM acc")
Acc = float(tp+tn)/float(tp+fp+tn+fn)
print(Acc)
print("precision")
prec = float(tp)/float(tp+fp)
print(prec)
print("recall")
rec = float(tp)/float(tp+fn)
print(rec)
print("F-score")
fs = float(2*tp)/float((2*tp)+fp+fn)
print(fs)



model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
loss, accuracy = model.evaluate(X_test, y_test)
print("\nLoss: %.2f, Accuracy: %.2f%%" % (loss, accuracy*100))
'''


