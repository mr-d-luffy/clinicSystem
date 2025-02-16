import json
from tkinter import *
from colorama import Fore
from pygame import mixer
from os import system
from module.clinic import clinic, clinicDocument

api = json.load(open("json/data.json")) # load the json file in project 
backend = clinic("clinic") # backend module in clinic file
documentBackend = clinicDocument() # function for create bill in document format(PDF)

# search data in database using this gui
class DatabaseWindow(Tk):
    # search data by id in this function 
    def databaseCustomerId(self):
        lx1 = Label(self, text="Customer ID : ", fg="white", bg="black")
        lx1.place(x=10,y=20)

        customerId = Entry(self, fg="white", bg="black")
        customerId.place(x=110, y=18)

        def searchData():
            cusid = customerId.get()
            backend.showDataById(cusid)
            exit()

        bx1 = Button(self, text="searchByID", fg="black", bg="white", command=searchData)
        bx1.place(x=170, y=70)

    # search data by number in this function
    def databaseCustomerNumber(self):
        lx2 = Label(self, text="CustomerNumber : ", fg="white", bg="black")
        lx2.place(x=10,y=20)

        customerNumber = Entry(self, fg="white", bg="black")
        customerNumber.place(x=130, y=18)

        def searchData():
            cusNumber = customerNumber.get()
            backend.showDataByNumber(cusNumber)
            exit()

        bx2 = Button(self, text="searchByNumber", fg="black", bg="white", command=searchData)
        bx2.place(x=150, y=70)


# this is for new window 
class customerIDWindow(DatabaseWindow):
    #delete data from database using this function
    def windowDelete(self):
        lx = Label(self, text="Customer ID : ", fg="white", bg="black")
        lx.place(x=10,y=20)

        customerId = Entry(self, fg="white", bg="black")
        customerId.place(x=110, y=18)

        def deleteData():
            cusid = customerId.get()
            print(cusid)
            backend.deleteDataById(cusid)
            exit()

        bx = Button(self, text="Delete", fg="black", bg="white", command=deleteData)
        bx.place(x=170, y=70)

