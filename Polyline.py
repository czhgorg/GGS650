#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      czhgorg
#
# Created:     28/11/2015
# Copyright:   (c) czhgorg 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import math
from Line import *


class Polyline:

    def __init__(self, points=[]):
        self.points = points

    # def getLength(self):
    #     i = 0
    #     length = 0.0
    #     while i<len(self.points)-1:
    #         length += math.sqrt((self.points[i+1].x -self.points[i].x)**2 + (self.points[i+1].y -self.points[i].y)**2 )
    #         i += 1
    #     return length

    def getMinX(self):
        minx = self.points[0].x
        for i in range(len(self.points)):
            if (self.points[i].x < minx):
                minx = self.points[i].x
        return minx

    def getMinY(self):
        miny = self.points[0].y
        for i in range(len(self.points)):
            if (self.points[i].y < miny):
                miny = self.points[i].y
        return miny

    def getMaxX(self):
        maxx = self.points[0].x
        for i in range(len(self.points)):
            if (self.points[i].x > maxx):
                maxx = self.points[i].x
        return maxx

    def getMaxY(self):
        maxy = self.points[0].y
        for i in range(len(self.points)):
            if (self.points[i].y > maxy):
                maxy = self.points[i].y
        return maxy


    #================Refer to MiniGIS================
    def intersect(self, polyline):
        interPoints = []
        for j in range(len(polyline.points)-1):
            for i in range(len(self.points)-1):
                ls1 = Line(self.points[i].x, self.points[i].y, self.points[i+1].x, self.points[i+1].y)
                ls2 = Line(polyline.points[j].x, polyline.points[j].y, polyline.points[j+1].x, polyline.points[j+1].y)
                interp = ls1.intersect(ls2)
                if interp:
                    interPoints.append(Point(int(interp.x), int(interp.y)))
                # if self.points[i].x > self.points[i+1].x:
                #     minx = self.points[i+1].x
                #     maxx = self.points[i].x
                # else:
                #     minx = self.points[i].x
                #     maxx = self.points[i+1].x
                #
                # if self.points[i].y > self.points[i+1].y:
                #     miny = self.points[i+1].y
                #     maxy = self.points[i].y
                # else:
                #     miny = self.points[i].y
                #     maxy = self.points[i+1].y
                #
                # if (polyline.points[j].x>=minx and polyline.points[j].x<=maxx) or (polyline.points[j].y>=miny and polyline.points[j].y<=maxy):
                #     ls1 = LineSeg(self.points[i].x, self.points[i].y, self.points[i+1].x, self.points[i+1].y)
                #     ls2 = LineSeg(polyline.points[j].x, polyline.points[j].y, polyline.points[j+1].x, polyline.points[j+1].y)
                #     interp = ls1.intersect(ls2)
                #     if interp:
                #         interPoints.append(Point(int(interp.x), int(interp.y)))

        return interPoints
