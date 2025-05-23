import os
import numpy as np
from PIL import Image
from flask import Flask, request, render_template, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from sklearn.cluster import KMeans
import io
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static', exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color code."""
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def extract_colors(image_path, num_colors=10):
    """Extract the most common colors from an image using K-means clustering."""
    # Open and process the image
    img = Image.open(image_path)
    
    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize image for faster processing (optional)
    img.thumbnail((150, 150))
    
    # Convert image to numpy array
    img_array = np.array(img)
    
    # Reshape the image to be a list of pixels
    pixels = img_array.reshape(-1, 3)
    
    # Remove any pixels that might be transparent or invalid
    pixels = pixels[~np.all(pixels == 0, axis=1)]
    
    # Use K-means clustering to find the most common colors
    kmeans = KMeans(n_clusters=min(num_colors, len(pixels)), random_state=42, n_init=10)
    kmeans.fit(pixels)
    
    # Get the colors and their frequencies
    colors = kmeans.cluster_centers_
    labels = kmeans.labels_
    
    # Count frequency of each cluster
    unique_labels, counts = np.unique(labels, return_counts=True)
    
    # Sort colors by frequency (most common first)
    color_counts = list(zip(colors, counts))
    color_counts.sort(key=lambda x: x[1], reverse=True)
    
    # Format the results
    color_palette = []
    for color, count in color_counts:
        # Convert numpy types to native Python types for JSON serialization
        rgb = tuple(int(c) for c in color.astype(int))
        hex_color = rgb_to_hex(rgb)
        percentage = float(count) / float(len(pixels)) * 100
        
        color_palette.append({
            'rgb': rgb,
            'hex': hex_color,
            'percentage': round(percentage, 1)
        })
    
    return color_palette

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # Extract colors from the uploaded image
            colors = extract_colors(file_path, num_colors=10)
            
            # Encode the image to base64 for display
            with open(file_path, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
            
            return jsonify({
                'success': True,
                'colors': colors,
                'image_data': img_data,
                'filename': filename
            })
            
        except Exception as e:
            return jsonify({'error': f'Error processing image: {str(e)}'}), 500
        
        finally:
            # Clean up uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)
    
    return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, JPEG, GIF, or BMP files.'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 