# coding: utf-8

from os.path import join
from PyQt4 import QtCore, QtGui

class DlgUpdatePlayer(QtGui.QDialog):
    def __init__(self,old_player_name):
        QtGui.QDialog.__init__(self)
        
        self.setWindowIcon(QtGui.QIcon(join("misc", "icon.ico")))
        self.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)

        self.txtName = QtGui.QLineEdit(self)
        self.label = QtGui.QLabel(self)


        self.boxLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom, self)

        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(self.label, 0, 0, 1, 1)
        gridLayout.addWidget(self.txtName, 0, 1, 1, 1)
   
        self.boxLayout.addLayout(gridLayout)
        self.boxLayout.addWidget(self.buttonBox)


        self.label.setText("Username")
        self.setWindowTitle("Update Playername Dialog")
        self.txtName.setFocus()
        self.txtName.setText(old_player_name)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.close)

    def getValues(self):
        """return new playername in unicode"""
        return unicode(self.txtName.text())

