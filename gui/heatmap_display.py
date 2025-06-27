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
            ax.imshow(blank, cmap='jet', aspect='auto', origin='upper')
        else:
            pts = mesh_obj["node"]
            tri = mesh_obj["element"]
            #perm0 = mesh_obj["perm0"]

            x, y = pts[:, 0], pts[:, 1]

            fig, ax = plt.subplots(figsize=(3, 2.5), dpi=600)
            ax.cla()
            ax.set_facecolor('black')
            fig.patch.set_facecolor('black')
            ax.tick_params(axis='x', colors='lime')
            ax.tick_params(axis='y', colors='lime')
            ax.xaxis.label.set_color('lime')
            ax.yaxis.label.set_color('lime')
            ax.title.set_color('lime')
            ax.spines['bottom'].set_color('lime')
            ax.spines['top'].set_color('lime')
            ax.spines['right'].set_color('lime')
            ax.spines['left'].set_color('lime')
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
    
    def update_heatmap_opencv(self, ds=[], mesh_obj=None, el_pos=None,
                            height=300, width=340):
        """
        Displays an EIT heat-map in a QLabel using OpenCV + Qt.

        Parameters
        ----------
        ds        : 1-D array-like, per-triangle data values
        mesh_obj  : dict with keys "node" (N×2) & "element" (M×3)
        el_pos    : sequence of node indices for electrode centres
        height    : output image height in pixels
        width     : output image width in pixels
        """

        # Image canvas
        img_h, img_w = height, width

        # ------------------------------------------------------------------
        # 1. NO DATA --> show placeholder
        # ------------------------------------------------------------------
        if mesh_obj is None or el_pos is None or len(ds) == 0:
            img = np.zeros((img_h, img_w, 3), dtype=np.uint8)
            cv2.putText(img, "No Data",
                        (img_w // 4, img_h // 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 128), 2, cv2.LINE_AA)

        # ------------------------------------------------------------------
        # 2. FULL RENDER
        # ------------------------------------------------------------------
        else:
            pts = mesh_obj["node"]      # (N, 2)
            tri = mesh_obj["element"]   # (M, 3)
            x, y = pts[:, 0], pts[:, 1]

            # ---------- coordinate normalisation ----------
            left_pad, right_pad = 20, 20
            top_pad, bottom_pad = 20, 60        # 40 px colour-bar + 20 px gap

            draw_w = img_w - left_pad - right_pad
            draw_h = img_h - top_pad - bottom_pad

            # X: simple min-max scaling → [left_pad, left_pad+draw_w]
            x_norm = (x - x.min()) / (x.max() - x.min()) * draw_w + left_pad

            # Y: scale to [0, draw_h], then invert, then shift down by top_pad
            y_norm = (y - y.min()) / (y.max() - y.min()) * draw_h
            y_norm = draw_h - y_norm               # flip vertical axis
            y_norm += top_pad

            # Blank RGB image
            img = np.zeros((img_h, img_w, 3), dtype=np.uint8)

            # ---------- colour-map normalisation ----------
            ds_norm = np.asarray(ds, dtype=float)
            ds_norm = (ds_norm - ds_norm.min()) / (np.ptp(ds_norm) + 1e-8)

            colormap = cv2.COLORMAP_VIRIDIS

            # ---------- paint each finite-element triangle ----------
            for i, t in enumerate(tri):
                pts_tri = np.array([
                    [int(x_norm[t[0]]), int(y_norm[t[0]])],
                    [int(x_norm[t[1]]), int(y_norm[t[1]])],
                    [int(x_norm[t[2]]), int(y_norm[t[2]])]
                ])
                color_val = int(ds_norm[i] * 255)
                color = cv2.applyColorMap(
                    np.array([[color_val]], dtype=np.uint8),
                    colormap
                )[0, 0].tolist()
                cv2.fillPoly(img, [pts_tri], color)

            # ---------- optional triangle outlines ----------
            for t in tri:
                pts_tri = np.array([
                    [int(x_norm[t[0]]), int(y_norm[t[0]])],
                    [int(x_norm[t[1]]), int(y_norm[t[1]])],
                    [int(x_norm[t[2]]), int(y_norm[t[2]])]
                ])
                cv2.polylines(img, [pts_tri], isClosed=True,
                            color=(60, 60, 60), thickness=1,
                            lineType=cv2.LINE_AA)

            # ---------- electrodes ----------
            for idx, e in enumerate(el_pos):
                centre = (int(x_norm[e]), int(y_norm[e]))
                cv2.circle(img, centre, 5, (10, 200, 50), -1)
                cv2.putText(img, str(idx),
                            (centre[0] + 4, centre[1] - 4),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (255, 255, 255), 1, cv2.LINE_AA)

            # ---------- horizontal colour-bar ----------
            bar_w, bar_h = img_w - 40, 8
            colorbar_y = img_h - 50            # 40 px bar + 10 px gap
            grad = np.linspace(0, 255, bar_w).astype(np.uint8)
            colorbar = cv2.applyColorMap(grad.reshape(1, -1), colormap)
            colorbar = cv2.resize(colorbar, (bar_w, bar_h),
                                interpolation=cv2.INTER_LINEAR)
            img[colorbar_y:colorbar_y + bar_h, 20:20 + bar_w] = colorbar

            # min / max labels
            cv2.putText(img, f"{ds_norm.min():.1f}", (10, img_h - 20),
                        cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.6,
                        (255, 255, 255), 1)
            cv2.putText(img, f"{ds_norm.max():.1f}", (img_w - 50, img_h - 20),
                        cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.6,
                        (255, 255, 255), 1)

        # ------------------------------------------------------------------
        # 3. Push into the QLabel
        # ------------------------------------------------------------------
        qimg = QImage(img.data, img.shape[1], img.shape[0],
                    img.strides[0], QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.setPixmap(
            pixmap.scaled(self.width(), self.height(),
                        Qt.AspectRatioMode.KeepAspectRatio)
        )
