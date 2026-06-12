#!/usr/bin/env python
# coding: utf-8

"""
pyfootballmngr

Copyright (C) <2012-2026> Markus Hackspacher

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

try:
    from PyQt6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt5 import QtCore, QtGui, QtWidgets


class DlgNewPlayer(QtWidgets.QDialog):
    """
    new player window
    """
    def __init__(self):
        """initial new player window

        :return:
        """
        QtWidgets.QDialog.__init__(self)
        self.setWindowIcon(QtGui.QIcon(join("misc", "icon.ico")))
        self.setModal(True)
        self.button_box = QtWidgets.QDialogButtonBox(self)
        self.button_box.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel |
                                           QtWidgets.QDialogButtonBox.StandardButton.Ok)

        self.text_name = QtWidgets.QLineEdit(self)
        self.label = QtWidgets.QLabel(self)

        self.box_layout = QtWidgets.QBoxLayout(
            QtWidgets.QBoxLayout.Direction.TopToBottom, self)

        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(self.label, 0, 0, 1, 1)
        grid_layout.addWidget(self.text_name, 0, 1, 1, 1)

        self.box_layout.addLayout(grid_layout)
        self.box_layout.addWidget(self.button_box)

        self.label.setText(self.tr("Player"))
        self.setWindowTitle(self.tr("New Player Dialog"))
        self.text_name.setFocus()

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.close)

    def get_values(self):
        """return new playername in unicode"""
        return str(self.text_name.text())
