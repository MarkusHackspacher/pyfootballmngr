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


class DlgUpdateMatch(QtWidgets.QDialog):
    """
    Update Match dialog
    """
    def __init__(
            self, data_of_users, id1, id2, team1, team2, goals1, goals2, date):
        """open Update Match dialog
        @type data_of_users: list
        @type id1: int
        @type id2: int
        @type team1: int
        @type team2: int
        @type goals1: int
        @type goals2: int
        @type date: date
        """
        QtWidgets.QDialog.__init__(self)

        self.setWindowIcon(QtGui.QIcon(join("misc", "icon.ico")))
        self.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel |
                                          QtWidgets.QDialogButtonBox.StandardButton.Ok)

        self.id1 = QtWidgets.QComboBox(self)
        self.id2 = QtWidgets.QComboBox(self)
        for user in data_of_users:
            self.id1.addItem(user[1])
            self.id2.addItem(user[1])
        self.team1 = QtWidgets.QLineEdit(self)
        self.team2 = QtWidgets.QLineEdit(self)
        self.goals1 = QtWidgets.QSpinBox(self)
        self.goals2 = QtWidgets.QSpinBox(self)
        self.users = QtWidgets.QLabel(self)
        self.team = QtWidgets.QLabel(self)
        self.goal = QtWidgets.QLabel(self)
        self.date_match = QtWidgets.QLabel(self)
        self.calendarWidget = QtWidgets.QCalendarWidget(self)

        self.boxLayout = QtWidgets.QBoxLayout(
            QtWidgets.QBoxLayout.Direction.TopToBottom, self)

        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(self.users, 0, 0, 1, 1)
        grid_layout.addWidget(self.id1, 0, 1, 1, 1)
        grid_layout.addWidget(self.id2, 0, 2, 1, 1)
        grid_layout.addWidget(self.team, 1, 0, 1, 1)
        grid_layout.addWidget(self.team1, 1, 1, 1, 1)
        grid_layout.addWidget(self.team2, 1, 2, 1, 1)
        grid_layout.addWidget(self.goal, 2, 0, 1, 1)
        grid_layout.addWidget(self.goals1, 2, 1, 1, 1)
        grid_layout.addWidget(self.goals2, 2, 2, 1, 1)
        grid_layout.addWidget(self.date_match, 3, 0, 1, 1)
        grid_layout.addWidget(self.calendarWidget, 3, 1, 2, 2)

        self.boxLayout.addLayout(grid_layout)
        self.boxLayout.addWidget(self.buttonBox)

        self.data_of_users = data_of_users

        self.users.setText(self.tr("Player"))
        self.team.setText(self.tr("Team"))
        self.goal.setText(self.tr("Goals"))
        self.date_match.setText(self.tr("Date of the match"))
        self.setWindowTitle(self.tr("Update Match Dialog"))
        user_index = 0
        for user in data_of_users:
            if id1 == user[0]:
                self.id1.setCurrentIndex(user_index)
            if id2 == user[0]:
                self.id2.setCurrentIndex(user_index)
            user_index += 1
        self.team1.setText(team1)
        self.team2.setText(team2)
        self.goals1.setValue(goals1)
        self.goals2.setValue(goals2)
        self.calendarWidget.setSelectedDate(
            QtCore.QDate.fromString(date, "yyyy-MM-dd"))
        self.id1.setFocus()

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.close)

    def get_values(self):
        """id1, id2, team1, team2, goals1, goals2, date
        """
        return str(self.data_of_users[self.id1.currentIndex()][0]), \
            str(self.data_of_users[self.id2.currentIndex()][0]), \
            str(self.team1.text()), str(self.team2.text()), \
            self.goals1.value(), self.goals2.value(), \
            self.calendarWidget.selectedDate().toPyDate()
