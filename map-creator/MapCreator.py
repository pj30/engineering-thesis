import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


vertices = ((200, 50,30), # top right
            (300, 50,30), # top left
            (200, 50,25), # bottom right
            (300, 50,25), # bottom left
            (320, 50,15), # bottom right
            (350, 50,20)) # bottom left

vertices = ((0, 0, 0), # top right
            (0, 1, 0), # top left
            (1, 0, 5), # bottom right
            (1, 1, 0), # bottom left
            (3, 2, 0), # bottom right
            (-2, 2, 0)) # bottom left
def main():
    pg.init()
    display = (800, 600)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
    glTranslatef(0.0,0.0, -50)
    glRotatef(0,0,0,0)
    #glViewport(0, 0, display[0], display[1])
    #glMatrixMode(GL_PROJECTION)
    #glLoadIdentity()
    #glOrtho(0, display[0], 0, display[1], 0, 600) # changes coordinate system - now it's from 0 to 800 and from 0 to 600
    #glMatrixMode(GL_MODELVIEW)
    pg.key.set_repeat(500, 30)
    #pg.button.set_repeat(500, 30)
    x_prev, y_prev = pg.mouse.get_pos()
    rotate = False
    while True:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    glRotatef(1, 1, 0, 0)
                if event.key == pg.K_DOWN:
                    glRotatef(-1, 1, 0, 0)
                if event.key == pg.K_LEFT:
                    glRotatef(-1, 0, 1, 0)
                if event.key == pg.K_RIGHT:
                    glRotatef(1, 0, 1, 0)
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 3:
                    rotate = True
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 3:
                    rotate = False
        if rotate:
            x, y = pg.mouse.get_pos()
            if x > x_prev:
                glRotatef(1, 0, 1, 0)
                x_prev = x
            elif x < x_prev:
                glRotatef(-1, 0, 1, 0)
                x_prev = x
            if y > y_prev:
                glRotatef(1, 1, 0, 0)
                y_prev = y
            elif y < y_prev:
                glRotatef(-1, 1, 0, 0)
                y_prev = y

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glEnableClientState(GL_VERTEX_ARRAY)

        glVertexPointer(3, GL_INT, 0, vertices)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 6)
        glDisableClientState(GL_VERTEX_ARRAY)
        pg.display.flip()
        pg.time.wait(10)

main()
