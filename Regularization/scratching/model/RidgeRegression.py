import numpy as np

def gradientDescent(X, y, y_pred, n_samples, lambda_param, weights):
    gradient = (1 / n_samples) * (X.T @ (y_pred - y)) + (lambda_param / n_samples) * (weights[1:] ** 2)
    gradient[0] -= (lambda_param / n_samples) * weights[0]  # Don't regularize the bias term
    return gradient

def normalEquation(X, y, lambda_param):
    # Identity matrix
    identity_metrix = lambda_param * np.eye(X.shape[1])
    identity_metrix[0, 0] = 0  # Bias term should not be regularized

    # Normal equation for ridge regression
    weights = np.dot(np.linalg.inv(np.dot(X.T, X) + identity_metrix), np.dot(X.T, y))
    return weights

class RidgeRegression:
    
    def __init__(self, lambda_param, weights = None):
        self.lambda_param = lambda_param
        self.weights = weights
        self.weights_history = []
        self.costs_history = []

    def training(self, X, y, type, lr = 0.1, n_iters = 100):
        if (type == "normalEq"):
            self.weights = normalEquation(X, y, self.lambda_param)
        elif (type == "gradientDes"):
            n_samples, n_features = X.shape
            self.weights = np.zeros(n_features)
            for _ in range(n_iters):
                self.weights_history.append(self.weights[1])
                y_pred = self.prediction(X)
                self.costs_history.append(self.costFunction(X, y, y_pred))
                weights_gradient = gradientDescent(X, y, y_pred, n_samples, self.lambda_param, self.weights)
                self.weights -= lr * weights_gradient
        else:
            raise Exception("Sorry, we don't have that type of optimization.")   
        
    def standardization(self, X):       # X_std = X - mean of X / standard deviation of X
        mean_x = np.array([np.mean(X)])
        std_x = np.array([np.std(X)])
        X_std = (X - mean_x) / std_x
        return X_std
    
    def get_Weights_History(self):
        return self.weights_history
    
    def get_Costs_History(self):
        return self.costs_history
    
    def prediction(self, X):
        return np.dot(X, self.weights)

    def costFunction(self, X, y, y_pred):
        rss = np.sum((y - y_pred) ** 2)
        regularization = self.lambda_param * np.sum(self.weights[1:] ** 2)
        return rss + regularization