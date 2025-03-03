# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Login_GUI.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(338, 220)
        self.label_104 = QLabel(Dialog)
        self.label_104.setObjectName(u"label_104")
        self.label_104.setGeometry(QRect(40, 40, 271, 16))
        self.label_104.setStyleSheet(u"color: rgb(240, 162, 101);")
        self.label_103 = QLabel(Dialog)
        self.label_103.setObjectName(u"label_103")
        self.label_103.setGeometry(QRect(20, 10, 291, 31))
        self.label_103.setStyleSheet(u"font: 24pt \".AppleSystemUIFont\";\n"
"color: rgb(252, 62, 39);")
        self.txt_userID = QLineEdit(Dialog)
        self.txt_userID.setObjectName(u"txt_userID")
        self.txt_userID.setGeometry(QRect(120, 105, 125, 21))
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(50, 105, 62, 16))
        self.txt_Password = QLineEdit(Dialog)
        self.txt_Password.setObjectName(u"txt_Password")
        self.txt_Password.setGeometry(QRect(120, 135, 125, 21))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(50, 135, 65, 21))
        self.btnLogin = QPushButton(Dialog)
        self.btnLogin.setObjectName(u"btnLogin")
        self.btnLogin.setGeometry(QRect(120, 165, 121, 32))
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(50, 80, 261, 16))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_104.setText(QCoreApplication.translate("Dialog", u"THAI SILK PRODUCTS COMPANY LIMITED", None))
        self.label_103.setText(QCoreApplication.translate("Dialog", u"\u0e1a\u0e23\u0e34\u0e29\u0e31\u0e17 \u0e44\u0e17\u0e22\u0e0b\u0e34\u0e25\u0e04\u0e4c\u0e42\u0e1b\u0e23\u0e14\u0e31\u0e04\u0e2a\u0e4c \u0e08\u0e33\u0e01\u0e31\u0e14", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"User ID", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Password", None))
        self.btnLogin.setText(QCoreApplication.translate("Dialog", u"Login", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u0e01\u0e23\u0e38\u0e13\u0e32\u0e43\u0e2a\u0e48\u0e23\u0e2b\u0e31\u0e2a\u0e1b\u0e23\u0e30\u0e08\u0e33\u0e15\u0e31\u0e27\u0e40\u0e08\u0e49\u0e32\u0e2b\u0e19\u0e49\u0e32\u0e17\u0e35\u0e48\u0e40\u0e1e\u0e37\u0e48\u0e2d\u0e40\u0e02\u0e49\u0e32\u0e2a\u0e39\u0e48\u0e23\u0e30\u0e1a\u0e1a", None))
    # retranslateUi

