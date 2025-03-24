import csv
import mysql.connector

# MySQL connection parameters
cnx = mysql.connector.connect(host="127.0.0.1",
                user="root",
                password="p@ssw0rd",
                database="thaisilkproducts"
                )
cursor = cnx.cursor()

# CSV file path
csv_file_path = 'other\\customer.csv'

with open(csv_file_path, mode='r', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    for row in reader:
        # sql = "INSERT INTO customers (customerID, name, address, village, leaderName, phone) VALUES " + str(val) 
        cursor.execute("INSERT INTO customers (customerID, name, address, village, leaderName, phone) VALUES (%s, %s, %s, %s, %s, %s)", row)

cnx.commit()
cursor.close()
cnx.close()


# csv_file_path = 'customer.csv'
# with open(csv_file_path, mode='r', encoding="utf-8") as csvfile:
#     reader = csv.reader(csvfile)
#     for row in reader:
#         print(', '.join(row))
#         #db.AddNewCustomer(row)

    #next(reader)  # Skip the header row
    #print(reader)
#     for row in reader:
#         cursor.execute("INSERT INTO your_table (column1, column2) VALUES (%s, %s)", row)

# cnx.commit()
# cursor.close()
# cnx.close()