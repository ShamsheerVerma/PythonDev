'''
Created on 8 Oct. 2018

@author: shamsheer
'''

import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import StringVar, Radiobutton, IntVar
import threading

from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics

import numpy as np
import pandas as pd
from datetime import datetime

from time import strftime



import psycopg2 as pg

now = datetime.now()

class UserInterface:
    
    def promotionRadioBttnFalse(self, event):
        
        self.promotion = "false"
        #print("Promotion = ", self.promotion)
        
    def promotionRadioBttnTrue(self, event):
        
        self.promotion = "true"
        #print("Promotion = ", self.promotion)
        
    
    def startTheModelButton(self, event):
        
        self.stopEvent=threading.Event()
        self.thread1 = threading.Thread(target=self.startModel, args = ())
        self.thread1.start()
        
        
        
    
    def shopID(self, shop):
        
        self.shop = shop
        #print("Shop Chosen = ", self.shop)
        
    
    def productID(self, product):
        
        self.product = product
        #print("Product Chosen = ", self.product)
            
    
    def __init__(self, master):
        
        ##-------------------------- Setting up the variables --------------------------##
        
        self.master = master
         
        self.thread1 = None
        self.stopEvent = None
         
        self.shop_dd_options = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.product_dd_options = ["108701", "99197", "103665", "105574", "106716", "114790", "115267", "115850", "116018", "119141" ]
         
        self.variable_shop = StringVar(self.master)
        self.variable_shop.set("Shop ID Drop Down")
         
        self.variable_product = StringVar(self.master)
        self.variable_product.set("Product ID Drop Down")
         
        self.shop_dd = OptionMenu(self.master, self.variable_shop, *self.shop_dd_options, command = self.shopID)
         
        self.product_dd = OptionMenu(self.master, self.variable_product, *self.product_dd_options, command = self.productID)
         
        self.mydate = StringVar(self.master)
        self.date = tk.Entry(self.master, textvariable = self.mydate, width=10)
         
        self.v = IntVar()
        self.onpromotion_false = Radiobutton(self.master, text="Promotion False", variable = self.v, value = 0)
        self.onpromotion_true = Radiobutton(self.master, text="Promotion True", variable = self.v, value = 1)
        
        
        self.output_quantity = Label(self.master, text = "xxxx")
        self.shop_dd_label = Label(self.master, text = "Please Select the Shop ID")
        self.product_dd_label = Label(self.master, text = "Please Select the Product ID")
        self.date_dd_label = Label(self.master, text = "Enter the Date : DD/MM/YYYY")
        self.output_dd_label = Label(self.master, text = "Output Quantity is : ")
        
        self.name1 = Label(self.master, text = "Shamsheer Verma : 12851248")
        self.name2 = Label(self.master, text = "Ankit Kapoor : 12982233")
        self.name3 = Label(self.master, text = "Avinash Pakanati: 12723514")
        
        
        
        self.start = Button(self.master, text = "START THE MODEL", bg='white', fg='black')
         
        ##-------------------------- Positioning the Drop Down, Input Box, RadioButtons, and Output --------------------------## 
         
        self.onpromotion_false.config(height = 1, width = 28)
        self.onpromotion_true.config(height = 1, width = 25)
        self.shop_dd.config(height=1, width = 20)
        self.product_dd.config(height=1, width = 20)
        self.output_quantity.config(height=1, width = 20)
        self.start.config(height=1, width=20)
        self.shop_dd_label.config(height=1, width = 30)
        self.product_dd_label.config(height=1, width = 30)
        self.date_dd_label.config(height=1, width = 30)
        self.output_dd_label.config(height=1, width = 20)
        self.name1.config(height=1, width = 30)
        self.name2.config(height=1, width = 30)
        self.name3.config(height=1, width = 30)
        
        
        self.onpromotion_false.grid(row = 1, column = 0, sticky=W, pady = 2)
        self.onpromotion_true.grid(row = 1, column = 1,  sticky=E, pady = 2)
        self.shop_dd.grid(row = 2, column = 1, sticky = E, pady = 2)
        self.product_dd.grid(row = 3, column = 1, sticky = E, pady = 2)
        self.date.grid(row = 4, column = 1,  sticky = N, pady = 2)
        self.output_quantity.grid(row = 5, column = 1, sticky = N, pady = 2)
        self.shop_dd_label.grid(row = 2, column = 0, sticky = N, pady = 2)
        self.product_dd_label.grid(row = 3, column =0, sticky = N, pady = 2)
        self.date_dd_label.grid(row = 4, column = 0, sticky = N, pady = 2)
        self.output_dd_label.grid(row = 5, column = 0, sticky = N, pady = 2)
        self.start.grid(row = 6, column =0, sticky = N, pady = 2, columnspan = 2)
        self.name1.grid(row = 9, column =0, sticky = S, pady = 2)
        self.name2.grid(row = 10, column =0, sticky = S, pady = 2)
        self.name3.grid(row = 11, column =0, sticky = S, pady = 2)
        self.name1.place(x=1, y=240)
        self.name2.place(x=1, y=260)
        self.name3.place(x=1, y=280)
        
        self.uts_photo = PhotoImage(file="uts_logo_new.png")
        self.uts_logo = Label(self.master, image = self.uts_photo)
        self.uts_logo.image = self.uts_photo
        self.uts_logo.grid(row = 8, column = 0, sticky = N, pady = 2, columnspan = 2)
        self.uts_logo.place(x=270, y=240)
        
        self.start.bind("<Button-1>", self.startTheModelButton)
        self.onpromotion_false.bind("<Button-1>", self.promotionRadioBttnFalse)
        self.onpromotion_true.bind("<Button-1>", self.promotionRadioBttnTrue)
        
    
    ##-----------------------------Starting the Model - Machine Learning Algorithms - Over Here----------------------------##
        
    def sqlConnection(self):
        
        self.conn = pg.connect(host='localhost', user = "",                    password="", database = "BIDS_Assignment_5")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM corporacion WHERE item_nbr = " + self.product)
        
        self.colnames = [desc[0] for desc in self.cur.description]
        self.rows = self.cur.fetchall()
        
        self.subset = pd.DataFrame(self.rows)
        
        self.conn.close()
        
        self.subset.columns = self.colnames
        print(self.subset)
        print("done")
        
        self.subset.replace(to_replace="false", value=0, regex=True)
        self.subset.replace(to_replace="true", value=1, regex=True)
        
        self.subset.dropna(inplace=True,axis=0,how='any')
        
        self.current_year=now.year
        self.current_month=now.month
        self.current_day=now.day
        
        self.subset['date'] = pd.to_datetime(self.subset['date'], format = '%Y-%m-%d')   #transforming date Column
        self.subset_year = self.subset['date'].dt.year
        self.subset_month = self.subset['date'].dt.month
        self.subset_day = self.subset['date'].dt.day
        self.subset['Duration'] = ((self.current_year * 365) + (self.current_month * 30) + self.current_day) - ((self.subset_year*365) + (self.subset_month*30) + self.subset_day)
        self.subset.drop('date',axis=1,inplace=True)
        self.randomForests()

    
    def randomForests(self):
        
        self.X_train,self.X_test,self.y_train,self.y_test=train_test_split(self.subset.drop(['id','unit_sales'],axis=1),self.subset['unit_sales'],test_size=0.3)
        
        self.lm = RandomForestRegressor(n_estimators=20)
        self.lm.fit(self.X_train, self.y_train)
        
        
        if self.promotion == 'true':
            self.promotiontf=1
        else:
            self.promotiontf=0
        
        #self.date = str(self.date)
        #print(datetime.now().date())
        #print(self.date)
        
        
        #print(self.date_input)
        self.rdate1 = datetime.strptime(self.date_input, "%Y%m%d").date()
        
        #print(self.rdate1)
        #self.rdate1 = strftime("%Y-%m-%d %H:%M:%S", str(self.date))
        self.duration = (datetime.now().date() - self.rdate1).days
        print(self.duration)
        self.mylist = {"date": self.duration, "store_nbr" : self.shop, "item_nbr" : self.product, "onpromotion" : self.promotiontf}
        print(self.mylist)
        self.output_df = pd.DataFrame(self.mylist, index=[0])
        self.lm_predict = self.lm.predict(self.output_df)
        np.round(self.lm_predict,0)
        self.output_quantity['text'] = self.lm_predict
        
    
    def startModel(self):
        
        self.date_input = str(eval(self.date.get()))
        
        print("clicking the button")
        print("Shop Number", self.shop)
        print("Product Number", self.product)
        print("Promotion True or False", self.promotion)
        print("Date", self.date_input)
        self.sqlConnection()
    
    
        
        

root = tk.Tk()
root.title("Corporacion Favorita : Sales Forecasting Tool")
root.geometry("500x300")
root.geometry("+0+100")
root.configure(bg="light grey")
root.resizable(width=False, height=False)
b = UserInterface(root)
root.mainloop()
        
         
           
    
    

    
