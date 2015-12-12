#!/usr/bin/env python
# coding: utf-8

"""
pyfootballmngr

Copyright (C) <2012-2015> Markus Hackspacher

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

import sys
from os.path import join
try:
    from PyQt5 import QtGui, QtCore, QtWidgets, uic
except ImportError:
    from PyQt4 import QtGui as QtWidgets
    from PyQt4 import QtGui, QtCore, uic

if sys.version_info < (3, 0):
    str = unicode


class DlgNewPlayer(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setWindowIcon(QtGui.QIcon(join("misc", "icon.ico")))
        self.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel |
                                          QtWidgets.QDialogButtonBox.Ok)

        self.txtName = QtWidgets.QLineEdit(self)
        self.label = QtWidgets.QLabel(self)

        self.boxLayout = QtWidgets.QBoxLayout(
            QtWidgets.QBoxLayout.TopToBottom, self)

        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(self.label, 0, 0, 1, 1)
        grid_layout.addWidget(self.txtName, 0, 1, 1, 1)

        self.boxLayout.addLayout(grid_layout)
        self.boxLayout.addWidget(self.buttonBox)

        self.label.setText(self.tr("Player"))
        self.setWindowTitle(self.tr("New Player Dialog"))
        self.txtName.setFocus()

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.close)

    def get_values(self):
        """return new playername in unicode"""
        return str(self.txtName.text())
