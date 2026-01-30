"""
Industrial Defect Detection Module
Detects defects in manufactured parts using edge detection and contour analysis
"""

import cv2
import numpy as np
from typing import List, Tuple, Dict

class DefectDetector:
    """Detects defects in industrial parts"""
    
    def __init__(self, min_defect_size=5.0, edge_threshold1=50, edge_threshold2=150):
        """
        Initialize defect detector
        
        Args:
            min_defect_size: Minimum defect size in mm (default: 5.0)
            edge_threshold1: Canny edge detection lower threshold
            edge_threshold2: Canny edge detection upper threshold
        """
        self.min_defect_size = min_defect_size
        self.edge_threshold1 = edge_threshold1
        self.edge_threshold2 = edge_threshold2
        
    def detect_defects(self, image: np.ndarray) -> Dict:
        """
        Detect defects in an image
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            dict: Detection results with defects, annotated image, and statistics
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Canny edge detection
        edges = cv2.Canny(blurred, self.edge_threshold1, self.edge_threshold2)
        
        # Dilate edges to connect nearby edges
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=1)
        
        # Find contours
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by size and shape
        defects = []
        annotated_image = image.copy()
        
        for contour in contours:
            # Calculate contour area (in pixels, assuming 1 pixel = 0.1mm)
            area_pixels = cv2.contourArea(contour)
            area_mm = area_pixels * 0.1  # Convert to mm²
            
            # Skip small contours (noise)
            if area_mm < self.min_defect_size:
                continue
            
            # Calculate bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            
            # Calculate aspect ratio
            aspect_ratio = float(w) / h if h > 0 else 0
            
            # Calculate circularity (how close to a circle)
            perimeter = cv2.arcLength(contour, True)
            if perimeter > 0:
                circularity = 4 * np.pi * area_pixels / (perimeter * perimeter)
            else:
                circularity = 0
            
            # Classify defect type
            defect_type = self._classify_defect(area_mm, aspect_ratio, circularity)
            
            defect = {
                'type': defect_type,
                'area_mm': area_mm,
                'area_pixels': area_pixels,
                'bbox': (x, y, w, h),
                'aspect_ratio': aspect_ratio,
                'circularity': circularity,
                'contour': contour
            }
            
            defects.append(defect)
            
            # Draw defect on image
            color = self._get_defect_color(defect_type)
            cv2.drawContours(annotated_image, [contour], -1, color, 2)
            cv2.rectangle(annotated_image, (x, y), (x + w, y + h), color, 2)
            
            # Add label
            label = f"{defect_type}: {area_mm:.1f}mm²"
            cv2.putText(annotated_image, label, (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Calculate statistics
        total_defects = len(defects)
        total_area = sum(d['area_mm'] for d in defects)
        defect_types = {}
        for defect in defects:
            defect_type = defect['type']
            defect_types[defect_type] = defect_types.get(defect_type, 0) + 1
        
        return {
            'defects': defects,
            'annotated_image': annotated_image,
            'statistics': {
                'total_defects': total_defects,
                'total_area_mm': total_area,
                'defect_types': defect_types,
                'pass': total_defects == 0,
                'fail': total_defects > 0
            }
        }
    
    def _classify_defect(self, area_mm: float, aspect_ratio: float, circularity: float) -> str:
        """
        Classify defect type based on characteristics
        
        Args:
            area_mm: Defect area in mm²
            aspect_ratio: Width/height ratio
            circularity: How circular the defect is (0-1)
            
        Returns:
            str: Defect type
        """
        # Crack: long and thin
        if aspect_ratio > 3.0 or aspect_ratio < 0.33:
            return "Crack"
        
        # Hole: circular
        elif circularity > 0.7:
            return "Hole"
        
        # Irregular shape: low circularity
        elif circularity < 0.3:
            return "Irregular Shape"
        
        # Misalignment: medium size, medium aspect ratio
        elif 10 < area_mm < 50:
            return "Misalignment"
        
        # Large defect
        elif area_mm > 50:
            return "Large Defect"
        
        # Small defect
        else:
            return "Small Defect"
    
    def _get_defect_color(self, defect_type: str) -> Tuple[int, int, int]:
        """Get color for defect type"""
        colors = {
            'Crack': (0, 0, 255),  # Red
            'Hole': (255, 0, 0),   # Blue
            'Irregular Shape': (0, 165, 255),  # Orange
            'Misalignment': (0, 255, 255),  # Yellow
            'Large Defect': (255, 0, 255),  # Magenta
            'Small Defect': (0, 255, 0)  # Green (less critical)
        }
        return colors.get(defect_type, (255, 255, 255))
    
    def update_thresholds(self, threshold1: int, threshold2: int):
        """Update Canny edge detection thresholds"""
        self.edge_threshold1 = threshold1
        self.edge_threshold2 = threshold2
    
    def update_min_defect_size(self, size: float):
        """Update minimum defect size"""
        self.min_defect_size = size





