# ###########################################
#       Data Base SQL Class                 #
#       used mysql.comnector library        #
# ###########################################
import mysql.connector

class Database:
    def __init__(self,):
        # print("MySQL Connector version: ",mysql.connector.__version__)
        self.connect_db()
    
    # Connect DB           
    def connect_db(self):
        try:
            # print("#: Connecting to SQL Database")
            self.db = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="p@ssw0rd",
                database="thaisilkproducts",
                port=3306
                )    
            self.cursor = self.db.cursor()
            # print("#: complete")
        except:
            print("#: Error connecting Database")   
        
    def select_all(self):
        cmd = "SELECT * FROM orders"
        self.cursor.execute(cmd)
        for row in self.cursor.fetchall():
            print (row)
    
    def query(self,cmd):
        self.cursor.execute(cmd)
        self.db.commit()
        return self.cursor.fetchall()
    
    # DBUploadRecrord
    def UploadReport(self,orderID):
        sql = "INSERT INTO uploadreport (orderID) VALUES ({});".format(orderID)
        self.cursor.execute(sql)
        self.db.commit()

    def LoadUploadReportDetail(self,orderID):
        sql = "SELECT time FROM uploadreport WHERE orderID='" + str(orderID) + "'" + 'ORDER BY id DESC LIMIT 1'
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # order list
    def DBLoadOrderIDList(self):
        sql = "SELECT * FROM WeightLossByOrder"
        self.cursor.execute(sql)
        row = self.cursor.fetchall()
        return row
    
    # External weight
    def LoadExternalWeightByOrder(self,id):
        sql = "SELECT weight FROM externalweights WHERE orderID='" + str(id) + "'"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def AddExternalWeightByOrder(self,val):
        sql = "INSERT INTO externalweights (orderID, weight) VALUES " + str(val)
        self.cursor.execute(sql)
        self.db.commit()
    
    def UpdateExternalWeightByOrder(self,id,weight):
        sql="UPDATE externalweights SET weight='" + weight + "' WHERE orderID = " + str(id)
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall() 
    
    # Config Serial port
    def updateSerialPortName(self,name):
        sql="UPDATE configs SET value='" + name + "' WHERE id = 1"
        self.cursor.execute(sql)
        self.db.commit()
    
    def LoadSerialPortName(self):
        sql = "SELECT value FROM configs WHERE id = 1"
        self.cursor.execute(sql)
        returnDB = self.cursor.fetchall()
        return returnDB[0][0]
       
    # orderWeightRejects
    def LoadWastWeightByOrder(self,id):
        sql = "SELECT WasteWeight, ContainerWeight FROM WeightLossByOrder WHERE orderID='" + str(id) + "'"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def DBUpdateWastWeightByOrder(self,id,weight):
        sql="UPDATE WeightLossByOrder SET WasteWeight='" + weight + "' WHERE orderID = " + str(id)
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall() 
    
    def DBUpdateContainerWeightByOrder(self,id,weight):
        sql="UPDATE WeightLossByOrder SET ContainerWeight='" + weight + "' WHERE orderID = " + str(id)
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall() 
    
    def AddNewOrderWeightRejects(self,val):
        sql = "INSERT INTO WeightLossByOrder (orderID, WasteWeight, ContainerWeight) VALUES " + str(val)
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()

    def SearchLastOrderWeight(self,id):
        sql = "SELECT COUNT(*) FROM WeightLossByOrder WHERE orderID='" + str(id) + "'"
        self.cursor.execute(sql)
        returnDB = self.cursor.fetchall()
        return returnDB[0][0]
    
    # reslute 
    def DBloadResulte(self,id):      
        #sql = "SELECT * FROM orders WHERE orderID=" + str(id)
        sql = "SELECT orders.time " +\
                ", orders.orderID " +\
                ", orders.basketNumber " +\
                ", orders.weight " +\
                ", orders.grade " +\
                ", orders.weightReject " +\
                ", orders.container " +\
                ", orders.containerWeight " +\
                ", orders.materialType " +\
                ", orders.price " +\
                ", customers.name " +\
                ", customers.village " +\
                ", customers.address " +\
                ", customers.leaderName " +\
                ", users.name " +\
                ", orders.building " +\
                "FROM orders " +\
                "LEFT JOIN grades ON orders.grade = grades.type " +\
                "LEFT JOIN customers ON orders.customerID = customers.customerID " +\
                "LEFT JOIN users ON orders.staffID = users.uid " +\
                "WHERE orderID='" + str(id) + "'"
        
        self.cursor.execute(sql)
        recordDetal = self.cursor.fetchall()
        return recordDetal
    
    def DBloadOrderDetails(self,id):
        #sql = "SELECT * FROM orders WHERE orderID=" + str(id)
        sql = "SELECT orders.orderID " +\
                ", orders.time " +\
                ", users.uid " +\
                ", users.name " +\
                ", customers.customerID " +\
                ", customers.leaderName " +\
                ", orders.building " +\
                ", orders.materialType " +\
                ", orders.containerWeight " +\
                ", orders.price " +\
                "FROM orders " +\
                "LEFT JOIN users ON orders.staffID = users.uid " +\
                "LEFT JOIN customers ON orders.customerID = customers.customerID " +\
                "WHERE orderID='" + str(id) + "' ORDER BY time ASC LIMIT 1"
        
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def DBloadOrderDetailsToList(self,id):
        #sql = "SELECT * FROM orders WHERE orderID=" + str(id)
        sql = "SELECT orders.orderID " +\
                ", orders.time " +\
                ", users.uid " +\
                ", users.name " +\
                ", customers.customerID " +\
                ", customers.leaderName " +\
                ", customers.village " +\
                ", customers.address " +\
                ", customers.leaderName " +\
                ", customers.phone " +\
                ", orders.materialType " +\
                ", orders.building " +\
                "FROM orders " +\
                "LEFT JOIN users ON orders.staffID = users.uid " +\
                "LEFT JOIN customers ON orders.customerID = customers.customerID " +\
                "WHERE orderID='" + str(id) + "' ORDER BY time ASC LIMIT 1"
        
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def DB_CountBasket(self,id):
        sql = "SELECT COUNT(*) FROM orders WHERE container='basket' AND orderID = '" + str(id) + "'"
        self.cursor.execute(sql)
        returnDB = self.cursor.fetchall()
        return returnDB[0][0]
        
    # weight record
    def DBweightRecord(self,val):
        # (`orderID`, `weight`, `basketNumber`, `grade`, `materialType`, `staffID`, `customerID`, `building`, `container`) VALUES ('20250304002', '21', '02', 'B', 'buriram', '0010', '102', 'A', 'basket');
        sql = "INSERT INTO orders (orderID, weight, basketNumber, grade, weightReject, materialType, price, staffID, customerID, building, container,containerWeight) VALUES " + str(val) 
        self.cursor.execute(sql)
        self.db.commit()
        # return self.cursor.fetchall()
    
    def DBloadRecord(self,OrderID):
        sql = "SELECT * FROM orders WHERE orderID='" + str(OrderID) + "' ORDER BY time DESC"
        self.cursor.execute(sql)
        recordDetal = self.cursor.fetchall()

        return recordDetal
        # sql = "SELECT COUNT(*) FROM orders WHERE orderID=" + str(OrderID)
        # self.cursor.execute(sql)
        # returnDB = self.cursor.fetchall()
        # total = returnDB[0][0]
        
        # sql = "SELECT * FROM orders WHERE orderID='" + str(OrderID) + "' ORDER BY time DESC"
        # self.cursor.execute(sql)
        # recordDetal = self.cursor.fetchall()
        # column = 10
        
        # return (column,total,recordDetal)
    
    def DBdeleteRecord(self, time):
        sql = "DELETE FROM orders WHERE id=" + str(time)

        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()
    
    # Get Last Order
    def GetLastOrder(self):
        # Get All customer data
        self.cursor.execute("SELECT orderID FROM orders ORDER BY id DESC LIMIT 1")
        recordDetal = self.cursor.fetchall()
        
        return recordDetal[0][0]
    
    # Check for login form
    def CheckPassword(self, id):
        # ตรวจสอบ username และ password
        sql = "SELECT password FROM users WHERE uid=" + str(id)
        self.cursor.execute(sql)
        returnDB = self.cursor.fetchall()
        password = returnDB[0][0]
        
        return password

    def loadSingleCustomer(self,id):
        sql = "SELECT * FROM customers WHERE customerID=" + str(id)
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def LoadNameFromUserID(self,id):
        sql = "SELECT name FROM users WHERE uid=" + str(id)
        self.cursor.execute(sql)
        returnDB = self.cursor.fetchall()
        name = returnDB[0][0]
        return name
    
    def LoadLevelFromUserID(self,id):
        sql = "SELECT level FROM users WHERE uid=" + str(id)
        self.cursor.execute(sql)
        returnDB = self.cursor.fetchall()
        name = returnDB[0][0]
        return name
    
    # config weight reject 
    def updateDB_BasketWeight(self,weight):
        sql="UPDATE baskets SET weightBasket='" + weight + "' WHERE id=1"
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()  
        
    def LoadDB_BasketWeight(self):
        self.cursor.execute("SELECT * FROM baskets")
        return self.cursor.fetchall()
    
    # config weight reject 
    def updateDB_MaterialPrice(self,buriram,sakonnakhon):
       # sql="UPDATE material SET price=%s, buriram=%s WHERE type=1"
        sql="UPDATE material SET price='" + buriram + "' WHERE id=1"
        self.cursor.execute(sql)
        self.db.commit()
        self.cursor.fetchall() 
        
               # sql="UPDATE material SET price=%s, buriram=%s WHERE type=1"
        sql="UPDATE material SET price='" + sakonnakhon + "' WHERE id=2"
        self.cursor.execute(sql)
        self.db.commit()
        self.cursor.fetchall() 
   
    def LoadMaterialPrice(self):
        self.cursor.execute("SELECT * FROM material")
        return self.cursor.fetchall()
    
    # config weight reject 
    def updateWeightReject(self,grade,weightReject):
        sql="UPDATE grades SET weightReject=%s WHERE type=%s"
        val = (weightReject,grade)
        self.cursor.execute(sql,val)
        self.db.commit()
        return self.cursor.fetchall()  
        
    def loadALLGradematerial(self):
        self.cursor.execute("SELECT * FROM grades")
        return self.cursor.fetchall()
        
    # Staff     
    def loadAllStaff(self):
        # count staff id
        self.cursor.execute("SELECT COUNT(*) FROM users")
        returnDB = self.cursor.fetchall()
        Totalstaff = returnDB[0][0]
        
        # Get All customer data
        self.cursor.execute("SELECT * FROM users")
        StaffDetail = self.cursor.fetchall()
        column = 6
        
        return (column,Totalstaff,StaffDetail)
    
    def AddNewStaff(self,val):
        sql = "INSERT INTO users (uid, username, password, level, name) VALUES " + str(val) 
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()
    
    def DeleteStaff(self,id):
        sql = "DELETE FROM users WHERE id=" + str(id)
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()
    
    def EditStaff(self, id, uid, username, password, level, name):
        sql="UPDATE users SET uid = %s, username = %s, password=%s, level=%s,name=%s  WHERE id=%s"
        val = (uid, username, password, level, name, id)
        self.cursor.execute(sql,val)
        self.db.commit()
        return self.cursor.fetchall()                    
                        
    # Customer 
    def AddNewCustomer(self,val):
        sql = "INSERT INTO customers (customerID, name, address, village, leaderName, phone) VALUES " + str(val) 
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()
    
    def EditCustomer(self, id, customerID, name, address, village_group, leader,phone):
        sql="UPDATE customers SET customerID=%s, name = %s, address=%s , village=%s ,leaderName=%s ,phone=%s WHERE id=%s"
        val = (customerID, name, address, village_group, leader,phone, id)
        self.cursor.execute(sql,val)
        self.db.commit()
        return self.cursor.fetchall()
    
    def LoadAllCustomer(self):
        # count customer id
        self.cursor.execute("SELECT COUNT(*) FROM customers")
        returnDB = self.cursor.fetchall()
        TotalCustomer = returnDB[0][0]
        
        # Get All customer data
        self.cursor.execute("SELECT * FROM customers")
        CustomerDetail = self.cursor.fetchall()
        column = 7
        
        return (column,TotalCustomer,CustomerDetail)

    def DeleteCustomer(self,id):
        sql = "DELETE FROM customers WHERE id=" + str(id)
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()
                        
if __name__ == "__main__":
    db = Database()
    # db.select_all()

    orderID = "202503100008"
    print(db.LoadUploadReportDetail(orderID))
            
