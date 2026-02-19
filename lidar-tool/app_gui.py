# app_gui.py
from PyQt5 import QtWidgets, QtCore
from pyvistaqt import QtInteractor

class LidarAppGui(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("LiDAR Visualizer")
        self.resize(1200, 800)

        self.central_widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # --- Sidebar ---
        self.sidebar_container = QtWidgets.QVBoxLayout()
        
        # File Controls
        self.btn_open_dir = QtWidgets.QPushButton("Open Directory")
        self.sidebar_container.addWidget(self.btn_open_dir)
        self.file_list = QtWidgets.QListWidget()
        self.sidebar_container.addWidget(self.file_list)
        
        # Visual Controls
        self.color_box = QtWidgets.QCheckBox("Color by Height (Z)")
        self.sidebar_container.addWidget(self.color_box)
        
        # NEW: Point Size Slider
        self.size_label = QtWidgets.QLabel("Point Size: 2")
        self.sidebar_container.addWidget(self.size_label)
        self.size_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.size_slider.setMinimum(1)
        self.size_slider.setMaximum(10)
        self.size_slider.setValue(2)
        self.sidebar_container.addWidget(self.size_slider)
        
        # Camera Views
        self.view_group = QtWidgets.QGroupBox("Camera Views")
        self.view_layout = QtWidgets.QVBoxLayout()
        self.btn_bev = QtWidgets.QPushButton("Bird's Eye View (Top)")
        self.btn_front = QtWidgets.QPushButton("Front View")
        self.btn_side = QtWidgets.QPushButton("Side View")
        self.btn_iso = QtWidgets.QPushButton("Isometric (3D)")
        self.view_layout.addWidget(self.btn_bev)
        self.view_layout.addWidget(self.btn_front)
        self.view_layout.addWidget(self.btn_side)
        self.view_layout.addWidget(self.btn_iso)
        self.view_group.setLayout(self.view_layout)
        self.sidebar_container.addWidget(self.view_group)
        
        # Info Panel
        self.info_group = QtWidgets.QGroupBox("Scan Info")
        self.info_layout = QtWidgets.QVBoxLayout()
        self.label_filename = QtWidgets.QLabel("File: None")
        self.label_points = QtWidgets.QLabel("Points: 0")
        self.info_layout.addWidget(self.label_filename)
        self.info_layout.addWidget(self.label_points)
        self.info_group.setLayout(self.info_layout)
        
        self.sidebar_container.addWidget(self.info_group)
        self.layout.addLayout(self.sidebar_container, 1)

        # --- 3D Viewport ---
        self.plotter = QtInteractor(self.central_widget)
        self.layout.addWidget(self.plotter.interactor, 4)
        
        self.plotter.set_background("black")
        self.plotter.add_axes()