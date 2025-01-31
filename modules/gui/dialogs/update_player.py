#!/usr/bin/env python
# coding: utf-8

"""
pyfootballmngr

Copyright (C) <2012-2024> Markus Hackspacher

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


class DlgUpdatePlayer(QtWidgets.QDialog):
    """
    Update Player Dialog
    """
    def __init__(self, old_player_name):
        """init Player Dialog

        :param old_player_name:
        :return:
        """
        QtWidgets.QDialog.__init__(self)

        self.setWindowIcon(QtGui.QIcon(join("misc", "icon.ico")))
        self.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel | QtWidgets.QDialogButtonBox.StandardButton.Ok)

        self.txtName = QtWidgets.QLineEdit(self)
        self.label = QtWidgets.QLabel(self)

        self.boxLayout = QtWidgets.QBoxLayout(
            QtWidgets.QBoxLayout.Direction.TopToBottom, self)

        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(self.label, 0, 0, 1, 1)
        grid_layout.addWidget(self.txtName, 0, 1, 1, 1)

        self.boxLayout.addLayout(grid_layout)
        self.boxLayout.addWidget(self.buttonBox)

        self.label.setText(self.tr("Player"))
        self.setWindowTitle(self.tr("Update Playername Dialog"))
        self.txtName.setFocus()
        self.txtName.setText(old_player_name)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.close)

    def get_values(self):
        """return new playername in unicode

        :return: playername
        """
        return str(self.txtName.text())
