import os
import random
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- AI DETECTION PLACEHOLDERS ---
# Replace these internal functions with your actual trained PyTorch/TensorFlow model inference code.

def analyze_image(file_path):
    """
    Actual Logic: 
    1. Load image via OpenCV/PIL
    2. Preprocess (Resize to 224x224, Normalize)
    3. Model prediction: model(image)
    """
    # Simulated ML model behavior for demonstration
    confidence = round(random.uniform(65.0, 99.9), 2)
    label = random.choice(["REAL", "FAKE"])
    return label, confidence

def analyze_video(file_path):
    """
    Actual Logic:
    1. Break video into frames using OpenCV
    2. Extract faces from frames
    3. Pass frames through a sequence model (RNN/LSTM/Transformer)
    """
    cap = cv2.VideoCapture(file_path)
    frame_count = 0
    # Just a sanity check to ensure OpenCV can read the video
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame_count += 1
    cap.release()
    
    # Simulated ML model behavior for demonstration
    confidence = round(random.uniform(70.0, 99.9), 2)
    label = random.choice(["REAL", "FAKE"])
    return label, confidence
# ---------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Determine file type
        file_extension = filename.rsplit('.', 1)[1].lower()
        
        try:
            if file_extension in {'png', 'jpg', 'jpeg'}:
                label, confidence = analyze_image(file_path)
                file_type = "Image"
            else:
                label, confidence = analyze_video(file_path)
                file_type = "Video"
            
            # Clean up the file after analysis if you don't want to save it permanently
            if os.path.exists(file_path):
                os.remove(file_path)

            return jsonify({
                'success': True,
                'file_type': file_type,
                'label': label,
                'confidence': f"{confidence}%"
            })

        except Exception as e:
            return jsonify({'error': f"Processing failed: {str(e)}"}), 500
            
    return jsonify({'error': 'Invalid file type. Upload images (JPG, PNG) or videos (MP4, AVI).'}), 400

if __name__ == '__main__':
    app.run(debug=True)