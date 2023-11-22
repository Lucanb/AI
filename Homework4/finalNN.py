import numpy as np

np.random.seed(42)

data = np.loadtxt("dataset.txt")
DataClasses = data[:,-1]
class_number = len(np.unique(DataClasses))

input_data = data[:,:-1]

labels = np.eye(class_number)[DataClasses.astype(int) - 1] #one-hot encoding

learning_rate = 0.01
epochs = 1000
input_size = input_data.shape[1]
output_size = class_number

hidden_layer_size1 = 10
weights1 = np.random.rand(input_size, hidden_layer_size1) 

hidden_layer_size2 = 5
weights2 = np.random.rand(hidden_layer_size1,hidden_layer_size2)

weights_out = np.random.rand(hidden_layer_size2,output_size)


def softmax(x):
    e_x = np.exp(x - np.max(x,axis=1,keepdims = True))
    return e_x/ np.sum(e_x,axis = 1,keepdims = True)

def forward_propagation(input,weights1,weights2,weights_out):
    dot_product1 = np.dot(input,weights1)
    hidden1_val = softmax(dot_product1)
    dot_product2 = np.dot(hidden1_val,weights2)
    hidden2_val = softmax(dot_product2)
    dot_product_out = np.dot(hidden2_val,weights_out)
    out_value = softmax(dot_product_out)
    return out_value
    
def bias_lose(prediction,labels):
    epsilon = 1e-15
    prediction = np.clip(prediction, epsilon, 1 - epsilon)
    loss = -np.sum(labels * np.log(prediction)) / len(labels)
    return loss

def backward_propagation(inputs,predictions,labels,weights1,weights2,weights_out):
    error_out = predictions - labels
    gradient_out = np.dot(hidden2.T,error_out) / len(inputs)
    error_hidden2 = np.dot(error_out,weights_out.T)
    gradient_hidden2 = np.dot(hidden1.T,error_hidden2) / len(inputs)
    error_hidden1 = np.dot(error_hidden2,weights2.T)
    gradient_hidden1 = np.dot(inputs.T,error_hidden1) / len(inputs)
    weights_out = weights_out - learning_rate * gradient_out
    weights2 = weights2 - learning_rate * gradient_hidden2
    weights1 = weights1 - learning_rate * gradient_hidden1

    return weights1,weights2,weights_out



for epoch in range(epochs):

    hidden1 = softmax(np.dot(input_data, weights1))
    hidden2 = softmax(np.dot(hidden1, weights2))
    predictions = forward_propagation(input_data, weights1, weights2, weights_out)

    loss = bias_lose(predictions, labels)
    weights1, weights2, weights_out = backward_propagation(input_data, predictions, labels, weights1, weights2, weights_out)
    if epoch % 100 == 0:
        print(f"Epoch {epoch}, Loss: {loss}")

print("Final Weights (Layer 1):")
print(weights1)
print("Final Weights (Layer 2):")
print(weights2)
print("Final Weights (Output Layer):")
print(weights_out)

test_data = np.array([[11.65, 13.07, 0.8575, 5.108, 2.85, 5.209, 5.135]])
test_predictions = forward_propagation(test_data, weights1, weights2, weights_out)
predicted_class = np.argmax(test_predictions, axis=1) + 1

print("Predicted Class for Test Data:")
print(predicted_class)
