from tkinter import *
import tkinter.messagebox as tmsg
from bs4 import BeautifulSoup
import smtplib
import time
import requests

# A function to get the real price of the product because when we will get the price of the product 
# The price will have some commas and values after dot
# What we don't want so we will remove those

def SendMail():
    GMailid=mail.get()
    
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    password=""
    with open("password.txt","r") as f:
        password=f.read()
    server.login('deadprogrammer1810@gmail.com',password)
    subject="Price fell down!"
    body="Check the link-"
    msg=f"Subject: {subject}\n\n{body}{URL.get()}"
    server.sendmail('deadprogrammer1810@gmail.com',GMailid,msg)
    print("EMAIL HAS BEEN SENT...")    

    server.quit()
    
    
def Check_Price():
    temp=int(expexted_cost.get())
    while(True):
        if(price<=temp):
            SendMail()
            break
        time.sleep(10)

def real_price(price):
    temp=""
    for i in price:
        if i!=0 :
            if i!=",":
                if i==".":
                    break
                temp+=i
    price=int(temp)
    return price

def check_Price():
    global price
    # Getting url
    header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
    url=URL.get()
    page=requests.get(url,headers=header)
    soup=BeautifulSoup(page.content,"html.parser")
    
    # Storing the name and the price of the product
    # title=soup.find(id="productTitle").get_text()
    price=soup.find(id="priceblock_ourprice").get_text()
    tmsg.showinfo("Price!!",f"The Current price of the product is {price}")
    info=tmsg.askquestion("Wanna get a mail??","Want to get notofied when the price falls down??")

    price=real_price(price[1:])
    if info=="yes":
        f1.pack_forget()
        f2=Frame(root)
        f2.pack()
        l3=Label(f2,text="Enter your mail id below!!",font=("lucida",30,"bold"))
        l3.pack()
        
        e2=Entry(f2,textvariable=mail,width=100,font=("lucida",30))
        e2.pack(padx=20,pady=30)

        l4=Label(f2,text="Enter your expexted price!!",font=("lucida",30,"bold"))
        l4.pack()
        
        e3=Entry(f2,textvariable=expexted_cost,width=100,font=("lucida",30))
        e3.pack(padx=20,pady=30)

        b2=Button(f2,text="Submit ",font=("lucida",30,"bold"),command=Check_Price)
        b2.pack(padx=20,pady=30)

# Initialization of Screen

root=Tk()
root.geometry("700x700")
root.configure(bg="gray")

f1=Frame(root,bg="gray")
f1.pack()

# Initializing variables

URL=StringVar()
URL.set("")
mail=StringVar()
mail.set("")
price=""
expexted_cost=StringVar()
expexted_cost.set("")

l1=Label(f1,text="Welcome to an amazing web Scrapper",font=("lucida",30,"bold"),fg="white",bg="yellow")
l1.pack()

l2=Label(f1,text="Enter the link of the product:",font=("lucida",25,"bold"),fg="white",bg="black")
l2.pack(side=LEFT,anchor="nw",pady=30)

e1=Entry(f1,textvariable=URL)
e1.place(x=20,y=150,width=300,height=50)

b1=Button(f1,text="Check price",font=("arial",20,"bold"),command=check_Price)
b1.pack(side=LEFT,pady=300)
