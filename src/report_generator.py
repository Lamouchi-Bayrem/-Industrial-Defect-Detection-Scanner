"""
Report Generator Module
Generates CSV reports for defect detection results
"""
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class ReportGenerator:
    """Generates CSV reports for defect detection"""
    
    def __init__(self, report_dir: str = "reports"):
        """
        Initialize report generator
        
        Args:
            report_dir: Directory to store reports
        """
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(exist_ok=True)
    
    def generate_report(self, image_name: str, detection_results: Dict, 
                       output_file: str = None) -> str:
        """
        Generate CSV report from detection results
        
        Args:
            image_name: Name of the scanned image
            detection_results: Results from defect detector
            output_file: Optional output file path
            
        Returns:
            str: Path to generated report
        """
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.report_dir / f"defect_report_{timestamp}.csv"
        else:
            output_file = Path(output_file)
        
        defects = detection_results['defects']
        statistics = detection_results['statistics']
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(['Industrial Defect Detection Report'])
            writer.writerow(['Generated:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            writer.writerow(['Image:', image_name])
            writer.writerow([])
            
            # Summary
            writer.writerow(['Summary'])
            writer.writerow(['Total Defects:', statistics['total_defects']])
            writer.writerow(['Total Defect Area (mm²):', f"{statistics['total_area_mm']:.2f}"])
            writer.writerow(['Status:', 'PASS' if statistics['pass'] else 'FAIL'])
            writer.writerow([])
            
            # Defect types breakdown
            writer.writerow(['Defect Types Breakdown'])
            for defect_type, count in statistics['defect_types'].items():
                writer.writerow([defect_type, count])
            writer.writerow([])
            
            # Detailed defect list
            writer.writerow(['Detailed Defect List'])
            writer.writerow([
                'ID', 'Type', 'Area (mm²)', 'Area (pixels)', 
                'X', 'Y', 'Width', 'Height', 'Aspect Ratio', 'Circularity'
            ])
            
            for i, defect in enumerate(defects, 1):
                x, y, w, h = defect['bbox']
                writer.writerow([
                    i,
                    defect['type'],
                    f"{defect['area_mm']:.2f}",
                    f"{defect['area_pixels']:.2f}",
                    x, y, w, h,
                    f"{defect['aspect_ratio']:.2f}",
                    f"{defect['circularity']:.2f}"
                ])
        
        return str(output_file)





