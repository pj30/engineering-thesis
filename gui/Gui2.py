import sys, os
import pygame as pg
import numpy as np
from pygame.locals import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QFrame, QAction, QPushButton, QTabWidget, QVBoxLayout, QToolBar, QListWidget, QOpenGLWidget
from PyQt5.QtGui import QIcon, QCursor, QMouseEvent, QPixmap
from PyQt5.QtOpenGL import *
from PyQt5.QtCore import *
from OpenGL.GL import *
from OpenGL.GLU import *

def IX(i, j, k): return (i + (M + 2) * (j + (L + 2) * k))

class FluidSimulator(QMainWindow):

    def __init__(self):
        super(FluidSimulator, self).__init__()
        self.initUI()

    def initUI(self):
        self.hidden = True
        self.setGeometry((res_width - width) / 2, (res_height - height) / 2, width, height)
        #self.setFixedSize(width, height)
        self.setWindowTitle('Fluid Simulator')
        self.setWindowIcon(QIcon('FluidSimulatorIcon.ico'))
        self.tab_widget = TabWidget(self)
        self.gl_widget = GLWidget(self)
        self.properties_widget = PropertiesWidget(self)
        self.properties_widget.hide()
        self.toggle_btn = someW(self)
        self.toggle_btn.clicked.connect(self.showProperties)
        self.show()

    def showProperties(self):

        if self.hidden == True:
            self.properties_widget.show()
            self.hidden = False
        else:
            self.properties_widget.hide()
            self.hidden = True

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

class PropertiesWidget(QListWidget):

    def __init__(self, parent):
        super(QListWidget, self).__init__(parent)

        self.width = 300
        self.height = 550
        self.setGeometry(width - 335, 90, self.width, self.height)

class someW(QPushButton):

    def __init__(self, parent):
        super(QPushButton, self).__init__(parent)
        self.width = 25
        self.height = 552
        self.setGeometry(width - 36, 89, self.width, self.height)
        self.setCheckable(True)

class GLWidget(QOpenGLWidget):

    def __init__(self, parent):
        super(QOpenGLWidget, self).__init__(parent)

        self.width = 1278 #78
        self.height = 550
        self.frame = 0
        self.setGeometry(10, 90, self.width, self.height)
        self.startTimer(0)
        self.rotationMode = False
        self.zoomMode = False
        self.setMouseTracking(True)
        self.x_prev = 0
        self.y_prev = 0
        self.x_rotation = 0
        self.y_rotation = 0
        self.zoom = 0

        self.move = QPixmap('move.png')
        self.move_cursor = QCursor(self.move)
        self.rotate = QPixmap('rotate.png')
        self.rotate_cursor = QCursor(self.rotate)
        self.setCursor(self.move_cursor)

    def initializeGL(self):

        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

    def paintGL(self):

        self.rotationGL()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glClearColor(1,1,1,1)

        glLoadIdentity() # matrix turns back to original state

        # transmormations
        gluPerspective(45, (res_width / res_height), 1, 200)
        glTranslatef(0, 0, -50)

        glTranslatef(0, 0, self.zoom)
        glRotatef(self.y_rotation, 1, 0, 0)
        glRotatef(self.x_rotation, 0, 1, 0)

        # draw
        self.drawWithTextures()
        self.drawWithoutTextures()

        glFlush()


    def draw_cube(self, i, j, k):
                        length = 1
                        # top side
                        glBegin(GL_POLYGON)
                        glVertex3f(i, j + length, k)
                        glVertex3f(i + length, j + length, k)
                        glVertex3f(i + length, j + length, k + length)
                        glVertex3f(i, j + length, k + length)
                        glEnd()

    def mouseMoveEvent(self, event):

        self.x = event.x()
        self.y = event.y()

    def mousePressEvent(self, event):

        button = event.button()
        if button == 2:
            self.rotationMode = True

    def mouseReleaseEvent(self, event):

        button = event.button()
        if button == 2:
            self.rotationMode = False

    def wheelEvent(self, event):

        delta = event.angleDelta() / 30
        self.zoom += delta.y()

    def timerEvent(self, event):

        self.update()

    def rotationGL(self):

        if self.rotationMode:

            self.setCursor(self.rotate_cursor)

            if self.x > self.x_prev:
                self.x_rotation += 1
            elif self.x < self.x_prev:
                self.x_rotation -= 1

            if self.y > self.y_prev:
                self.y_rotation += 1
            elif self.y < self.y_prev:
                self.y_rotation -= 1

            self.x_prev = self.x
            self.y_prev = self.y
        else:
            self.setCursor(self.move_cursor)

    def drawWithoutTextures(self):

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glColor3f(1, 1, 1)
        self.draw()

    def drawWithTextures(self):

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glColor3f(0.5, 0.5, 0.25)
        self.draw()

    def draw(self):

        glEnableClientState(GL_VERTEX_ARRAY)

        for i in range(terrain_width):
            glVertexPointer(3, GL_FLOAT, 0, vertices[i,:,:])
            glDrawArrays(GL_QUAD_STRIP, 0, strips_number)

        for i in range(N + 2):
            for j in range(M + 2):
                for k in range(L + 2):
                    if array[self.frame, IX(i, j, k)] >= .15:
                        glColor3f(0, 0, 1)
                        self.draw_cube(i, j, k)
        if self.frame < 498:
            self.frame += 1
        elif self.frame == 498:
            self.frame = 0
            #print(array[self.frame, :].sum())
            #print(self.frame)

        glDisableClientState(GL_VERTEX_ARRAY)

    def draw_point(self, i, j, k):
        glBegin(GL_POINT)
        glVertex3f(i, j, k)
        glEnd()

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

N = 10
M = 10
L = 10
size_1D = N + 2
size_2D = size_1D * (M + 2)
size_3D = size_2D * (L + 2)
array = np.load('array2.npy')
a = array[0, :]
b = array[499, :]
a = np.reshape(a, (N + 2, M + 2, L + 2))
b = np.reshape(b, (N + 2, M + 2, L + 2))
print(a[1 : N, 1 : M, 1 : L].sum(), b[1 : N, 1 : M, 1 : L].sum())
res_width = 1366
res_height = 768
width = 1300
height = 650
terrain_width = 50
terrain_height = 50
strips_number = terrain_width * 2
terrain = Terrain(terrain_width, terrain_height)
vertices = terrain.generateVertices()
app = QApplication(sys.argv)
window = FluidSimulator()
sys.exit(app.exec_())
