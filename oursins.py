# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Oursins
                                 A QGIS plugin
 Analyse en oursins
                              -------------------
        begin                : 2014-10-04
        copyright            : (C) 2014 by Lionel Cacheux
								           Sébastien Barre
        email                : lionel.cacheux@gmx.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from oursinsdialog import OursinsDialog
import os.path

import math

# Import the PyQt and QGIS libraries
from PyQt4 import QtGui, QtCore
from qgis.utils import *
# Pour afficher un message dans la barre de message
from PyQt4.QtGui import QProgressBar
from qgis.gui import QgsMessageBar
from qgis.utils import iface
import sys, os, imp

class Oursins:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'oursins_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = OursinsDialog()

    def initGui(self):
        text = QtGui.QApplication.translate("Oursins","Flow maps (oursins)", None, QtGui.QApplication.UnicodeUTF8)
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/oursins/oursins.png"),
            text, self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # text = QtGui.QApplication.translate("Oursins","Oursins", None, QtGui.QApplication.UnicodeUTF8)
        # Add toolbar button and menu item
        if hasattr( self.iface, 'addDatabaseToolBarIcon' ):
            self.iface.addVectorToolBarIcon(self.action)
        else:
            self.iface.addToolBarIcon(self.action)
        if hasattr( self.iface, 'addPluginToVectorMenu' ):
            self.iface.addPluginToVectorMenu( text, self.action )
        else:
            self.iface.addPluginToMenu(text, self.action)

    def unload(self):
        text = QtGui.QApplication.translate("Oursins","Flow maps (oursins)", None, QtGui.QApplication.UnicodeUTF8)
        if hasattr( self.iface, 'removePluginVectorMenu' ):
            self.iface.removePluginVectorMenu(text, self.action )
        else:
            self.iface.removePluginMenu( text, self.action )
        if hasattr( self.iface, 'removeVectorToolBarIcon' ):
            self.iface.removeVectorToolBarIcon(self.action)
        else:
            self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work 
    def run(self):
        # Populate the combo boxes
        self.dlg.populateLayers()
        self.dlg.populateTables()
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)

	    if self.dlg.inputFlowTable.currentText() == '' 	\
                or self.dlg.originVar.currentText() == ''	\
		or self.dlg.inputLayers.currentText() == ''  	\
                or self.dlg.geographicVar.currentText() == '' 	\
                or self.dlg.flowValue.currentText() == '':
                    zToolTip1 = QtGui.QApplication.translate("Oursins","Error", None, QtGui.QApplication.UnicodeUTF8)
                    zToolTip2 = QtGui.QApplication.translate("Oursins","Nothing to do !...", None, QtGui.QApplication.UnicodeUTF8)
	            iface.messageBar().pushMessage(zToolTip1, zToolTip2 , level = QgsMessageBar.WARNING, duration = 10)
            elif (self.dlg.shapefileOutput.isChecked() and self.dlg.outputFilename.text() == '')  :
                    zToolTip1 = QtGui.QApplication.translate("Oursins","Error", None, QtGui.QApplication.UnicodeUTF8)
                    zToolTip2 = QtGui.QApplication.translate("Oursins","no valid shapefile name for output", None, QtGui.QApplication.UnicodeUTF8)
                    iface.messageBar().pushMessage(zToolTip1, zToolTip2 , level = QgsMessageBar.WARNING, duration = 10)
            else:

		    QApplication.setOverrideCursor( QCursor( Qt.WaitCursor ) )  # processing

		    inputLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.dlg.inputLayers.currentText())[0]


		    # Restrict to selected features 
		    if inputLayer.selectedFeatures():
		        features = inputLayer.selectedFeatures()
		    else:
			features = inputLayer.getFeatures()

		    geographicIdName = self.dlg.geographicVar.currentText()
		    IdIndex = inputLayer.fieldNameIndex(geographicIdName)
		    inputTable = QgsMapLayerRegistry.instance().mapLayersByName(self.dlg.inputFlowTable.currentText())[0]
		    originVarName = self.dlg.originVar.currentText()
		    originIndex = inputTable.fieldNameIndex(originVarName)
		    destinationVarName = self.dlg.destinationVar.currentText()
		    destinationIndex = inputTable.fieldNameIndex(destinationVarName)
		    valueVarName = self.dlg.flowValue.currentText()
		    valueIndex = inputTable.fieldNameIndex(valueVarName)
		    minValue = self.dlg.minValue.value()
		    maxDistanceKM = self.dlg.maxDist.value()
	 
		    coordinates = self.createDictionnary(inputLayer,IdIndex)

		    flowTable, notInLayer = self.flowList(inputTable, originIndex, destinationIndex, valueIndex, coordinates, minValue, maxDistanceKM)
		    
		    #print flowTable

		    #Create a new lineString layer
		    attributesVar = [(QgsField("ORIGINE", QVariant.String)) , (QgsField("DEST", QVariant.String)), (QgsField("FLUX", QVariant.Double)), (QgsField("DIST_KM", QVariant.Double))]
		    crsString = inputLayer.crs().authid()  
		    outputLayer = QgsVectorLayer("LineString?crs=" + crsString, "Oursins_"+inputTable.name(), "memory")
		    outputLayer.startEditing()
		    outputLayer.dataProvider().addAttributes(attributesVar)
		    outputLayer.updateFields()
		    if self.dlg.shapefileOutput.isChecked():
			shapefilename = self.dlg.outputFilename.text()


		    linesList = []
		    for elem in flowTable:
		        outFeat = QgsFeature()
		        # Create a QgsCircularStringV2
		        circularRing = QgsCircularStringV2()
		        if elem[1] != elem[2]:
		            #vertexList =[]   
		            #vertexList = [QgsPoint(elem[3]), QgsPoint(elem[4])]
		            dX = (QgsPoint(elem[4]).x()-QgsPoint(elem[3]).x())/2
		            dY = (QgsPoint(elem[4]).y()-QgsPoint(elem[3]).y())/2
		            X2 = QgsPoint(elem[3]).x() + dX 
		            Y2 = QgsPoint(elem[3]).y() + dY					
		            if self.dlg.curved.isChecked():
		                X2 = X2 -dY/5
		                Y2 = Y2 +dX/5					
					
		            # Set first point, intermediate point for curvature and end point
		            circularRing.setPoints([QgsPointV2(elem[3]),QgsPointV2(X2, Y2),QgsPointV2(elem[4])])
		        else:
		            X2 = QgsPoint(elem[3]).x() - 500
		            Y2 = QgsPoint(elem[3]).y() + 2000
		            X3 = QgsPoint(elem[3]).x() - 1000
		            Y3 = QgsPoint(elem[3]).y()
		            # Set first point, intermediate point for curvature and end point
		            circularRing.setPoints([QgsPointV2(elem[3]),QgsPointV2(X2, Y2),QgsPointV2(X3, Y3)])
		        # Create geometry using the instance of QgsCircularStringV2
		        geom_from_curve = QgsGeometry(circularRing)
		        #outFeat.setGeometry(QgsGeometry.fromPolyline(vertexList))
		        outFeat.setGeometry(geom_from_curve)
		        outFeat.setAttributes([elem[1], elem[2], elem[0],elem[5]/1000.0])

		        linesList.append(outFeat)
		        del outFeat
          
		    outputLayer.addFeatures(linesList)
		    outputLayer.commitChanges()
		    outputLayer.setSelectedFeatures([])

		    if self.dlg.memoryLayerOutput.isChecked():       	# load memory layer in canevas
			rendererV2 = outputLayer.rendererV2()
			# style of lines
			style_path = os.path.join( os.path.dirname(__file__), "styleOursins.qml" )
			(errorMsg, result) = outputLayer.loadNamedStyle( style_path )
			QgsMapLayerRegistry.instance().addMapLayer(outputLayer)


		    elif self.dlg.shapefileOutput.isChecked():		# save shapefile 

			error = QgsVectorFileWriter.writeAsVectorFormat(outputLayer, shapefilename, "CP1250", None, "ESRI Shapefile")
			if self.dlg.addToCanevas.isChecked():	# load layer and style
			    layername = os.path.splitext(os.path.basename(str(shapefilename)))[0]
			    outputLayer = QgsVectorLayer(shapefilename, layername, "ogr")
			    rendererV2 = outputLayer.rendererV2()
			    # style of lines
			    style_path = os.path.join( os.path.dirname(__file__), "styleOursins.qml" )
			    (errorMsg, result) = outputLayer.loadNamedStyle( style_path )
			    QgsMapLayerRegistry.instance().addMapLayer(outputLayer)

		        
		    
		    del outputLayer
		    if len(flowTable) >0 :
			pass
		        #iface.messageBar().pushMessage(u"Analyse en oursins terminée  ", "Valeur(s) hors champ : %d" %(notInLayer), level = QgsMessageBar.INFO, duration = 30)
		    else:
			zToolTip1 = QtGui.QApplication.translate("Oursins","Attention", None, QtGui.QApplication.UnicodeUTF8)
		        zToolTip2 = QtGui.QApplication.translate("Oursins","No valid datas found !", None, QtGui.QApplication.UnicodeUTF8)
		        iface.messageBar().pushMessage(zToolTip1, zToolTip2 , level = QgsMessageBar.WARNING, duration = 0)
		    QApplication.restoreOverrideCursor()  # processing end


    def createDictionnary(self, inputLayer,index):  # creates a dictionnary of coordinates
        ''' 
            Extracts the coordinates of the centroids of the features from a layer and creates a dictionnary : ID -> (x,y). 
        '''
        coordinatesDictionnary = {}

	# Only selected features 
	if inputLayer.selectedFeatures():
            features = inputLayer.selectedFeatures()
        else:
	    features = inputLayer.getFeatures()

        for elem in features:
            centroid = elem.geometry().centroid().asPoint()
            IDvalue = elem.attributes()[index]
            coordinatesDictionnary[IDvalue] = centroid

        return coordinatesDictionnary



    def flowList(self, flowTable, indexOrigin, indexDestination, indexValue, coordinatesDictionnary, minValue, maxDistance):
        '''
            list of attributes for the new layer
            (flowValue, originID, destinationID, originCoordinates, destinationCoordinates, lineLength)
        '''
        linesList = []
        notInLayer = 0


        for elem in flowTable.getFeatures():
            try:
                if elem.attributes()[indexValue] and elem.attributes()[indexDestination] and elem.attributes()[indexOrigin]:# and (elem.attributes()[indexDestination] != elem.attributes()[indexOrigin]):
                    value = float(elem.attributes()[indexValue])

                    originID = elem.attributes()[indexOrigin]
                    destinationID = elem.attributes()[indexDestination]

                    if value > minValue:
                        originCoordinates = coordinatesDictionnary[originID]
                        destinationCoordinates = coordinatesDictionnary[destinationID]
                        d = QgsDistanceArea()
                        distance = d.measureLine(originCoordinates,destinationCoordinates)
                        if maxDistance == 0 or (maxDistance > 0 and distance < maxDistance * 1000) :
                            linesList.append([value,originID, destinationID, originCoordinates, destinationCoordinates, distance])

            except:
                notInLayer += 1

        return linesList, notInLayer
                    




           
