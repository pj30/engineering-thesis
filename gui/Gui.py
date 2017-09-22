import sys, os
import pygame as pg
import numpy as np
from pygame.locals import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QFrame, QAction, QPushButton, QTabWidget, QVBoxLayout, QToolBar
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtOpenGL import *
from PyQt5.QtCore import *
from OpenGL.GL import *
from OpenGL.GLU import *

class FluidSimulator(QMainWindow):

    def __init__(self):
        super(FluidSimulator, self).__init__()
        self.initUI()

    def initUI(self):

        self.setGeometry((res_width - width) / 2, (res_height - height) / 2, width, height)
        self.setFixedSize(width, height)
        self.setWindowTitle('Fluid Simulator')
        self.setWindowIcon(QIcon('FluidSimulatorIcon.ico'))

        self.tab_widget = TabWidget(self)
        self.gl_widget = GLWidget(self)

        self.show()

class TabWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)
        self.move(0, 0)
        self.resize(width, 100)

        # initialize actions
        self.new_file = QAction(QIcon('New.png'), 'new', self)
        self.new_file.triggered.connect(self.close_application)
        self.open_file = QAction(QIcon('Open.png'), 'open', self)

        # initialize tab screen
        self.tabs = QTabWidget()
        self.file_tab = QWidget()
        self.create_tab = QWidget()
        self.simulate_tab = QWidget()
        self.results_tab = QWidget()
        self.tabs.resize(res_width, res_height)

        #add tabs
        self.tabs.addTab(self.file_tab, 'file')
        self.tabs.addTab(self.create_tab, 'create')
        self.tabs.addTab(self.simulate_tab, 'simulate')
        self.tabs.addTab(self.results_tab, 'result')

        # create tabs
        self.toolbar = QToolBar(self)
        self.addFileTab()
        self.addCreateTab()
        self.addSimulateTab()
        self.addResultsTab()

        # add tabs to layout
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def close_application(self):

        sys.exit()

    def addFileTab(self):

        self.toolbar = QToolBar(self)
        self.file_tab.layout = QVBoxLayout(self)
        self.fileMenuActions()
        self.file_tab.layout.addWidget(self.toolbar)
        self.file_tab.setLayout(self.file_tab.layout)

    def addCreateTab(self):

        self.toolbar = QToolBar(self)
        self.create_tab.layout = QVBoxLayout(self)
        self.createMenuActions()
        self.create_tab.layout.addWidget(self.toolbar)
        self.create_tab.setLayout(self.create_tab.layout)

    def addSimulateTab(self):

        self.toolbar = QToolBar(self)
        self.simulate_tab.layout = QVBoxLayout(self)
        self.simulateMenuActions()
        self.simulate_tab.layout.addWidget(self.toolbar)
        self.simulate_tab.setLayout(self.simulate_tab.layout)

    def addResultsTab(self):

        self.toolbar = QToolBar(self)
        self.results_tab.layout = QVBoxLayout(self)
        self.resultsMenuActions()
        self.results_tab.layout.addWidget(self.toolbar)
        self.results_tab.setLayout(self.results_tab.layout)

    def fileMenuActions(self):

        self.toolbar.clear()
        self.toolbar.addAction(self.new_file)
        self.toolbar.addAction(self.open_file)

    def createMenuActions(self):

        self.toolbar.clear()

    def simulateMenuActions(self):

        self.toolbar.clear()
        self.toolbar.addAction(self.open_file)

    def resultsMenuActions(self):

        self.toolbar.clear()
        self.toolbar.addAction(self.open_file)

class GLWidget(QGLWidget):

    def __init__(self, parent):
        super(GLWidget, self).__init__(parent)

        self.width = 1178
        self.height = 550
        self.setGeometry(10, 90, self.width, self.height)
        self.cursor = QCursor()
        self.startTimer(0)

    def paintGL(self):

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            #glLoadIdentity()

            glColor3f(1.0, 1.5, 0.0)

            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glEnableClientState(GL_VERTEX_ARRAY)

            for i in range(terrain_width):
                glVertexPointer(3, GL_FLOAT, 0, vertices[i,:,:])
                glDrawArrays(GL_QUAD_STRIP, 0, strips_number)

            glDisableClientState(GL_VERTEX_ARRAY)
            glRotatef(1, 2, 0, 0)
            glFlush()

    def timerEvent(self, event):

        self.update()

    def initializeGL(self):

        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

        glMatrixMode(GL_PROJECTION)
        #glLoadIdentity()
        gluPerspective(45, (width / height), 0.1, 120.0)
        glTranslatef(0.0,0.0, -50)
        glRotatef(1, 0, 75, 0)
        glMatrixMode(GL_MODELVIEW)

class Terrain(object):

    def __init__(self, width, height):

        self.width = width
        self.height = height * 2
        self.center_width = self.width / 2
        self.center_height = height

    def generateVertices(self):

        vertices = np.empty((self.width, self.height, 3), dtype = float)

        for i in range(self.width):
            sum_j = 0
            add_x = 0
            add_y = 0
            for j in range(self.height):
                vertices[i, j, :] = (add_x + i - self.center_width, 0, add_y - self.center_width)
                sum_j += 1

                if (add_x == 0):
                    add_x = 1
                else:
                    add_x = 0

                if (sum_j % 2 == 0):
                    add_y += 1

        return vertices

res_width = 1366
res_height = 768
width = 1200
height = 650
terrain_width = 20
terrain_height = 20
strips_number = terrain_width * 2
terrain = Terrain(terrain_width, terrain_height)
vertices = terrain.generateVertices()
app = QApplication(sys.argv)
window = FluidSimulator()
window.show()
sys.exit(app.exec_())
