# ###########################################
#       Data Base SQL Class                 #
#       used mysql.comnector library        #
# ###########################################
import mysql.connector

class Database:
    def __init__(self,):
        self.connect_db()
    
    # Connect DB           
    def connect_db(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="p@ssw0rd",
                database="ThaiSilkProducts"
                )    
            self.cursor = self.db.cursor()
            # print("#: Connect SQL Database complete")
        except:
            print("#: Error connecting Database")   
        
    def select_all(self):
        cmd = "SELECT * FROM customer"
        self.cursor.execute(cmd)
        for row in self.cursor.fetchall():
            print (row)
    
    def query(self,cmd):
        self.cursor.execute(cmd)
        self.db.commit()
        return self.cursor.fetchall()

    # reslute 
    def DBloadResulte(self,id):
        sql = "SELECT COUNT(*) FROM orders WHERE orderID=" + str(id)
        self.cursor.execute(sql)
        returnDB = self.cursor.fetchall()
        total = returnDB[0][0]
        
        #sql = "SELECT * FROM orders WHERE orderID=" + str(id)
        sql = "SELECT orders.time " +\
                ", orders.basketNumber " +\
                ", orders.grade " +\
                ", grade.weightReject " +\
                "FROM orders " +\
                "LEFT JOIN grade ON orders.grade = grade.grade " +\
                "WHERE orderID='" + str(id) + "'"
        
        self.cursor.execute(sql)
        recordDetal = self.cursor.fetchall()
        return total,recordDetal
    # weight record
    def DBweightRecord(self,val):
        # (`orderID`, `weight`, `basketNumber`, `grade`, `materialType`, `staffID`, `customerID`, `building`, `container`) VALUES ('20250304002', '21', '02', 'B', 'buriram', '0010', '102', 'A', 'basket');
        sql = "INSERT INTO orders (orderID, weight, basketNumber, grade, materialType, staffID, customerID, building, container) VALUES " + str(val) 
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()
    
    def DBloadRecord(self,id):
        sql = "SELECT COUNT(*) FROM orders WHERE orderID=" + str(id)
        self.cursor.execute(sql)
        returnDB = self.cursor.fetchall()
        total = returnDB[0][0]
        
        sql = "SELECT * FROM orders WHERE orderID='" + str(id) + "' ORDER BY time DESC"
        self.cursor.execute(sql)
        recordDetal = self.cursor.fetchall()
        column = 10
        
        return (column,total,recordDetal)
    
    def DBdeleteRecord(self, time):
        sql = "DELETE FROM orders WHERE time='" + str(time) + "'"

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
        sql = "SELECT password FROM users WHERE id=" + str(id)
        self.cursor.execute(sql)
        returnDB = self.cursor.fetchall()
        password = returnDB[0][0]
        
        return password

    def loadSigleCustomer(self,id):
        sql = "SELECT * FROM customers WHERE id=" + str(id)
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def LoadNameFromUserID(self,id):
        sql = "SELECT name FROM users WHERE id=" + str(id)
        self.cursor.execute(sql)
        returnDB = self.cursor.fetchall()
        name = returnDB[0][0]
        return name
    
    # config weight reject 
    def updateDB_BasketWeight(self,weight):
        sql="UPDATE baskets SET weightReject='" + weight + "' WHERE type = 'baskert'"
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()  
        
    def LoadDB_BasketWeight(self):
        self.cursor.execute("SELECT * FROM baskets")
        return self.cursor.fetchall()
    
    # config weight reject 
    def updateDB_MaterialPrice(self,price,type):
        sql="UPDATE material SET price=%s, buriram=%s WHERE type=1"
        val = (price,type)
        self.cursor.execute(sql,val)
        self.db.commit()
        return self.cursor.fetchall()  
    
    def LoadMaterialPrice(self):
        self.cursor.execute("SELECT * FROM material")
        return self.cursor.fetchall()
    
    # config weight reject 
    def updateWeightReject(self,grade,weightReject):
        sql="UPDATE grade SET weightReject=%s WHERE grade=%s"
        val = (weightReject,grade)
        self.cursor.execute(sql,val)
        self.db.commit()
        return self.cursor.fetchall()  
    
    def loadALLGradematerial(self):
        self.cursor.execute("SELECT * FROM grade")
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
        column = 5
        
        return (column,Totalstaff,StaffDetail)
    
    def AddNewStaff(self,val):
        sql = "INSERT INTO users (id, username, password, level, name) VALUES " + str(val) 
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()
    
    def DeleteStaff(self,id):
        sql = "DELETE FROM users WHERE id=" + str(id)
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()
    
    def EditStaff(self, id, username, password, level, name):
        sql="UPDATE users SET username = %s, password=%s, level=%s,name=%s  WHERE id=%s"
        val = (username, password, level, name, id)
        self.cursor.execute(sql,val)
        self.db.commit()
        return self.cursor.fetchall()                    
                        
    # Customer 
    def AddNewCustomer(self,val):
        sql = "INSERT INTO customers (id, name, address, village, leaderName, phone) VALUES " + str(val) 
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()
    
    def EditCustomer(self, id, name, address, village_group, leader,phone):
        sql="UPDATE customers SET name = %s, address=%s , village=%s ,leaderName=%s ,phone=%s WHERE id=%s"
        val = (name, address, village_group, leader,phone, id)
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
        column = 6
        
        return (column,TotalCustomer,CustomerDetail)

    def DeleteCustomer(self,id):
        sql = "DELETE FROM customers WHERE id=" + str(id)
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()
                        
if __name__ == "__main__":
    db = Database()
    DB_Resulte = db.DBloadResulte('20250305005')
    print(DB_Resulte)
    
    # password = db.CheckPassword("0040")
    # print(password)
    
    # sql = "INSERT INTO customer (id, name) VALUES ('001', 'AOM')"            
    # db.query(sql)    
    #db.select_all()
    
    # cmd = "SELECT * FROM dataLoger WHERE total_product = 9"
    # resultes = db.query(cmd)
    # for row in resultes:
    #     print (row)   
   # INSERT INTO `ThaiSilkProducts`.`customer` (`id`, `name`, `surname`, `address`, `phone`, `group`, `headgroup`) VALUES ('003', 'A', 'A', 'A', 'A', 'D', 'B');



