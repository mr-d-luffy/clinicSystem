from json import load
from colorama import Fore
from random import sample
from datetime import datetime
from pandas import read_sql_query
from qrcode import make
from PIL import Image
from fpdf import FPDF
import sqlite3

api = load(open("json/data.json")) # load the json file in project

class clinic:
    #this constructor created for input filename and Connect to the database
    def __init__(self, tableName):
        self.connection = sqlite3.connect(api["path"][2])
        self.c = self.connection.cursor()
        self.tableName = tableName
    
    # create table in database by this function
    def createDatabase(self):
        try:
            self.c.execute(f"CREATE TABLE {self.tableName} (dateTime text, name text, contactNumber text, customerID text, test text, age text, gender text, fees text, qrcodeimage blob)")
            self.connection.commit()
        except(sqlite3.Error) as e:
            print(Fore.RED,f"Database already connected {e}",Fore.WHITE)

    # this function create 12 digit id for searsh in database
    @staticmethod
    def createID():
        number = "1234567890"
        alpha = "abcdefghijklmnoqrstuvwxyz"
        all = number+alpha
        ID = ''.join(sample(all, 12))
        return ID
    
    # store data in database using this function
    def storeData(self, name, contactNumber, customerID, test, age, gender, fees, bynaryQR):
        date = datetime.now()
        try:
            self.c.execute(f"INSERT INTO {self.tableName} VALUES (?,?,?,?,?,?,?,?,?)", (date, name, contactNumber, customerID, test, age, gender, fees, bynaryQR))
            self.connection.commit()
        except(sqlite3.Error) as e:
            print(Fore.RED,e,Fore.WHITE)

    # show data from database by id using this function
    def showDataById(self, customerID):
        try:
            self.c.execute(f"SELCET * FROM {self.tableName} where customerID={customerID}")
            self.c.fetchall()
            self.connection.commit()
            self.connection.close()
        except(sqlite3.Error) as e:
            print(Fore.RED,e,Fore.WHITE)

    # show data from database by number using this function
    def showDataByNumber(self, contactNumber):
        try:
            self.c.execute(f"SELECT * FROM {self.tableName} where contactNumber={contactNumber}")
            self.c.fetchall()
            self.connection.commit()
            self.connection.close()
        except(sqlite3.Error) as e:
            print(Fore.RED,e,Fore.WHITE)

    # delete data from database using this function
    def deleteDataById(self, customerID):
        try:
            self.c.execute(f"DELETE * FROM {self.tableName} WHERE customerID={customerID} ")
            self.connection.commit()
            self.connection.close()
        except(sqlite3.Error) as e:
            print(Fore.RED,e,Fore.WHITE)

    # read database using this function
    def readDatabase(self):
        try:
            query = f"SELECT * FROM {self.tableName}"
            data = read_sql_query(query, self.connection)
            print(data)
        except(Exception) as e:
            print(Fore.RED, e, Fore.WHITE)

    #this function for create qrcode from the input data
    @staticmethod
    def createQrcode(data, fileName):
        try:
            image = make(data)
            image.save(f"{api["path"][5]}{fileName}.png")
            Photo = Image.open(f"{api["path"][5]}{fileName}.png")
            Photo.show() # open qrcode in new window using this function
        except(Exception) as e:
            print(Fore.RED, e, Fore.WHITE)

    # Canvert image into binary Form to store in database
    @staticmethod
    def imageToBinary(image):
        try:
            with open(f"{api["path"][5]}{image}.png", "rb") as File:
                data = File.read()
                File.close()
            return data
        except(Exception) as e:
            print(Fore.RED,e,Fore.WHITE)

# this class for make data into dcoument format(PDF)
class clinicDocument(FPDF, clinic) :
    # get the output print in PDF format using this function
    def printDocument(self, name, age, gender, number, customerid, test, fees):
        try:
            self.add_page()
            self.set_font("Arial", "IB", 12)
            self.ln(1)
            self.cell(0,10, f"Name : {name}")
            self.ln(2)
            self.cell(0,20, f"Age : {age}")
            self.ln(3)
            self.cell(0,30, f"Gender : {gender}")
            self.ln(4)
            self.cell(0,40, f"Number : {number}")
            self.ln(5)
            self.cell(0,50, f"ID : {customerid}")
            self.ln(6)
            self.cell(0,60, f"test : {test}")
            self.ln(7)
            self.cell(0,70, f"fees : {fees}")
            self.ln(8)
            self.output(f"{api["path"][6]}{customerid}.pdf")
        except(Exception) as e:
            print(Fore.RED, e, Fore.WHITE)

if __name__=="__main__":
    c = clinic("clinic")
    cd = clinicDocument()
    
    
    