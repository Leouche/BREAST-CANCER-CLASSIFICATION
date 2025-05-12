from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import os
from typing import Dict, Any, Tuple

class BreastCancerPredictor:
    def __init__(self, model_path: str):
        self.model = self._load_model(model_path)
        
    def _load_model(self, model_path: str) -> Any:
        try:
            return joblib.load(model_path)
        except Exception as e:
            raise RuntimeError(f"Model initialization failed: {str(e)}")
    
    def predict(self, features: np.ndarray) -> Tuple[int, float]:
        features = features.reshape(1, -1)
        prediction = self.model.predict(features)[0]
        confidence = float(np.max(self.model.predict_proba(features))) if hasattr(self.model, "predict_proba") else 1.0
        return int(prediction), confidence

class CustomError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

def create_app() -> Flask:
    app = Flask(__name__, static_folder=None)
    CORS(app)
    
    # Configure paths
    base_dir = os.path.abspath(os.path.dirname(__file__))
    model_path = os.path.join(base_dir, '..', 'models', 'random_forest.pkl')
    frontend_dir = os.path.join(base_dir, '..', 'frontend')
    
    # Initialize predictor
    predictor = BreastCancerPredictor(model_path)
    
    @app.errorhandler(CustomError)
    def handle_custom_error(error: CustomError) -> Tuple[Dict, int]:
        return jsonify({"error": error.message}), error.status_code
    
    @app.route('/')
    def serve_frontend():
        return send_from_directory(frontend_dir, 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path: str):
        if os.path.exists(os.path.join(frontend_dir, path)):
            return send_from_directory(frontend_dir, path)
        raise CustomError("Resource not found", 404)
    
    @app.route("/predict", methods=["POST"])
    def predict():
        try:
            data = request.get_json()
            if not data or "features" not in data:
                raise CustomError("Missing 'features' in request")
                
            features = np.array(data["features"])
            if len(features) != 30:
                raise CustomError(
                    f"Invalid feature count: expected 30, got {len(features)}",
                    400
                )
            
            prediction, confidence = predictor.predict(features)
            return jsonify({
                "prediction": prediction,
                "confidence": confidence,
                "model_type": "random_forest"
            })
            
        except CustomError as e:
            raise e
        except Exception as e:
            app.logger.error(f"Prediction error: {str(e)}")
            raise CustomError("Prediction processing failed", 500)
    
    @app.route("/health")
    def health_check():
        return jsonify({
            "status": "operational",
            "model_status": "loaded",
            "feature_count": 30
        })
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000)