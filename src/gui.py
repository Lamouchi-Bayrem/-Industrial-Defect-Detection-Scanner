

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np
from pathlib import Path

from defect_detector import DefectDetector
from report_generator import ReportGenerator


class DefectDetectionGUI:
    """Main GUI application for defect detection"""
    
    def __init__(self, root):
        """
        Initialize the GUI
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Industrial Defect Detection Scanner")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2b2b2b')
        
        # Detection components
        self.detector = DefectDetector()
        self.report_generator = ReportGenerator()
        
        # Current image
        self.current_image = None
        self.current_image_path = None
        self.detection_results = None
        
        # Camera
        self.cap = None
        self.is_scanning = False
        
        # Setup UI
        self.setup_ui()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top panel - Controls
        control_frame = tk.Frame(main_frame, bg='#2b2b2b')
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # File operations
        file_frame = tk.Frame(control_frame, bg='#2b2b2b')
        file_frame.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            file_frame,
            text="📁 Load Image",
            command=self.load_image,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=8
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            file_frame,
            text="💾 Save Result",
            command=self.save_result,
            bg='#2196F3',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=8
        ).pack(side=tk.LEFT, padx=2)
        
        # Camera operations
        camera_frame = tk.Frame(control_frame, bg='#2b2b2b')
        camera_frame.pack(side=tk.LEFT, padx=5)
        
        self.scan_button = tk.Button(
            camera_frame,
            text="📷 Start Scan",
            command=self.toggle_scan,
            bg='#FF9800',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=8
        )
        self.scan_button.pack(side=tk.LEFT, padx=2)
        
        # Detection button
        detect_frame = tk.Frame(control_frame, bg='#2b2b2b')
        detect_frame.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            detect_frame,
            text="🔍 Detect Defects",
            command=self.detect_defects,
            bg='#9C27B0',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=8
        ).pack(side=tk.LEFT, padx=2)
        
        # Export report button
        tk.Button(
            control_frame,
            text="📊 Export Report",
            command=self.export_report,
            bg='#F44336',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=8
        ).pack(side=tk.RIGHT, padx=2)
        
        # Main content area
        content_frame = tk.Frame(main_frame, bg='#2b2b2b')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Images
        left_panel = tk.Frame(content_frame, bg='#2b2b2b')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Original image
        original_frame = tk.LabelFrame(
            left_panel,
            text="Original Image",
            bg='#2b2b2b',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=10,
            pady=10
        )
        original_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.original_label = tk.Label(
            original_frame,
            text="No image loaded",
            bg='#1e1e1e',
            fg='white',
            font=('Arial', 12)
        )
        self.original_label.pack(fill=tk.BOTH, expand=True)
        
        # Annotated image
        annotated_frame = tk.LabelFrame(
            left_panel,
            text="Detection Result",
            bg='#2b2b2b',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=10,
            pady=10
        )
        annotated_frame.pack(fill=tk.BOTH, expand=True)
        
        self.annotated_label = tk.Label(
            annotated_frame,
            text="No detection performed",
            bg='#1e1e1e',
            fg='white',
            font=('Arial', 12)
        )
        self.annotated_label.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Info and settings
        right_panel = tk.Frame(content_frame, bg='#2b2b2b', width=350)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right_panel.pack_propagate(False)
        
        # Statistics frame
        stats_frame = tk.LabelFrame(
            right_panel,
            text="Detection Statistics",
            bg='#2b2b2b',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=10,
            pady=10
        )
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.stats_text = tk.Text(
            stats_frame,
            bg='#1e1e1e',
            fg='#00ff00',
            font=('Consolas', 9),
            wrap=tk.WORD,
            height=15
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Settings frame
        settings_frame = tk.LabelFrame(
            right_panel,
            text="Detection Settings",
            bg='#2b2b2b',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=10,
            pady=10
        )
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Min defect size
        tk.Label(
            settings_frame,
            text="Min Defect Size (mm):",
            bg='#2b2b2b',
            fg='white',
            font=('Arial', 9)
        ).pack(anchor='w')
        self.min_size_var = tk.DoubleVar(value=5.0)
        min_size_scale = tk.Scale(
            settings_frame,
            from_=1.0,
            to=20.0,
            resolution=0.5,
            orient=tk.HORIZONTAL,
            variable=self.min_size_var,
            bg='#2b2b2b',
            fg='white',
            command=self.update_settings
        )
        min_size_scale.pack(fill=tk.X, pady=2)
        
        # Edge threshold 1
        tk.Label(
            settings_frame,
            text="Edge Threshold 1:",
            bg='#2b2b2b',
            fg='white',
            font=('Arial', 9)
        ).pack(anchor='w', pady=(10, 0))
        self.threshold1_var = tk.IntVar(value=50)
        threshold1_scale = tk.Scale(
            settings_frame,
            from_=10,
            to=200,
            orient=tk.HORIZONTAL,
            variable=self.threshold1_var,
            bg='#2b2b2b',
            fg='white',
            command=self.update_settings
        )
        threshold1_scale.pack(fill=tk.X, pady=2)
        
        # Edge threshold 2
        tk.Label(
            settings_frame,
            text="Edge Threshold 2:",
            bg='#2b2b2b',
            fg='white',
            font=('Arial', 9)
        ).pack(anchor='w', pady=(10, 0))
        self.threshold2_var = tk.IntVar(value=150)
        threshold2_scale = tk.Scale(
            settings_frame,
            from_=50,
            to=300,
            orient=tk.HORIZONTAL,
            variable=self.threshold2_var,
            bg='#2b2b2b',
            fg='white',
            command=self.update_settings
        )
        threshold2_scale.pack(fill=tk.X, pady=2)
        
        # Pause/Resume button (for scanning)
        self.pause_button = tk.Button(
            right_panel,
            text="⏸️ Pause",
            command=self.pause_scan,
            bg='#616161',
            fg='white',
            font=('Arial', 9),
            state=tk.DISABLED
        )
        self.pause_button.pack(fill=tk.X, pady=5)
    
    def load_image(self):
        """Load image from file"""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                image = cv2.imread(file_path)
                if image is None:
                    messagebox.showerror("Error", "Could not load image file")
                    return
                
                self.current_image = image
                self.current_image_path = file_path
                self.display_image(image, self.original_label)
                self.detection_results = None
                self.update_stats()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def display_image(self, image, label_widget, max_size=(600, 400)):
        """Display image in label widget"""
        if image is None:
            return
        
        # Resize image to fit
        height, width = image.shape[:2]
        scale = min(max_size[0] / width, max_size[1] / height, 1.0)
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        resized = cv2.resize(image, (new_width, new_height))
        
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_image)
        img_tk = ImageTk.PhotoImage(image=img)
        
        label_widget.config(image=img_tk, text='')
        label_widget.image = img_tk  # Keep reference
    
    def detect_defects(self):
        """Detect defects in current image"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        try:
            # Update detector settings
            self.update_settings()
            
            # Detect defects
            self.detection_results = self.detector.detect_defects(self.current_image)
            
            # Display annotated image
            annotated = self.detection_results['annotated_image']
            self.display_image(annotated, self.annotated_label)
            
            # Update statistics
            self.update_stats()
            
        except Exception as e:
            messagebox.showerror("Error", f"Detection failed: {str(e)}")
    
    def update_stats(self):
        """Update statistics display"""
        self.stats_text.delete(1.0, tk.END)
        
        if self.detection_results is None:
            self.stats_text.insert(tk.END, "No detection performed yet.\n")
            self.stats_text.insert(tk.END, "Load an image and click 'Detect Defects'.")
            return
        
        stats = self.detection_results['statistics']
        defects = self.detection_results['defects']
        
        self.stats_text.insert(tk.END, "=== DETECTION RESULTS ===\n\n")
        self.stats_text.insert(tk.END, f"Total Defects: {stats['total_defects']}\n")
        self.stats_text.insert(tk.END, f"Total Area: {stats['total_area_mm']:.2f} mm²\n\n")
        
        status = "✅ PASS" if stats['pass'] else "❌ FAIL"
        self.stats_text.insert(tk.END, f"Status: {status}\n\n")
        
        if stats['defect_types']:
            self.stats_text.insert(tk.END, "Defect Types:\n")
            for defect_type, count in stats['defect_types'].items():
                self.stats_text.insert(tk.END, f"  • {defect_type}: {count}\n")
            self.stats_text.insert(tk.END, "\n")
        
        if defects:
            self.stats_text.insert(tk.END, "Defect Details:\n")
            for i, defect in enumerate(defects, 1):
                self.stats_text.insert(tk.END, f"\n{i}. {defect['type']}\n")
                self.stats_text.insert(tk.END, f"   Area: {defect['area_mm']:.2f} mm²\n")
                x, y, w, h = defect['bbox']
                self.stats_text.insert(tk.END, f"   Position: ({x}, {y})\n")
                self.stats_text.insert(tk.END, f"   Size: {w} x {h} px\n")
    
    def update_settings(self, *args):
        """Update detector settings"""
        self.detector.update_min_defect_size(self.min_size_var.get())
        self.detector.update_thresholds(
            self.threshold1_var.get(),
            self.threshold2_var.get()
        )
    
    def toggle_scan(self):
        """Toggle camera scanning"""
        if not self.is_scanning:
            self.start_scan()
        else:
            self.stop_scan()
    
    def start_scan(self):
        """Start camera scanning"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Could not open camera")
                return
            
            self.is_scanning = True
            self.scan_button.config(text="🛑 Stop Scan")
            self.pause_button.config(state=tk.NORMAL)
            self.scan_loop()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start scan: {str(e)}")
    
    def stop_scan(self):
        """Stop camera scanning"""
        self.is_scanning = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.scan_button.config(text="📷 Start Scan")
        self.pause_button.config(state=tk.DISABLED, text="⏸️ Pause")
        self.original_label.config(image='', text="Scanning stopped")
    
    def pause_scan(self):
        """Pause/resume scanning"""
        # This is a placeholder - in a real implementation, you'd pause frame capture
        pass
    
    def scan_loop(self):
        """Camera scanning loop"""
        if not self.is_scanning:
            return
        
        ret, frame = self.cap.read()
        if ret:
            # Flip horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            self.current_image = frame.copy()
            self.display_image(frame, self.original_label)
        
        # Continue loop
        self.root.after(30, self.scan_loop)
    
    def save_result(self):
        """Save detection result image"""
        if self.detection_results is None:
            messagebox.showwarning("Warning", "No detection result to save")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Result",
            defaultextension=".jpg",
            filetypes=[
                ("JPEG", "*.jpg"),
                ("PNG", "*.png"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                cv2.imwrite(file_path, self.detection_results['annotated_image'])
                messagebox.showinfo("Success", f"Result saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def export_report(self):
        """Export detection report to CSV"""
        if self.detection_results is None:
            messagebox.showwarning("Warning", "No detection results to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export Report",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                image_name = Path(self.current_image_path).name if self.current_image_path else "Camera Scan"
                report_path = self.report_generator.generate_report(
                    image_name,
                    self.detection_results,
                    file_path
                )
                messagebox.showinfo("Success", f"Report exported to {report_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export report: {str(e)}")
    
    def on_closing(self):
        """Handle window closing"""
        self.stop_scan()
        self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = DefectDetectionGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()





