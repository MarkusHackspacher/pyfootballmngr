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
from gui.main_window import WndMain
from gui.dialogs.new_player import DlgNewPlayer
from gui.dialogs.update_player import DlgUpdatePlayer
from gui.dialogs.new_match import DlgNewMatch
from gui.dialogs.update_match import DlgUpdateMatch
from datahandler import Datahandler


class Main(QtCore.QObject):
    def __init__(self, arguments):
        """open the GUI
        @param arguments: language (en, de)
        @type arguments: string
        @return: none
        """
        QtCore.QObject.__init__(self)
        self.app = QtGui.QApplication([])
        if len(arguments) > 1:
            locale = arguments[1]
        else:
            locale = unicode(QtCore.QLocale.system().name())
            print "locale: " + unicode(locale)
        translator = QtCore.QTranslator(self.app)
        translator.load(join("modules", "pyfbm_" + unicode(locale)))
        self.app.installTranslator(translator)

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
        self.main.actionUpdate_Player.triggered.connect(self.update_player)
        self.main.actionRemove_Player.triggered.connect(self.delete_player)
        self.main.actionAdd_Match.triggered.connect(self.new_match)
        self.main.actionUpdate_Match.triggered.connect(self.update_match)
        self.main.actionRemove_Match.triggered.connect(self.delete_match)
        self.main.actionExampleData.triggered.connect(self.onExampleData)
        self.main.actionAbout.triggered.connect(self.onInfo)
        self.main.actionExit.triggered.connect(self.onexit)
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
            text = self.tr("Goal Difference of")
            self.main.lblInfo2.setText("{0} {1}: {2:+}".format(
             text, self.data_handler.get_users(id)[0][0],
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
            a.setWindowTitle(self.tr('Info'))
            a.setText(self.tr('no player selected'))
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
            a.setWindowTitle(self.tr('Info'))
            a.setText(self.tr('no player selected'))
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
        self.data_handler.insert_user(self.tr("Isabelle"))
        self.data_handler.insert_user(self.tr("Max"))
        self.data_handler.insert_user(self.tr("Emily"))
        self.data_handler.insert_user(self.tr("Jack"))
        self.data_handler.insert_user(self.tr("George"))
        self.data_handler.insert_match(1, 3, self.tr("Manchester City"),
         self.tr("Chelsea"), 1, 0, "2002-11-08")
        self.data_handler.insert_match(2, 5, self.tr("Manchester Utd"),
         self.tr("Aston Villa"), 2, 2, "2010-07-09")
        self.data_handler.insert_match(4, 3, self.tr("Chelsea"),
         self.tr("Tottenham"), 1, 4, "2008-01-24")
        self.data_handler.insert_match(3, 5, self.tr("Arsenal"),
         self.tr("Liverpool"), 0, 2, "2011-06-15")
        self.data_handler.insert_match(5, 1, self.tr("Arsenal"),
         self.tr("Manchester Utd"), 4, 4, "2001-12-01")
        self.data_handler.insert_match(4, 2, self.tr("Manchester City"),
         self.tr("Fulham"), 0, 2, "2011-11-11")
        self.update_main_users()

    def onInfo(self):
        """ Programm Info
        """
        text = self.tr('an alternative to paper-pencil method when recording'
        'the results. Develop 2012-2013 Markus Hackspacher '
        'http://github.com/MarkusHackspacher/pyfootballmngr \n'
        'licence: GNU GPLv3')
        a = QtGui.QMessageBox()
        a.setWindowTitle(self.tr('Info'))
        a.setText(text)
        a.setInformativeText('')
        a.exec_()

    def onexit(self):
        """exit and close
        """
        self.data_handler.close()
        self.main.close()

    def mainLoop(self):
        self.app.exec_()
