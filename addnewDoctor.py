import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql

#connect to database
con_db = pymysql.connect(host='localhost', user='root', password='123456789')
mycursor = con_db.cursor()
query = 'use facerecognation_attendance_System'
mycursor.execute(query)


new_doctor_window = Tk()
new_doctor_window.title("Add Lecturer")
new_doctor_window.geometry("1450x720+40+40")
new_doctor_window.config(bg="#ECF9FF")
new_doctor_window.resizable(False,False)
img_logo = tkinter.PhotoImage(file='logo.png',master=new_doctor_window)
new_doctor_window.iconphoto(False,img_logo)


lect_list_frame = LabelFrame(new_doctor_window,text="Lecturer List")

search_frame = LabelFrame(new_doctor_window,text="Search")

lect_data_frame = LabelFrame(new_doctor_window,text="Lecturer Data")

lect_list_frame.pack(fill="both",expand="yes",padx=20,pady=10)
search_frame.pack(fill="both",expand="yes",padx=20,pady=10)
lect_data_frame.pack(fill="both",expand="yes" ,padx=20,pady=10)

def backfw_btn():
    new_doctor_window.withdraw()
    import dashboard_admin
    dashboard_admin.admin_dashboard_window.deiconify()

bfw_btn = tkinter.PhotoImage(file='backfw.png',master=new_doctor_window)
back_forward_btn = Button(lect_list_frame,cursor='hand2',image=bfw_btn,bd=0,
                          bg="#ECF9FF",activebackground="#ECF9FF",height=60,width=60,command=backfw_btn)
back_forward_btn.place(x=10,y=5)



#styling the head of table
s = ttk.Style(new_doctor_window)
s.theme_use('clam')
s.configure('Treeview.Heading', background="green3")

trv = ttk.Treeview(lect_list_frame, columns=(1,2,3,4,5),show="headings",height="7")
trv.place(x=150,y=2)
yscrollbar = ttk.Scrollbar(lect_list_frame,orient="vertical",command=trv.yview)
yscrollbar.pack(side=RIGHT,fill='y')

trv.column(1, anchor=CENTER)
trv.heading(1, text="lecturer_id")

trv.column(2, anchor=CENTER)
trv.heading(2, text="full_name")

trv.column(3, anchor=CENTER)
trv.heading(3, text="email")

trv.column(4, anchor=CENTER)
trv.heading(4, text="pass")

trv.column(5, anchor=CENTER)
trv.heading(5, text="dep_name")

#show the table of the lecturer
show_table_lect_query="select * from lecturer"
def showdata(row):
    trv.delete(*trv.get_children())
    for i in row:
        trv.insert('','end',values=i)
try:
    mycursor.execute(show_table_lect_query)
    row = mycursor.fetchall()#returns all the rows as a list of tuples.
    showdata(row)
except Exception as err:
    messagebox.showwarning('Error', 'DB exception: %s' % err)

#reset btn
def reset():
    try:
        mycursor.execute(show_table_lect_query)
        row = mycursor.fetchall()
        showdata(row)
    except Exception as err:
        messagebox.showwarning('Error', 'DB exception: %s' % err)

#search section
#get data
txtvar_of_lecid = StringVar(master=new_doctor_window)
txtvar_of_full_name = StringVar(master=new_doctor_window)
txtvar_of_lectemail = StringVar(master=new_doctor_window)
txtvar_of_password = StringVar(master=new_doctor_window)
txtvar_of_department = StringVar(master=new_doctor_window)

#search for record
def search():
    q = search_entry.get()
    if q =='':
        messagebox.showerror('Error','Enter name to search')
    else:
        try:
            search_query = "select * from lecturer where full_name like '%"+q+"%' or email like '%"+q+"%' or lecturer_id like '%"+q+"%' "
            mycursor.execute(search_query)
            row = mycursor.fetchall()
            showdata(row)
        except Exception as err:
            messagebox.showwarning('Error', 'DB exception: %s' % err)

search_labl = Label(search_frame,text="Search",font=('Microsoft YaHei UI Light ',10,'bold'))
search_labl.pack(side=tkinter.LEFT,padx=10)
search_entry = Entry(search_frame,width=25,fg='#181823',border=1,bg="#ECF9FF",
                     font=('Microsoft YaHei UI Light ',15))
search_entry.pack(side=tkinter.LEFT, padx=20)

