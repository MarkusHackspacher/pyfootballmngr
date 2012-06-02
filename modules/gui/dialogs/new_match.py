from os.path import join
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class DlgNewMatch(QtGui.QDialog):
    def __init__(self, data_of_users):
        QtGui.QDialog.__init__(self)
        
        self.setWindowIcon(QtGui.QIcon(join("misc", "icon.ico")))
        self.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)

        self.id1 = QtGui.QComboBox(self)
        self.id2 = QtGui.QComboBox(self)
        for user in data_of_users:
            self.id1.addItem((user[1]))
            self.id2.addItem(_fromUtf8(user[1]))
        self.team1 = QtGui.QLineEdit(self)
        self.team2 = QtGui.QLineEdit(self)
        self.goals1 = QtGui.QSpinBox(self)
        self.goals2 = QtGui.QSpinBox(self)
        self.date = QtGui.QLineEdit(self)
        self.users = QtGui.QLabel(self)
        self.team = QtGui.QLabel(self)
        self.goal = QtGui.QLabel(self)
        self.date_match = QtGui.QLabel(self)


        self.boxLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom, self)

        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(self.users, 0, 0, 1, 1)
        gridLayout.addWidget(self.id1, 0, 1, 1, 1)
        gridLayout.addWidget(self.id2, 0, 2, 1, 1)
        gridLayout.addWidget(self.team, 1, 0, 1, 1)
        gridLayout.addWidget(self.team1, 1, 1, 1, 1)
        gridLayout.addWidget(self.team2, 1, 2, 1, 1)
        gridLayout.addWidget(self.goal, 2, 0, 1, 1)
        gridLayout.addWidget(self.goals1, 2, 1, 1, 1)
        gridLayout.addWidget(self.goals2, 2, 2, 1, 1)
        gridLayout.addWidget(self.date_match, 3, 0, 1, 1)
        gridLayout.addWidget(self.date, 3, 1, 2, 1)
   
        self.boxLayout.addLayout(gridLayout)
        self.boxLayout.addWidget(self.buttonBox)

        self.data_of_users = data_of_users

        self.users.setText("Users")
        self.team.setText("Team")
        self.goal.setText("Goals")
        self.date_match.setText("Date of the match")
        self.setWindowTitle("New Match Dialog")
        self.id1.setFocus()


        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.close)
        
    def getValues(self):
        """id1, id2, team1, team2, goals1, goals2, date"""
        return str(self.data_of_users[self.id1.currentIndex()][0]), str(self.data_of_users[self.id2.currentIndex()][0]), \
         unicode(self.team1.text()), unicode(self.team2.text()),\
         self.goals1.value(), self.goals2.value(), str(self.date.text())

