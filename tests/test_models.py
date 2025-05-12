import unittest
import pickle
from sklearn.metrics import accuracy_score

class TestModels(unittest.TestCase):
    def setUp(self):
        self.model = pickle.load(open('../models/random_forest.pkl', 'rb'))
        self.X_test, self.y_test = ...  # Load test data

    def test_accuracy(self):
        pred = self.model.predict(self.X_test)
        self.assertGreater(accuracy_score(self.y_test, pred), 0.9)

if __name__ == '__main__':
    unittest.main()