serch_btn = Button(search_frame,text="Search",activebackground="#ECF9FF",bd=0,cursor="hand2",
                   width=10,pady=5,background="#57a1f8",fg="white",
                   font=('Microsoft YaHei UI Light ',10,'bold'),command=search)
serch_btn.pack(side=tkinter.LEFT , padx=6)

reset_btn = Button(search_frame,text="Reset",activebackground="#ECF9FF",bd=0,cursor="hand2",
                   width=10,pady=5,background="#57a1f8",fg="white",
                   font=('Microsoft YaHei UI Light ',10,'bold'),command=reset)
reset_btn.pack(side=tkinter.LEFT,padx=6)

#Lecturer data section
def getrow(event):
    row_data = trv.identify_row(event.y)
    data = trv.item(trv.focus())
    txtvar_of_lecid.set(data['values'][0])
    txtvar_of_full_name.set(data['values'][1])
    txtvar_of_lectemail.set(data['values'][2])
    txtvar_of_password.set(data['values'][3])
    txtvar_of_department.set(data['values'][4])

trv.bind("<Double-1>", getrow)

#start Lecturer ID
course_id_label = Label(lect_data_frame, text="Lecturer ID",font=('Microsoft YaHei UI Light ',10,'bold'))
course_id_label.grid(row=0,column=0,padx=5,pady=3)

course_id_entry = Entry(lect_data_frame,state='disabled',width=25,fg='#181823',border=1,bg="#ECF9FF",
                        font=('Microsoft YaHei UI Light ',11),textvariable=txtvar_of_lecid)
course_id_entry.grid(row=0,column=1,padx=5,pady=3)
#end Lecturer ID

#start Full Name
lec_fullname_label = Label(lect_data_frame, text="Full Name",
                        font=('Microsoft YaHei UI Light ',10,'bold'))
lec_fullname_label.grid(row=1,column=0,padx=5,pady=3)
lec_fullname_entry = Entry(lect_data_frame,width=25,fg='#181823',border=1,bg="#ECF9FF",
                        font=('Microsoft YaHei UI Light ',11),textvariable=txtvar_of_full_name)
lec_fullname_entry.grid(row=1,column=1,padx=5,pady=3)
#end Full Name

#start Email
lec_email_label = Label(lect_data_frame, text="Email",
                        font=('Microsoft YaHei UI Light ',10,'bold'))
lec_email_label.grid(row=2,column=0,padx=5,pady=3)
lec_email_entry = Entry(lect_data_frame,width=25,fg='#181823',border=1,bg="#ECF9FF",
                        font=('Microsoft YaHei UI Light ',11),textvariable=txtvar_of_lectemail)
lec_email_entry.grid(row=2,column=1,padx=5,pady=3)
#end Email

#start Password
password_label = Label(lect_data_frame, text="Password",
                         font=('Microsoft YaHei UI Light ',10,'bold'))
password_label.grid(row=3,column=0,padx=5,pady=3)
dpassword_entry = Entry(lect_data_frame,width=25,fg='#181823',border=1,bg="#ECF9FF",
                         font=('Microsoft YaHei UI Light ',11),textvariable=txtvar_of_password)
dpassword_entry.grid(row=3,column=1,padx=5,pady=3)
#end Password

#start department
dept_combobox = ttk.Combobox(lect_data_frame, width=15, textvariable=txtvar_of_department)

password_label = Label(lect_data_frame, text="Department",
                         font=('Microsoft YaHei UI Light ',10,'bold'))
password_label.grid(row=0,column=2,padx=5,pady=3)

dept_combobox['values'] = (' علوم حاسب',
                          ' نظم ومعلومات',
                          ' اداره اعمال',
                          )

dept_combobox.grid(row=0,column=3,padx=5,pady=3)
#end department
def clear():
    txtvar_of_lecid.set('')
    lec_fullname_entry.delete(0,END)
    lec_email_entry.delete(0,END)
    dpassword_entry.delete(0,END)
    txtvar_of_department.set('')
    search_entry.delete(0, END)


