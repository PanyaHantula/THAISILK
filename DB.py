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

    # Check for login form
    def CheckPassword(self, id):
        # ตรวจสอบ username และ password
        sql = "SELECT password FROM users WHERE id=" + str(id)
        self.cursor.execute(sql)
        returnDB = self.cursor.fetchall()
        password = returnDB[0][0]
        
        return password
    
    def LoadNameFromUserID(self,uID):
        sql = "SELECT name FROM users WHERE id=" + str(uID)
        self.cursor.execute(sql)
        returnDB = self.cursor.fetchall()
        name = returnDB[0][0]
        return name
    
    # config weight reject 
    def updateDB_BasketWeight(self,weight):
        sql="UPDATE basket SET weight=" + weight + "WHERE id=1"
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()  
        
    def LoadDB_BasketWeight(self):
        self.cursor.execute("SELECT * FROM basket")
        return self.cursor.fetchall()
    
    # config weight reject 
    def updateDB_MaterialPrice(self,sakon,buriram):
        sql="UPDATE material SET sakon=%s, buriram=%s WHERE id=1"
        val = (sakon,buriram)
        self.cursor.execute(sql,val)
        self.db.commit()
        return self.cursor.fetchall()  
    
    def LoadDB_MaterialPrice(self):
        self.cursor.execute("SELECT * FROM material")
        return self.cursor.fetchall()
    
    # config weight reject 
    def updateWeightReject(self,A,B,C,D,E,F):
        sql="UPDATE grade SET A=%s, B=%s, C=%s, D=%s, E=%s, F=%s WHERE idgrade=1"
        val = (A,B,C,D,E,F)
        self.cursor.execute(sql,val)
        self.db.commit()
        return self.cursor.fetchall()  
    
    def loadGradematerial(self):
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
    password = db.CheckPassword("0040")
    print(password)
    
    # sql = "INSERT INTO customer (id, name) VALUES ('001', 'AOM')"            
    # db.query(sql)    
    #db.select_all()
    
    # cmd = "SELECT * FROM dataLoger WHERE total_product = 9"
    # resultes = db.query(cmd)
    # for row in resultes:
    #     print (row)   
   # INSERT INTO `ThaiSilkProducts`.`customer` (`id`, `name`, `surname`, `address`, `phone`, `group`, `headgroup`) VALUES ('003', 'A', 'A', 'A', 'A', 'D', 'B');



