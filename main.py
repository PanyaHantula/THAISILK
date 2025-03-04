############################################
#           Pyside 6 + Qt Designer         #
############################################
import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QWidget, QHeaderView
from PySide6.QtCore import QThread, QObject, Signal, Slot, QTimer
from main_GUI import Ui_MainWindow
from Login_GUI import Ui_Dialog
from DB import Database

import datetime
import time
import random 

############################################
#       sunford get weigth Thread          #
############################################
class SunfordWeightWorker(QObject):
    # PyQt Signals
    WeightThreadProgress = Signal(float)
    
    @Slot()
    def getWeight(self):
        # while True:
        #     self.weightDummy = random.uniform(10, 20)
        #     self.WeightThreadProgress.emit(self.weightDummy)
        #     print(self.weightDummy)
        #     time.sleep(10)
        pass
        
    def reset(self):
        self.weightDummy = 0
                  
class MainWindow(QMainWindow):
    def __init__(self, UserID_Login):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = Database()
              
        self.LoadUserStaffName(UserID_Login)
        self.loadCustomerTable()
        self.loadStaffTable()
        self.loadGradeMaterial()
        self.loadMaterialPrice()
        self.loadBasketWeight()
              
        self.setClock()
        self.setcmb()
        self.btnLink()
        self.GenetareOrderID()
        # self.setThread()
                
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
        
        # Button main Page setup
        self.ui.btn_customerSelect.clicked.connect(self.SelectCustomerToMainpage)
        self.ui.btn_orderSet.clicked.connect(self.OrderID_Set)
        self.ui.btn_Create_Order.clicked.connect(self.CreateOrder)
        self.ui.btn_RandomWeight.clicked.connect(self.randomweight)
        self.ui.btn_Save_Main.clicked.connect(self.RecordWeight)
        self.ui.btn_DeleteData_main.clicked.connect(self.DeleteRecordMain)
        self.ui.cmb_container.activated.connect(self.changeContanierType)
        self.GradeSelectSetup()
        
        # Reslutes Page
        self.ui.btn_CreateResulte.clicked.connect(self.LoadRecordToResultes)
        
    # Resulte Page
    def LoadRecordToResultes(self):
        id = self.ui.txt_OrderID_Search.text()
        total,recordDetal = self.db.DBloadResulte('20250305005')
        
        column_names = ['เวลา','ตะกร้า','เกรด','น้ำหนัก']

        # Set Table Dimensions
        self.ui.tb_ReslutesDetail.setRowCount(len(recordDetal))
        self.ui.tb_ReslutesDetail.setColumnCount(len(column_names))
        self.ui.tb_ReslutesDetail.setHorizontalHeaderLabels(column_names)

        header = self.ui.tb_ReslutesDetail.horizontalHeader()         
        for col in range(len(column_names)):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)

        # Populate Table
        for row_idx, row_data in enumerate(recordDetal):
            for col_idx, cell_data in enumerate(row_data):
                self.ui.tb_ReslutesDetail.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
               
        # show ORder Details
        # lbl_OrderID_3
        # lbl_Order_Date_3
        # lbl_Order_Time_3
        # lbl_Staff_ID_2
        # lbl_Staff_name_3
        # lbl_customer_ID_2
        # lbl_customer_name_3
        # lbl_customer_Group_2
        # lbl_customer_HeadGroup_2
        # lbl_building_2
        # lbl_MaterialType_2
    # Record Page
    def RecordWeight(self):
        orderID = self.ui.lbl_OrderID_main.text()
        weight = self.ui.lbl_weight.text()
        basketNumber = self.ui.txt_basketName.text()
        grade = self.ui.lbl_MaterialGrade_main.text()
        MaterialType = self.ui.lbl_MaterialType_main.text()
        Staff_ID = self.ui.lbl_Staff_ID.text()
        customer_ID = self.ui.lbl_customer_ID.text()
        building_main = self.ui.lbl_building_main.text()
        container = self.ui.cmb_container.currentText()
        
        if (orderID != "-"):
            if (basketNumber != "") and (grade != "?"):
                # (orderID, weight, basketNumber, grade, materialType, staffID, customerID, building, container)
                val = (orderID, weight, basketNumber, grade, MaterialType, Staff_ID, customer_ID, building_main, container)
                self.db.DBweightRecord(val)
                self.LoadRecordToMain()
                self.ui.lbl_weight.setText('00.00')
                self.ui.lbl_MaterialGrade_main.setText("?")
                
                if (self.ui.cmb_container.currentText() == "basket"):
                    self.ui.txt_basketName.clear()
            else:
                dlg = QMessageBox(self)
                dlg.setWindowTitle("ผิดพลาด")
                dlg.setText("โปรดใส่เบอร์ตระกร้า \nและ เลือกเกรดวัตุดิบ")
                dlg.setStandardButtons(QMessageBox.Ok)
                dlg.exec()  
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("ผิดพลาด")
            dlg.setText("โปรดสร้างรายการการรับซื้อก่อน")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.exec() 
            
    def LoadRecordToMain(self):
        id = self.ui.lbl_OrderID.text()
        column,row,recordData = self.db.DBloadRecord(id)

        # create Table
        self.ui.tb_MainRecordDetail.setRowCount(row)
        self.ui.tb_MainRecordDetail.setColumnCount(column)
        #self.ui.tb_MainRecordDetail.setHorizontalHeaderItem(0, QTableWidgetItem("order ID"))
        self.ui.tb_MainRecordDetail.setHorizontalHeaderItem(0, QTableWidgetItem("เวลา"))
        self.ui.tb_MainRecordDetail.setHorizontalHeaderItem(1, QTableWidgetItem("เลขที่"))
        self.ui.tb_MainRecordDetail.setHorizontalHeaderItem(2, QTableWidgetItem("น้ำหนัก"))
        self.ui.tb_MainRecordDetail.setHorizontalHeaderItem(3, QTableWidgetItem("ตะกร้า"))
        self.ui.tb_MainRecordDetail.setHorizontalHeaderItem(4, QTableWidgetItem("เกรด"))
        self.ui.tb_MainRecordDetail.setHorizontalHeaderItem(5, QTableWidgetItem("ชนิดพันธุ์"))
        self.ui.tb_MainRecordDetail.setHorizontalHeaderItem(6, QTableWidgetItem("ผู้ซื้อ"))
        self.ui.tb_MainRecordDetail.setHorizontalHeaderItem(7, QTableWidgetItem("ผู้ขาย"))
        self.ui.tb_MainRecordDetail.setHorizontalHeaderItem(8, QTableWidgetItem("อาคาร"))
        self.ui.tb_MainRecordDetail.setHorizontalHeaderItem(9, QTableWidgetItem("พาชนะ"))
        
        header = self.ui.tb_MainRecordDetail.horizontalHeader()         
        for col in range(column):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
            
        tablerow = 0
        for row in recordData:
            # self.ui.tb_MainRecordDetail.setItem(tablerow,0,QTableWidgetItem(str(row[0])))
            self.ui.tb_MainRecordDetail.setItem(tablerow,0,QTableWidgetItem(str(row[1])))
            self.ui.tb_MainRecordDetail.setItem(tablerow,1,QTableWidgetItem(str(row[2])))
            self.ui.tb_MainRecordDetail.setItem(tablerow,2,QTableWidgetItem(str(row[3])))
            self.ui.tb_MainRecordDetail.setItem(tablerow,3,QTableWidgetItem(str(row[4])))
            self.ui.tb_MainRecordDetail.setItem(tablerow,4,QTableWidgetItem(str(row[5])))
            self.ui.tb_MainRecordDetail.setItem(tablerow,5,QTableWidgetItem(str(row[6])))
            self.ui.tb_MainRecordDetail.setItem(tablerow,6,QTableWidgetItem(str(row[7])))
            self.ui.tb_MainRecordDetail.setItem(tablerow,7,QTableWidgetItem(str(row[8])))
            self.ui.tb_MainRecordDetail.setItem(tablerow,8,QTableWidgetItem(str(row[9])))
            self.ui.tb_MainRecordDetail.setItem(tablerow,9,QTableWidgetItem(str(row[10])))
            tablerow += 1
    
    def DeleteRecordMain(self):
        Time = self.ui.tb_MainRecordDetail.item(self.ui.tb_MainRecordDetail.currentIndex().row(),1).text()
        SelectRowToDetete = self.ui.tb_MainRecordDetail.currentRow()
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle("ลบข้อมูล")
        dlg.setText("ต้องการลบข้อมูลหรือไม่ ??\n เวลาที่ต้องการลบ : \n" + Time)
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button = dlg.exec()
        
        if button == QMessageBox.Yes:
            if SelectRowToDetete < 0:
                return
            self.ui.tb_MainRecordDetail.removeRow(SelectRowToDetete)
            self.db.DBdeleteRecord(Time)
            self.LoadRecordToMain()
    
    # Change container type
    def changeContanierType(self):
        self.ui.cmb_container.currentText()
        if (self.ui.cmb_container.currentText() == "bag"):
            self.ui.txt_basketName.setText("0")
            self.ui.txt_basketName.setEnabled(False) # disable comboBox
        else:
            self.ui.txt_basketName.clear()
            self.ui.txt_basketName.setEnabled(True)  # enable comboBox 
    
    # Grade Select
    def GradeSelectSetup(self):
        self.ui.btn_Grade_A.clicked.connect(self.grade_A_set)
        self.ui.btn_Grade_B.clicked.connect(self.grade_B_set)
        self.ui.btn_Grade_C.clicked.connect(self.grade_C_set)
        self.ui.btn_Grade_D.clicked.connect(self.grade_D_set)
        self.ui.btn_Grade_E.clicked.connect(self.grade_E_set)
        self.ui.btn_Grade_F.clicked.connect(self.grade_F_set)
    
    def grade_A_set(self):
        self.ui.lbl_MaterialGrade_main.setText("A")
    def grade_B_set(self):
        self.ui.lbl_MaterialGrade_main.setText("B")
    def grade_C_set(self):
        self.ui.lbl_MaterialGrade_main.setText("C")
    def grade_D_set(self):
        self.ui.lbl_MaterialGrade_main.setText("D")
    def grade_E_set(self):
        self.ui.lbl_MaterialGrade_main.setText("E")
    def grade_F_set(self):
        self.ui.lbl_MaterialGrade_main.setText("F")        
    
    # sunford 
    def setThread(self):
        # Initialize worker and thread
        self.SunfordThread = QThread()
        self.SunfordThread.setObjectName('SunfordWeight')   # Create thread 
        self.SunfordWorker = SunfordWeightWorker()                # Create worker
        self.SunfordWorker.moveToThread(self.SunfordThread) # move worker to thread 
        self.SunfordThread.started.connect(self.SunfordWorker.getWeight)     # Connect Thread
        self.SunfordWorker.WeightThreadProgress.connect(self.UpdateWeight)     # Connect signals and slots
        self.SunfordThread.start()    # Start Thread
        
    def UpdateWeight(self,weight):
        self.ui.lbl_weight.setText(str("{:.2f}".format(weight)))
    
    def randomweight(self):
        self.UpdateWeight(random.uniform(10, 20))
        
    # Create Order
    def CreateOrder(self):
        orderID = self.ui.lbl_OrderID.text()
        customerID = self.ui.lbl_customer_name.text()
        material = self.ui.cmb_MaterialType.currentText()
        if ((orderID != "-") and (customerID != "-") and (material != "-")):
            self.ui.lbl_OrderID_main.setText(orderID)
            self.ui.lbl_Order_Date_main.setText(self.ui.lbl_Order_Date.text())
            self.ui.lbl_Order_Time_main.setText(self.ui.lbl_Order_Time.text())
            self.ui.lbl_customer_name_main.setText(customerID)
            self.ui.lbl_Staff_name_main.setText(self.ui.lbl_Staff_name.text())
            self.ui.lbl_building_main.setText(self.ui.cmd_building.currentText())
            self.ui.lbl_MaterialType_main.setText(material)
            self.ui.lbl_customer_NameLeadGroup_main.setText(self.ui.lbl_customer_LeadGroupName.text())

        else:
            self.msgBoxError()
            
    # OrderID Setup   
    def OrderID_Set(self):
        now = datetime.datetime.now()
        
        self.ui.lbl_Order_Time.setText(now.strftime("%H:%M:%S"))
        self.ui.lbl_Order_Date.setText(now.strftime("%d-%b-%Y"))
        self.ui.lbl_OrderID.setText(self.ui.txt_OrderID_Set.text())
        self.ui.txt_OrderID_Search.setText(str(self.ui.lbl_OrderID.text()))    # Set OrderID to Resulte Page
        self.ui.txt_OrderID_Set.clear()
        
        # Load record to main table
        self.LoadRecordToMain()

    def GenetareOrderID(self):
        # Get Last Order
        LastOrder = self.db.GetLastOrder()
        LastOrder = LastOrder[8:]
        
        now = datetime.datetime.now()
        NowOrder = str(now.strftime("%Y%m%d")) + LastOrder
        NowOrder = int(NowOrder) + 1
        
        self.ui.txt_OrderID_Set.setText(str(NowOrder))
    
    # Load Customer Detail    
    def SelectCustomerToMainpage(self):
        customerID = self.ui.txt_customerID.text()
        try:
            customerDetails = self.db.loadSigleCustomer(customerID)
            # print(customerDetails[0][0])
            self.ui.lbl_customer_ID.setText(str(customerDetails[0][0]))
            self.ui.lbl_customer_name.setText(str(customerDetails[0][1]))
            self.ui.lbl_customer_Address.setText(str(customerDetails[0][2]))
            self.ui.lbl_customer_Group.setText(str(customerDetails[0][3]))
            self.ui.lbl_customer_LeadGroupName.setText(str(customerDetails[0][4]))
            self.ui.lbl_customer_phone.setText(str(customerDetails[0][5]))
            
        except:
            QMessageBox.warning(self, "ผิดพลาด", "ไม่มีรหัสผู้ขายนี้อยู่ในฐานข้อมูล")

        self.ui.txt_customerID.clear()
        
    def LoadUserStaffName (self, userID):
        StaffName = self.db.LoadNameFromUserID(userID)
        self.ui.lbl_Staff_ID.setText(userID)
        self.ui.lbl_Staff_name.setText(StaffName)
    
    # Set Clock
    def setClock(self):
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
    
    def showTime(self):
        label_time = datetime.datetime.now().strftime("%H:%M")
        self.ui.lbl_Clock.setText(label_time)
        
        dateNow = datetime.datetime.now().strftime("%d-%b-%Y")
        self.ui.lbl_dateNow.setText(dateNow)
        
    # Update Basket 
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
        self.ui.txt_ConfigWeigthBasket.setText(str(weight[0][2]))
        
    # Load material price
    def updateDB_MaterialPrice(self):
        price_sakon = self.ui.txt_Price_material_SAKON.text()
        price_buriram = self.ui.txt_Price_material_BURIRAM.text()
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle("แก้ไขข้อมูล")
        dlg.setText("ต้องการแก้ข้อมูลราคารับซื้อวัตถุดิบหรือไม่ ??")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button = dlg.exec()
        
        if button == QMessageBox.Yes:
            if ((price_sakon != "") or (price_buriram != "") ):
                self.db.updateDB_MaterialPrice(price_buriram,'buriram')
                self.db.updateDB_MaterialPrice(price_sakon,'sakonnakhon')
                self.loadMaterialPrice()
            else:
                return
            
    def loadMaterialPrice(self):
        price = self.db.LoadMaterialPrice()
        self.ui.txt_Price_material_BURIRAM.setText(str(price[0][2]))
        self.ui.txt_Price_material_SAKON.setText(str(price[1][2]))
           
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
                self.db.updateWeightReject('A',A)
                self.db.updateWeightReject('B',B)
                self.db.updateWeightReject('C',C)
                self.db.updateWeightReject('D',D)
                self.db.updateWeightReject('E',E)
                self.db.updateWeightReject('F',F)
                self.loadGradeMaterial()
            else:
                return
            
    def loadGradeMaterial(self):
        grade = self.db.loadALLGradematerial()
        # print((grade))
        # print(grade[0][2])

        self.ui.txt_config_Grade_A.setText(str(grade[0][2]))
        self.ui.txt_config_Grade_B.setText(str(grade[1][2]))
        self.ui.txt_config_Grade_C.setText(str(grade[2][2]))
        self.ui.txt_config_Grade_D.setText(str(grade[3][2]))
        self.ui.txt_config_Grade_E.setText(str(grade[4][2]))
        self.ui.txt_config_Grade_F.setText(str(grade[5][2]))
    
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
        self.ui.cmb_MaterialType.addItem("-")     
        self.ui.cmb_MaterialType.addItem("buriram")     
        self.ui.cmb_MaterialType.addItem("sakonnakhon")     
        
        self.ui.cmd_building.addItem("A") 
        self.ui.cmd_building.addItem("B") 
        self.ui.cmd_building.addItem("C") 
        self.ui.cmd_building.addItem("D") 
        
        self.ui.cmb_level_staff_config.addItem("employee")
        self.ui.cmb_level_staff_config.addItem("manager")
        self.ui.cmb_level_staff_config.addItem("admin")
        
        self.ui.cmb_container.addItem("basket")
        self.ui.cmb_container.addItem("bag")

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

        self.ui.txt_Password.clear()
        self.ui.txt_userID.clear()
        
    def open_main_window(self,uID):
        self.main_window = MainWindow(uID)
        self.main_window.show()
        self.close()  # ปิดหน้าต่าง Login
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MainWindow("0010")
    MainWindow.show()
    app.exec()  
    
    # for login form
    # app = QApplication(sys.argv)
    # login_window = LoginWindow()
    # login_window.show()
    # app.exec()    