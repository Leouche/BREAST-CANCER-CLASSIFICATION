import requests
import numpy as np

def test_prediction():
    # Valid input
    response = requests.post(
        "http://localhost:5000/predict",
        json={"features": list(np.random.rand(30))}  # Random valid features
    )
    assert response.status_code == 200
    assert "prediction" in response.json()
    
    # Invalid input (missing features)
    response = requests.post(
        "http://localhost:5000/predict",
        json={"features": [1,2,3]}  # Too short
    )
    assert response.status_code == 400

if __name__ == "__main__":
    test_prediction()
    print("All tests passed!")