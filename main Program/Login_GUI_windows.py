# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Login_GUI_windows.ui'
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
        Dialog.resize(463, 303)
        font = QFont()
        font.setFamilies([u"DB Adman X"])
        font.setPointSize(18)
        Dialog.setFont(font)
        self.txt_userID = QLineEdit(Dialog)
        self.txt_userID.setObjectName(u"txt_userID")
        self.txt_userID.setGeometry(QRect(171, 155, 161, 31))
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(105, 160, 61, 21))
        self.label.setStyleSheet(u"")
        self.txt_Password = QLineEdit(Dialog)
        self.txt_Password.setObjectName(u"txt_Password")
        self.txt_Password.setGeometry(QRect(171, 195, 161, 31))
        font1 = QFont()
        font1.setPointSize(10)
        self.txt_Password.setFont(font1)
        self.txt_Password.setEchoMode(QLineEdit.Password)
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(85, 200, 81, 21))
        self.label_2.setStyleSheet(u"")
        self.btnLogin = QPushButton(Dialog)
        self.btnLogin.setObjectName(u"btnLogin")
        self.btnLogin.setGeometry(QRect(185, 240, 121, 32))
        self.btnLogin.setStyleSheet(u"font: 75 20pt \"DB SaiKrok X\";")
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(75, 115, 336, 26))
        font2 = QFont()
        font2.setFamilies([u"DB Adman X"])
        font2.setPointSize(18)
        font2.setBold(True)
        font2.setItalic(False)
        self.label_3.setFont(font2)
        self.label_3.setStyleSheet(u"")
        self.label_51 = QLabel(Dialog)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setGeometry(QRect(10, 35, 441, 41))
        font3 = QFont()
        font3.setFamilies([u"DB Adman X"])
        font3.setPointSize(34)
        font3.setBold(True)
        self.label_51.setFont(font3)
        self.label_51.setStyleSheet(u"color: rgb(252, 62, 39);\n"
"")
        self.label_51.setAlignment(Qt.AlignCenter)
        self.label_50 = QLabel(Dialog)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setGeometry(QRect(10, 80, 441, 16))
        font4 = QFont()
        font4.setFamilies([u"DB Adman X"])
        font4.setPointSize(20)
        font4.setBold(True)
        font4.setItalic(False)
        font4.setStrikeOut(False)
        self.label_50.setFont(font4)
        self.label_50.setStyleSheet(u"color: rgb(240, 162, 101);\n"
"")
        self.label_50.setAlignment(Qt.AlignCenter)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"User ID", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Password", None))
        self.btnLogin.setText(QCoreApplication.translate("Dialog", u"\u0e40\u0e02\u0e49\u0e32\u0e2a\u0e39\u0e48\u0e23\u0e30\u0e1a\u0e1a", None))
#if QT_CONFIG(shortcut)
        self.btnLogin.setShortcut(QCoreApplication.translate("Dialog", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u0e01\u0e23\u0e38\u0e13\u0e32\u0e43\u0e2a\u0e48\u0e23\u0e2b\u0e31\u0e2a\u0e1b\u0e23\u0e30\u0e08\u0e33\u0e15\u0e31\u0e27\u0e40\u0e08\u0e49\u0e32\u0e2b\u0e19\u0e49\u0e32\u0e17\u0e35\u0e48\u0e40\u0e1e\u0e37\u0e48\u0e2d\u0e40\u0e02\u0e49\u0e32\u0e2a\u0e39\u0e48\u0e23\u0e30\u0e1a\u0e1a", None))
        self.label_51.setText(QCoreApplication.translate("Dialog", u"\u0e1a\u0e23\u0e34\u0e29\u0e31\u0e17 \u0e44\u0e17\u0e22\u0e0b\u0e34\u0e25\u0e04\u0e4c\u0e42\u0e1b\u0e23\u0e14\u0e31\u0e04\u0e2a\u0e4c \u0e08\u0e33\u0e01\u0e31\u0e14", None))
        self.label_50.setText(QCoreApplication.translate("Dialog", u"THAI SILK PRODUCTS COMPANY LIMITED", None))
    # retranslateUi

