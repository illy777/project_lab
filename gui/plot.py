from PyQt5.QtWidgets import QDialog,QApplication,QGridLayout,QPushButton
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class PLOT(QDialog):
    def __init__(self):
        super().__init__()

        self.resize(600, 600)
        self.initUi()

    def initUi(self):

        self.mainLayout = QGridLayout(self)
        self.figure = Figure(figsize=(6, 4))
        self.mc = FigureCanvas(self.figure)
        self.ax1 = self.figure.add_subplot(111)

        self.water = QPushButton('water')
        self.water.setDefault(False)

        self.start = QPushButton('start')
        self.start.setDefault(False)

        self.mainLayout.addWidget(self.water, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.start, 0, 1, 1, 1)
        self.mainLayout.addWidget(self.mc, 1, 0, 8, 2)

    def eitplot(self, ds=[], mesh_obj=None, el_pos=None):
            
            pts = mesh_obj.node
            tri = mesh_obj.element
            perm0 = mesh_obj.perm
            x, y = pts[:, 0], pts[:, 1]

            self.ax1.cla()
            im=self.ax1.tripcolor(x, y, tri, ds, cmap=plt.cm.viridis)#vmin=0.1,vmax=0.7
            cb=self.figure.colorbar(im)
            #################### Display electrode points and labels#######################

            self.ax1.plot(pts[:, 0][el_pos], pts[:, 1][el_pos],'ro')
            for i, e in enumerate(el_pos):
                self.ax1.text(x[e], y[e], str(i), size=12)
            ############################################################
            text = self.ax1.text(0.5, 0.5, '', ha='center')




            self.ax1.axis('equal')
            self.mc.draw()
            self.mc.flush_events()
            cb.remove()
