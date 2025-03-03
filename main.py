############################################
#           Pyside 6 + Qt Designer         #
############################################
import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, \
                            QMessageBox, QWidget, QVBoxLayout, QLabel, QLineEdit, QHeaderView
from PySide6.QtCore import QThread, QObject, Signal, Slot, QTimer

import datetime
import time

from main_GUI import Ui_MainWindow
from Login_GUI import Ui_Dialog
from DB import Database
          
class MainWindow(QMainWindow):
    def __init__(self, userID):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = Database()
        
        self.setcmb()
        self.btnLink()
        
        self.loadCustomerTable()
        self.loadStaffTable()
        self.loadGradeMaterial()
        self.loadMaterialPrice()
        self.loadBasketWeight()
        
        StaffName = self.db.LoadNameFromUserID(userID)
        self.ui.lbl_Staff_ID.setText(userID)
        self.ui.lbl_Staff_name.setText(StaffName)
    
    # Config btn link to function
    def btnLink(self):   
        # Button of customer config 
        self.ui.btn_add_customer.clicked.connect(self.add_customer)
        self.ui.btn_delete_customer.clicked.connect(self.delete_Customer)
        self.ui.tb_customerDetail.clicked.connect(self.loadTextboxCustomer)
        self.ui.btn_edit_customer.clicked.connect(self.edit_Customer)
        self.ui.btn_clear_customer.clicked.connect(self.clear_from_addnewCustomer)
        
        # Button of staff config 
        self.ui.btn_add_staff.clicked.connect(self.add_staff)
        self.ui.btn_delete_staff.clicked.connect(self.delete_staff)
        self.ui.tb_staffDetail.clicked.connect(self.loadTextboxStaff)
        self.ui.btn_edit_staff.clicked.connect(self.edit_staff)
        self.ui.btn_clear_staff_config.clicked.connect(self.clear_from_addNewStaff)
    
        # Button config part
        self.ui.btn_SaveWeightOfGradeConfig.clicked.connect(self.updateGradeMatrial)
        self.ui.btn_SavePriceMaterial.clicked.connect(self.updateDB_MaterialPrice)
        self.ui.btn_Save_ConfigWeigthBasket.clicked.connect(self.updateDB_BasketWeight)
    
    # Load basket weight
    def updateDB_BasketWeight(self):
        weight = self.ui.txt_ConfigWeigthBasket.text()
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle("แก้ไขข้อมูล")
        dlg.setText("ต้องการแก้ข้อมูลน้ำหนักตะกร้าหรือไม่ ??")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button = dlg.exec()
        
        if button == QMessageBox.Yes:
            if (weight != ""):
                self.db.updateDB_BasketWeight(weight)
                self.loadBasketWeight()
            else:
                return
            
    def loadBasketWeight(self):
        weight = self.db.LoadDB_BasketWeight()
        self.ui.txt_ConfigWeigthBasket.setText(str(weight[0][1]))
        
    # Load material price
    def updateDB_MaterialPrice(self):
        sakon = self.ui.txt_Price_material_SAKON.text()
        buriram = self.ui.txt_Price_material_BURIRAM.text()
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle("แก้ไขข้อมูล")
        dlg.setText("ต้องการแก้ข้อมูลราคารับซื้อวัตถุดิบหรือไม่ ??")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button = dlg.exec()
        
        if button == QMessageBox.Yes:
            if ((sakon != "") or (buriram != "") ):
                self.db.updateDB_MaterialPrice(sakon,buriram)
                self.loadMaterialPrice()
            else:
                return
            
    def loadMaterialPrice(self):
        price = self.db.LoadDB_MaterialPrice()
        self.ui.txt_Price_material_SAKON.setText(str(price[0][1]))
        self.ui.txt_Price_material_BURIRAM.setText(str(price[0][2]))
           
    # Load Grade for set weight reject 
    def updateGradeMatrial(self):
        A = self.ui.txt_config_Grade_A.text()
        B = self.ui.txt_config_Grade_B.text()
        C = self.ui.txt_config_Grade_C.text()
        D = self.ui.txt_config_Grade_D.text()
        E = self.ui.txt_config_Grade_E.text()
        F = self.ui.txt_config_Grade_F.text()
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle("แก้ไขข้อมูล")
        dlg.setText("ต้องการแก้ข้อมูลเกรดวัตถุดิบหรือไม่ ??")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button = dlg.exec()
        
        if button == QMessageBox.Yes:
            if ((A != "") or (B != "") or (C != "") or (D != "") or (E != "") or (F != "")):
                self.db.updateWeightReject(A,B,C,D,E,F)
                self.loadGradeMaterial()
            else:
                return
            
    def loadGradeMaterial(self):
        grade = self.db.loadGradematerial()
        # print((grade))
        # print(grade[0][2])

        self.ui.txt_config_Grade_A.setText(str(grade[0][1]))
        self.ui.txt_config_Grade_B.setText(str(grade[0][2]))
        self.ui.txt_config_Grade_C.setText(str(grade[0][3]))
        self.ui.txt_config_Grade_D.setText(str(grade[0][4]))
        self.ui.txt_config_Grade_E.setText(str(grade[0][5]))
        self.ui.txt_config_Grade_F.setText(str(grade[0][6]))
    
    # ---------- staff Config ------------    
    def loadTextboxStaff(self):
        id = self.ui.tb_staffDetail.item(self.ui.tb_staffDetail.currentIndex().row(),0).text()
        username = self.ui.tb_staffDetail.item(self.ui.tb_staffDetail.currentIndex().row(),1).text()
        password = self.ui.tb_staffDetail.item(self.ui.tb_staffDetail.currentIndex().row(),2).text()
        level = self.ui.tb_staffDetail.item(self.ui.tb_staffDetail.currentIndex().row(),3).text()
        name = self.ui.tb_staffDetail.item(self.ui.tb_staffDetail.currentIndex().row(),4).text()
        
        self.ui.txt_staff_id_config.setText(id)
        self.ui.txt_username_staff_config.setText(username)
        self.ui.txt_password_staff_config.setText(password)
        self.ui.cmb_level_staff_config.setCurrentText(level)
        self.ui.txt_name_staff_config.setText(name)
            
    def edit_staff(self):
        id = self.ui.txt_staff_id_config.text()
        username = self.ui.txt_username_staff_config.text()
        password = self.ui.txt_password_staff_config.text()
        level = self.ui.cmb_level_staff_config.currentText()
        name = self.ui.txt_name_staff_config.text()
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle("แก้ไขข้อมูล")
        dlg.setText("ต้องการแก้ข้อมูลผู้ใช้งานหรือไม่ ??\n ผู้ขาย : " + name)
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button = dlg.exec()
        
        if button == QMessageBox.Yes:
            if (self.ui.txt_name_staff_config.text() != ""):
                self.db.EditStaff(id, username, password, level, name)
                self.loadStaffTable()
                self.clear_from_addNewStaff()
            else:
                return
            
    def delete_staff(self):
        staffID = self.ui.tb_staffDetail.item(self.ui.tb_staffDetail.currentIndex().row(),0).text()
        name = self.ui.tb_staffDetail.item(self.ui.tb_staffDetail.currentIndex().row(),4).text()
        SelectRowToDetete = self.ui.tb_staffDetail.currentRow()
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle("ลบข้อมูล")
        dlg.setText("ต้องการลบข้อมูลผู้ใช้งานหรือไม่ ??\n ผู้ขาย : " + name)
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button = dlg.exec()
        
        if button == QMessageBox.Yes:
            if SelectRowToDetete < 0:
                return
            self.ui.tb_staffDetail.removeRow(SelectRowToDetete)
            self.db.DeleteStaff(staffID)
            self.loadStaffTable()
            self.clear_from_addNewStaff()
            
    def loadStaffTable(self):
        # Get customer data from DB
        column,row,staffData = self.db.loadAllStaff()
        
        # create Table
        self.ui.tb_staffDetail.setRowCount(row)
        self.ui.tb_staffDetail.setColumnCount(column)
        self.ui.tb_staffDetail.setHorizontalHeaderItem(0, QTableWidgetItem("id"))
        self.ui.tb_staffDetail.setHorizontalHeaderItem(1, QTableWidgetItem("username"))
        self.ui.tb_staffDetail.setHorizontalHeaderItem(2, QTableWidgetItem("password"))
        self.ui.tb_staffDetail.setHorizontalHeaderItem(3, QTableWidgetItem("level"))
        self.ui.tb_staffDetail.setHorizontalHeaderItem(4, QTableWidgetItem("name"))
        
        header = self.ui.tb_staffDetail.horizontalHeader()         
        for col in range(column):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        
        tablerow = 0
        for row in staffData:
            self.ui.tb_staffDetail.setItem(tablerow,0,QTableWidgetItem(str(row[0])))
            self.ui.tb_staffDetail.setItem(tablerow,1,QTableWidgetItem(row[1]))
            self.ui.tb_staffDetail.setItem(tablerow,2,QTableWidgetItem(row[2]))
            self.ui.tb_staffDetail.setItem(tablerow,3,QTableWidgetItem(row[3]))
            self.ui.tb_staffDetail.setItem(tablerow,4,QTableWidgetItem(row[3]))
            tablerow += 1
    
    def add_staff(self):      
        if (self.ui.txt_staff_id_config.text() != ""):
                id = self.ui.txt_staff_id_config.text()
                username = self.ui.txt_username_staff_config.text()
                password = self.ui.txt_password_staff_config.text()
                level = self.ui.cmb_level_staff_config.currentText()
                name = self.ui.txt_name_staff_config.text()
                
                val = (id, username, password, level, name)
                self.db.AddNewStaff(val)
                self.loadStaffTable()
                self.clear_from_addNewStaff()
        else:
            self.msgBoxError()
    
    def clear_from_addNewStaff(self):
        self.ui.txt_staff_id_config.clear()
        self.ui.txt_username_staff_config.clear()
        self.ui.txt_password_staff_config.clear()
        self.ui.cmb_level_staff_config.setCurrentText("employee")
        self.ui.txt_name_staff_config.clear()
       
    # ------ Customer Config ---------    
    def search_Customer(self):
        pass
        
    def loadTextboxCustomer(self):
        id = self.ui.tb_customerDetail.item(self.ui.tb_customerDetail.currentIndex().row(),0).text()
        name = self.ui.tb_customerDetail.item(self.ui.tb_customerDetail.currentIndex().row(),1).text()
        address = self.ui.tb_customerDetail.item(self.ui.tb_customerDetail.currentIndex().row(),2).text()
        village_group = self.ui.tb_customerDetail.item(self.ui.tb_customerDetail.currentIndex().row(),3).text()
        leader = self.ui.tb_customerDetail.item(self.ui.tb_customerDetail.currentIndex().row(),4).text()
        phone = self.ui.tb_customerDetail.item(self.ui.tb_customerDetail.currentIndex().row(),5).text()
        
        self.ui.txt_customerID_DB.setText(id)
        self.ui.txt_name_customer_DB.setText(name)
        self.ui.txt_address_customer_DB.setText(address)
        self.ui.txt_group_customer_DB.setText(village_group)
        self.ui.txt_leaderName_customer_DB.setText(leader)
        self.ui.txt_phone_customer_DB.setText(phone)
    
    def edit_Customer(self):
        id = self.ui.txt_customerID_DB.text()
        name = self.ui.txt_name_customer_DB.text()
        address = self.ui.txt_address_customer_DB.text()
        village_group = self.ui.txt_group_customer_DB.text()
        leader = self.ui.txt_leaderName_customer_DB.text()
        phone = self.ui.txt_phone_customer_DB.text()
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle("แก้ไขข้อมูล")
        dlg.setText("ต้องการแก้ข้อมูลผู้ใช้งานหรือไม่ ??\n ผู้ขาย : " + name)
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button = dlg.exec()
        
        if button == QMessageBox.Yes:
            if (self.ui.txt_customerID_DB.text() != ""):
                self.db.EditCustomer(id, name, address, village_group, leader, phone)
                self.loadCustomerTable()
                self.clear_from_addnewCustomer()
            else:
                return
          
    def delete_Customer(self):
        customerID = self.ui.tb_customerDetail.item(self.ui.tb_customerDetail.currentIndex().row(),0).text()
        name = self.ui.tb_customerDetail.item(self.ui.tb_customerDetail.currentIndex().row(),1).text()
        SelectRowToDetete = self.ui.tb_customerDetail.currentRow()
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle("ลบข้อมูล")
        dlg.setText("ต้องการลบข้อมูลผู้ใช้งานหรือไม่ ??\n ผู้ขาย : " + name)
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button = dlg.exec()
        
        if button == QMessageBox.Yes:
            if SelectRowToDetete < 0:
                return
            self.ui.tb_customerDetail.removeRow(SelectRowToDetete)
            self.db.DeleteCustomer(customerID)
            self.loadCustomerTable()
            
    def loadCustomerTable(self):
        # Get customer data from DB
        column,row,customerData = self.db.LoadAllCustomer()
        
        # create Table
        self.ui.tb_customerDetail.setRowCount(row)
        self.ui.tb_customerDetail.setColumnCount(column)
        self.ui.tb_customerDetail.setHorizontalHeaderItem(0, QTableWidgetItem("รหัสผู้ขาย"))
        self.ui.tb_customerDetail.setHorizontalHeaderItem(1, QTableWidgetItem("ชื่อ"))
        self.ui.tb_customerDetail.setHorizontalHeaderItem(2, QTableWidgetItem("จังหวัด"))
        self.ui.tb_customerDetail.setHorizontalHeaderItem(3, QTableWidgetItem("กลุ่ม/หมู่บ้าน"))
        self.ui.tb_customerDetail.setHorizontalHeaderItem(4,QTableWidgetItem("หัวหน้ากลุ่ม"))
        self.ui.tb_customerDetail.setHorizontalHeaderItem(5, QTableWidgetItem("เบอร์โทรศัพท์"))
        
        header = self.ui.tb_customerDetail.horizontalHeader()         
        for col in range(column):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
            
        tablerow = 0
        for row in customerData:
            self.ui.tb_customerDetail.setItem(tablerow,0,QTableWidgetItem(str(row[0])))
            self.ui.tb_customerDetail.setItem(tablerow,1,QTableWidgetItem(row[1]))
            self.ui.tb_customerDetail.setItem(tablerow,2,QTableWidgetItem(row[2]))
            self.ui.tb_customerDetail.setItem(tablerow,3,QTableWidgetItem(row[3]))
            self.ui.tb_customerDetail.setItem(tablerow,4,QTableWidgetItem(row[4]))
            self.ui.tb_customerDetail.setItem(tablerow,5,QTableWidgetItem(row[5]))
            tablerow += 1

    def add_customer(self):      
        if (self.ui.txt_name_customer_DB.text() != ""):
                id = self.ui.txt_customerID_DB.text()
                name = self.ui.txt_name_customer_DB.text()
                address = self.ui.txt_address_customer_DB.text()
                group = self.ui.txt_group_customer_DB.text()
                leader = self.ui.txt_leaderName_customer_DB.text()
                phone = self.ui.txt_phone_customer_DB.text()
                                
                val = (id, name, address, group, leader, phone)
                self.db.AddNewCustomer(val)
                self.loadCustomerTable()
                self.clear_from_addnewCustomer()
        else:
            self.msgBoxError()

    def clear_from_addnewCustomer(self):
        self.ui.txt_customerID_DB.clear()
        self.ui.txt_name_customer_DB.clear()
        self.ui.txt_address_customer_DB.clear()
        self.ui.txt_phone_customer_DB.clear()
        self.ui.txt_group_customer_DB.clear()
        self.ui.txt_leaderName_customer_DB.clear()  
        self.ui.txt_phone_customer_DB.clear()
             
    def msgBoxError(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("ผิดพลาด")
        dlg.setText("โปรดใส่ข้อมูลให้ครบ")
        dlg.setStandardButtons(QMessageBox.Ok)
        dlg.exec()     
    
    def setcmb(self):
        # add item to material type
        self.ui.cmb_MaterialType.addItem("บุรีรัมย์]")     
        self.ui.cmb_MaterialType.addItem("สกลนคร")     
        
        self.ui.cmd_building.addItem("A") 
        self.ui.cmd_building.addItem("B") 
        self.ui.cmd_building.addItem("C") 
        self.ui.cmd_building.addItem("D") 
        
        self.ui.cmb_level_staff_config.addItem("employee")
        self.ui.cmb_level_staff_config.addItem("manager")
        self.ui.cmb_level_staff_config.addItem("admin")

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)            
        self.ui.btnLogin.clicked.connect(self.btn_login_handler)
        
    def btn_login_handler(self):
        password = self.ui.txt_Password.text()
        userID = self.ui.txt_userID.text()

        # Read DB
        try:
            db = Database()
            PasswordDB = db.CheckPassword(userID)
            if str(password) == str(PasswordDB):
                self.open_main_window(userID)
            else:
                QMessageBox.warning(self, "ผิดพลาด", "Password ไม่ถูกต้อง")
        except:
            QMessageBox.warning(self, "ผิดพลาด", "ไม่มี User ID นี้ในระบบ")
  
    def open_main_window(self,uID):
        self.main_window = MainWindow(uID)
        self.main_window.show()
        self.close()  # ปิดหน้าต่าง Login
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    app.exec()    