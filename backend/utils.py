import numpy as np
from sklearn.preprocessing import StandardScaler

def preprocess_input(features):
    """Standardize input features"""
    scaler = StandardScaler()
    return scaler.fit_transform(np.array(features).reshape(1, -1))