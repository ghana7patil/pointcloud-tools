# main.py
import sys
import os

if sys.platform.startswith("linux"):
    os.environ["QT_QPA_PLATFORM"] = "xcb"

from PyQt5 import QtWidgets, QtCore
import numpy as np

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)

from app_gui import LidarAppGui
from cloud_loader import CloudLoader

class LidarController(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.app = QtWidgets.QApplication(sys.argv)
        
        self.loader = CloudLoader()
        self.gui = LidarAppGui()
        
        self.current_dir = ""
        self._first_load_done = False

        # Connect Signals
        self.gui.btn_open_dir.clicked.connect(self.select_directory)
        self.gui.file_list.itemSelectionChanged.connect(self.load_selected_file)
        self.gui.color_box.stateChanged.connect(self.reload_visualization)
        
        # NEW: Connect View & Slider Signals
        self.gui.size_slider.valueChanged.connect(self.update_point_size)
        self.gui.btn_bev.clicked.connect(lambda: self.gui.plotter.view_xy())    # Top/BEV
        self.gui.btn_front.clicked.connect(lambda: self.gui.plotter.view_xz())  # Front
        self.gui.btn_side.clicked.connect(lambda: self.gui.plotter.view_yz())   # Side
        self.gui.btn_iso.clicked.connect(lambda: self.gui.plotter.view_isometric()) # 3D
        
        self.gui.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Right:
                self.navigate_list(1)
                return True
            elif event.key() == QtCore.Qt.Key_Left:
                self.navigate_list(-1)
                return True
        return super().eventFilter(source, event)

    def select_directory(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self.gui, "Select Data Directory")
        if directory:
            self.current_dir = directory
            self.refresh_file_list()

    def refresh_file_list(self):
        self.gui.file_list.clear()
        if not self.current_dir: return
        
        all_files = os.listdir(self.current_dir)
        valid_files = [f for f in all_files if os.path.splitext(f)[1].lower() in self.loader.supported_extensions]
        valid_files.sort()
        self.gui.file_list.addItems(valid_files)

    def navigate_list(self, direction):
        if self.gui.file_list.count() == 0: return
        
        current_row = self.gui.file_list.currentRow()
        next_row = current_row + direction
        if 0 <= next_row < self.gui.file_list.count():
            self.gui.file_list.setCurrentRow(next_row)

    def update_point_size(self):
        val = self.gui.size_slider.value()
        self.gui.size_label.setText(f"Point Size: {val}")
        self.reload_visualization()

    def reload_visualization(self):
        self.load_selected_file(reset_camera=False)

    def load_selected_file(self, reset_camera=True):
        items = self.gui.file_list.selectedItems()
        if not items: return
        
        filename = items[0].text()
        file_path = os.path.join(self.current_dir, filename)
        
        try:
            cloud = self.loader.load_file(file_path)
            self.update_plot(cloud, reset_camera)
            
            self.gui.label_filename.setText(f"File: {filename}")
            self.gui.label_points.setText(f"Points: {cloud.n_points}")
            
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            QtWidgets.QMessageBox.critical(self.gui, "Load Error", str(e))

    def update_plot(self, cloud, reset_camera):
        self.gui.plotter.clear()
        
        p_size = self.gui.size_slider.value()
        
        if self.gui.color_box.isChecked():
            z_values = cloud.points[:, 2] 
            self.gui.plotter.add_mesh(
                cloud, scalars=z_values, cmap="viridis", 
                point_size=p_size, render_points_as_spheres=True, name="main_cloud"
            )
        else:
            self.gui.plotter.add_mesh(
                cloud, color="white", point_size=p_size, 
                render_points_as_spheres=True, name="main_cloud"
            )
        
        if reset_camera and not self._first_load_done:
            self.gui.plotter.reset_camera()
            self._first_load_done = True

    def run(self):
        self.gui.show()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    controller = LidarController()
    controller.run()