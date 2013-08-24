#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pyfootballmngr

Copyright (C) <2012-2013> Markus Hackspacher

This file is part of pyfootballmngr.

pyfootballmngr is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyfootballmngr is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyfootballmngr.  If not, see <http://www.gnu.org/licenses/>.
"""

from os.path import join
from PyQt4 import QtCore, QtGui


class PlayerModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.data = data

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.data)

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        headers = {
            0: self.tr("ID"),
            1: self.tr("Username"),
            2: self.tr("Reg. Date"),
        }
        if Qt_Orientation == QtCore.Qt.Horizontal and int_role == 0:
            return headers[p_int]

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        if self.data:
            return len(self.data[0])
        else:
            return 0

    def data(self, QModelIndex, int_role=None):
        if not QModelIndex.isValid():
            return QtCore.QVariant()
        elif int_role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.data[QModelIndex.row()]
         [QModelIndex.column()])


class WndMain(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowIcon(QtGui.QIcon(join("misc", "icon.ico")))
        self.centralwidget = QtGui.QWidget(self)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)

        self.gbPlayers = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(
         QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
         self.gbPlayers.sizePolicy().hasHeightForWidth())
        self.gbPlayers.setSizePolicy(sizePolicy)

        self.tViewPlayers = QtGui.QTableView(self.gbPlayers)
        self.tViewPlayers.setSelectionMode(
         QtGui.QAbstractItemView.SingleSelection)
        self.tViewPlayers.setSelectionBehavior(
         QtGui.QAbstractItemView.SelectRows)
        self.tViewPlayers.setGridStyle(QtCore.Qt.SolidLine)

        self.verticalLayout_2 = QtGui.QVBoxLayout(self.gbPlayers)
        self.verticalLayout_2.addWidget(self.tViewPlayers)

        self.gridLayout.addWidget(self.gbPlayers, 0, 0, 2, 1)
        self.gbLastMatches = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
         QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
         self.gbLastMatches.sizePolicy().hasHeightForWidth())
        self.gbLastMatches.setSizePolicy(sizePolicy)

        self.verticalLayout_3 = QtGui.QVBoxLayout(self.gbLastMatches)
        self.lViewMatches = QtGui.QListWidget(self.gbLastMatches)

        self.verticalLayout_3.addWidget(self.lViewMatches)
        self.gridLayout.addWidget(self.gbLastMatches, 0, 1, 1, 2)
        self.gbPlayerInfo = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
         QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
         self.gbPlayerInfo.sizePolicy().hasHeightForWidth())
        self.gbPlayerInfo.setSizePolicy(sizePolicy)

        self.verticalLayout = QtGui.QVBoxLayout(self.gbPlayerInfo)

        self.lblInfo1 = QtGui.QLabel(self.gbPlayerInfo)
        self.lblInfo2 = QtGui.QLabel(self.gbPlayerInfo)
        self.lblInfo3 = QtGui.QLabel(self.gbPlayerInfo)

        self.verticalLayout.addWidget(self.lblInfo1)
        self.verticalLayout.addWidget(self.lblInfo2)
        self.verticalLayout.addWidget(self.lblInfo3)

        self.gridLayout.addWidget(self.gbPlayerInfo, 1, 1, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 747, 21))

        self.setMenuBar(self.menubar)
        self.actionAdd_Player = QtGui.QAction(self)
        self.actionUpdate_Player = QtGui.QAction(self)
        self.actionRemove_Player = QtGui.QAction(self)
        self.actionAdd_Match = QtGui.QAction(self)
        self.actionUpdate_Match = QtGui.QAction(self)
        self.actionRemove_Match = QtGui.QAction(self)
        self.actionExampleData = QtGui.QAction(self)
        self.actionGo_to_the_website = QtGui.QAction(self)
        self.actionAbout = QtGui.QAction(self)
        self.actionExit = QtGui.QAction(self)

        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setTitle(self.tr("File"))

        self.menuFile.addAction(self.actionAdd_Player)
        self.menuFile.addAction(self.actionUpdate_Player)
        self.menuFile.addAction(self.actionRemove_Player)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionAdd_Match)
        self.menuFile.addAction(self.actionUpdate_Match)
        self.menuFile.addAction(self.actionRemove_Match)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExampleData)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.menu_help = QtGui.QMenu(self.menubar)
        self.menu_help.setTitle(self.tr("Help"))

        self.menu_help.addAction(self.actionGo_to_the_website)
        self.menu_help.addAction(self.actionAbout)
        self.menubar.addAction(self.menu_help.menuAction())

        self.tViewPlayers.horizontalHeader().setResizeMode(
         QtGui.QHeaderView.Stretch)

        self.setWindowTitle(self.tr("Football statistics manager"))
        self.gbPlayers.setTitle(self.tr("Players"))
        self.gbLastMatches.setTitle(self.tr("Last matches"))
        self.gbPlayerInfo.setTitle(self.tr("Information"))

        self.actionAdd_Player.setText(self.tr("Add player"))
        self.actionUpdate_Player.setText(self.tr("Update player"))
        self.actionRemove_Player.setText(self.tr("Remove player"))
        self.actionAdd_Match.setText(self.tr("Add match"))
        self.actionUpdate_Match.setText(self.tr("Update match"))
        self.actionRemove_Match.setText(self.tr("Remove match"))
        self.actionExampleData.setText(self.tr("Load example data"))
        self.actionGo_to_the_website.setText(self.tr("Go to the website"))
        self.actionAbout.setText(self.tr("About"))
        self.actionExit.setText(self.tr("Exit"))

        self.actionAdd_Player.setShortcut("Ctrl+N")
        self.actionRemove_Player.setShortcut("Del")

    def update_users(self, users):
        edited = [(id, name, rd) for id, name, rd, last in users]
        m = PlayerModel(edited)
        self.tViewPlayers.setModel(m)

    def update_matches(self, matches):
        self.lViewMatches.clear()
        edited = ["%s - %s : %d - %d" % (dat[3], dat[4], dat[5],
         dat[6]) for dat in matches]
        map(self.lViewMatches.addItem, edited)