def update():
    try:
        email ="@gmail.com"
        if txtvar_of_lectemail.get() == '' or txtvar_of_lecid.get() == '' or txtvar_of_full_name.get() == '' \
                or txtvar_of_password.get() == '' or txtvar_of_department.get() == '':
            messagebox.showerror('Eror', 'All fields are required')
        elif email not in txtvar_of_lectemail.get() or txtvar_of_lectemail.get()[:1] == '@' \
                or txtvar_of_lectemail.get()==email:
            messagebox.showerror("Error", "Email must be like: example@gmail.com")
        else:
            t1 = txtvar_of_full_name.get()
            t2 = txtvar_of_lectemail.get()
            t3 = txtvar_of_password.get()
            t4 = txtvar_of_department.get()
            t5 = txtvar_of_lecid.get()
            if messagebox.askyesno("Confirm", "Are you sure want to update"):
                update_email_query = "update lecturer set full_name=%s , email=%s , pass=%s , dep_name=%s where lecturer_id =%s"
                mycursor.execute(update_email_query, (t1,t2,t3,t4,t5))
                con_db.commit()
                reset()
                clear()
                messagebox.showinfo('Done', 'Updated Successfully')
            else:
                return True
    except Exception as err:
        messagebox.showwarning('Error','DB exception: %s' % err)


def delete():
    try:
        if txtvar_of_lecid.get() == '' or txtvar_of_lectemail.get() == '' or txtvar_of_lecid.get() == '' or txtvar_of_full_name.get() == '' or txtvar_of_password.get() == '' or txtvar_of_department.get() == '':
            messagebox.showerror('Eror', 'All fields are required')
        elif messagebox.askyesno("Confirm", "Are you sure want to delete this record"):
            delete_lec_query = "delete from lecturer where lecturer_id = %s"
            mycursor.execute(delete_lec_query, (txtvar_of_lecid.get()))
            con_db.commit()
            reset()
            clear()
            messagebox.showinfo('Done', 'Record is deleted')
        else:
            return True
    except Exception as err:
        messagebox.showwarning('Error','DB exception: %s' % err)



def insert():
    try:
        query = 'select * from lecturer where lecturer_id=%s '
        mycursor.execute(query, (txtvar_of_lecid.get()))
        row_lec_id = mycursor.fetchone()
        query = 'select * from lecturer where email=%s '
        mycursor.execute(query, (txtvar_of_lectemail.get()))
        row_lec_email = mycursor.fetchone()
        email ="@gmail.com"
        if txtvar_of_lectemail.get() == '' or txtvar_of_full_name.get() == '' \
                or txtvar_of_password.get() == '' or txtvar_of_department.get() == '':
            messagebox.showerror('Eror', 'All fields are required')
        elif email not in txtvar_of_lectemail.get() or txtvar_of_lectemail.get()[:1] == '@':
            messagebox.showerror("Error","Email must be like: example@gmail.com")
        elif row_lec_id is not None or row_lec_email is not None:
            messagebox.showerror("Error", 'This record is already exist')
        else:
            insert_lec_query = "insert into lecturer(full_name,email,pass,dep_name) values(%s,%s,%s,%s)"
            mycursor.execute(insert_lec_query, (
                txtvar_of_full_name.get(), txtvar_of_lectemail.get(), txtvar_of_password.get(),
                txtvar_of_department.get()))
            messagebox.showinfo('Done', 'Record is inserted')
            con_db.commit()
            reset()
            clear()
    except Exception as err:
        messagebox.showwarning('Error','DB exception: %s' % err)

#start update button
update_btn = Button(lect_data_frame,width=20,text="Update",cursor='hand2',fg='white',
                    background="#57a1f8",bd=0,activebackground="#ECF9FF",
                   font=('Microsoft YaHei UI Light ',11,'bold'),command=update)
update_btn.place(x=310,y=150)
#end update button

#start delete button
delete_btn = Button(lect_data_frame,width=20,text="Delete",cursor='hand2',fg='white',
                    background="#57a1f8",bd=0,activebackground="#ECF9FF",
                   font=('Microsoft YaHei UI Light ',11,'bold'),command=delete)
delete_btn.place(x=510,y=150)
#end update button

#start insert button
insert_btn = Button(lect_data_frame,width=20,text="Insert",cursor='hand2',fg='white',
                    background="#57a1f8",bd=0,activebackground="#ECF9FF",
                   font=('Microsoft YaHei UI Light ',11,'bold'),command=insert)
insert_btn.place(x=710,y=150)
#end insert button

#start clear button
clear_btn = Button(lect_data_frame,width=20,text="Clear Fields",cursor='hand2',fg='white',
                    background="#57a1f8",bd=0,activebackground="#ECF9FF",
                   font=('Microsoft YaHei UI Light ',11,'bold'),command=clear)
clear_btn.place(x=910,y=150)
#end clear button

new_doctor_window.mainloop()

