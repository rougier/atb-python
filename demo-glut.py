#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (C) 2009-2010 Nicolas P. Rougier
#
# Distributed under the terms of the BSD License. The full license is in
# the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------
import sys
import OpenGL.GL as gl, OpenGL.GLUT as glut
import atb
import trackball
from ctypes import *


def quit(*args, **kwargs):
    sys.exit()

def draw_background():
    viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
    gl.glDisable (gl.GL_LIGHTING)
    gl.glDisable (gl.GL_DEPTH_TEST)
    gl.glBegin(gl.GL_QUADS)
    gl.glColor(1.0,1.0,1.0)
    gl.glVertex(0,0,-1),
    gl.glVertex(viewport[2],0,-1)
    gl.glColor(0.0,0.0,1.0)
    gl.glVertex(viewport[2],viewport[3],0)
    gl.glVertex(0,viewport[3],0)
    gl.glEnd()

def draw_teapot():
    if fill.value:
        gl.glEnable (gl.GL_LIGHTING)
        gl.glEnable (gl.GL_DEPTH_TEST)
        gl.glColor3f(color[0],color[1],color[2])
        gl.glPolygonOffset (1, 1)
        gl.glEnable (gl.GL_POLYGON_OFFSET_FILL)
        if shape.value == 0:
            glut.glutSolidCube(1)
        elif shape.value == 1:
            glut.glutSolidTorus(0.25, 0.50, 32, 32)
        else:
            glut.glutSolidTeapot(.75)
    gl.glDisable (gl.GL_LIGHTING)
    gl.glDisable (gl.GL_POLYGON_OFFSET_FILL)
    gl.glEnable (gl.GL_LINE_SMOOTH)
    gl.glEnable (gl.GL_BLEND)                     
    gl.glDepthMask (gl.GL_FALSE)
    gl.glColor4f(0,0,0,.5)
    if shape.value == 0:
        glut.glutWireCube(1)
    elif shape.value == 1:
        glut.glutWireTorus(0.25, 0.50, 32, 32)
    else:
        glut.glutWireTeapot(.75)
    gl.glDepthMask (gl.GL_TRUE)

def on_reshape(width, height):
    gl.glViewport(0, 0, width, height)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(0, width, 0, height, -1, 1)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    atb.TwWindowSize(width,height)

def on_draw():        
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, diffuse)
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, ambient)
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPECULAR,specular)
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION,position)
    if lighted:
        gl.glEnable(gl.GL_LIGHT0)
    else:
        gl.glDisable(gl.GL_LIGHT0)
    draw_background()
    trackball.push()
    draw_teapot()
    trackball.pop()
    atb.TwDraw()
    glut.glutSwapBuffers()

def on_motion(x,y):
    global mouse
    viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
    _y = int(viewport[3]-y)
    dx, dy = x-mouse[0], _y-mouse[1]
    button, state = mouse[2], mouse[3]
    mouse[0], mouse[1] = x, _y
    if not atb.TwEventMouseMotionGLUT(x,y):
        if state == glut.GLUT_DOWN and button == glut.GLUT_LEFT_BUTTON:
            trackball.drag_to(x,_y,dx,dy)
    bar.update()
    glut.glutPostRedisplay()


def on_mouse(button, state, x, y):
    global mouse
    viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
    _y = int(viewport[3]-y)
    mouse[0], mouse[1], mouse[2], mouse[3] = x, _y, button, state
    if not atb.TwEventMouseButtonGLUT(button,state,x,y):
        if button == 3:
            trackball.zoom_to(x,_y,0,+3)
        elif button == 4:
            trackball.zoom_to(x,_y,0,-3)
    glut.glutPostRedisplay()

def on_keyboard(code, x, y):
    atb.TwEventKeyboardGLUT(code,x,y)
    glut.glutPostRedisplay()

def on_special(code, x, y):
    atb.TwEventSpecialLUT(code,x,y)
    glut.glutPostRedisplay()


if __name__ == '__main__':
    glut.glutInit(sys.argv)
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH)
    glut.glutInitWindowSize(800,600)
    glut.glutCreateWindow(sys.argv[0])
    atb.init()

    trackball = trackball.Trackball(45,135,1.25,4)
    mouse = [0,0,-1,-1]
    diffuse = (c_float*4)(1.0, 1.0, 1.0, 1.0)
    ambient = (c_float*4)(0.3, 0.3, 0.3, 1.0)
    specular = (c_float*4)(0.0, 0.0, 0.0, 1.0)
    position = (c_float*4)(2.0, 2.0, 2.0, 0.0)

    bar = atb.Bar(name="Controls", label='Controls', help="Scene atb",
                  position=(10, 10), size=(200, 320))
    fill = c_bool(1)
    color = (c_float * 3)(1.0,1.0,0.5)
    shape = c_int(0)
    lighted = c_bool(1)

    bar.add_var("Trackball/Phi", step=0.5,   getter=trackball._get_phi, setter=trackball._set_phi)
    bar.add_var("Trackball/Theta", step=0.5, getter=trackball._get_theta, setter=trackball._set_theta)
    bar.add_var("Trackball/Zoom", step=0.01, getter=trackball._get_zoom, setter=trackball._set_zoom)

    bar.add_var("Light/State", lighted)
    bar.add_var("Light/Position", position, vtype=atb.TW_TYPE_QUAT4F)
    bar.add_var("Light/Diffuse", diffuse)
    bar.add_var("Light/Ambient", ambient)
    bar.add_var("Light/Specular", specular)

    Shape = atb.enum("Shape", {'Cube':0, 'Torus':1, 'Teapot':2})
    bar.add_var("Object/Shape", shape, vtype=Shape)
    bar.add_var("Object/Fill", fill)
    bar.add_var("Object/Color", color)
    bar.add_separator("")
    bar.add_button("Quit", quit, key="ESCAPE", help="Quit application")

    gl.glEnable (gl.GL_BLEND)
    gl.glEnable (gl.GL_COLOR_MATERIAL)
    gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)
    gl.glBlendFunc (gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    glut.glutMouseFunc(on_mouse)
    glut.glutReshapeFunc(on_reshape)
    glut.glutDisplayFunc(on_draw)
    glut.glutPassiveMotionFunc(on_motion)
    glut.glutMotionFunc(on_motion)
    glut.glutKeyboardFunc(on_keyboard)
    glut.glutSpecialFunc(on_special)
    glut.glutMainLoop()
