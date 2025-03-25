############################################
#           Pyside 6 + Qt Designer         #
############################################
import sys
from PySide6.QtCore import QThread, QObject, Signal, Slot, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, \
    QMessageBox, QWidget, QHeaderView, QFileDialog
from main_GUI_windows import Ui_MainWindow
from Login_GUI_windows import Ui_Dialog
from DB import Database
from gsheet import *
import pandas as pd
import datetime
import serial
import random 
import numpy as np

############################################
#       sunford get weigth Thread          #
############################################
class SunfordWeightRead(QObject):
        # PyQt Signals
    WeightThreadProgress = Signal(str)

    def __init__(self,SerialPortName):
        super().__init__()

        # port = "/dev/tty.PL2303G-USBtoUART11140"
        baud_rate = "9600"
        try:
            self.ser = serial.Serial(SerialPortName, baud_rate, timeout=1)
            print(f"Connected to {SerialPortName} at {baud_rate} baud.")
        except Exception as e:
            print(f"Error: {e}")
            return
    
    @Slot()
    def getWeight(self):
        while True:
            try:
                if self.ser.in_waiting > 0:
                    rx = self.ser.readline().decode('utf-8').strip()
                    if (rx == "?"):
                        rx = self.ser.readline().decode('utf-8').strip()
                        # print(f"{rx}") 
                        self.WeightThreadProgress.emit(rx)
            except Exception as e:
                print(f"Error reading serial: {e}")
                self.WeightThreadProgress.emit("ERROR")
                break
        pass
                      
