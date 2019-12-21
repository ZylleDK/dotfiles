#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 11:10:41 2019

@author: ros
"""

import cv2

class Display:

    def __init__(self, name):
        """ Creates a window with name = 'name' """
        self.name = name
        cv2.namedWindow(self.name, cv2.WINDOW_NORMAL)

    def update(self, image):
        """ Udates the assosiated window with new image """
        cv2.imshow(self.name, image)

    def resize(self, x, y):
        """ Resize the assosiated window to specified size """
        cv2.resizeWindow(self.name, x, y)
