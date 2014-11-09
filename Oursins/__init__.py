# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Oursins
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
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load Oursins class from file Oursins
    from oursins import Oursins
    return Oursins(iface)
