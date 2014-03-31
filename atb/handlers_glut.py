#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (C) 2009-2010  Nicolas P. Rougier
#
# Distributed under the terms of the BSD License. The full license is in
# the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------
import string
from raw import *

_pyatb_glut_key_map = {
 32: 32, #ord(' ')
 45: 45, #ord('-')
 46: 46, #ord('.')
 48: 48, #"0"
 49: 49, #1
 50: 50, #2
 51: 51, #3
 52: 52, #4
 53: 53, #5
 54: 54, #6
 55: 55, #7
 56: 56, #8
 57: 57, #'9'
 97: 65, #'a''A'
 98: 66,
 99: 67,
 100: 68,
 101: 69,
 102: 70,
 103: 71,
 104: 72,
 105: 73,
 106: 74,
 107: 75,
 108: 76,
 109: 77,
 110: 78,
 111: 79,
 112: 80,
 113: 81,
 114: 82,
 115: 83,
 116: 84,
 117: 85,
 118: 86,
 119: 87,
 120: 88,
 121: 89,
 122: 90, #'z''Z'
 65288: 8, #'\b'
 65293: 13
}

_pyatb_glut_button_map = {
 2: TW_MOUSE_LEFT, 
 4: TW_MOUSE_MIDDLE, 
 8: TW_MOUSE_RIGHT
}

_pyatb_glut_window_key_MOD_SHIFT = 1
_pyatb_glut_window_key_MOD_CTRL = 2
_pyatb_glut_window_key_MOD_ALT =4 

def map_key(key):
    return _pyatb_glut_key_map[key]

def map_button(button):
    return _pyatb_glut_button_map[button]

def map_modifiers(modifiers):
    ret = TW_KMOD_NONE
    if modifiers & _pyatb_glut_window_key_MOD_SHIFT:
        ret |= TW_KMOD_SHIFT
    if modifiers & _pyatb_glut_window_key_MOD_CTRL:
        ret |= TW_KMOD_CTRL
    if modifiers & _pyatb_glut_window_key_MOD_ALT:
        ret |= TW_KMOD_ALT
    return ret


class Handlers(object):

    def __init__(self, window):
        self.window = window

    def on_resize(self, width, height):
        TwWindowSize(width, height)

    def on_key_press(self, symbol, modifiers):
        try:
            TwKeyPressed(map_key(symbol), map_modifiers(modifiers))
            self.window.draw()
            return True
        except:
            pass 
        return False
    def on_mouse_press(self, x, y, button):
        if not button in _pyatb_glut_button_map.keys():
            return False
        if TwMouseButton(TW_MOUSE_PRESSED, map_button(button)):
            self.window.draw()
            return True

    def on_mouse_release(self, x, y, button):
        if not button in _pyatb_glut_button_map.keys():
            return False
        if TwMouseButton(TW_MOUSE_RELEASED, map_button(button)):
            self.window.draw()
            return True

    def on_mouse_drag(self, x, y, dx, dy, buttons):
        if TwMouseMotion(x, self.window.height-y):
            self.window.draw()
            return True

    def on_mouse_motion(self, x, y, dx, dy):
        if TwMouseMotion(x, self.window.height-y):
            self.window.draw()
            return True

    def on_draw(self):
        TwDraw()
