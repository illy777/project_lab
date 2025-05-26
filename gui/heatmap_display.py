# Copyright (c) 2025 
# SPDX-License-Identifier: MIT
# Author: Ömer Faruk KANMAZ <kanmazomerfaruk@outlook.com>
#
# Descritpion: This module is the heatmap visualization for the EIT system, using PyQt6 and OpenCV for rendering.
## This module is the heatmap display for the EIT system, using PyQt6 and OpenCV for rendering.

import numpy as np
import cv2
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

    def update_heatmap_matplot(self, ds=[], mesh_obj=None, el_pos=None):
        """
        Displays an EIT heatmap using the same logic as eitplot, with axis numbers.
        """
        import matplotlib.pyplot as plt

        if mesh_obj is None or el_pos is None or len(ds) == 0:
            blank = np.zeros((100, 100), dtype=np.float32)
            fig, ax = plt.subplots(figsize=(3, 2.5), dpi=1200)
            ax.imshow(blank, cmap='jet', aspect='auto')
        else:
            pts = mesh_obj["node"]
            tri = mesh_obj["element"]
            #perm0 = mesh_obj["perm0"]

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
    
    def update_heatmap_opencv(self, ds=[], mesh_obj=None, el_pos=None):
        """
        Displays an EIT heatmap using OpenCV, with sophisticated color mapping and overlays.
        """
        # Set image size
        img_h, img_w = 350, 350

        # If no data, show a blank heatmap
        if mesh_obj is None or el_pos is None or len(ds) == 0:
            img = np.zeros((img_h, img_w, 3), dtype=np.uint8)
            cv2.putText(img, "No Data", (img_w//4, img_h//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,128), 2, cv2.LINE_AA)
        else:
            pts = mesh_obj["node"]
            tri = mesh_obj["element"]
            #perm0 = mesh_obj["perm0"]
            x, y = pts[:, 0], pts[:, 1]

            # Normalize coordinates to fit image
            x_norm = (x - x.min()) / (x.max() - x.min()) * (img_w - 40) + 20
            y_norm = (y - y.min()) / (y.max() - y.min()) * (img_h - 40) + 20

            # Create a blank image
            img = np.zeros((img_h, img_w, 3), dtype=np.uint8)

            # Draw triangles with color mapping
            ds_norm = np.array(ds)
            ds_norm = (ds_norm - ds_norm.min()) / (np.ptp(ds_norm) + 1e-8)  # Normalize to [0,1]
            colormap = cv2.COLORMAP_VIRIDIS

            for i, t in enumerate(tri):
                pts_tri = np.array([
                    [int(x_norm[t[0]]), int(y_norm[t[0]])],
                    [int(x_norm[t[1]]), int(y_norm[t[1]])],
                    [int(x_norm[t[2]]), int(y_norm[t[2]])]
                ])
                color_val = int(ds_norm[i] * 255)
                color = cv2.applyColorMap(np.array([[color_val]], dtype=np.uint8), colormap)[0,0].tolist()
                cv2.fillPoly(img, [pts_tri], color)

            # Draw triangle edges for clarity
            for t in tri:
                pts_tri = np.array([
                    [int(x_norm[t[0]]), int(y_norm[t[0]])],
                    [int(x_norm[t[1]]), int(y_norm[t[1]])],
                    [int(x_norm[t[2]]), int(y_norm[t[2]])]
                ])
                cv2.polylines(img, [pts_tri], isClosed=True, color=(60,60,60), thickness=1, lineType=cv2.LINE_AA)

            # Draw electrodes as red circles and label them
            for idx, e in enumerate(el_pos):
                center = (int(x_norm[e]), int(y_norm[e]))
                cv2.circle(img, center, 7, (0,0,255), -1)
                cv2.putText(img, str(idx), (center[0]+8, center[1]-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1, cv2.LINE_AA)

            # Add a colorbar (vertical, right side)
            bar_h = img_h - 40
            bar_w = 10
            colorbar = np.linspace(0, 255, bar_h).astype(np.uint8)[::-1]
            colorbar_img = cv2.applyColorMap(colorbar.reshape(-1,1), colormap)
            img[20:20+bar_h, img_w-30:img_w-30+bar_w] = colorbar_img

            # Add min/max text for colorbar
            cv2.putText(img, f"{ds_norm.max():.2f}", (img_w-28, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1)
            cv2.putText(img, f"{ds_norm.min():.2f}", (img_w-28, img_h-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1)

        # Convert to QImage and display
        qimg = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.setPixmap(pixmap.scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatio))