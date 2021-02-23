
#---Can Machine Learning Actually Predict the Stock Market---

stock_symbol = 'AAPL'

##################################### -PLS READ- ################################################################################################


'''

    The code below is a model used to predict tomorrow's stock price for some company.
    All you have to do to use this model is change the variable above to a companies stock symbol.
    An example of a companies stock symbol is like TSLA for Tesla or AAPL for Apple.
    When you input the symbol run the entire code and it will output it's prediction for tomorrows stock price.
    
    Necessary installation:
    To use this model you do have to install 2 necessary libraries.
    1. Scikit Learn. To install this library go to your anaconda prompt and type: pip install scikit-learn
    2. Keras. To install this library go to your anaconda prompt and type: pip install keras
    

'''

##################################### -Importing Necessary Libraries- ################################################################################################

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import math
from datetime import datetime
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler


##################################### -Part 1 - Data preprocessing- ################################################################################################

#--Summary: The code in this section with prepare the training set to train our model

today = datetime.today().strftime('%Y-%m-%d')

#imports all the stock prices from 2012 to todays date
df = web.DataReader(stock_symbol, data_source = 'yahoo', start = '2012-01-01', end = today)

#Create a new dataframe with only the Close column
data = df.filter(['Close'])

#Convert the dataframe to a numpy array
dataset = data.values

#Get the number of rows to train the model on
training_data_len = math.ceil(len(dataset)*.8)

#Feature scaling
scale = MinMaxScaler(feature_range = (0,1))
scaled_data = scale.fit_transform(dataset)

#create the scaled training set
train_data = scaled_data[0:training_data_len,:]

#split data into x_train and y_train
#creating a data structure with 60 timesteps and 1 output 
#(60 timesteps is the previous 60 stock pices and then trying to predict the next one)
X_train = []
y_train = []
for i in range(60,len(train_data)):
    #the values before that 60th value
    X_train.append(train_data[i-60:i,0])
    #the 60th value 
    y_train.append(train_data[i,0])

#convert them to numpy arays
X_train, y_train = np.array(X_train), np.array(y_train)

#Reshaping (adding a dimension in a numpy array)
#from keras documentation          Batch_size,    timesteps,    imput_dim
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1],1 ))
X_train.shape


##################################### -Part 2 - Building the RNN Model- ################################################################################################

#--Summary: The code in this section will build the model and train it on the training set

regressor = Sequential()

#Adding the first LSTM layer 
regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1],1)))

#Adding a second LSTM layer 
regressor.add(LSTM(units = 50, return_sequences = False))

#Adding a network of neurons
regressor.add(Dense(units = 25))

#adding the output layer
regressor.add(Dense(units = 1))

#Compiling the RNN
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

#Fitting the RNN to the training set
regressor.fit(X_train, y_train, epochs = 1, batch_size = 1) #this takes long


##################################### -Part 3 - Predicting Tomorrows Stock- ################################################################################################

#--Summary: The code in this section will predict tomorrows stock price using our trained model

quote = web.DataReader(stock_symbol, data_source = 'yahoo', start = '2012-01-01', end = today)
#Create a new dataframe with only the Close column
new_df = quote.filter(['Close'])

#The dataframe only keeps the last 60 days worth of data
last_60_days = new_df[-60:].values
last_60_days_scaled = scale.transform(last_60_days)

#This chunk of code gets the data ready to be put in the model
x_test = []
x_test.append(last_60_days_scaled)
x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1],1 ))

#Predicts tommorow's price given the last 60 days worth of data and our model
pred_price = regressor.predict(x_test)
pred_price = scale.inverse_transform(pred_price)

#what the predicted price will be the next day
print('Tomorrows stock price for ' +stock_symbol+ ' is: ' + str(pred_price))













