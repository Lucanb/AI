import numpy as np

np.random.seed(42)

data = np.loadtxt("dataset.txt")
DataClasses = data[:, -1]
class_number = len(np.unique(DataClasses))

input_data = data[:, :-1]

class_1_indices = np.where(DataClasses == 1)[0]
class_2_indices = np.where(DataClasses == 2)[0]
class_3_indices = np.where(DataClasses == 3)[0]

np.random.shuffle(class_1_indices)
np.random.shuffle(class_2_indices)
np.random.shuffle(class_3_indices)

test_indices = np.concatenate([
    class_1_indices[:21],
    class_2_indices[:21],
    class_3_indices[:21]
])
train_indices = np.setdiff1d(np.arange(len(data)), test_indices)

train_data = data[train_indices]
test_data = data[test_indices]

train_input_data = train_data[:, :-1]
test_input_data = test_data[:, :-1]

train_labels = np.eye(class_number)[train_data[:, -1].astype(int) - 1]  # one-hot encoding
test_labels = np.eye(class_number)[test_data[:, -1].astype(int) - 1]  # one-hot encoding

print(train_input_data.shape)
print(test_input_data.shape)

learning_rate = 0.01
epochs = 1000
input_size = input_data.shape[1]
output_size = class_number

hidden_layer_size1 = 10
weights1 = np.random.rand(input_size, hidden_layer_size1)

hidden_layer_size2 = 5
weights2 = np.random.rand(hidden_layer_size1, hidden_layer_size2)

weights_out = np.random.rand(hidden_layer_size2, output_size)

biases1 = np.random.randn(1, hidden_layer_size1) * 0.01
biases2 = np.random.randn(1, hidden_layer_size2) * 0.01
biases_out = np.random.randn(1, output_size) * 0.01


def softmax(x):
    e_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return e_x / np.sum(e_x, axis=1, keepdims=True)


def softmax_derivative(x):
    s = softmax(x)
    return s * (1 - s)


def forward_propagation(input, weights1, biases1, weights2, biases2, weights_out, biases_out):
    dot_product1 = np.dot(input, weights1) + biases1
    hidden1_val = softmax(dot_product1)
    dot_product2 = np.dot(hidden1_val, weights2) + biases2
    hidden2_val = softmax(dot_product2)
    dot_product_out = np.dot(hidden2_val, weights_out) + biases_out
    out_value = softmax(dot_product_out)
    return out_value


def bias_lose(prediction, labels):
    epsilon = 1e-15
    prediction = np.clip(prediction, epsilon, 1 - epsilon)
    loss = -np.sum(labels * np.log(prediction)) / len(labels)
    return loss


def backward_propagation(inputs, predictions, labels, weights1, biases1, weights2, biases2, weights_out, biases_out):
    dot_product1 = np.dot(inputs, weights1) + biases1
    hidden1_val = softmax(dot_product1)
    dot_product2 = np.dot(hidden1_val, weights2) + biases2
    hidden2_val = softmax(dot_product2)
    error_out = predictions - labels
    gradient_out = np.dot(hidden2_val.T, error_out) / len(inputs)
    softmax_hidden2_derivative = softmax_derivative(dot_product2)
    error_hidden2 = np.dot(error_out, weights_out.T) * softmax_hidden2_derivative
    gradient_hidden2 = np.dot(hidden1_val.T, error_hidden2) / len(inputs)
    softmax_hidden1_derivative = softmax_derivative(dot_product1)
    error_hidden1 = np.dot(error_hidden2, weights2.T) * softmax_hidden1_derivative
    gradient_hidden1 = np.dot(inputs.T, error_hidden1) / len(inputs)
    weights_out = weights_out - learning_rate * gradient_out
    biases_out = biases_out - learning_rate * np.sum(error_out, axis=0, keepdims=True) / len(inputs)
    weights2 = weights2 - learning_rate * gradient_hidden2
    biases2 = biases2 - learning_rate * np.sum(error_hidden2, axis=0, keepdims=True) / len(inputs)
    weights1 = weights1 - learning_rate * gradient_hidden1
    biases1 = biases1 - learning_rate * np.sum(error_hidden1, axis=0, keepdims=True) / len(inputs)

    return weights1, biases1, weights2, biases2, weights_out, biases_out


def forward_propagation_single(input_vector, weights1, biases1, weights2, biases2, weights_out, biases_out):
    dot_product1 = np.dot(input_vector, weights1) + biases1
    hidden1_val = softmax(dot_product1)
    dot_product2 = np.dot(hidden1_val, weights2) + biases2
    hidden2_val = softmax(dot_product2)
    dot_product_out = np.dot(hidden2_val, weights_out) + biases_out
    out_value = softmax(dot_product_out)
    return out_value


for epoch in range(epochs):
    hidden1 = softmax(np.dot(train_input_data, weights1) + biases1)
    hidden2 = softmax(np.dot(hidden1, weights2) + biases2)
    predictions = forward_propagation(train_input_data, weights1, biases1, weights2, biases2, weights_out, biases_out)

    loss = bias_lose(predictions, train_labels)
    weights1, biases1, weights2, biases2, weights_out, biases_out = backward_propagation(train_input_data, predictions,
                                                                                          train_labels, weights1, biases1,
                                                                                          weights2, biases2, weights_out,
                                                                                          biases_out)
    if epoch % 100 == 0:
        print(f"Epoch {epoch}, Loss: {loss}")

print("Final Weights Layer 1:")
print(weights1)
print("Final Weights Layer 2:")
print(weights2)
print("Final Weights Output Layer:")
print(weights_out)

correct_predictions = 0
for test_input, test_label in zip(test_input_data, test_labels):
    test_prediction = forward_propagation_single(test_input, weights1, biases1, weights2, biases2, weights_out, biases_out)

    predicted_class = np.argmax(test_prediction) + 1
    true_class = np.argmax(test_label) + 1
    if predicted_class == true_class:
        correct_predictions += 1

accuracy = correct_predictions / len(test_input_data)
print(f"Accuracy on Test Data: {accuracy * 100:.2f}%")
