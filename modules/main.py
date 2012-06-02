# coding: utf-8

from PyQt4 import QtCore, QtGui
from gui.main_window import WndMain
from gui.dialogs.new_player import DlgNewPlayer
from gui.dialogs.update_player import DlgUpdatePlayer
from gui.dialogs.new_match import DlgNewMatch
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
        self.connect(self.main.actionUpdate_Player, QtCore.SIGNAL('triggered()'), self.update_player)
        self.main.actionRemove_Player.triggered.connect(self.delete_player)
        self.main.actionAdd_Match.triggered.connect(self.new_match)
        self.connect(self.main.actionUpdate_Match, QtCore.SIGNAL('triggered()'), self.update_match)
        self.main.actionRemove_Match.triggered.connect(self.delete_match)
        self.connect(self.main.actionAbout, QtCore.SIGNAL('triggered()'), self.onInfo)
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
            row = self.main.tViewPlayers.selectionModel().selectedIndexes()[0].row()
        except Exception:  
            id = None 
        else:
            id = m[row][0]

        match_of_users = self.data_handler.get_matches(id)
        text = "{} - {}".format(self.data_handler.get_users(match_of_users[self.main.lViewMatches.currentRow()][1])[0][0], \
         self.data_handler.get_users(match_of_users[self.main.lViewMatches.currentRow()][2])[0][0])
        self.main.lblInfo1.setText(text)
        if id:
            self.main.lblInfo2.setText("Tordifferenz von {}: {:+}".format(self.data_handler.get_users(id)[0][0], self.data_handler.get_diff(id)))
            #ToDo: get_fav_team, output is not very useful
            #self.main.lblInfo3.setText("Bestes Team: {}".format(self.data_handler.get_fav_team(id)))

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
            row = self.main.tViewPlayers.selectionModel().selectedIndexes()[0].row()
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
            row = self.main.tViewPlayers.selectionModel().selectedIndexes()[0].row()
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
            index = QtCore.QModelIndex(self.main.tViewPlayers.model().index(row - 1, 0))
            self.main.tViewPlayers.selectionModel().setCurrentIndex(index, QtGui.QItemSelectionModel.SelectCurrent)

    def new_match(self):
        """insert a new match
        """
        dlg = DlgNewMatch(self.data_handler.get_users())

        if dlg.exec_():
            id1, id2, team1, team2, goals1, goals2, date = dlg.getValues()
            self.data_handler.insert_match(id1, id2, team1, team2, goals1, goals2, date)
        self.update_main_matches()
        
    def update_match(self):
        """Todo: update a new match           
        """
        done

    def delete_match(self):
        """delete a match
        """
        try:
            m = self.main.tViewPlayers.model().data
            row = self.main.tViewPlayers.selectionModel().selectedIndexes()[0].row()
        except Exception:  
            id = None 
        else:
            id = m[row][0]
        match_of_users = self.data_handler.get_matches(id)
        self.data_handler.delete_match(match_of_users[self.main.lViewMatches.currentRow()][0])

        self.update_main_matches(id)
        
    def onInfo(self):
        """ Programm Info
        """
        text = u'eine Alternative zur Stift&Papier-Methode beim Notieren der Ergebnisse\n'
        text = text + u'Von 12345z, veröffentlicht auf http://www.python-forum.de/viewtopic.php?f=9&t=27313\n'
        text = text + u'und https://sourceforge.net/p/pyfootballmngr'
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