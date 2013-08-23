#!/usr/bin/env python
# coding: utf-8

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


class DlgUpdatePlayer(QtGui.QDialog):
    def __init__(self, old_player_name):
        QtGui.QDialog.__init__(self)

        self.setWindowIcon(QtGui.QIcon(join("misc", "icon.ico")))
        self.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel |
         QtGui.QDialogButtonBox.Ok)

        self.txtName = QtGui.QLineEdit(self)
        self.label = QtGui.QLabel(self)

        self.boxLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom, self)

        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(self.label, 0, 0, 1, 1)
        gridLayout.addWidget(self.txtName, 0, 1, 1, 1)

        self.boxLayout.addLayout(gridLayout)
        self.boxLayout.addWidget(self.buttonBox)

        self.label.setText(self.tr("Player"))
        self.setWindowTitle(self.tr("Update Playername Dialog"))
        self.txtName.setFocus()
        self.txtName.setText(old_player_name)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.close)

    def getValues(self):
        """return new playername in unicode"""
        return unicode(self.txtName.text())
