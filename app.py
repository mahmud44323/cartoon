from flask import Flask, request, render_template, redirect, url_for
import cv2
import numpy as np
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Ensure the uploads directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def convert(image_path):
    original_image = cv2.imread(image_path)
    Gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    Blur_image = cv2.GaussianBlur(Gray_image, (3, 3), 0)
    detect_edge = cv2.adaptiveThreshold(Blur_image, 255,
                                        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 5)

    output = cv2.bitwise_and(original_image, original_image, mask=detect_edge)

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.png')
    cv2.imwrite(output_path, output)

    return output_path

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return redirect(request.url)
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        output_image_path = convert(file_path)
        return redirect(url_for('display_image', filename='output.png'))

    return render_template('upload.html')

@app.route('/display/<filename>')
def display_image(filename):
    return render_template('display.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
