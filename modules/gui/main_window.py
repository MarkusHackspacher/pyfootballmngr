#!/usr/bin/env python
# coding: utf-8

# pyfootballmngr

# Copyright (C) <2012-2024> Markus Hackspacher

# This file is part of pyfootballmngr.

# pyfootballmngr is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pyfootballmngr is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pyfootballmngr.  If not, see <http://www.gnu.org/licenses/>.

from os.path import join

try:
    from PyQt6 import QtCore, QtGui, QtWidgets
    from PyQt6.QtGui import QAction
    from PyQt6.QtWidgets import QSizePolicy
except ImportError:
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtWidgets import QAction
    from PyQt5.QtWidgets.QSizePolicy import SizeHint

class PlayerModel(QtCore.QAbstractTableModel):
    """
    Method rowCount, headerData and columnCount
    of class modules.gui.main_window.PlayerModel
    overrides method
    of class PyQt5.QtCore.QAbstractItemModel.QAbstractItemModel.
    """
    def __init__(self, data, parent=None):
        """initial Player Model

        :param data:
        :param parent:
        :return:
        """
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.data = data

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        """overrides method of class PyQt5.QtCore.QAbstractItemModel.QAbstractItemModel

        :param QModelIndex_parent:
        :param args:
        :param kwargs:
        :return:
        """
        return len(self.data)

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        """overrides method of class PyQt5.QtCore.QAbstractItemModel.QAbstractItemModel

        :param p_int:
        :param Qt_Orientation:
        :param int_role:
        :return:
        """
        headers = {
            0: self.tr("ID"),
            1: self.tr("Username"),
            2: self.tr("Reg. Date"),
        }
        if Qt_Orientation == QtCore.Qt.Orientation.Horizontal and int_role == 0:
            return headers[p_int]

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        """overrides method of class PyQt5.QtCore.QAbstractItemModel.QAbstractItemModel

        :param QModelIndex_parent:
        :param args:
        :param kwargs:
        :return:
        """
        if self.data:
            return len(self.data[0])
        else:
            return 0

    def data(self, QModelIndex, int_role=None):
        """QAbstractTableModel.data() is abstract and must be overridden

        :param QModelIndex:
        :param int_role:
        :return:
        """
        if not QModelIndex.isValid():
            return None
        elif int_role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        return self.data[QModelIndex.row()][QModelIndex.column()]


class WndMain(QtWidgets.QMainWindow):
    """
    The main window
    """
    def __init__(self):
        """
        setup the main window
        :return:
        """
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowIcon(QtGui.QIcon(join("misc", "icon.ico")))
        self.centralwidget = QtWidgets.QWidget(self)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)

        self.gbPlayers = QtWidgets.QGroupBox(self.centralwidget)
        size_policy = QSizePolicy(QSizePolicy.Policy.Preferred,
                                  QSizePolicy.Policy.Preferred)
        size_policy.setHorizontalStretch(2)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.gbPlayers.sizePolicy().hasHeightForWidth())
        self.gbPlayers.setSizePolicy(size_policy)

        self.tViewPlayers = QtWidgets.QTableView(self.gbPlayers)
        self.tViewPlayers.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.tViewPlayers.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tViewPlayers.setGridStyle(QtCore.Qt.PenStyle.SolidLine)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.gbPlayers)
        self.verticalLayout_2.addWidget(self.tViewPlayers)

        self.gridLayout.addWidget(self.gbPlayers, 0, 0, 2, 1)
        self.gbLastMatches = QtWidgets.QGroupBox(self.centralwidget)
        size_policy = QSizePolicy(QSizePolicy.Policy.Preferred,
                                  QSizePolicy.Policy.Preferred)
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.gbLastMatches.sizePolicy().hasHeightForWidth())
        self.gbLastMatches.setSizePolicy(size_policy)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.gbLastMatches)
        self.lViewMatches = QtWidgets.QListWidget(self.gbLastMatches)

        self.verticalLayout_3.addWidget(self.lViewMatches)
        self.gridLayout.addWidget(self.gbLastMatches, 0, 1, 1, 2)
        self.gbPlayerInfo = QtWidgets.QGroupBox(self.centralwidget)
        size_policy = QSizePolicy(QSizePolicy.Policy.Preferred,
                                  QSizePolicy.Policy.Preferred)
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.gbPlayerInfo.sizePolicy().hasHeightForWidth())
        self.gbPlayerInfo.setSizePolicy(size_policy)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.gbPlayerInfo)

        self.lblInfo1 = QtWidgets.QLabel(self.gbPlayerInfo)
        self.lblInfo2 = QtWidgets.QLabel(self.gbPlayerInfo)
        self.lblInfo3 = QtWidgets.QLabel(self.gbPlayerInfo)

        self.verticalLayout.addWidget(self.lblInfo1)
        self.verticalLayout.addWidget(self.lblInfo2)
        self.verticalLayout.addWidget(self.lblInfo3)

        self.gridLayout.addWidget(self.gbPlayerInfo, 1, 1, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 747, 21))

        self.setMenuBar(self.menubar)
        self.actionAdd_Player = QAction(self)
        self.actionUpdate_Player = QAction(self)
        self.actionRemove_Player = QAction(self)
        self.actionAdd_Match = QAction(self)
        self.actionUpdate_Match = QAction(self)
        self.actionRemove_Match = QAction(self)
        self.actionExampleData = QAction(self)
        self.actionAbout = QAction(self)
        self.actionExit = QAction(self)

        self.menuFile = QtWidgets.QMenu(self.menubar)
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

        self.menu_help = QtWidgets.QMenu(self.menubar)
        self.menu_help.setTitle(self.tr("Help"))

        self.menu_help.addAction(self.actionAbout)
        self.menubar.addAction(self.menu_help.menuAction())

        try:
            self.tViewPlayers.horizontalHeader().setResizeMode(
                QtGui.QHeaderView.ResizeMode.Stretch)
        except AttributeError:
            self.tViewPlayers.horizontalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeMode.Stretch)

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
        self.actionAbout.setText(self.tr("About"))
        self.actionExit.setText(self.tr("Exit"))

        self.actionAdd_Player.setShortcut("Ctrl+N")
        self.actionRemove_Player.setShortcut("Del")

    def update_users(self, users):
        """
        Open update users window

        :param users:
        :return:
        """
        edited = [(id, name, rd) for id, name, rd, last in users]
        m = PlayerModel(edited)
        self.tViewPlayers.setModel(m)

    def update_matches(self, matches):
        """
        Open update matches window

        :param matches:
        :return:
        """
        self.lViewMatches.clear()
        edited = ["{0!s} - {1!s} : {2:d} - {3:d}".format(dat[3], dat[4],
                  dat[5], dat[6]) for dat in matches]
        self.lViewMatches.addItems(edited)
