# Michael Hickey
# Neural Network Model for Black Jack


from keras.models import Sequential
from keras.layers import Dense
import numpy as np 
import os

os.chdir("dataset")

if __name__ == "__main__":
	# Fix the random seed so you can reproduce the sequence.
	np.random.seed(1)

	# Load a dataset.
	dataset = np.loadtxt("black_jack_dataset.csv", delimiter = ",")

	# We want all the rows, and only 4 columns.
	input_data = dataset[ : , 2:4]
	answer = dataset[ : , 4]

	# Define the model
	model = Sequential()

	# Add layers to the network.
	model.add(Dense(12, input_dim = 2, activation = "relu") )
	# Second Layer
	#model.add(Dense(10, activation = "relu") )
	# Third Layer
	model.add(Dense(8, activation = "relu") )
	# Fourth Layer
	model.add(Dense(4, activation = "relu") )	
	# This is the output layer, notice there is one neuron for the output.
	model.add(Dense(1, activation = "sigmoid") )

	# Compile the model.
	model.compile(loss = "binary_crossentropy", optimizer = "adam", metrics = ["accuracy"])

	# Fit (aka. train) the model on the dataset
	# Put the data in, get an answer from the model, run it for size_of_sataset iterations, on batch sizes of 10.
	size_of_dataset = 960
	model.fit(input_data, answer, epochs = size_of_dataset, batch_size = 32)

	# Score the model.
	scores = model.evaluate(input_data, answer)
	print("\n%s: %.2f%%" %(model.metrics_names[1], scores[1]*100) )