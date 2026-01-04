# Industrial Defect Detection Scanner

A GUI tool for scanning manufactured parts (e.g., circuit boards) via camera to detect defects like cracks or misalignments using edge detection and anomaly spotting.

## Features

- ✅ **Real-time Defect Detection**: Uses Canny edge detection and contour analysis
- ✅ **Multiple Defect Types**: Detects cracks, holes, misalignments, and irregular shapes
- ✅ **Camera Scanning**: Real-time scanning from webcam
- ✅ **Image Upload**: Load images from file for analysis
- ✅ **Adjustable Thresholds**: Customize detection sensitivity
- ✅ **CSV Report Export**: Generate detailed reports with defect statistics
- ✅ **Visual Annotations**: Color-coded defect highlighting
- ✅ **Statistics Dashboard**: Real-time defect count and area calculations

## Defect Types Detected

- **Crack**: Long, thin defects (high aspect ratio)
- **Hole**: Circular defects (high circularity)
- **Irregular Shape**: Non-standard defects (low circularity)
- **Misalignment**: Medium-sized positioning issues
- **Large Defect**: Defects larger than 50mm²
- **Small Defect**: Minor defects (less critical)

## Requirements

- Python 3.8+
- Webcam/Camera (optional, for scanning)
- Windows/Linux/macOS

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python run.py
   ```

## Usage

### Loading Images

1. Click **"Load Image"** to select an image file
2. Supported formats: JPG, PNG, BMP, TIFF

### Camera Scanning

1. Click **"Start Scan"** to begin real-time camera scanning
2. Position the part in front of the camera
3. Click **"Stop Scan"** when ready

### Detecting Defects

1. Load an image or use camera scan
2. Adjust detection settings if needed:
   - **Min Defect Size**: Minimum defect size in mm (default: 5.0)
   - **Edge Threshold 1**: Lower Canny threshold (default: 50)
   - **Edge Threshold 2**: Upper Canny threshold (default: 150)
3. Click **"Detect Defects"** to analyze the image
4. View results in the annotated image and statistics panel

### Exporting Results

- **Save Result**: Save the annotated image with defect markings
- **Export Report**: Generate a CSV report with detailed defect information

## Detection Algorithm

1. **Preprocessing**: Convert to grayscale and apply Gaussian blur
2. **Edge Detection**: Canny edge detection with adjustable thresholds
3. **Contour Analysis**: Find and analyze contours
4. **Defect Classification**: Classify defects based on:
   - Area (mm²)
   - Aspect ratio (width/height)
   - Circularity (how close to a circle)
5. **Visualization**: Draw color-coded annotations

## Report Format

CSV reports include:
- Summary statistics (total defects, area, status)
- Defect type breakdown
- Detailed defect list with:
  - Defect ID and type
  - Area measurements (mm² and pixels)
  - Bounding box coordinates
  - Aspect ratio and circularity

## Project Structure

```
defect_detection/
├── src/
│   ├── __init__.py
│   ├── defect_detector.py    # Core detection logic
│   ├── report_generator.py    # CSV report generation
│   └── gui.py                 # Main GUI application
├── reports/                   # Generated reports (auto-created)
├── requirements.txt
├── run.py                     # Entry point
└── README.md
```

## Technical Details

- **OpenCV**: Image processing and computer vision
- **NumPy**: Numerical operations
- **PIL/Pillow**: Image handling
- **Tkinter**: GUI framework
- **Pandas**: Data handling (for future enhancements)

## Calibration

For accurate measurements:
- Ensure consistent lighting
- Use a reference object of known size for calibration
- Adjust thresholds based on your specific use case
- The current implementation assumes 1 pixel = 0.1mm (adjust in code if needed)

## Troubleshooting

### No Defects Detected
- Lower the minimum defect size threshold
- Adjust edge detection thresholds
- Ensure good lighting and image quality
- Check that defects are visible in the original image

### Too Many False Positives
- Increase minimum defect size
- Adjust edge detection thresholds upward
- Improve image quality (reduce noise)

### Camera Not Working
- Ensure camera is connected and not used by other applications
- Check camera permissions
- Try restarting the application

## Future Enhancements

- [ ] Machine learning-based defect classification
- [ ] Calibration tool for accurate measurements
- [ ] Batch processing for multiple images
- [ ] PDF report generation
- [ ] Database integration for defect tracking
- [ ] Real-time conveyor belt simulation
- [ ] Integration with industrial cameras

## License

This project is provided as-is for educational and portfolio purposes.





