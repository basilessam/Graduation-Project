import tkinter
from tkinter import *
import pymysql

doctor_window = Tk()
doctor_window.title('Dashboard')
doctor_window.geometry("925x500+300+200")
doctor_window.config(bg="#ECF9FF")
doctor_window.resizable(False,False)
img_logo = tkinter.PhotoImage(file='logo.png', master=doctor_window)
doctor_window.iconphoto(False, img_logo)

con_db = pymysql.connect(host='localhost', user='root', password='123456789')
mycursor = con_db.cursor()
query = 'use facerecognation_attendance_System'
mycursor.execute(query)

#back forward button
def backfw_btn():
    query = "delete from currentlogin"
    mycursor.execute(query)
    con_db.commit()
    doctor_window.withdraw()
    import main
    main.login_window.deiconify()


bfw_btn = tkinter.PhotoImage(file='logout.png',master=doctor_window)
back_forward_btn = Button(doctor_window,cursor='hand2',image=bfw_btn,bd=0,bg="#ECF9FF",activebackground="#ECF9FF",height=80,width=80,command=backfw_btn)
back_forward_btn.place(x=10,y=5)

doctor_window.mainloop()