class MainWindow(QMainWindow):
    def __init__(self, UserID_Login):
        super().__init__()

        global userLogin
        userLogin = UserID_Login
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("ระบบรับซื้อใบหม่อน") 
        
        # data base config
        self.db = Database()            
        self.SetUserID_LevelRule(UserID_Login)
        self.loadCustomerTable()
        self.loadStaffTable()
        self.loadMaterialGrade()
        self.loadMaterialPrice()
        self.loadBasketWeight()
        self.LoadSerialPortConfig()
        self.LoadOrderIDList()

        # GUI Config      
        self.setClock()
        self.SetItemAllCombox()
        self.btnLink()
        self.Gen_OrderID_AutoNumber()
        self.setThread()

    # Config btn link to function
    def btnLink(self):   
        ############# customer config #############
        self.ui.btn_add_customer.clicked.connect(self.add_customer)
        self.ui.btn_delete_customer.clicked.connect(self.delete_Customer)
        self.ui.tb_customerDetail.clicked.connect(self.loadTextboxCustomer)
        self.ui.btn_edit_customer.clicked.connect(self.edit_Customer)
        self.ui.btn_clear_customer.clicked.connect(self.clear_from_addnewCustomer)
        
        ############# staff config #############
        self.ui.btn_add_staff.clicked.connect(self.add_staff)
        self.ui.btn_delete_staff.clicked.connect(self.delete_staff)
        self.ui.tb_staffDetail.clicked.connect(self.loadTextboxStaff)
        self.ui.btn_edit_staff.clicked.connect(self.edit_staff)
        self.ui.btn_clear_staff_config.clicked.connect(self.clear_from_addNewStaff)
    
        ############# config part #############
        self.ui.btn_SaveWeightOfGradeConfig.clicked.connect(self.updateGradeMatrial)
        self.ui.btn_SavePriceMaterial.clicked.connect(self.updateDB_MaterialPrice)
        self.ui.btn_Save_ConfigWeigthBasket.clicked.connect(self.updateDB_BasketWeight)
        self.ui.btn_SerialPortSet.clicked.connect(self.SetSerialPort)
        
        ############# main Page setup #############
        self.ui.btn_customerSelect.clicked.connect(self.SelectCustomerToMainpage)
        self.ui.btn_orderSet.clicked.connect(self.OrderID_Set)
        self.ui.btn_Create_Order.clicked.connect(self.CreateOrder)
        self.ui.btn_RandomWeight.clicked.connect(self.randomweight)
        self.ui.btn_Save_Main.clicked.connect(self.RecordWeight)
        self.ui.btn_DeleteData_main.clicked.connect(self.DeleteRecordMain)
        self.ui.cmb_container.activated.connect(self.changeContanierType)
        self.ui.btn_SaveWasteWeight.clicked.connect(self.RecordWasteWeight)
        self.ui.btn_SaveContainerWeight.clicked.connect(self.RecordContainerWeight)
        self.GradeSelectSetup()

        # Disable btn befor create order
        # self.ui.btn_RandomWeight.hide()
        self.ui.btn_Save_Main.setDisabled(True)
        self.ui.btn_DeleteData_main.setDisabled(True)

        # Disabled btn Wast and bag weight befor Create Order
        self.ui.btn_SaveWasteWeight.setDisabled(True)
        self.ui.btn_SaveContainerWeight.setDisabled(True)

        # self.ui.btn_RandomWeight.hide()
        self.ui.txt_wasteWeight.setDisabled(True)
        self.ui.txt_ContainerWeight.setDisabled(True)
        
        #############  Resulte Page #############
        self.ui.btn_CreateResulte.clicked.connect(self.LoadRecordToResultes)
        self.ui.btn_SaveExternalWeight.clicked.connect(self.RecordExternalWeight)
        self.ui.checkBox_ExteranalWeight.stateChanged.connect(self.SetExternalWeight)
        self.ui.btn_UploadReport.clicked.connect(self.UploadData)
        
        self.ui.btn_UploadReport.setDisabled(True)
        self.ui.btn_SaveExternalWeight.setDisabled(True)
        self.ui.txt_ExternalWeightInput.setDisabled(True)
        
        ############ ALL Database List ############
        self.ui.tb_ALL_DataList.clicked.connect(self.LoadDataRecordByOrderList)
        self.ui.btn_SaveExcelFile.clicked.connect(self.exportToExcel)

    #################### Load data record by order list ###################
    # Load data record by order list when start program
    def LoadOrderIDList(self):
        orderList = self.db.DBLoadOrderIDList()
        column_names = ['เลขที่รายการรับซื้อ']
        # Set Table Dimensions
        self.ui.tb_ALL_DataList.setRowCount(len(orderList))
        self.ui.tb_ALL_DataList.setColumnCount(len(column_names))
        self.ui.tb_ALL_DataList.setHorizontalHeaderLabels(column_names)

        # create Table
        header = self.ui.tb_ALL_DataList.horizontalHeader()         
        for col in range(len(column_names)):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)

        tablerow = 0
        for row in orderList:
            self.ui.tb_ALL_DataList.setItem(tablerow,0,QTableWidgetItem(str(row[1])))
            tablerow += 1
    
    ################### LoadDataRecordByOrderList function ###################
    def LoadDataRecordByOrderList(self):
        # Load data record with orderID to table list
        orderID = self.ui.tb_ALL_DataList.item(self.ui.tb_ALL_DataList.currentIndex().row(),0).text()
        recordDetal = self.db.DBloadResulte(orderID)
        
        column_names = ['เวลา','เลขที่รับซื้อ','ตะกร้า','น้ำหนัก','เกรด','หักน้ำหนัก','ภาชนะ','น้ำหนักภาชนะ','น้ำหนักสุทธิ','ชนิดพันธุ์','ราคา','ชื่อผู้ขาย','หมู่บ้าน','จังหวัด','หัวหน้ากลุ่ม','ผู้รับซื้อ','อาคาร']

        # Set Table Dimensions
        self.ui.tb_ALL_DataRecoreList.setRowCount(len(recordDetal))
        self.ui.tb_ALL_DataRecoreList.setColumnCount(len(column_names))
        self.ui.tb_ALL_DataRecoreList.setHorizontalHeaderLabels(column_names)

        # create Table
        header = self.ui.tb_ALL_DataRecoreList.horizontalHeader()         
        for col in range(len(column_names)):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)

        tablerow = 0
        for row in recordDetal:
            self.ui.tb_ALL_DataRecoreList.setItem(tablerow,0,QTableWidgetItem(str(row[0])))
            self.ui.tb_ALL_DataRecoreList.setItem(tablerow,1,QTableWidgetItem(str(row[1])))
            self.ui.tb_ALL_DataRecoreList.setItem(tablerow,2,QTableWidgetItem(str(row[2])))
            self.ui.tb_ALL_DataRecoreList.setItem(tablerow,3,QTableWidgetItem(str(row[3])))
            self.ui.tb_ALL_DataRecoreList.setItem(tablerow,4,QTableWidgetItem(str(row[4])))
            self.ui.tb_ALL_DataRecoreList.setItem(tablerow,5,QTableWidgetItem(str(row[5])))
            self.ui.tb_ALL_DataRecoreList.setItem(tablerow,6,QTableWidgetItem(str(row[6])))
            self.ui.tb_ALL_DataRecoreList.setItem(tablerow,7,QTableWidgetItem(str(row[7])))

            self.ui.tb_ALL_DataRecoreList.setItem(tablerow,9,QTableWidgetItem(str(row[8])))
            self.ui.tb_ALL_DataRecoreList.setItem(tablerow,10,QTableWidgetItem(str(row[9])))
            self.ui.tb_ALL_DataRecoreList.setItem(tablerow,11,QTableWidgetItem(str(row[10])))
            self.ui.tb_ALL_DataRecoreList.setItem(tablerow,12,QTableWidgetItem(str(row[11])))
            self.ui.tb_ALL_DataRecoreList.setItem(tablerow,13,QTableWidgetItem(str(row[12])))
            self.ui.tb_ALL_DataRecoreList.setItem(tablerow,14,QTableWidgetItem(str(row[13])))
            self.ui.tb_ALL_DataRecoreList.setItem(tablerow,15,QTableWidgetItem(str(row[14])))
            self.ui.tb_ALL_DataRecoreList.setItem(tablerow,16,QTableWidgetItem(str(row[15])))
            tablerow += 1

        # calculate final weight per basket
        colIndex = 8
        for rowIndex in range (tablerow):
            weight = float(self.ui.tb_ALL_DataRecoreList.item(rowIndex, 3).text())
            weightReject = float(self.ui.tb_ALL_DataRecoreList.item(rowIndex, 5).text())
            weightBasket = float(self.ui.tb_ALL_DataRecoreList.item(rowIndex, 7).text())
            finalWeightPerUnit = weight - weightReject - weightBasket
            self.ui.tb_ALL_DataRecoreList.setItem(rowIndex, colIndex, QTableWidgetItem(str(("{0:.2f}".format(finalWeightPerUnit)))))

        self.LoadOrderDetailByOrderList(orderID)

    ################### LoadOrderDetailByOrderList function ###################
    def LoadOrderDetailByOrderList(self,id):
        # Load data record to Resulte page and calculate again
        orderID = self.ui.tb_ALL_DataList.item(self.ui.tb_ALL_DataList.currentIndex().row(),0).text()
        self.ui.txt_OrderID_Search.setText(orderID)
        self.ui.btn_CreateResulte.click()

        # load order and customer detail
        ReturnDB  = self.db.DBloadOrderDetailsToList(orderID)
        if ReturnDB == []:
            return
        else:
            ReturnDB = list(ReturnDB[0])

        # load weight detail
        totalWeight = self.ui.lbl_Resulte_TotalWeightMeterial.text()
        TotalWeightReject = self.ui.lbl_Resulte_TotalWeightReject.text()
        TotalWeightBasket = self.ui.lbl_Resulte_TotalWeightBasket.text()
        TotalCountBasket = self.ui.lbl_Resulte_TotalBasket.text()
        weightBasket = self.ui.lbl_Resulte_weightBasket.text()
        
        bagWeight = self.ui.lbl_Resulte_ContainerWeight.text()
        WestWight = self.ui.lbl_Resulte_TotalWeightReject_west.text()
        externalWight = self.ui.lbl_Resulte_ExternalWeight.text()
        finalWeight = self.ui.lbl_Resulte_TotalWeight_toManuFactory.text()
        price = self.ui.lbl_Resulte_Price.text()
        cost = self.ui.lbl_Resulte_TotalPrice.text()

        val = [totalWeight,
               TotalWeightReject,
               TotalWeightBasket,
               TotalCountBasket,
               weightBasket,
               WestWight,
               bagWeight,
               externalWight,
               finalWeight,
               price,
               cost]

        # conbine data
        OrderDetails = ReturnDB + val

        Row_names = ['เลขที่',
                     'วัน/เวลา',
                     'รหัสผู้รับซื้อ',
                     'ผู้รับซื้อ',
                     'รหัสผู้ขาย',
                     'ผู้ขาย',
                     'หมู่บ้าน',
                     'จังหวัด',
                     'หัวหน้ากลุ่ม',
                     'โทรศัพท์',
                     'ชนิดพันธุ์',
                     'อาคาร',
                     'น้ำหนักรวม(kg)',
                     'น้ำหนักใบเสียรวม(kg)',
                     'น้ำหนักตะกร้ารวม(kg)',
                     'จำนวนตะกร้า(ใบ)',
                     'น้ำหนักตะกร้า(kg)',
                     'น้ำหนักสิ่งเจือปน(kg)',
                     'น้ำหนักถุงบรรจุ(kg)',
                     'น้ำหนักหน้าไร่(kg)',
                     'น้ำหนักสุทธิ(kg)',
                     'ราคารับซื้ิอ',
                     'รวมเป็นเงินสุทธิ'
                     ]
        column = 2

        # Set Table Dimensions
        self.ui.tb_OrderDetail.setRowCount(len(Row_names))
        self.ui.tb_OrderDetail.setColumnCount(column)
        self.ui.tb_OrderDetail.setHorizontalHeaderItem(0, QTableWidgetItem("รายการ"))
        self.ui.tb_OrderDetail.setHorizontalHeaderItem(1, QTableWidgetItem("ข้อมูล"))
        
        header = self.ui.tb_OrderDetail.horizontalHeader()         
        for col in range(column):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)

        for row in range(len(Row_names)):
            self.ui.tb_OrderDetail.setItem(row,0,QTableWidgetItem(str(Row_names[row])))
            self.ui.tb_OrderDetail.setItem(row,1,QTableWidgetItem(str(OrderDetails[row])))

    ################### Export data to excel ###################
    def exportToExcel(self):  
        # create record deteail column header list
        columnHeaders = ['เวลา','เลขที่รับซื้อ','ตะกร้า','น้ำหนัก','เกรด','หักน้ำหนัก','ภาชนะ','น้ำหนักภาชนะ','น้ำหนักสุทธิ','ชนิดพันธุ์','ราคา','ชื่อผู้ขาย','หมู่บ้าน','จังหวัด','หัวหน้ากลุ่ม','ผู้รับซื้อ','อาคาร']
        WeightRecordDetail = pd.DataFrame(columns=columnHeaders)
        for row in range(self.ui.tb_ALL_DataRecoreList.rowCount()):
            for col in range(self.ui.tb_ALL_DataRecoreList.columnCount()):
                WeightRecordDetail.at[row, columnHeaders[col]] = self.ui.tb_ALL_DataRecoreList.item(row, col).text()

        # create order detail column header list
        columnHeaders = ['รายการ','ข้อมูล']
        OrderDetail = pd.DataFrame(columns=columnHeaders)
        for row in range(self.ui.tb_OrderDetail.rowCount()):
            for col in range(self.ui.tb_OrderDetail.columnCount()):
                OrderDetail.at[row, columnHeaders[col]] = self.ui.tb_OrderDetail.item(row, col).text()

        self.result_df = pd.concat([OrderDetail, WeightRecordDetail], axis=1)
        # save Excel File
        try:     
               # Get File name   
            path = QFileDialog.getSaveFileName(self,
            caption='Select a data file',
            filter='Excel File (*.xlsx *.xls)')
            #print(path)
            self.result_df.to_excel(path[0], index=False)

            dlg = QMessageBox(self)
            dlg.setWindowTitle("บันทึกข้อมูล")
            dlg.setText("บันทึกข้อมูลสำเร็จ")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.exec()    

            self.log(f"UserID {str(userLogin)} - Export data to excel") # logfile

        except:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("ผิดพลาด")
            dlg.setText("การบันทึกข้อมูลไม่สำเร็จ")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.exec()    

    ################### UploadData to google function ###################
    def UploadData(self):  
    # create record deteail column header list
        columnHeaders = ['เวลา','เลขที่รับซื้อ','ตะกร้า','น้ำหนัก','เกรด','หักน้ำหนัก','ภาชนะ','น้ำหนักภาชนะ','น้ำหนักสุทธิ','ชนิดพันธุ์','ราคา','ชื่อผู้ขาย','หมู่บ้าน','จังหวัด','หัวหน้ากลุ่ม','ผู้รับซื้อ','อาคาร']
        WeightRecordDetail = pd.DataFrame(columns=columnHeaders)
        for row in range(self.ui.tb_ALL_DataRecoreList.rowCount()):
            for col in range(self.ui.tb_ALL_DataRecoreList.columnCount()):
                WeightRecordDetail.at[row, columnHeaders[col]] = self.ui.tb_ALL_DataRecoreList.item(row, col).text()

        # create order detail column header list
        columnHeaders = ['รายการ','ข้อมูล']
        OrderDetail = pd.DataFrame(columns=columnHeaders)
        for row in range(self.ui.tb_OrderDetail.rowCount()):
            for col in range(self.ui.tb_OrderDetail.columnCount()):
                OrderDetail.at[row, columnHeaders[col]] = self.ui.tb_OrderDetail.item(row, col).text()

        result_df = pd.concat([OrderDetail, WeightRecordDetail], axis=1)
        result_df = result_df.replace(np.nan, None)
        
        # Creating an empty list that is convert from dataframe to list
        res=[]
        for column in result_df.columns:
            li = result_df[column].tolist()
            res.append(li)

        # Transpose Elements of Two Dimensional List 
        val = [list(row) for row in zip(*res)]

        id = self.ui.txt_OrderID_Search.text()
        uploadCompleated = self.db.LoadUploadReportDetail(id)
        if uploadCompleated != []:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("แจ้งเตือน")
            dlg.setText("เลขที่รายการรับซื้อนี้เคยอัปโหลดข้อมูล Google Sheet แล้ว!!!\nต้องการอัปโหลดข้อมูลซ้ำหรือไม่ ??")
            dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            dlg.setIcon(QMessageBox.Question)
            button = dlg.exec()

            if button == QMessageBox.Yes:
                # Googls Sheet config
                self.gSheet = googlesheet()
                self.creds = self.gSheet.connect_sheet()

                # upload to google sheet
                self.gSheet.UpdateSheet(self.creds,val)
                self.db.UploadReport(id)

                dlg = QMessageBox(self)
                dlg.setWindowTitle("แจ้งเตือน")
                dlg.setText("การอัปโหลดข้อมูลสำเร็จ")
                dlg.setStandardButtons(QMessageBox.Ok)
                dlg.exec() 

                self.log(f"UserID {str(userLogin)} - UploadData to google sheet --> {id}") # logfile
            else:
                return

        else:
            # Googls Sheet config
            self.gSheet = googlesheet()
            self.creds = self.gSheet.connect_sheet()

            # upload to google sheet
            self.gSheet.UpdateSheet(self.creds,val)
            self.db.UploadReport(id)
            self.log(f"UserID {str(userLogin)} - UploadData to google sheet --> {id}") # logfile

    ################### RecordWasteWeight function ###################
    def RecordWasteWeight(self):

        self.ui.txt_wasteWeight.setText(self.ui.lbl_weight.text())
        self.ui.lbl_weight.setText('00.00')
        wastWeight = self.ui.txt_wasteWeight.text()
        orderID = self.ui.lbl_OrderID_main.text()
        
        self.ui.lbl_Resulte_TotalWeightReject_west.setText(wastWeight)      
        self.db.DBUpdateWastWeightByOrder(orderID,wastWeight)
        self.LoadWastWeight()
        self.calOrder()
        
        self.log(f"UserID {str(userLogin)} - Create Record Wast Weight --> {orderID}") # logfile

    ################### RecordContainerWeight function ###################
    def RecordContainerWeight(self):

        self.ui.txt_ContainerWeight.setText(self.ui.lbl_weight.text())
        self.ui.lbl_weight.setText('00.00')
        ContainerWeight = self.ui.txt_ContainerWeight.text()
        orderID = self.ui.lbl_OrderID_main.text()
        
        self.ui.lbl_Resulte_ContainerWeight.setText(ContainerWeight)       
        self.db.DBUpdateContainerWeightByOrder(orderID,ContainerWeight)
        self.LoadWastWeight()
        self.calOrder()

        self.log(f"UserID {str(userLogin)} - Create Record Containe Weight --> {orderID}") # logfile

    ################### External Weight function###################
    def SetExternalWeight(self):
        # Active btn and Input Text
        # print(self.ui.checkBox_ExteranalWeight.isChecked()) 
        if (self.ui.checkBox_ExteranalWeight.isChecked()):
            self.ui.txt_ExternalWeightInput.setDisabled(False)
            self.ui.btn_SaveExternalWeight.setDisabled(False)
        else:
            self.ui.btn_SaveExternalWeight.setDisabled(True)
            self.ui.txt_ExternalWeightInput.setDisabled(True)

    def RecordExternalWeight(self):
        self.ui.lbl_Resulte_ExternalWeight.setText(self.ui.txt_ExternalWeightInput.text())

        orderID = self.ui.lbl_OrderID_3.text()
        ExternalWeight = self.ui.lbl_Resulte_ExternalWeight.text()
        self.db.UpdateExternalWeightByOrder(orderID,ExternalWeight)

        if float(ExternalWeight) > 0:
            self.CalOrderExternalWeight()
            self.log(f"UserID {str(userLogin)} - Create Record External Weight --> {orderID}") # logfile
        else:
            self.LoadRecordToResultes()
    
    def CalOrderExternalWeight(self):       
        self.ui.lbl_Resulte_TotalWeight_Accounting.setText(self.ui.lbl_Resulte_ExternalWeight.text())

        # calculate payment
        Price = float(self.ui.lbl_Resulte_Price.text())
        finalWeight = float(self.ui.lbl_Resulte_TotalWeight_Accounting.text())

        finalPayment = finalWeight * Price
        self.ui.lbl_Resulte_TotalPrice.setText(str(("{0:.2f}".format(finalPayment))))

    ################### Record Weight ###################
    # Load Record data To Resultes page with orderID
    def LoadRecordToResultes(self):
        # id = '20250305005'
        # check orderID is saved in DB ??

        id = self.ui.txt_OrderID_Search.text()
        recordDetal = self.db.DBloadResulte(id)
        if recordDetal == []:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("ผิดพลาด")
            dlg.setText("เลขที่รายการรับซื้อนี้ ไม่พบข้อมูล\nโปรดตรวจสอบเลขที่รายการรับซื้อให้ถูกต้อง \nหรือ ตรวจสอบการบันทึกน้ำหนักที่หน้าแรกใหม่อีกครั้ง")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.exec()   
            return
        else:
            column_names = ['เวลา','เลขที่รับซื้อ','ตะกร้า','น้ำหนัก','เกรด','หักน้ำหนัก','ภาชนะ','น้ำหนักภาชนะ','น้ำหนักสุทธิ','ชนิดพันธุ์','ราคา','ชื่อผู้ขาย','หมู่บ้าน','จังหวัด','หัวหน้ากลุ่ม','ผู้รับซื้อ','อาคาร']

            # Set Table Dimensions
            self.ui.tb_ReslutesDetail.setRowCount(len(recordDetal))
            self.ui.tb_ReslutesDetail.setColumnCount(len(column_names))
            self.ui.tb_ReslutesDetail.setHorizontalHeaderLabels(column_names)

            # create Table
            header = self.ui.tb_ReslutesDetail.horizontalHeader()         
            for col in range(len(column_names)):
                header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)

            tablerow = 0
            for row in recordDetal:
                self.ui.tb_ReslutesDetail.setItem(tablerow,0,QTableWidgetItem(str(row[0])))
                self.ui.tb_ReslutesDetail.setItem(tablerow,1,QTableWidgetItem(str(row[1])))
                self.ui.tb_ReslutesDetail.setItem(tablerow,2,QTableWidgetItem(str(row[2])))
                self.ui.tb_ReslutesDetail.setItem(tablerow,3,QTableWidgetItem(str(row[3])))
                self.ui.tb_ReslutesDetail.setItem(tablerow,4,QTableWidgetItem(str(row[4])))
                self.ui.tb_ReslutesDetail.setItem(tablerow,5,QTableWidgetItem(str(row[5])))
                self.ui.tb_ReslutesDetail.setItem(tablerow,6,QTableWidgetItem(str(row[6])))
                self.ui.tb_ReslutesDetail.setItem(tablerow,7,QTableWidgetItem(str(row[7])))

                self.ui.tb_ReslutesDetail.setItem(tablerow,9,QTableWidgetItem(str(row[8])))
                self.ui.tb_ReslutesDetail.setItem(tablerow,10,QTableWidgetItem(str(row[9])))
                self.ui.tb_ReslutesDetail.setItem(tablerow,11,QTableWidgetItem(str(row[10])))
                self.ui.tb_ReslutesDetail.setItem(tablerow,12,QTableWidgetItem(str(row[11])))
                self.ui.tb_ReslutesDetail.setItem(tablerow,13,QTableWidgetItem(str(row[12])))
                self.ui.tb_ReslutesDetail.setItem(tablerow,14,QTableWidgetItem(str(row[13])))
                self.ui.tb_ReslutesDetail.setItem(tablerow,15,QTableWidgetItem(str(row[14])))
                self.ui.tb_ReslutesDetail.setItem(tablerow,16,QTableWidgetItem(str(row[15])))
                tablerow += 1
                
            # calculate final weight per basket
            colIndex = 8
            for rowIndex in range (tablerow):
                weight = float(self.ui.tb_ReslutesDetail.item(rowIndex, 3).text())
                weightReject = float(self.ui.tb_ReslutesDetail.item(rowIndex, 5).text())
                weightBasket = float(self.ui.tb_ReslutesDetail.item(rowIndex, 7).text())
                finalWeightPerUnit = weight - weightReject - weightBasket
                self.ui.tb_ReslutesDetail.setItem(rowIndex, colIndex, QTableWidgetItem(str(("{0:.2f}".format(finalWeightPerUnit)))))
            
            # calculate final weight per basket
            SumRawWeight = 0.0
            SumWeightReject = 0.0
            for rowIndex in range (tablerow):
                SumRawWeight += float(self.ui.tb_ReslutesDetail.item(rowIndex, 3).text())
                SumWeightReject += float(self.ui.tb_ReslutesDetail.item(rowIndex, 5).text())
                
            self.ui.lbl_Resulte_TotalWeightMeterial.setText(str(("{0:.2f}".format(SumRawWeight))))    
            self.ui.lbl_Resulte_TotalWeightReject.setText(str(("{0:.2f}".format(SumWeightReject))))
                
            ######### มีบางครั้งข้อมูลโหลดไม่ได้ แสดงผลหน้า Resulte ผิดพลาด       
            OrderDetails = self.db.DBloadOrderDetails(id) 
            orderID = OrderDetails[0][0]
            
            # show Order Details
            self.ui.lbl_OrderID_3.setText(str(orderID))
            datettime = str(OrderDetails[0][1])
            self.ui.lbl_Order_Date_3.setText(datettime[:10])
            self.ui.lbl_Order_Time_3.setText((datettime[10:]))
            self.ui.lbl_Staff_ID_2.setText(OrderDetails[0][2])
            self.ui.lbl_Staff_name_3.setText(OrderDetails[0][3])
            self.ui.lbl_customer_ID_2.setText(OrderDetails[0][4])
            self.ui.lbl_customer_HeadGroup_2.setText(OrderDetails[0][5])
            self.ui.lbl_building_2.setText(OrderDetails[0][6])
            self.ui.lbl_MaterialType_2.setText(OrderDetails[0][7])
            
            # load basket weight and materail typr
            self.ui.lbl_Resulte_weightBasket.setText(str(OrderDetails[0][8]))
            self.ui.lbl_Resulte_Type.setText(self.ui.lbl_MaterialType_2.text())
            self.ui.lbl_Resulte_Price.setText(str(OrderDetails[0][9]))

            # Update TotalBasket
            totalBasket = self.db.DB_CountBasket(id)
            weightBasket = self.ui.lbl_Resulte_weightBasket.text()
            totalBasketWeight = float(totalBasket) * float(weightBasket)
            
            self.ui.lbl_Resulte_TotalBasket.setText(str(totalBasket))
            self.ui.lbl_Resulte_TotalWeightBasket.setText(str(("{0:.2f}".format(totalBasketWeight))))
    
            # Load wast and bag weight
            weightLoss = self.db.LoadWastWeightByOrder(str(orderID))
            wastWeight = weightLoss[0][0]
            Bagweight = weightLoss[0][1]

            self.ui.lbl_Resulte_TotalWeightReject_west.setText(str(wastWeight))
            self.ui.txt_wasteWeight.setText(str(wastWeight))
            
            self.ui.lbl_Resulte_ContainerWeight.setText(str(Bagweight))
            self.ui.txt_ContainerWeight.setText(str(Bagweight))

            # cal Order function
            # reset external weight 
            self.ui.lbl_Resulte_ExternalWeight.setText("0.0")

            # cal accounting
            self.calOrder()

            # load external weight and recalculate accounting again
            ExternalWeight = self.db.LoadExternalWeightByOrder(orderID)

            if float(ExternalWeight[0][0]) > 0:
                self.ui.lbl_Resulte_ExternalWeight.setText(str(ExternalWeight[0][0]))
                self.ui.lbl_Resulte_TotalWeight_Accounting.setText(str(ExternalWeight[0][0]))
                self.CalOrderExternalWeight()

            # Check Upload report to google complate
            uploadCompleated = self.db.LoadUploadReportDetail(id)
            if uploadCompleated == []:
                self.ui.lbl_uploadreport.setText("-")
            else:
                self.ui.lbl_uploadreport.setText(str(uploadCompleated[0][0]))

    ################### Record Weight ###################   
    # calculate order in resulte page 
    # Active with button cal_resulte is clicked
    def calOrder(self):
        # Cal final weight to processing line 
        Raw_Weight = float(self.ui.lbl_Resulte_TotalWeightMeterial.text())
        WeightReject = float(self.ui.lbl_Resulte_TotalWeightReject.text())
        WeightBasket = float(self.ui.lbl_Resulte_TotalWeightBasket.text())
        ContainerWeight = float(self.ui.lbl_Resulte_ContainerWeight.text())
        WestWeightReject_west = float(self.ui.lbl_Resulte_TotalWeightReject_west.text())
        
        finalWeight = Raw_Weight - WeightReject - WeightBasket - ContainerWeight - WestWeightReject_west
        
        # update finalWeightT
        self.ui.lbl_Resulte_TotalWeight_toManuFactory.setText(str(("{0:.2f}".format(finalWeight))))
        self.ui.lbl_Resulte_TotalWeight_Accounting.setText(str(("{0:.2f}".format(finalWeight))))

        # calculate payment
        Price = float(self.ui.lbl_Resulte_Price.text())
        
        finalPayment = finalWeight * Price
        self.ui.lbl_Resulte_TotalPrice.setText(str(("{0:.2f}".format(finalPayment))))

        self.ui.btn_UploadReport.setDisabled(False)
    
    ################### Record Weight ###################    
    # Record Weight
    def RecordWeight(self):
        orderID = self.ui.lbl_OrderID_main.text()
        weight = self.ui.lbl_weight.text()
        basketNumber = self.ui.txt_basketName.text()

        grade = self.ui.lbl_MaterialGrade_main.text()
        if (grade == "A"):
            weightReject = self.ui.txt_config_Grade_A.text()
        elif (grade == "B"):
            weightReject = self.ui.txt_config_Grade_B.text()
        elif (grade == "C"):
            weightReject = self.ui.txt_config_Grade_C.text()
        elif (grade == "D"):
            weightReject = self.ui.txt_config_Grade_D.text()
        elif (grade == "E"):
            weightReject = self.ui.txt_config_Grade_E.text()
        elif (grade == "F"):
            weightReject = self.ui.txt_config_Grade_F.text()

        MaterialType = self.ui.lbl_MaterialType_main.text()
        if (MaterialType == "buriram"):
            Price = self.ui.txt_Price_material_BURIRAM.text()
        elif (MaterialType == "sakonnakhon"):
            Price = self.ui.txt_Price_material_SAKON.text()  

        Staff_ID = self.ui.lbl_Staff_ID.text()
        customer_ID = self.ui.lbl_customer_ID.text()
        building_main = self.ui.lbl_building_main.text()

        container = self.ui.cmb_container.currentText()
        if container == "basket":
            containerWeight = self.ui.txt_ConfigWeigthBasket.text()
        else:
            containerWeight = 0
            
        if (orderID != "-"):
            if (basketNumber != ""):
                val = (orderID, weight, basketNumber, grade, weightReject, MaterialType, Price, Staff_ID, customer_ID, building_main, container,containerWeight)
                self.db.DBweightRecord(val)
                self.LoadRecordToMain()
                self.ui.lbl_weight.setText('00.00')
                self.ui.lbl_MaterialGrade_main.setText("A")
                
                if (self.ui.cmb_container.currentText() == "basket"):
                    self.ui.txt_basketName.clear()
            else:
                dlg = QMessageBox(self)
                dlg.setWindowTitle("ผิดพลาด")
                dlg.setText("โปรดใส่เบอร์ตระกร้า")
                dlg.setStandardButtons(QMessageBox.Ok)
                dlg.exec()  
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("ผิดพลาด")
            dlg.setText("โปรดสร้างรายการการรับซื้อก่อน")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.exec() 

    ################### LoadRecordToMain ###################    
    # Load Record To table in Main when orderId is saved         
    def LoadRecordToMain(self):
        orderID = self.ui.lbl_OrderID.text()
        recordDetal = self.db.DBloadRecord(orderID)
        
        column_names = ['ON','time','เลขที่','น้ำหนัก','เบอร์ตะกร้า','เกรด','หักน้ำหนัก','สายพันธู์','ราคา','ผู้ซื้อ','ผู้ขาย','อาคาร','ภาชนะ','น้ำหนักภาชนะ']

        # Set Table Dimensions
        self.ui.tb_MainRecordDetail.setRowCount(len(recordDetal))
        self.ui.tb_MainRecordDetail.setColumnCount(len(column_names))
        self.ui.tb_MainRecordDetail.setHorizontalHeaderLabels(column_names)

        # create Table
        header = self.ui.tb_MainRecordDetail.horizontalHeader()         
        for col in range(len(column_names)):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        
        # Populate Table
        for row_idx, row_data in enumerate(recordDetal):
            for col_idx, cell_data in enumerate(row_data):
                self.ui.tb_MainRecordDetail.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))

    ################### DeleteRecordMain ###################    
    # even function when button delete is clicked             
    def DeleteRecordMain(self):
        id = self.ui.tb_MainRecordDetail.item(self.ui.tb_MainRecordDetail.currentIndex().row(),0).text()
        SelectRowToDetete = self.ui.tb_MainRecordDetail.currentRow()
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle("ลบข้อมูล")
        dlg.setText("ต้องการลบข้อมูลหรือไม่ ??\n เวลาที่ต้องการลบ : \n" + id)
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button = dlg.exec()
        
        if button == QMessageBox.Yes:
            if SelectRowToDetete < 0:
                return
            self.ui.tb_MainRecordDetail.removeRow(SelectRowToDetete)
            self.db.DBdeleteRecord(id)
            self.LoadRecordToMain()
    
    ################### Change container type ###################
    def changeContanierType(self):
        self.ui.cmb_container.currentText()
        if (self.ui.cmb_container.currentText() == "bag"):
            self.ui.txt_basketName.setText("0")
            self.ui.txt_basketName.setEnabled(False) # disable comboBox
        else:
            self.ui.txt_basketName.clear()
            self.ui.txt_basketName.setEnabled(True)  # enable comboBox 
    
    ################### Grade Select ###################
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
        
    ################### sunford reading and update Thread ########################## 
    # sunford 
    def setThread(self):
        # Initialize worker and thread
        self.SunfordThread = QThread()
        self.SunfordThread.setObjectName('SunfordWeight')   # Create thread 
        
        SerialPortName = self.ui.txt_SerialPortName.text()
        self.SunfordWorker = SunfordWeightRead(SerialPortName)                # Create worker
        self.SunfordWorker.moveToThread(self.SunfordThread)         # move worker to thread 
        self.SunfordThread.started.connect(self.SunfordWorker.getWeight)     # Connect Thread
        self.SunfordWorker.WeightThreadProgress.connect(self.UpdateWeight)     # Connect signals and slots
        self.SunfordThread.start()    # Start Thread
        
    def UpdateWeight(self,weight):
        self.ui.lbl_weight.setText(weight)
    
    ################### randomweight ########################## 
    # random Weight when con't connect to meachine
    def randomweight(self):
        randomWeight = (random.uniform(10, 20))
        self.UpdateWeight(str("{:.2f}".format(randomWeight)))
  
    ################### OrderID_Set ########################## 
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

            # check old orderID in DB with data in mainWeight table if emtry orderID that it create
            LastOrderWeightRejects = self.db.SearchLastOrderWeight(orderID)
            if (LastOrderWeightRejects == 0):
                # print('Create a AddNewOrderWeightRejects')
                val = (orderID,'0','0')
                self.db.AddNewOrderWeightRejects(val)

                val = (orderID,'0')
                self.db.AddExternalWeightByOrder(val)     

            # Enable save weight of main page
            self.ui.btn_Save_Main.setDisabled(False)
            self.ui.btn_DeleteData_main.setDisabled(False)    

            self.log(f"UserID {str(userLogin)} - Create Order --> {orderID}") # logfile

        else:
            self.msgBoxError()
            
    ################### OrderID_Set ########################## 
    # Set orderID that load record data and wast weight when orderID are saved in DB 
    def OrderID_Set(self):
        now = datetime.datetime.now()
        
        self.ui.lbl_Order_Time.setText(now.strftime("%H:%M:%S"))
        self.ui.lbl_Order_Date.setText(now.strftime("%d-%b-%Y"))
        self.ui.lbl_OrderID.setText(self.ui.txt_OrderID_Set.text())
        self.ui.txt_OrderID_Search.setText(str(self.ui.lbl_OrderID.text()))    # Set OrderID to Resulte Page
        self.ui.txt_OrderID_Set.clear()
        
        # Load record to main table
        self.LoadRecordToMain()
        self.LoadWastWeight()

    ################### LoadWastWeight function ########################## 
    # load wast weight of order inside DB that is used for edit order
    # --- Please revise this function -----
    def LoadWastWeight(self):
        # Enable btn Wast and bag weight
        orderID = self.ui.lbl_OrderID.text()
        self.ui.btn_SaveWasteWeight.setDisabled(False)
        self.ui.btn_SaveContainerWeight.setDisabled(False)    
    
        # check old orderID in DB with data in mainWeight table if emtry orderID that it create
        LastOrderWeightRejects = self.db.SearchLastOrderWeight(orderID)
        if (LastOrderWeightRejects != 0):
            # Load wast and bag weight
            weightLoss = self.db.LoadWastWeightByOrder(str(orderID))
            wastWeight = weightLoss[0][0]
            Bagweight = weightLoss[0][1]

            # update text in main and resulte page
            self.ui.lbl_Resulte_TotalWeightReject_west.setText(str(wastWeight))
            self.ui.txt_wasteWeight.setText(str(wastWeight))
            
            self.ui.lbl_Resulte_ContainerWeight.setText(str(Bagweight))
            self.ui.txt_ContainerWeight.setText(str(Bagweight))    

            # load external weight
            externalWeight = self.db.LoadExternalWeightByOrder(orderID)
            self.ui.txt_ExternalWeightInput.setText(str(externalWeight[0][0]))
            self.ui.lbl_Resulte_ExternalWeight.setText(str(externalWeight[0][0]))

    ################### Gen_OrderID_AutoNumber config ########################## 
    def Gen_OrderID_AutoNumber(self):
        # please set orderID before use program 
        # Set oderID as "YYYYMMDD0001"
        LastOrder = str(self.db.GetLastOrder())
        LastOrder = LastOrder[8:]
        
        now = datetime.datetime.now()
        NowOrder = str(now.strftime("%Y%m%d")) + LastOrder
        NowOrder = int(NowOrder) + 1
        
        self.ui.txt_OrderID_Set.setText(str(NowOrder))
    
    ################### Clock config ##########################   
    # Get customer detail from DB and display on main page
    def SelectCustomerToMainpage(self):
        customerID = self.ui.txt_customerID.text()      # get customerID from txtbox
        try:
            customerDetails = self.db.loadSingleCustomer(customerID)       # Get customer detail from DB 
            # print(customerDetails[0][0])   # display data from DB before pare to lable
           
            # Diaplay customer to main page
            self.ui.lbl_customer_ID.setText(str(customerDetails[0][1]))
            self.ui.lbl_customer_name.setText(str(customerDetails[0][2]))
            self.ui.lbl_customer_Address.setText(str(customerDetails[0][3]))
            self.ui.lbl_customer_Group.setText(str(customerDetails[0][4]))
            self.ui.lbl_customer_LeadGroupName.setText(str(customerDetails[0][5]))
            self.ui.lbl_customer_phone.setText(str(customerDetails[0][6]))
            
        except:
            QMessageBox.warning(self, "ผิดพลาด", "ไม่มีรหัสผู้ขายนี้อยู่ในฐานข้อมูล")

        self.ui.txt_customerID.clear()      # clear customer txt box

    ################### Set UserID LevelRule function ##########################    
    def SetUserID_LevelRule (self, userID):
        # logfile
        self.log(f"UserID {str(userLogin)} - login")

        StaffName = self.db.LoadNameFromUserID(userID)
        self.ui.lbl_Staff_ID.setText(userID)
        self.ui.lbl_Staff_name.setText(StaffName)
        
        self.UserLevel = self.db.LoadLevelFromUserID(userID)
        showLevel = "(" + self.UserLevel + ")"
        self.ui.lbl_UserLevelShow.setText(showLevel)
        
        if (self.UserLevel == "admin"):
            pass

        elif (self.UserLevel == "manager"):
            self.ui.groupBox_19.setDisabled(True)       # user edit
            self.ui.groupBox_3.hide()                   # hidden uer table
            # self.ui.groupBox_23.setDisabled(True) 

        elif (self.UserLevel == "employee"):
            self.ui.groupBox_4.setDisabled(True)        # customer edit
            self.ui.groupBox_12.setDisabled(True)       # grade edit
            self.ui.groupBox_13.setDisabled(True)       # basket weight edit
            self.ui.groupBox_15.setDisabled(True)       # type Price edit
            self.ui.groupBox_19.setDisabled(True)       # user edit
            self.ui.groupBox_3.hide()                   # hidden uer table
            # self.ui.groupBox_23.setDisabled(True) 

    ################### Clock config ##########################
    # update clock with 1 min interval
    def setClock(self):
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
    
    def showTime(self):
        label_time = datetime.datetime.now().strftime("%H:%M")
        self.ui.lbl_Clock.setText(label_time)
        
        dateNow = datetime.datetime.now().strftime("%d-%b-%Y")
        self.ui.lbl_dateNow.setText(dateNow)
    
    # ################## Serial Port config ##########################  
    def SetSerialPort(self):
        SerialPortName = self.ui.txt_SerialPortName.text()
        self.db.updateSerialPortName(SerialPortName)
        self.log(f"UserID {str(userLogin)} - Update Serial Port Name") # logfile
    
    def LoadSerialPortConfig(self):
        comport = self.db.LoadSerialPortName()
        self.ui.txt_SerialPortName.setText(comport)  
          
    # ################## BasketWeight config ##########################  
    def updateDB_BasketWeight(self):
        weight = self.ui.txt_ConfigWeigthBasket.text()
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle("แก้ไขข้อมูล")
        dlg.setText("ต้องการแก้ข้อมูลน้ำหนักตะกร้าหรือไม่ ??")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button = dlg.exec()
        
        if button == QMessageBox.Yes:
            if (weight != ""):
                self.db.updateDB_BasketWeight(str(weight))
                self.loadBasketWeight()

                self.log(f"UserID {str(userLogin)} - Update Basket Weight") # logfile
            else:
                return
                 
    def loadBasketWeight(self):
        weight = self.db.LoadDB_BasketWeight()
        self.ui.txt_ConfigWeigthBasket.setText(str(weight[0][2]))

    # ################### Material Price config #########################  
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
                self.db.updateDB_MaterialPrice(price_buriram,price_sakon)
                self.loadMaterialPrice()
                self.log(f"UserID {str(userLogin)} - Update Matrial Price") # logfile
            else:
                return
                
    def loadMaterialPrice(self):
        price = self.db.LoadMaterialPrice()
        self.ui.txt_Price_material_BURIRAM.setText(str(price[0][2]))
        self.ui.txt_Price_material_SAKON.setText(str(price[1][2]))

    # ################### Material Grade config #########################  
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
                self.loadMaterialGrade()

                self.log(f"UserID {str(userLogin)} - Update Matrial Grade") # logfile
            else:
                return
 
    def loadMaterialGrade(self):
        grade = self.db.loadALLGradematerial()
        # print((grade))
        # print(grade[0][2])

        self.ui.txt_config_Grade_A.setText(str(grade[0][2]))
        self.ui.txt_config_Grade_B.setText(str(grade[1][2]))
        self.ui.txt_config_Grade_C.setText(str(grade[2][2]))
        self.ui.txt_config_Grade_D.setText(str(grade[3][2]))
        self.ui.txt_config_Grade_E.setText(str(grade[4][2]))
        self.ui.txt_config_Grade_F.setText(str(grade[5][2]))
    
    # ################## staff Config ##########################    
    def loadTextboxStaff(self):
        self.id_EditUser = self.ui.tb_staffDetail.item(self.ui.tb_staffDetail.currentIndex().row(),0).text()
        uid = self.ui.tb_staffDetail.item(self.ui.tb_staffDetail.currentIndex().row(),1).text()
        username = self.ui.tb_staffDetail.item(self.ui.tb_staffDetail.currentIndex().row(),2).text()
        password = self.ui.tb_staffDetail.item(self.ui.tb_staffDetail.currentIndex().row(),3).text()
        level = self.ui.tb_staffDetail.item(self.ui.tb_staffDetail.currentIndex().row(),4).text()
        name = self.ui.tb_staffDetail.item(self.ui.tb_staffDetail.currentIndex().row(),5).text()
        
        self.ui.txt_staff_id_config.setText(uid)
        self.ui.txt_username_staff_config.setText(username)
        self.ui.txt_password_staff_config.setText(password)
        self.ui.cmb_level_staff_config.setCurrentText(level)
        self.ui.txt_name_staff_config.setText(name)
            
    def edit_staff(self):
        uid = self.ui.txt_staff_id_config.text()
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
                self.db.EditStaff(self.id_EditUser,uid, username, password, level, name)
                self.loadStaffTable()
                self.clear_from_addNewStaff()

                self.log(f"UserID {str(userLogin)} - Edit User") # logfile
            else:
                return
            
    def delete_staff(self):
        id = self.ui.tb_staffDetail.item(self.ui.tb_staffDetail.currentIndex().row(),0).text()
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
            # self.ui.tb_staffDetail.removeRow(SelectRowToDetete)
            self.db.DeleteStaff(id)
            self.loadStaffTable()
            self.clear_from_addNewStaff()

            self.log(f"UserID {str(userLogin)} - Delete User") # logfile
            
    def loadStaffTable(self):
        # Get customer data from DB
        column,row,staffData = self.db.loadAllStaff()
        
        # create Table
        self.ui.tb_staffDetail.setRowCount(row)
        self.ui.tb_staffDetail.setColumnCount(column)
        self.ui.tb_staffDetail.setHorizontalHeaderItem(0, QTableWidgetItem("ON"))
        self.ui.tb_staffDetail.setHorizontalHeaderItem(1, QTableWidgetItem("id"))
        self.ui.tb_staffDetail.setHorizontalHeaderItem(2, QTableWidgetItem("username"))
        self.ui.tb_staffDetail.setHorizontalHeaderItem(3, QTableWidgetItem("password"))
        self.ui.tb_staffDetail.setHorizontalHeaderItem(4, QTableWidgetItem("level"))
        self.ui.tb_staffDetail.setHorizontalHeaderItem(5, QTableWidgetItem("name"))
        
        header = self.ui.tb_staffDetail.horizontalHeader()         
        for col in range(column):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        
        tablerow = 0
        for row in staffData:
            self.ui.tb_staffDetail.setItem(tablerow,0,QTableWidgetItem(str(row[0])))
            self.ui.tb_staffDetail.setItem(tablerow,1,QTableWidgetItem(row[1]))
            self.ui.tb_staffDetail.setItem(tablerow,2,QTableWidgetItem(row[2]))
            self.ui.tb_staffDetail.setItem(tablerow,3,QTableWidgetItem(row[3]))
            self.ui.tb_staffDetail.setItem(tablerow,4,QTableWidgetItem(row[4]))
            self.ui.tb_staffDetail.setItem(tablerow,5,QTableWidgetItem(row[5]))
            tablerow += 1
    
    def add_staff(self):      
        if (self.ui.txt_staff_id_config.text() != ""):
                uid = self.ui.txt_staff_id_config.text()
                username = self.ui.txt_username_staff_config.text()
                password = self.ui.txt_password_staff_config.text()
                level = self.ui.cmb_level_staff_config.currentText()
                name = self.ui.txt_name_staff_config.text()
                
                val = (uid, username, password, level, name)
                self.db.AddNewStaff(val)
                self.loadStaffTable()
                self.clear_from_addNewStaff()

                self.log(f"UserID {str(userLogin)} - ADD User") # logfile
        else:
            self.msgBoxError()
    
    def clear_from_addNewStaff(self):
        self.ui.txt_staff_id_config.clear()
        self.ui.txt_username_staff_config.clear()
        self.ui.txt_password_staff_config.clear()
        self.ui.cmb_level_staff_config.setCurrentText("employee")
        self.ui.txt_name_staff_config.clear()

    # ############################################  
    # ------ Customer Config ---------     
    def loadTextboxCustomer(self):
        self.ID_EditCustomer = self.ui.tb_customerDetail.item(self.ui.tb_customerDetail.currentIndex().row(),0).text()
        customerID = self.ui.tb_customerDetail.item(self.ui.tb_customerDetail.currentIndex().row(),1).text()
        name = self.ui.tb_customerDetail.item(self.ui.tb_customerDetail.currentIndex().row(),2).text()
        address = self.ui.tb_customerDetail.item(self.ui.tb_customerDetail.currentIndex().row(),3).text()
        village_group = self.ui.tb_customerDetail.item(self.ui.tb_customerDetail.currentIndex().row(),4).text()
        leader = self.ui.tb_customerDetail.item(self.ui.tb_customerDetail.currentIndex().row(),5).text()
        phone = self.ui.tb_customerDetail.item(self.ui.tb_customerDetail.currentIndex().row(),6).text()
        
        self.ui.txt_customerID_DB.setText(customerID)
        self.ui.txt_name_customer_DB.setText(name)
        self.ui.txt_address_customer_DB.setText(address)
        self.ui.txt_group_customer_DB.setText(village_group)
        self.ui.cmb_leaderName_customer_DB.setCurrentText(leader)
        self.ui.txt_phone_customer_DB.setText(phone)

    def edit_Customer(self):
        customerID = self.ui.txt_customerID_DB.text()
        name = self.ui.txt_name_customer_DB.text()
        address = self.ui.txt_address_customer_DB.text()
        village_group = self.ui.txt_group_customer_DB.text()
        leader = self.ui.cmb_leaderName_customer_DB.currentText()
        phone = self.ui.txt_phone_customer_DB.text()
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle("แก้ไขข้อมูล")
        dlg.setText("ต้องการแก้ข้อมูลผู้ใช้งานหรือไม่ ??\n ผู้ขาย : " + name)
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button = dlg.exec()
        
        if button == QMessageBox.Yes:
            if (self.ui.txt_customerID_DB.text() != ""):
                self.db.EditCustomer(self.ID_EditCustomer , customerID, name, address, village_group, leader, phone)
                self.loadCustomerTable()
                self.clear_from_addnewCustomer()

                self.log(f"UserID {str(userLogin)} - Edit Customer") # logfile
            else:
                return
          
    def delete_Customer(self):
        id = self.ui.tb_customerDetail.item(self.ui.tb_customerDetail.currentIndex().row(),0).text()
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
            self.db.DeleteCustomer(id)
            self.loadCustomerTable()

            self.log(f"UserID {str(userLogin)} - Delete Customer") # logfile
            
    def loadCustomerTable(self):
        # Get customer data from DB
        column,row,customerData = self.db.LoadAllCustomer()
        
        # create Table
        self.ui.tb_customerDetail.setRowCount(row)
        self.ui.tb_customerDetail.setColumnCount(column)
        self.ui.tb_customerDetail.setHorizontalHeaderItem(0, QTableWidgetItem("ON"))
        self.ui.tb_customerDetail.setHorizontalHeaderItem(1, QTableWidgetItem("รหัสผู้ขาย"))
        self.ui.tb_customerDetail.setHorizontalHeaderItem(2, QTableWidgetItem("ชื่อ"))
        self.ui.tb_customerDetail.setHorizontalHeaderItem(3, QTableWidgetItem("จังหวัด"))
        self.ui.tb_customerDetail.setHorizontalHeaderItem(4, QTableWidgetItem("กลุ่ม/หมู่บ้าน"))
        self.ui.tb_customerDetail.setHorizontalHeaderItem(5,QTableWidgetItem("หัวหน้ากลุ่ม"))
        self.ui.tb_customerDetail.setHorizontalHeaderItem(6, QTableWidgetItem("เบอร์โทรศัพท์"))
        
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
            self.ui.tb_customerDetail.setItem(tablerow,6,QTableWidgetItem(row[6]))
            tablerow += 1
                            
    def add_customer(self):      
        if (self.ui.txt_name_customer_DB.text() != ""):
                id = self.ui.txt_customerID_DB.text() 
                name = self.ui.txt_name_customer_DB.text()
                address = self.ui.txt_address_customer_DB.text()
                group = self.ui.txt_group_customer_DB.text()
                leader = self.ui.cmb_leaderName_customer_DB.currentText()
                phone = self.ui.txt_phone_customer_DB.text()
                                
                val = (id, name, address, group, leader, phone)
                self.db.AddNewCustomer(val)
                self.loadCustomerTable()
                self.clear_from_addnewCustomer()

                self.log(f"UserID {str(userLogin)} - add customer") # logfile
        else:
            self.msgBoxError()

    def clear_from_addnewCustomer(self):
        self.ui.txt_customerID_DB.clear()
        self.ui.txt_name_customer_DB.clear()
        self.ui.txt_address_customer_DB.clear()
        self.ui.txt_phone_customer_DB.clear()
        self.ui.txt_group_customer_DB.clear()
        self.ui.cmb_leaderName_customer_DB.setCurrentText("-")
        self.ui.txt_phone_customer_DB.clear()

    #  ################### msgBoxError #########################
    def msgBoxError(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("ผิดพลาด")
        dlg.setText("โปรดใส่ข้อมูลให้ครบ")
        dlg.setStandardButtons(QMessageBox.Ok)
        dlg.exec()     
    
    ################### SetItemCombox #########################
    def SetItemAllCombox(self):
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
        
        self.ui.cmb_leaderName_customer_DB.addItem("-")
        self.ui.cmb_leaderName_customer_DB.addItem("บริษัท ไทยซิลค์โปรดัคส์ จำกัด")
        self.ui.cmb_leaderName_customer_DB.addItem("คุณนันทพัทธ  พุกกะนะสุตร")
        self.ui.cmb_leaderName_customer_DB.addItem("คุณอารียา  แสไธสง")
        self.ui.cmb_leaderName_customer_DB.addItem("คุณบุญรอด  สร้างการนอก")
        self.ui.cmb_leaderName_customer_DB.addItem("คุณอำนวย  มีสถาน")
        self.ui.cmb_leaderName_customer_DB.addItem("บริษัท ไร่นายจุล คุ้นวงศ์ จำกัด")

    def log(self,msg):

        dateNow = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        val = dateNow + " : " + msg + "\n"
        # print(val)

        f = open("log.txt", "a")
        f.write(val)
        f.close()

############################################
#  Login Windows
# - please revise a login method

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)   
        self.setWindowTitle("ระบบรับซื้อใบหม่อน")          
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
    login_window = LoginWindow()
    login_window.show()
    app.exec()    
    
    # For Testing Program
    # app = QApplication(sys.argv)
    # MainWindow = MainWindow("0010")
    # MainWindow.show()
    # app.exec()  