class main(customerIDWindow):
    def __ini__(self):
        self.name = self.customerName.get()
        self.age = self.customerage.get()
        self.cusId = self.backend.createID() 
        self.gender = self.selectMenu.get()
        self.number = self.contactNumber.get()
        self.test = self.customerTest.get()
        self.fees = self.customerFees.get()

    # this function is a create GUI window by using tkinter module 
    def App(self):
        # gui for input a customer name 
        l1 = Label(text="Customer Name : ", fg="white", bg="black")
        l1.place(x=10, y=20)
        customerName = Entry(fg="white", bg="black")
        customerName.place(x=130, y=16)

        # gui for input customer age
        l2 = Label(text="age : ", fg="white", bg="black")
        l2.place(x=335, y=20)
        customerage = Entry(fg="white", bg="black")
        customerage.place(x=390, y=16)

        # gui for input customer gender
        l3 = Label(text="Gender : ", fg="white", bg="black")
        l3.place(x=30, y=60)
        selectMenu = StringVar()
        selectMenu.set("Choose gender")
        dm1 = OptionMenu(self, selectMenu, *api["gender"])
        dm1.place(x=90, y=60)

        # gui for input customer contact number 
        l4 = Label(text="Contact : ", fg="white", bg="black")
        l4.place(x=255, y=60)
        contactNumber = Entry(fg="white", bg="black")
        contactNumber.place(x=330, y=56)

        # gui for input clinical tests
        l5 = Label(text="Test : ", fg="white", bg="black")
        l5.place(x=35, y=110)
        customerTest = Entry(fg="white", bg="black")
        customerTest.place(x=90, y=108)

        # gui for input test fees
        l6 = Label(text="Fees : ", fg="white", bg="black")
        l6.place(x=300, y=110)
        customerFees = Entry(fg="white", bg="black")
        customerFees.place(x=350, y=108)

        # this function for onclick event in windows (for submit a data in sqlite database)
        def update():
            name = customerName.get()
            age = customerage.get()
            cusId = backend.createID() 
            gender = selectMenu.get()
            number = contactNumber.get()
            test = customerTest.get()
            fees = customerFees.get()

            data = {
                "CustomerName":name,
                "Customer age":age,
                "CustomerId":cusId,
                "Gender":gender,
                "ConatactNumber":number,
                "Test":test,
                "Fees":fees   
            }

            print(name, age, cusId, gender, number, test, fees)
            backend.createQrcode(data, cusId) # this is for make qrcode in this path:qrcode/FileName.png
            binaryImage = backend.imageToBinary(cusId) # convert image into binary format
            backend.storeData(name, number, cusId, test, age, gender, fees, binaryImage) #store data in database using this funtion
            backend.readDatabase() #reading the database using this function
            App.destroy()

        # gui for submit data to the database
        bt1 = Button(text="Submit", fg="black", bg="white", command=update)
        bt1.place(x=100, y=200)

        def documentPrint(self):
            documentBackend.printDocument(self.name, self.age, self.gender, self.number, self.cusId, self.test, self.fees)

        # print PDF in document page
        bt2 = Button(text="print", fg="black", bg="white", command=documentPrint)
        bt2.place(x=200, y=200)

        # Create id window onclicking this button Function
        def showDataByID():
            databaseApp = DatabaseWindow()
            databaseApp.databaseCustomerId()
            databaseApp.title(api["company"])
            databaseApp.geometry("400x125")
            databaseApp.configure(bg=api["background"])
            databaseApp.resizable(api["windowSize"][0], api["windowSize"][0])
            databaseApp.mainloop()
            

        # show data from database
        bt3 = Button(text="searchDataById", fg="black", bg="white", command=showDataByID)
        bt3.place(x=300, y=200)

        # Create number window onclicking this button Function
        def showDataByNumber():
            databaseApp = DatabaseWindow()
            databaseApp.databaseCustomerNumber()
            databaseApp.title(api["company"])
            databaseApp.geometry("400x125")
            databaseApp.configure(bg=api["background"])
            databaseApp.resizable(api["windowSize"][0], api["windowSize"][0])
            databaseApp.mainloop()
            

        # show data from database
        bt3 = Button(text="searchDataByNumber", fg="black", bg="white", command=showDataByNumber)
        bt3.place(x=300, y=230)

        # making a new window for delete customer data from database 
        def deleteRecord():
            deleteWindow = customerIDWindow()
            deleteWindow.windowDelete()
            deleteWindow.title(api["company"])
            deleteWindow.geometry("400x125")
            deleteWindow.configure(bg=api["background"])
            deleteWindow.resizable(api["windowSize"][0], api["windowSize"][0])
            deleteWindow = mainloop()

        # delete data button
        bt4 = Button(text="deleteData", fg="black", bg="white", command=deleteRecord)
        bt4.place(x=425, y=200)
        
        closeWindow = lambda : App.destroy()

        # close the window
        bt5 = Button(text="close", fg="black", bg="white", command=closeWindow)
        bt5.place(x=535, y=200)

# this code run on only this file (you can import this module in other file this code can not run)
if __name__== "__main__":
    system("clear") # clean the terminal for better view
    App = main() # creating object for main window
    App.App() # Run App
    App.title(api["company"]) # set title in main window
    App.geometry("650x350") # set size of main window
    App.configure(bg=api["background"]) # background color of main window
    App.resizable(api["windowSize"][1], api["windowSize"][1]) # set window resize True or False 

    # set the application background music using this code
    try:
        mixer.init()
        mixer.music.load(open(api["path"][4]))
        mixer.music.play()
    except(Exception) as e:
        print(Fore.RED,e,Fore.WHITE)

    # set the application icon using this code
    try:
        logo = PhotoImage(file=api["path"][3])
        App.iconphoto(False, logo)
    except(Exception) as e:
        print(Fore.RED,e,Fore.WHITE)
        
    App.mainloop()
