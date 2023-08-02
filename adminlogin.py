import tkinter
from tkinter import *
from tkinter import messagebox
import pymysql

adminlogin_window = Tk()
adminlogin_window.title('Admin Login')
adminlogin_window.geometry("925x500+300+200")
adminlogin_window.config(bg="#ECF9FF")
adminlogin_window.resizable(False, False)

#back forward button
def backfw_btn():
    adminlogin_window.withdraw()
    import main
    main.login_window.deiconify()

bfw_btn = tkinter.PhotoImage(file='backfw.png',master=adminlogin_window)
back_forward_btn = Button(adminlogin_window,cursor='hand2',image=bfw_btn,bd=0,bg="#ECF9FF",activebackground="#ECF9FF",height=80,width=80,command=backfw_btn)
back_forward_btn.place(x=10,y=5)


#logo image
img_logo =tkinter.PhotoImage(file='logo.png',master=adminlogin_window)
Label(adminlogin_window, image=img_logo,bg="white", background="#ECF9FF").place(x=50, y=120)

adminlogin_window.iconphoto(False,img_logo)

frame = Frame(adminlogin_window, width=350, height=370, bg="#ECF9FF")
frame.place(x=480, y=50)

heading = Label(frame, text="Log In", fg="black", bg="#ECF9FF", font=('Microsoft YaHei UI Light ', 25, 'bold'))
heading.place(x=100, y=5)


def on_enter(e):
    admin_username_entry.delete(0, 'end')

def on_leave(e):
    name = admin_username_entry.get()
    if name == '':
        admin_username_entry.insert(0, 'Admin User Name')


admin_username_entry = Entry(frame, width=35, fg='#181823', border=0, bg="#ECF9FF", font=('Microsoft YaHei UI Light ', 15))
admin_username_entry.place(x=30, y=100)
admin_username_entry.insert(0, 'Admin User Name')
admin_username_entry.bind('<FocusIn>', on_enter)
admin_username_entry.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg="black").place(x=25, y=125)


def on_enter(e):
    admin_pass_entry.delete(0, 'end')


def on_leave(e):
    password = admin_pass_entry.get()
    if password == '':
        admin_pass_entry.insert(0, 'Password')


admin_pass_entry = Entry(frame, width=35, fg='#181823', border=0, bg="#ECF9FF", font=('Microsoft YaHei UI Light ', 15))
admin_pass_entry.place(x=30, y=180)
admin_pass_entry.insert(0, 'Password')
admin_pass_entry.bind('<FocusIn>', on_enter)
admin_pass_entry.bind('<FocusOut>', on_leave)
Frame(frame, width=295, height=2, bg="black").place(x=25, y=205)

def hide():
    eye_img.config(file='closedeye.png')
    admin_pass_entry.config(show='*')
    openeye_btn.config(command=show)
def show():
    eye_img.config(file='openeye.png')
    admin_pass_entry.config(show='')
    openeye_btn.config(command=hide)

eye_img = tkinter.PhotoImage(file='openeye.png',master=adminlogin_window)
openeye_btn = Button(frame,bd=0,image=eye_img,activebackground="#ECF9FF",command=hide)
openeye_btn.place(x=280, y=170)



#connect to database
def adminlogin():
   if admin_username_entry.get()=='Admin User Name' or admin_pass_entry.get()=='Password':
       messagebox.showerror('Error', 'all fields are required')
   else:
       con_db = pymysql.connect(host='localhost', user='root', password='123456789')
       mycursor = con_db.cursor()
       query = 'use facerecognation_attendance_System'
       mycursor.execute(query)
       query = 'select * from admin where full_name=%s and pass=%s'
       mycursor.execute(query,(admin_username_entry.get(),admin_pass_entry.get()))
       row = mycursor.fetchone()
       if row == None:
           messagebox.showerror('Error', 'invalid username or password')
       else:
           adminlogin_window.withdraw()
           import dashboard_admin
           dashboard_admin.admin_dashboard_window.deiconify()

btn_login = Button(frame,cursor='hand2',width=25,pady=7,padx=20,text="Login",
                   bg="#57a1f8",fg='white',font=('Microsoft YaHei UI Light ',12,'bold'),border=0, command=adminlogin)
btn_login.place(x=25, y=250)

adminlogin_window.mainloop()