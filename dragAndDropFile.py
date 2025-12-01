"""
PDF Drag and Drop File Selector
Creates a PyQt6 dialog window for dragging and dropping PDF files
"""

import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,   # type: ignore
                            QWidget, QLabel, QPushButton, QTextEdit, QFileDialog,
                            QMessageBox, QFrame) # type: ignore
from PyQt6.QtCore import Qt, pyqtSignal # type: ignore
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QFont, QPalette, QColor # type: ignore

class DropZone(QFrame):
    """Custom widget that accepts drag and drop files"""
    
    # Signal emitted when files are dropped
    files_dropped = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the drop zone appearance"""
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self.setLineWidth(2)
        self.setMidLineWidth(1)
        
        # Set minimum size
        self.setMinimumSize(400, 200)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Title label
        title_label = QLabel("📁 Drag & Drop PDF Files Here")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        # Instructions label
        instructions = QLabel(
            "• Drag PDF files into this area\n"
            "• Or click 'Browse Files' button below\n"
            "• Multiple files supported\n"
            "• Only PDF files will be accepted"
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setStyleSheet("color: gray; font-size: 12px;")
        
        # Add to layout
        layout.addStretch()
        layout.addWidget(title_label)
        layout.addWidget(instructions)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Set initial style
        self.set_normal_style()
    
    def set_normal_style(self):
        """Set normal appearance"""
        self.setStyleSheet("""
            QFrame {
                background-color: #000000;
                border: 2px dashed #cccccc;
                border-radius: 10px;
            }
        """)
    
    def set_hover_style(self):
        """Set hover appearance when dragging over"""
        self.setStyleSheet("""
            QFrame {
                background-color: #e6f3ff;
                border: 2px dashed #007acc;
                border-radius: 10px;
            }
        """)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            # Check if any of the dragged files are PDFs
            urls = event.mimeData().urls()
            has_pdf = any(url.toLocalFile().lower().endswith('.pdf') for url in urls)
            
            if has_pdf:
                event.acceptProposedAction()
                self.set_hover_style()
            else:
                event.ignore()
        else:
            event.ignore()
    
    def dragLeaveEvent(self, event):
        """Handle drag leave event"""
        self.set_normal_style()
        super().dragLeaveEvent(event)
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop event"""
        self.set_normal_style()
        
        if event.mimeData().hasUrls():
            files = []
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if os.path.isfile(file_path) and file_path.lower().endswith('.pdf'):
                    files.append(file_path)
            
            if files:
                self.files_dropped.emit(files)
                event.acceptProposedAction()
            else:
                QMessageBox.warning(self, "No PDF Files", 
                                  "Please drop only PDF files.")
        else:
            event.ignore()

class PDFDropDialog(QMainWindow):
    """Main dialog window for PDF drag and drop"""
    
    def __init__(self):
        super().__init__()
        self.selected_files = []
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main UI"""
        self.setWindowTitle("PDF File Selector - Drag & Drop")
        self.setGeometry(100, 100, 600, 500)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("🔧 PDF File Processor")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #333; margin: 10px;")
        
        # Drop zone
        self.drop_zone = DropZone()
        self.drop_zone.files_dropped.connect(self.handle_dropped_files)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Browse button
        self.browse_btn = QPushButton("📂 Browse Files")
        self.browse_btn.clicked.connect(self.browse_files)
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        # Clear button
        self.clear_btn = QPushButton("🗑️ Clear All")
        self.clear_btn.clicked.connect(self.clear_files)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        
        # Process button
        self.process_btn = QPushButton("⚡ Process PDFs")
        self.process_btn.clicked.connect(self.process_files)
        self.process_btn.setEnabled(False)
        self.process_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover:enabled {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        buttons_layout.addWidget(self.browse_btn)
        buttons_layout.addWidget(self.clear_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.process_btn)
        
        # File list display
        self.file_list = QTextEdit()
        self.file_list.setMaximumHeight(150)
        self.file_list.setPlaceholderText("Selected PDF files will appear here...")
        self.file_list.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                font-family: monospace;
                background-color: #000000;
            }
        """)
        
        # Status label
        self.status_label = QLabel("Ready to accept PDF files")
        self.status_label.setStyleSheet("color: #666; padding: 5px;")
        
        # Add all widgets to layout
        layout.addWidget(title)
        layout.addWidget(self.drop_zone)
        layout.addLayout(buttons_layout)
        layout.addWidget(QLabel("📋 Selected Files:"))
        layout.addWidget(self.file_list)
        layout.addWidget(self.status_label)
        
        central_widget.setLayout(layout)
    
    def handle_dropped_files(self, files):
        """Handle files dropped into the drop zone"""
        for file_path in files:
            if file_path not in self.selected_files:
                self.selected_files.append(file_path)
        
        self.update_file_list()
        self.status_label.setText(f"✅ Added {len(files)} PDF file(s)")
    
    def browse_files(self):
        """Open file dialog to browse for PDF files"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select PDF Files",
            "",
            "PDF Files (*.pdf);;All Files (*)"
        )
        
        if files:
            for file_path in files:
                if file_path not in self.selected_files:
                    self.selected_files.append(file_path)
            
            self.update_file_list()
            self.status_label.setText(f"✅ Added {len(files)} PDF file(s) via browse")
    
    def clear_files(self):
        """Clear all selected files"""
        self.selected_files.clear()
        self.update_file_list()
        self.status_label.setText("🗑️ All files cleared")
    
    def update_file_list(self):
        """Update the file list display"""
        if self.selected_files:
            file_text = ""
            for i, file_path in enumerate(self.selected_files, 1):
                filename = os.path.basename(file_path)
                file_size = os.path.getsize(file_path) / 1024  # KB
                file_text += f"{i}. {filename} ({file_size:.1f} KB)\n"
                file_text += f"   Path: {file_path}\n\n"
            
            self.file_list.setText(file_text.strip())
            self.process_btn.setEnabled(True)
            self.status_label.setText(f"📁 {len(self.selected_files)} PDF file(s) ready")
        else:
            self.file_list.clear()
            self.process_btn.setEnabled(False)
            self.status_label.setText("Ready to accept PDF files")
    
    def process_files(self):
        """Process the selected PDF files"""
        if not self.selected_files:
            QMessageBox.warning(self, "No Files", "Please select PDF files first.")
            return
        
        # Here you can add your PDF processing logic
        # For now, let's just show the file paths
        
        message = f"Processing {len(self.selected_files)} PDF file(s):\n\n"
        for i, file_path in enumerate(self.selected_files, 1):
            message += f"{i}. {os.path.basename(file_path)}\n"
        
        message += f"\n📂 File paths available in self.selected_files list"
        
        QMessageBox.information(self, "Processing Files", message)
        
        # Print file paths to console for development
        print("🔧 PDF File Paths:")
        for file_path in self.selected_files:
            print(f"   📄 {file_path}")
        
        self.status_label.setText("✅ Processing completed!")

def main():
    """Main function to run the application"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("PDF Drag & Drop Processor")
    app.setOrganizationName("PDF Tools")
    
    # Create and show the dialog
    dialog = PDFDropDialog()
    dialog.show()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()