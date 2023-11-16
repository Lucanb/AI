import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.001):
        self.input = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate

        self.W1 = np.random.randn(hidden_size, input_size)
        self.b1 = np.zeros((hidden_size, 1))
        self.W2 = np.random.randn(output_size, hidden_size)
        self.b2 = np.zeros((output_size, 1))

    def sigmoid(self, element):
        return 1 / (1 + np.exp(-element))

    def forward_propagation(self, X):
        dot_prod = np.dot(self.W1, X) + self.b1
        activ1 = np.tanh(dot_prod)
        dot_prod2 = np.dot(self.W2, activ1) + self.b2
        activ2 = self.sigmoid(dot_prod2)

        cache = {"dot_prod": dot_prod, "activ1": activ1, "dot_prod2": dot_prod2, "activ2": activ2}
        return activ2, cache

    def backward_propagation(self, X, Y, cache):
        m = X.shape[1]

        dZ2 = cache["activ2"] - Y
        dW2 = 1 / m * np.dot(dZ2, cache["activ1"].T)
        db2 = 1 / m * np.sum(dZ2, axis=1, keepdims=True)

        dZ1 = np.dot(self.W2.T, dZ2) * (1 - np.power(cache["activ1"], 2))
        dW1 = 1 / m * np.dot(dZ1, X.T)
        db1 = 1 / m * np.sum(dZ1, axis=1, keepdims=True)

        return {"dW1": dW1, "db1": db1, "dW2": dW2, "db2": db2}

    def update_parameters(self, grads):
        self.W1 -= self.learning_rate * grads["dW1"]
        self.b1 -= self.learning_rate * grads["db1"]
        self.W2 -= self.learning_rate * grads["dW2"]
        self.b2 -= self.learning_rate * grads["db2"]

    def train(self, X, Y, epochs=1000):
        for epoch in range(epochs):
            activ2, cache = self.forward_propagation(X)
            cost = -1 / X.shape[1] * np.sum(Y * np.log(activ2) + (1 - Y) * np.log(1 - activ2))
            grads = self.backward_propagation(X, Y, cache)
            self.update_parameters(grads)
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Cost: {cost}")

    def predict(self, X):
        activ2, _ = self.forward_propagation(X)
        predictions = (activ2 > 0.5).astype(int)
        return predictions

def read_data(file_url, column_names):
    df = pd.read_csv(file_url, sep="\s+", header=None, names=column_names)
    return df

data_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00236/seeds_dataset.txt"
column_names = ["atribute1", "atribute2", "atribute3", "atribute4", "atribute5", "atribute6", "atribute7", "class"]
df = read_data(data_url, column_names)

train_data, test_data, train_labels, test_labels = train_test_split(
    df.drop("class", axis=1),
    df["class"],
    test_size=0.2,
    random_state=42
)

train_data = train_data.T.values
test_data = test_data.T.values

train_labels = (train_labels - 1).values.reshape(1, -1)
test_labels = (test_labels - 1).values.reshape(1, -1)

input_size = train_data.shape[0]
hidden_size = 4
output_size = 1
neural_net = NeuralNetwork(input_size, hidden_size, output_size, learning_rate=0.001)
neural_net.train(train_data, train_labels, epochs=1000)

predictions = neural_net.predict(test_data)

accuracy = np.mean(predictions == test_labels)
print(f"Accuracy: {accuracy}")
