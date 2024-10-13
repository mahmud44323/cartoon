from flask import Flask, request, jsonify, render_template_string
import cv2
import os
import numpy as np

app = Flask(__name__)

# Function to apply cartoon effect with enhanced quality
def convert(image):
    # Convert to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Apply bilateral filter to smooth the image
    smooth = cv2.bilateralFilter(image, d=15, sigmaColor=200, sigmaSpace=200)

    # Convert to grayscale
    gray = cv2.cvtColor(smooth, cv2.COLOR_RGB2GRAY)

    # Apply adaptive thresholding to get edges
    edges = cv2.adaptiveThreshold(gray, 255, 
                                   cv2.ADAPTIVE_THRESH_MEAN_C, 
                                   cv2.THRESH_BINARY, 
                                   blockSize=15, C=10)

    # Combine edges with the smooth image
    cartoon = cv2.bitwise_and(smooth, smooth, mask=edges)

    # Enhance colors and increase contrast
    cartoon = cv2.cvtColor(cartoon, cv2.COLOR_RGB2HSV)
    cartoon[:, :, 1] = cv2.add(cartoon[:, :, 1], 40)  # Increase saturation
    cartoon[:, :, 2] = cv2.add(cartoon[:, :, 2], 30)  # Increase value (brightness)
    cartoon = cv2.cvtColor(cartoon, cv2.COLOR_HSV2RGB)

    # Apply a small Gaussian blur to create a 3D effect
    cartoon = cv2.GaussianBlur(cartoon, (5, 5), 0)

    # Enhance edges for a more 3D look
    cartoon = cv2.addWeighted(cartoon, 1.5, cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB), -0.5, 0)

    return cartoon

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cartoon Effect</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: 'Arial', sans-serif;
            }

            body {
                background: linear-gradient(135deg, #e2e2e2, #ffffff);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                overflow: hidden;
            }

            .container {
                background: #ffffff;
                border-radius: 20px;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
                padding: 30px;
                width: 90%;
                max-width: 600px;
                text-align: center;
                position: relative;
            }

            h1 {
                margin-bottom: 20px;
                color: #333;
                font-size: 26px;
            }

            input[type="file"] {
                display: none;
            }

            label {
                background: #4CAF50;
                color: white;
                border-radius: 12px;
                padding: 15px 25px;
                cursor: pointer;
                margin: 10px 0;
                display: inline-block;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                transition: background 0.3s;
            }

            label:hover {
                background: #45a049;
            }

            button {
                background: #4CAF50;
                border: none;
                border-radius: 12px;
                color: white;
                padding: 10px 20px;
                cursor: pointer;
                font-size: 16px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                transition: background 0.3s;
            }

            button:hover {
                background: #45a049;
            }

            .result-image {
                margin-top: 20px;
                display: none;
            }

            img {
                max-width: 100%;
                border-radius: 12px;
                margin-top: 10px;
            }

            .loading {
                display: none;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 24px;
                color: #333;
            }

            .loading:before {
                content: '';
                display: inline-block;
                width: 30px;
                height: 30px;
                border: 5px solid #4CAF50;
                border-radius: 50%;
                border-top-color: transparent;
                animation: spin 1s linear infinite;
                margin-right: 10px;
            }

            @keyframes spin {
                to {
                    transform: rotate(360deg);
                }
            }

            @media (max-width: 600px) {
                .container {
                    width: 95%;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Upload Image for Cartoon Effect</h1>
            <form id="image-upload-form" action="/upload" method="post" enctype="multipart/form-data">
                <label for="file"><i class="fas fa-upload"></i> Choose File</label>
                <input type="file" name="file" id="file" accept="image/*" required>
                <button type="submit">Upload</button>
                <div class="loading">Processing...</div>
            </form>
            <div class="result-image">
                <h2>Cartoon Image:</h2>
                <img id="cartoon-image" src="" alt="Cartoon Image" style="max-width: 100%;">
            </div>
        </div>
        <script>
            document.getElementById('image-upload-form').addEventListener('submit', function(event) {
                event.preventDefault();  // Prevent default form submission

                const formData = new FormData(this);
                const loadingIndicator = document.querySelector('.loading');
                const resultImage = document.querySelector('.result-image');

                // Show loading animation
                loadingIndicator.style.display = 'block';

                fetch('/upload', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    loadingIndicator.style.display = 'none';  // Hide loading animation
                    if (data.cartoon_image_url) {
                        document.getElementById('cartoon-image').src = data.cartoon_image_url;
                        resultImage.style.display = 'block';  // Show the image container
                    } else {
                        alert(data.error);
                    }
                })
                .catch(error => {
                    loadingIndicator.style.display = 'none';  // Hide loading animation on error
                    console.error('Error:', error);
                });
            });
        </script>
    </body>
    </html>
    ''')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Read the image file into a numpy array
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    image = cv2.imread(file_path)

    # Apply the cartoon effect
    cartoon_image = convert(image)

    # Save the cartoon image
    cartoon_file_path = os.path.join('static', 'cartoon_' + file.filename)
    cv2.imwrite(cartoon_file_path, cartoon_image)

    # Return the URL of the cartoon image as JSON
    return jsonify({"cartoon_image_url": f"/static/cartoon_{file.filename}"})

if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    app.run(host='0.0.0.0', port=5001)  # Make the app accessible on all interfaces
