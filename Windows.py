#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      czhgorg
#
# Created:     29/11/2015
# Copyright:   (c) czhgorg 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import Tkinter
import tkMessageBox, tkFileDialog
import struct
import time
from Polyline import *
from Point import *
import Calibration

class Windows:

    def __init__(self, winWidth, winHeight):
        #----------------Initialize the attributes of the class----------------
        self.winWidth = winWidth
        self.winHeight = winHeight
        self.scale = 2
        self.maxScale = 16.0
        self.curScale = 1
        self.root = Tkinter.Tk()
        self.root.title('GGS 650 Project (Author: Chen Zhang)')
        self.canvas = Tkinter.Canvas(self.root, height = winHeight, width = winWidth, borderwidth=0, highlightthickness=0, background='white')
        self.allPolylines = []
        self.allCaliPolylines = []
        self.colors = []
        self.intersections = []

        #----------------Set the window----------------
        #--------Add buttons to top of the windows--------
        self.addButtons()
        #--------Set horizontal scrollbar--------
        self.hbar = Tkinter.Scrollbar(self.canvas, orient=Tkinter.HORIZONTAL)
        self.hbar.pack(side=Tkinter.BOTTOM, fill=Tkinter.Y, ipadx=self.winWidth/2)
        self.hbar.config(command=self.canvas.xview)
        #--------Set vertical scrollbar--------
        self.vbar = Tkinter.Scrollbar(self.canvas, orient=Tkinter.VERTICAL)
        self.vbar.pack(side=Tkinter.RIGHT, fill=Tkinter.X, ipady=self.winHeight/2)
        self.vbar.config(command=self.canvas.yview)
        #--------Set canvas--------
        self.canvas.config(width=self.winWidth, height=self.winHeight)
        self.canvas.config(scrollregion=[0, 0, int(self.winWidth*self.curScale), int(self.winHeight*self.curScale)])
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas.pack(side=Tkinter.BOTTOM, expand=Tkinter.YES, fill=Tkinter.BOTH)

        self.layer1 = 0
        self.layer2 = 0


    #================Add buttons================
    def addButtons(self):
        frame = Tkinter.Frame(self.root)
        frame.pack(side=Tkinter.TOP, fill=Tkinter.BOTH)

        #----------------Drawing roads----------------
        def __drawRoadsHandler():
            if self.layer1==0:
                shpFile = tkFileDialog.askopenfilename(parent=self.root, initialdir=".", title='Please select a shpfile', defaultextension='.shp', filetypes=(("shp file", "*.shp"),("all files", "*.*")))
                self.addLayer(shpFile,"red")
                self.layer1 = 1
            else:
                tkMessageBox.showinfo("NOTE", "Please clean the canvas if you want to reload layer 1")

        #----------------Drawing roads----------------
        def __drawRiversHandler():
            if self.layer2==0:
                shpFile = tkFileDialog.askopenfilename(parent=self.root, initialdir=".", title='Please select a shpfile', defaultextension='.shp', filetypes=(("shp file", "*.shp"),("all files", "*.*")))
                self.addLayer(shpFile,"blue")
                self.layer2 = 1
            else:
                tkMessageBox.showinfo("NOTE", "Please clean the canvas if you want to reload layer 2")

        def __cleanCanvasHandler():
            self.canvas.delete("all")
            self.layer1 = 0
            self.layer2 = 0
            self.curScale = 1
            self.allPolylines = []
            self.allCaliPolylines = []
            self.colors = []
            self.intersections = []


        #----------------Zooming in----------------
        def __zoomInHandler():
            if self.curScale<self.maxScale:
                self.curScale = self.curScale*self.scale
                self.canvas.scale("all", 0, 0, self.scale, self.scale)
                canvasHeight = self.winHeight*self.curScale
                canvasWidth = self.winWidth*self.curScale
                self.canvas.config(scrollregion=[0,0, int(canvasWidth), int(canvasHeight)])
                print("zoomInHandler, scale", self.curScale)
            else:
                tkMessageBox.showinfo("Oops", "This is the maximum canvas size")

        #----------------Zooming out----------------
        def __zoomOutHandler():
            if self.curScale>0.5:
                scale = 0.5
                self.curScale = self.curScale*scale
                self.canvas.scale("all", 0, 0, scale, scale)
                canvasHeight = self.winHeight*self.curScale
                canvasWidth = self.winWidth*self.curScale
                self.canvas.config(scrollregion=[0,0, int(canvasWidth), int(canvasHeight)])
                print("zoomOutHandle, scale:", self.curScale)
            else:
                tkMessageBox.showinfo("Oops", "This is the minimum canvas size")

        #----------------Zooming to default window size----------------
        def __defaultScaleHandler():
            self.canvas.scale("all", 0, 0, 1/self.curScale, 1/self.curScale)
            self.curScale = 1.0
            self.canvas.config(scrollregion=[0, 0, int(self.winWidth), int(self.winHeight)])

        #----------------Intersection----------------
        def __intersectionHandler():
            starttime = time.clock()
            for i in range(len(self.allCaliPolylines)):
                for j in range(len(self.allCaliPolylines)):
                    if i!=j:
                        layer1 = self.allCaliPolylines[i]
                        layer2 = self.allCaliPolylines[j]
                        for polyline1 in layer1:
                            minx1 = polyline1.getMinX()
                            miny1 = polyline1.getMinY()
                            maxx1 = polyline1.getMaxX()
                            maxy1 = polyline1.getMaxY()
                            for polyline2 in layer2:
                                minx2 = polyline2.getMinX()
                                miny2 = polyline2.getMinY()
                                maxx2 = polyline2.getMaxX()
                                maxy2 = polyline2.getMaxY()
                                if (minx1>maxx2)or(maxx1<minx2)or(minx2>maxx1)or(maxx2<minx1)or(miny1>maxy2)or(maxy1<miny2)or(miny2>maxy1)or(maxy2<miny1):
                                    pass
                                else:
                                    intersections = polyline1.intersect(polyline2)
                                    if len(intersections)>0:
                                        self.intersections.append(intersections[0])

            for point in self.intersections:
                self.canvas.scale(self.canvas.create_oval(int(point.x)-30, int(point.y)-30, int(point.x)+30, int(point.y)+30, fill = "yellow", width = 1), 0, int(self.winHeight*self.curScale), self.curScale/self.maxScale, self.curScale/self.maxScale)
            print str(time.clock()-starttime) + ' seconds'
            print len(self.intersections)

        #----------------Quit function----------------
        def __quitHandler():
            print 'GoodBye'
            self.root.destroy()

        #----------------Add buttons to the window----------------
        drawRoads = Tkinter.Button(frame, width = 12, text='Layer1',fg="white", background="red", command=__drawRoadsHandler)
        drawRoads.pack(side = Tkinter.LEFT)
        drawRivers = Tkinter.Button(frame, width = 12,text= 'Layer2',fg="white", background="blue", command=__drawRiversHandler)
        drawRivers.pack(side = Tkinter.LEFT)
        cleanCanvas = Tkinter.Button(frame, width = 12,text= 'Clean Canvas',fg="black", command=__cleanCanvasHandler)
        cleanCanvas.pack(side = Tkinter.LEFT)
        zoomIn = Tkinter.Button(frame, width = 12,text= 'Zoom In',fg="black", command=__zoomInHandler)
        zoomIn.pack(side = Tkinter.LEFT)
        zoomOut = Tkinter.Button(frame, width = 12, text= 'Zoom Out',fg="black", command=__zoomOutHandler)
        zoomOut.pack(side = Tkinter.LEFT)
        defaultScale = Tkinter.Button(frame, width = 12,text= 'Zoom To Layer',fg="black", command=__defaultScaleHandler)
        defaultScale.pack(side = Tkinter.LEFT)
        intersection = Tkinter.Button(frame, width = 12,text= 'Intersection',fg="black", command=__intersectionHandler)
        intersection.pack(side = Tkinter.LEFT)
        quit = Tkinter.Button(frame, width = 12,text= 'Quit',fg="black", command=__quitHandler)
        quit.pack(side = Tkinter.LEFT)


    #========================Read shapefiles and add polylines to layer================
    def addLayer(self, shp_file1, color):

        self.colors.append(color)

        #----------------Read polylines in shp file----------------
        #shp_file = open(fileName+'.shp','rb')
        shp_file = open(shp_file1,'rb')
        fileLength = struct.unpack('>iiiiiii', shp_file.read(28))[6]
        offset = 100
        shp_file.seek(offset)
        polylines = []
        while offset<fileLength*2:
            #--------Read the parts index
            shp_file.read(44)
            partsNumber, pointsNumber = struct.unpack('<ii', shp_file.read(8))
            s = shp_file.read(4*partsNumber)
            offset += 44+8+4*partsNumber
            #--------Save points of the polyline in the list
            points = []
            for i in range(pointsNumber):
                x, y = struct.unpack('<dd', shp_file.read(16))
                offset += 16
                point = Point(int(x),int(y))
                points.append(point)
            #--------Save polylines in the list
            polyline = Polyline(points)
            polylines.append(polyline)

        self.allPolylines.append(polylines)
        self.allCaliPolylines = Calibration.caliLayers(self.allPolylines, self.winWidth, self.winHeight, self.maxScale)
        self.canvas.delete("all")
        self.refreshWindows()


    def refreshWindows(self):

        colorNum = 0
        for caliPolylines in self.allCaliPolylines:
            for i in range(len(caliPolylines)):
                for j in range(len(caliPolylines[i].points)-1):
                    self.canvas.create_line(caliPolylines[i].points[j].x, caliPolylines[i].points[j].y, caliPolylines[i].points[j+1].x, caliPolylines[i].points[j+1].y, fill=self.colors[colorNum], width=2)
            colorNum += 1

        self.canvas.scale("all", 0, int(self.winHeight*self.curScale), self.curScale/self.maxScale, self.curScale/self.maxScale)
