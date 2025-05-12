class BreastCancerUI {
    constructor(apiUrl) {
        this.apiUrl = apiUrl;
        this.featureNames = [
            "radius_mean", "texture_mean", "perimeter_mean", "area_mean",
            "smoothness_mean", "compactness_mean", "concavity_mean",
            "concave_points_mean", "symmetry_mean", "fractal_dimension_mean",
            "radius_se", "texture_se", "perimeter_se", "area_se",
            "smoothness_se", "compactness_se", "concavity_se",
            "concave_points_se", "symmetry_se", "fractal_dimension_se",
            "radius_worst", "texture_worst", "perimeter_worst", "area_worst",
            "smoothness_worst", "compactness_worst", "concavity_worst",
            "concave_points_worst", "symmetry_worst", "fractal_dimension_worst"
        ];
        this.initializeUI();
        this.bindEvents();
    }

    initializeUI() {
        const container = document.getElementById('input-container');
        this.featureNames.forEach(feature => {
            const inputGroup = this.createInputGroup(feature);
            container.appendChild(inputGroup);
        });
    }

    createInputGroup(feature) {
        const div = document.createElement('div');
        div.className = 'input-group';
        div.innerHTML = `
            <label for="${feature}">${this.formatFeatureName(feature)}:</label>
            <input type="number" step="0.0001" id="${feature}" required>
        `;
        return div;
    }

    formatFeatureName(feature) {
        return feature
            .replace(/_/g, ' ')
            .split(' ')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    bindEvents() {
        document.getElementById('predict-btn').addEventListener('click', 
            () => this.handlePrediction());
    }

    async handlePrediction() {
        const resultDiv = document.getElementById('result');
        this.showLoading(resultDiv);
        
        try {
            const features = this.collectFeatures();
            const prediction = await this.makePrediction(features);
            this.displayResult(resultDiv, prediction);
        } catch (error) {
            this.handleError(resultDiv, error);
        }
    }

    showLoading(resultDiv) {
        resultDiv.innerHTML = '<p>Analyzing data...</p>';
        resultDiv.className = '';
    }

    collectFeatures() {
        return this.featureNames.map(feature => {
            const value = parseFloat(document.getElementById(feature).value);
            if (isNaN(value)) {
                throw new Error(`Invalid input for ${this.formatFeatureName(feature)}`);
            }
            return value;
        });
    }

    async makePrediction(features) {
        const response = await fetch(this.apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ features })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || `Server error: ${response.status}`);
        }

        return await response.json();
    }

    displayResult(resultDiv, data) {
        const predictionText = data.prediction === 1 ? 
            'Benign (non-cancerous)' : 'Malignant (cancerous)';
        const confidence = (data.confidence * 100).toFixed(2);
        
        resultDiv.className = data.prediction === 1 ? 'benign' : 'malignant';
        resultDiv.innerHTML = `
            <h2>Analysis Result: ${predictionText}</h2>
            <p>Confidence Level: ${confidence}%</p>
        `;
    }

    handleError(resultDiv, error) {
        resultDiv.className = 'error';
        resultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
        console.error('Prediction error:', error);
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new BreastCancerUI('https://breastcancerclassification.onrender.com/predict');
});