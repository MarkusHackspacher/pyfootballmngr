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

from PyQt4 import QtCore, QtGui
from gui.main_window import WndMain
from gui.dialogs.new_player import DlgNewPlayer
from gui.dialogs.update_player import DlgUpdatePlayer
from gui.dialogs.new_match import DlgNewMatch
from gui.dialogs.update_match import DlgUpdateMatch
from datahandler import Datahandler


class Main(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.app = QtGui.QApplication([])
        self.data_handler = Datahandler("datenbank.sqlite")

        self.init()
        self.connect_slots()

    def init(self):
        self.main = WndMain()
        self.update_main_users()
        self.update_main_matches(0)
        self.main.show()

    def connect_slots(self):
        self.main.actionAdd_Player.triggered.connect(self.new_player)
        self.connect(self.main.actionUpdate_Player, QtCore.SIGNAL(
         'triggered()'), self.update_player)
        self.main.actionRemove_Player.triggered.connect(self.delete_player)
        self.main.actionAdd_Match.triggered.connect(self.new_match)
        self.connect(self.main.actionUpdate_Match, QtCore.SIGNAL(
         'triggered()'), self.update_match)
        self.main.actionRemove_Match.triggered.connect(self.delete_match)
        self.connect(self.main.actionExampleData, QtCore.SIGNAL('triggered()'),
         self.onExampleData)
        self.connect(self.main.actionAbout, QtCore.SIGNAL('triggered()'),
         self.onInfo)
        self.main.actionExit.triggered.connect(self.exit)
        self.main.tViewPlayers.clicked.connect(self.player_selected)
        self.main.lViewMatches.clicked.connect(self.match_selected)

    def player_selected(self, index):
        id = self.model_index_to_id(index.row())
        self.update_main_matches(id)

    def match_selected(self, index):
        """ show informations about a match in information box"""
        try:
            m = self.main.tViewPlayers.model().data
            row = self.main.tViewPlayers.selectionModel().selectedIndexes(
             )[0].row()
        except Exception:
            id = None
        else:
            id = m[row][0]

        match_of_users = self.data_handler.get_matches(id)
        text = u"{} - {}".format(self.data_handler.get_users(match_of_users
         [self.main.lViewMatches.currentRow()][1])[0][0],
         self.data_handler.get_users(match_of_users[
         self.main.lViewMatches.currentRow()][2])[0][0])
        self.main.lblInfo1.setText(text)
        if id:
            self.main.lblInfo2.setText(u"Tordifferenz von {}: {:+}".format(
             self.data_handler.get_users(id)[0][0],
             self.data_handler.get_diff(id)))

    def model_index_to_id(self, row):
        m = self.main.tViewPlayers.model().data
        return m[row][0]

    def update_main_matches(self, id=None):
        """update match table
        """
        self.main.update_matches(self.data_handler.get_matches(id))

    def update_main_users(self):
        """update user table
        """
        self.main.update_users(self.data_handler.get_users())

    def new_player(self):
        """insert a new user
        """
        dlg = DlgNewPlayer()

        if dlg.exec_():
            user = dlg.getValues()
            self.data_handler.insert_user(user)
        self.update_main_users()

    def update_player(self):
        """update a user/player name
        """
        try:
            m = self.main.tViewPlayers.model().data
            row = self.main.tViewPlayers.selectionModel().selectedIndexes(
             )[0].row()
        except Exception:
            a = QtGui.QMessageBox()
            a.setWindowTitle('Info')
            a.setText('no player selected')
            a.exec_()
            return

        id = m[row][0]

        dlg = DlgUpdatePlayer(m[row][1])

        if dlg.exec_():
            user = dlg.getValues()
            self.data_handler.update_user(id, user)

        self.update_main_users()

    def delete_player(self):
        """delete a user
        """
        try:
            m = self.main.tViewPlayers.model().data
            row = self.main.tViewPlayers.selectionModel().selectedIndexes(
             )[0].row()
        except Exception:
            a = QtGui.QMessageBox()
            a.setWindowTitle('Info')
            a.setText('no player selected')
            a.exec_()
            return

        id = m[row][0]
        self.data_handler.delete_user(id)

        self.update_main_users()

        if row > 0:
            index = QtCore.QModelIndex(self.main.tViewPlayers.model().index(
             row - 1, 0))
            self.main.tViewPlayers.selectionModel().setCurrentIndex(index,
             QtGui.QItemSelectionModel.SelectCurrent)

    def new_match(self):
        """insert a new match
        """
        dlg = DlgNewMatch(self.data_handler.get_users())

        if dlg.exec_():
            id1, id2, team1, team2, goals1, goals2, date = dlg.getValues()
            self.data_handler.insert_match(
             id1, id2, team1, team2, goals1, goals2, date)
        self.update_main_matches()

    def update_match(self):
        """update a match
        """
        try:
            m = self.main.tViewPlayers.model().data
            row = self.main.tViewPlayers.selectionModel().selectedIndexes(
             )[0].row()
        except Exception:
            id = None
        else:
            id = m[row][0]
        match_of_users = self.data_handler.get_matches(id)
        dlg = DlgUpdateMatch(self.data_handler.get_users(),
         match_of_users[self.main.lViewMatches.currentRow()][1],
         match_of_users[self.main.lViewMatches.currentRow()][2],
         match_of_users[self.main.lViewMatches.currentRow()][3],
         match_of_users[self.main.lViewMatches.currentRow()][4],
         match_of_users[self.main.lViewMatches.currentRow()][5],
         match_of_users[self.main.lViewMatches.currentRow()][6],
         match_of_users[self.main.lViewMatches.currentRow()][7])

        if dlg.exec_():
            id1, id2, team1, team2, goals1, goals2, date = dlg.getValues()
            self.data_handler.update_match(match_of_users[
             self.main.lViewMatches.currentRow()][0], id1, id2, team1,
             team2, goals1, goals2, date)

        self.update_main_matches(id)

    def delete_match(self):
        """delete a match
        """
        try:
            m = self.main.tViewPlayers.model().data
            row = self.main.tViewPlayers.selectionModel(
             ).selectedIndexes()[0].row()
        except Exception:
            id = None
        else:
            id = m[row][0]
        match_of_users = self.data_handler.get_matches(id)
        self.data_handler.delete_match(match_of_users[
         self.main.lViewMatches.currentRow()][0])

        self.update_main_matches(id)

    def onExampleData(self):
        """ Load Example Data
        """
        self.data_handler.insert_user("Patrick")
        self.data_handler.insert_user("Max")
        self.data_handler.insert_user(u"Bärbel")
        self.data_handler.insert_user("Janis")
        self.data_handler.insert_user("Jessy")
        self.data_handler.insert_match(1, 3, "Bayern", "Dortmund",
         1, 0, "2002-11-08")
        self.data_handler.insert_match(2, 5, "Hamburg", "Freiburg",
         2, 2, "2010-07-09")
        self.data_handler.insert_match(4, 3, "Dortmund", "Stuttgart",
         1, 4, "2008-01-24")
        self.data_handler.insert_match(3, 5, "Lautern", "Berlin",
         0, 2, "2011-06-15")
        self.data_handler.insert_match(5, 1, "Frankfurt", "Hoffenheim",
         4, 4, "2001-12-01")
        self.data_handler.insert_match(4, 2, u"1860 München", "Hoffenheim",
         0, 2, "2011-11-11")
        self.update_main_users()

    def onInfo(self):
        """ Programm Info
        """
        text = (u'eine Alternative zur Stift&Papier-Methode beim Notieren der '
        u'Ergebnisse. Von 12345z veröffentlicht 2011 auf '
        u'http://www.python-forum.de/viewtopic.php?f=9&t=27313 '
        u'und https://sourceforge.net/p/pyfootballmngr\n'
        'Erweitert 2012-2013 Markus Hackspacher '
        'https://github.com/MarkusHackspacher/pyfootballmngr \n'
        u'Lizenz: GNU GPLv3')
        a = QtGui.QMessageBox()
        a.setWindowTitle('Info')
        a.setText(text)
        a.setInformativeText('')
        a.exec_()

    def exit(self):
        """exit and close
        """
        self.data_handler.close()
        self.main.close()

    def mainLoop(self):
        self.app.exec_()
