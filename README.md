# 🎨 Color Palette Generator

A beautiful and modern web application that extracts the top 10 most common colors from uploaded images using advanced image processing with NumPy and machine learning clustering techniques.

## Features

- **Drag & Drop Interface**: Easy-to-use drag and drop file upload
- **Multiple Format Support**: PNG, JPG, JPEG, GIF, and BMP files
- **Color Analysis**: Uses K-means clustering with NumPy for accurate color extraction
- **Beautiful UI**: Modern, responsive design with gradient backgrounds
- **Color Information**: Shows hex codes, RGB values, and percentage distribution
- **Copy to Clipboard**: Click any color to copy its hex code
- **Mobile Responsive**: Works perfectly on desktop and mobile devices

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Image Processing**: NumPy for array operations and Pillow (PIL) for image handling
- **Machine Learning**: Scikit-learn K-means clustering for color grouping
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Styling**: Modern CSS with gradients and animations

## Installation

1. **Clone or download this repository**
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note**: If you encounter NumPy compatibility issues with scikit-learn, run:
   ```bash
   pip install "numpy<2"
   ```

## Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to:
   ```
   http://localhost:8080
   ```

## How It Works

### Image Processing Algorithm

1. **Image Upload**: User uploads an image through the web interface
2. **Preprocessing**: 
   - Convert image to RGB format if needed
   - Resize image for faster processing (thumbnail to 150x150)
   - Convert to NumPy array for mathematical operations
3. **Pixel Analysis**: 
   - Reshape image array to list of RGB pixels
   - Remove any invalid/transparent pixels
4. **Color Clustering**: 
   - Apply K-means clustering to group similar colors
   - Extract cluster centers as representative colors
5. **Frequency Analysis**: 
   - Count pixels in each cluster
   - Calculate percentage distribution
6. **Results**: 
   - Sort colors by frequency (most common first)
   - Return top 10 colors with hex codes, RGB values, and percentages

### Web Interface

- **Modern Design**: Gradient backgrounds, rounded corners, and smooth animations
- **Responsive Layout**: CSS Grid for color palette display
- **Interactive Elements**: Hover effects, loading animations, and click-to-copy functionality
- **User Feedback**: Success/error messages and loading indicators

## File Structure

```
colour_palette_generator/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main web interface
└── static/
    └── uploads/          # Temporary upload directory (auto-created)
```

## API Endpoints

### GET `/`
Returns the main web interface.

### POST `/upload`
Processes uploaded image and returns color analysis.

**Request**: Multipart form data with image file
**Response**: JSON with color palette data
```json
{
    "success": true,
    "colors": [
        {
            "rgb": [255, 128, 64],
            "hex": "#ff8040", 
            "percentage": 15.3
        }
        // ... more colors
    ],
    "image_data": "base64_encoded_image",
    "filename": "uploaded_filename.jpg"
}
```

## Security Features

- **File Type Validation**: Only allows image file types
- **File Size Limit**: Maximum 16MB upload size
- **Secure Filenames**: Uses Werkzeug's secure_filename
- **Temporary Storage**: Uploaded files are automatically deleted after processing

## Browser Compatibility

- ✅ Chrome/Chromium (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)

## Example Usage

1. Visit the website at `http://localhost:8080`
2. Drag an image onto the upload area or click "Choose File"
3. Wait for processing (usually takes 1-3 seconds)
4. View the extracted color palette
5. Click any color to copy its hex code to clipboard
6. Click "Upload Another Image" to analyze a new image

## Performance Notes

- Images are resized to 150x150 pixels for faster processing
- K-means clustering is optimized for up to 10 color clusters
- Processing time is typically under 3 seconds for most images
- Temporary files are automatically cleaned up after processing

## Troubleshooting

**NumPy compatibility issues?**
- Run `pip install "numpy<2"` to downgrade to a compatible version
- This is due to scikit-learn being compiled with NumPy 1.x

**Port 8080 already in use?**
- Change the port in `app.py` (last line) to a different number
- Update the URL in your browser accordingly

**Large files taking too long?**
- The app automatically resizes images for faster processing
- Maximum file size is 16MB

**Colors don't look accurate?**
- The algorithm groups similar colors together
- Very detailed images may have colors averaged by the clustering algorithm
- Try images with more distinct color regions for better results

**Browser compatibility issues?**
- Make sure you're using a modern browser
- Enable JavaScript
- Some older browsers may not support all features

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this color palette generator!

## License

This project is open source and available under the MIT License. 