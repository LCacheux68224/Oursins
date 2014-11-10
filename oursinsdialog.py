# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OursinsDialog
                                 A QGIS plugin
 Analyse en oursins
                             -------------------
        begin                : 2014-10-04
        copyright            : (C) 2014 by Lionel Cacheux
        email                : lionel.cacheux@gmail.com
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

from PyQt4 import QtCore, QtGui
import qgis.core as qgis
from ui_oursins import Ui_Oursins
# create the dialog for zoom to point

# which provide convenience functions for handling QGIS vector layers
import sys, os, imp
import fTools
path = os.path.dirname(fTools.__file__)
ftu = imp.load_source('ftools_utils', os.path.join(path,'tools','ftools_utils.py'))


class OursinsDialog(QtGui.QDialog, Ui_Oursins):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)


	self.buttonBox.rejected.connect(self.reject)
	self.buttonBox.accepted.connect(self.accept)
        self.oldPath = ''
        self.selectFilename.clicked.connect(self.browse)
        self.shapefileOutput.toggled.connect(self.radio_shapefile)
        self.inputLayers.currentIndexChanged.connect(self.populateAttributesLayers)
        self.inputFlowTable.currentIndexChanged.connect(self.populateAttributesTables)


    def radio_filtrage(self):
            if self.filtrage.isChecked():
                    self.label_17.setEnabled(True)
                    self.label_18.setEnabled(True)

            else:
                    self.label_17.setEnabled(False)
                    self.label_18.setEnabled(False)

    def radio_shapefile(self):
            if self.shapefileOutput.isChecked():
                    self.addToCanevas.setEnabled(True)
                    self.outputFilename.setEnabled(True)
                    self.selectFilename.setEnabled(True)
                    self.label_4.setEnabled(False)

            else:
                    self.addToCanevas.setEnabled(False)
                    self.outputFilename.setEnabled(False)
                    self.outputFilename.clear()
                    self.selectFilename.setEnabled(False)
                    self.label_4.setEnabled(False)



    def browse( self ):

        fileName0 = QtGui.QFileDialog.getSaveFileName(self, 'Enregistrer sous',
                                        self.oldPath, "Shapefile (*.shp);;All files (*)")
        fileName = os.path.splitext(str(fileName0))[0]+'.shp'
        if os.path.splitext(str(fileName0))[0] != '':
            self.oldPath = os.path.dirname(fileName)
        layername = os.path.splitext(os.path.basename(str(fileName)))[0]
        if (layername=='.shp'):
            return
        self.outputFilename.setText(fileName)

    def populateLayers( self ):
	self.inputLayers.clear()     #InputLayer
        myListLayers = []
        myListLayers = ftu.getLayerNames( [ qgis.QGis.Polygon, qgis.QGis.Point ] )
        self.inputLayers.addItems( myListLayers )

    def populateTables( self ):
	self.inputFlowTable.clear()     #InputTable
        myList = []
        myList = ftu.getLayerNames([qgis.QGis.NoGeometry])
        self.inputFlowTable.addItems( myList )

    def populateAttributesLayers( self ):

        layerName = self.inputLayers.currentText()
        self.geographicVar.clear()
        if layerName != "":         
            layer = qgis.QgsMapLayerRegistry.instance().mapLayersByName(layerName)[0]
            fieldList = [field.name()
               for field in list(layer.pendingFields().toList())
               if field.type() not in (QtCore.QVariant.Double, QtCore.QVariant.Int)]
            self.geographicVar.addItems(fieldList)

    def populateAttributesTables( self ):

        layerName = self.inputFlowTable.currentText()
        self.originVar.clear()
	self.destinationVar.clear()
        self.flowValue.clear()
        if layerName != "":         
            layer = qgis.QgsMapLayerRegistry.instance().mapLayersByName(layerName)[0]
            fieldList = [field.name()
               for field in list(layer.pendingFields().toList())
               if field.type() not in (QtCore.QVariant.Double, QtCore.QVariant.Int)]
            self.originVar.addItems(fieldList)
            self.destinationVar.addItems(fieldList)
            fieldList2 = [field.name()
               for field in list(layer.pendingFields().toList())
               if field.type() in (QtCore.QVariant.Double, QtCore.QVariant.Int)]
            self.flowValue.addItems(fieldList2)


