#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      czhgorg
#
# Created:     29/11/2015
# Copyright:   (c) czhgorg 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from Polyline import *
from Point import *

#=================Function for calculating minimium and maximium of x and y=================
def calMinAndMax(polylines):

    minx = polylines[0].getMinX()
    miny = polylines[0].getMinY()
    maxx = polylines[0].getMaxX()
    maxy = polylines[0].getMaxY()

    for i in range(len(polylines)):
        if (polylines[i].getMinX() < minx):
            minx = polylines[i].getMinX()
        if (polylines[i].getMinY() < miny):
            miny = polylines[i].getMinY()
        if (polylines[i].getMaxX() > maxx):
            maxx = polylines[i].getMaxX()
        if (polylines[i].getMaxY() > maxy):
            maxy = polylines[i].getMaxY()

    minAndMax = [minx, miny, maxx, maxy]
    return minAndMax



#=================Function for calculating ratio=================
def calRatio(polylines, windowsX, windowsY):

    minx = calMinAndMax(polylines)[0]
    miny = calMinAndMax(polylines)[1]
    maxx = calMinAndMax(polylines)[2]
    maxy = calMinAndMax(polylines)[3]

    ratioX = (maxx-minx)/windowsX
    ratioY = (maxy-miny)/windowsY

    if ratioX>ratioY:
        return ratioX
    else:
        return ratioY



#=================Function for calibrating coordinates for diplaying=================
# def calibrate(polylines, windowsX, windowsY):
#
#     caliPolylines = []
#     ratio = calRatio(polylines, windowsX, windowsY)
#     minx = calMinAndMax(polylines)[0]
#     miny = calMinAndMax(polylines)[1]
#     #print "ratio:",ratio
#
#     for i in range(len(polylines)):
#         #print "polyline",i,":"
#         points = []
#         for j in range(len(polylines[i].points)):
#             points.append(Point((polylines[i].points[j].x-minx)/ratio, windowsY-(polylines[i].points[j].y-miny)/ratio))
#         caliPolylines.append(Polyline(points))
#
#     return caliPolylines



def caliLayers(allPolylines, windowsX, windowsY, scale):

    caliAllPolylines = []
    ratio = calRatio(allPolylines[0], windowsX, windowsY)
    minx = calMinAndMax(allPolylines[0])[0]
    miny = calMinAndMax(allPolylines[0])[1]

    for polylines in allPolylines:
        if calRatio(polylines, windowsX, windowsY)>ratio:
            ratio = calRatio(polylines, windowsX, windowsY)
        if calMinAndMax(polylines)[0]<minx:
            minx = calMinAndMax(polylines)[0]
        if calMinAndMax(polylines)[1]<miny:
            miny = calMinAndMax(polylines)[1]

    for polylines in allPolylines:
        caliPolylines = []
        for i in range(len(polylines)):
            points = []
            for j in range(len(polylines[i].points)):
                points.append(Point((polylines[i].points[j].x-minx)*scale/ratio, windowsY-(polylines[i].points[j].y-miny)*scale/ratio))
            caliPolylines.append(Polyline(points))
        caliAllPolylines.append(caliPolylines)

    return caliAllPolylines