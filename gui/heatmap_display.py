import numpy as np
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap

class HeatmapDisplay(QLabel):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(350, 250)
        self.setStyleSheet("border: 1px solid #00ff99;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("EIT Heatmap")
        self.setScaledContents(True)

    def update_heatmap(self, ds=[], mesh_obj=None, el_pos=None):
        """
        Displays an EIT heatmap using the same logic as eitplot, with axis numbers.
        """
        import matplotlib.pyplot as plt

        if mesh_obj is None or el_pos is None or len(ds) == 0:
            blank = np.zeros((100, 100), dtype=np.float32)
            fig, ax = plt.subplots(figsize=(3, 2.5), dpi=1200)
            ax.imshow(blank, cmap='jet', aspect='auto')
        else:
            pts = mesh_obj.node
            tri = mesh_obj.element
            x, y = pts[:, 0], pts[:, 1]

            fig, ax = plt.subplots(figsize=(3, 2.5), dpi=600)
            ax.cla()
            im = ax.tripcolor(x, y, tri, ds, cmap=plt.cm.viridis)
            cb = fig.colorbar(im, ax=ax)

            # Display electrode points and labels
            ax.plot(pts[:, 0][el_pos], pts[:, 1][el_pos], 'ro')
            for i, e in enumerate(el_pos):
                ax.text(x[e], y[e], str(i), size=8)
            # Optionally, add a center text like your reference
            ax.text(0.5, 0.5, '', ha='center', transform=ax.transAxes)
            ax.axis('equal')
            # Do NOT call ax.axis('off') or remove ticks

            fig.tight_layout(pad=0)
            cb.remove()

        fig.canvas.draw()
        width, height = fig.canvas.get_width_height()
        img = np.frombuffer(fig.canvas.get_renderer().buffer_rgba(), dtype=np.uint8).reshape(height, width, 4)
        img = img[..., :3]  # Drop the alpha channel to get RGB
        qimg = QImage(img.copy(), width, height, 3 * width, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.setPixmap(pixmap.scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatio))
        plt.close(fig)