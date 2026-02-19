# cloud_loader.py
import numpy as np
import open3d as o3d
import pyvista as pv
import os

class CloudLoader:
    def __init__(self):
        self.supported_extensions = {'.pcd', '.ply', '.xyz', '.bin', '.npy'}

    def load_file(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.npy':
            return self._load_numpy(file_path)
        elif ext == '.bin':
            return self._load_kitti_bin(file_path)
        elif ext in {'.pcd', '.ply', '.xyz'}:
            return self._load_with_o3d(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def _load_with_o3d(self, path):
        # Open3D Reader
        pcd = o3d.io.read_point_cloud(path)
        if pcd.is_empty():
            raise ValueError("File is empty or corrupted.")
        points = np.asarray(pcd.points)
        return pv.PolyData(points)

    def _load_kitti_bin(self, path):
        # Binary Reader (Float32, 4 columns: x,y,z,intensity)
        data = np.fromfile(path, dtype=np.float32).reshape(-1, 4)
        return pv.PolyData(data[:, :3])

    def _load_numpy(self, path):
        # Numpy Reader
        data = np.load(path)
        # Ensure it's at least (N, 3)
        if data.ndim == 2 and data.shape[1] >= 3:
            return pv.PolyData(data[:, :3])
        raise ValueError(f"Invalid shape {data.shape} for point cloud. Expected (N, 3+)")