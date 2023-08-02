import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql

con_db = pymysql.connect(host='localhost', user='root', password='123456789')
mycursor = con_db.cursor()
query = 'use facerecognation_attendance_System'
mycursor.execute(query)

modify_window = Tk()
modify_window.title("Modify Data")
modify_window.geometry("1450x720+40+40")
modify_window.config(bg="#ECF9FF")
modify_window.resizable(False,False)
img_logo =tkinter.PhotoImage(file='logo.png',master=modify_window)
modify_window.iconphoto(False,img_logo)


course_list_frame = LabelFrame(modify_window,text="Course List")
search_frame = LabelFrame(modify_window,text="Search")
course_data_frame = LabelFrame(modify_window,text="Course Data")

course_list_frame.pack(fill="both",expand="yes",padx=20,pady=10)
search_frame.pack(fill="both",expand="yes",padx=20,pady=10)
course_data_frame.pack(fill="both",expand="yes",padx=20,pady=10)

def backfw_btn():
    modify_window.withdraw()
    import dashboard_admin
    dashboard_admin.admin_dashboard_window.deiconify()

bfw_btn = tkinter.PhotoImage(file='backfw.png',master=modify_window)
back_forward_btn = Button(course_list_frame,cursor='hand2',image=bfw_btn,bd=0,bg="#ECF9FF",activebackground="#ECF9FF",height=60,width=60,command=backfw_btn)
back_forward_btn.place(x=10,y=5)



def showdata(row):
    trv.delete(*trv.get_children())
    for i in row:
        trv.insert('','end',values=i)

#styling the head of table
s = ttk.Style(modify_window)
s.theme_use('clam')
s.configure('Treeview.Heading', background="green3")

trv = ttk.Treeview(course_list_frame, columns=(1,2,3,4,5,6),show="headings",height="7")
trv.pack()

trv.column(1, anchor=CENTER)
trv.heading(1, text="course_id")

trv.column(2, anchor=CENTER)
trv.heading(2, text="course_name")

trv.column(3, anchor=CENTER)
trv.heading(3, text="lecturer_email")

trv.column(4, anchor=CENTER)
trv.heading(4, text="dept_name of course")

trv.column(5, anchor=CENTER)
trv.heading(5, text="full_name")

trv.column(6, anchor=CENTER)
trv.heading(6, text="email")



#show the table course related to table  of the lecturer
try:
    query = 'select distinct co.course_id , co.course_name, co.lecturer_email ,co.dept_name , lec.full_name , lec.email from course co left outer join lecturer lec on lec.email = co.lecturer_email'
    mycursor.execute(query)
    row = mycursor.fetchall()
    showdata(row)
    con_db.commit()
except Exception as err:
    messagebox.showwarning('Error', 'DB exception: %s' % err)

#reset btn
def reset():
    try:
        query = 'select distinct co.course_id , co.course_name, co.lecturer_email ,co.dept_name , lec.full_name , lec.email from course co left outer join lecturer lec on lec.email = co.lecturer_email'
        mycursor.execute(query)
        row = mycursor.fetchall()
        showdata(row)
        con_db.commit()
    except Exception as err:
        messagebox.showwarning('Error', 'DB exception: %s' % err)

#search for record
#txtvar_of_search = StringVar()
def search():
    q = search_entry.get()
    if q =='':
        messagebox.showerror('Error','Enter Email to search')
    else:
        try:
            qeury = "select distinct co.course_id , co.course_name, co.lecturer_email ,co.dept_name , lec.full_name , lec.email from course co join lecturer lec on lec.email = co.lecturer_email and co.lecturer_email like '%" + q + "%' "
            mycursor.execute(qeury)
            row = mycursor.fetchall()
            showdata(row)
        except Exception as err:
            messagebox.showwarning('Error', 'DB exception: %s' % err)


#get data
def getrow(event):
    row_data = trv.identify_row(event.y)
    data = trv.item(trv.focus())
    txtvar_of_coursename.set(data['values'][1])
    txtvar_of_lectemail.set(data['values'][2])
    txtvar_of_department.set(data['values'][3])

trv.bind("<Double-1>", getrow)

#search section
search_labl = Label(search_frame,text="Search by email",font=('Microsoft YaHei UI Light ',10,'bold'))
search_labl.pack(side=tkinter.LEFT,padx=10)
search_entry = Entry(search_frame,
                     width=25,fg='#181823',border=1,bg="#ECF9FF",font=('Microsoft YaHei UI Light ',15))
search_entry.pack(side=tkinter.LEFT, padx=20)

serch_btn = Button(search_frame,text="Search",activebackground="#ECF9FF",bd=0,cursor="hand2",
                   width=10,pady=5,background="#57a1f8",fg="white",font=('Microsoft YaHei UI Light ',10,'bold'),command=search)
serch_btn.pack(side=tkinter.LEFT , padx=6)

reset_btn = Button(search_frame,text="Reset",activebackground="#ECF9FF",bd=0,cursor="hand2",
                   width=10,pady=5,background="#57a1f8",fg="white",font=('Microsoft YaHei UI Light ',10,'bold'),command=reset)
reset_btn.pack(side=tkinter.LEFT,padx=6)

#Course data section to update
txtvar_of_coursename = StringVar(master=modify_window)
txtvar_of_lectemail = StringVar(master=modify_window)
txtvar_of_department = StringVar(master=modify_window)

course_name_label = Label(course_data_frame, text="Course Name",font=('Microsoft YaHei UI Light ',10,'bold'))
course_name_label.grid(row=0,column=0,padx=5,pady=3)
course_name_entry = Entry(course_data_frame,state='disabled',width=25,fg='#181823',border=1,bg="#ECF9FF",
                        font=('Microsoft YaHei UI Light ',11),textvariable=txtvar_of_coursename)
course_name_entry.grid(row=0,column=1,padx=5,pady=3)

lec_email_label = Label(course_data_frame, text="The email Of the Doctor To Be Changed",
                        font=('Microsoft YaHei UI Light ',10,'bold'))
lec_email_label.grid(row=1,column=0,padx=5,pady=3)
lec_email_entry = Entry(course_data_frame,width=25,fg='#181823',border=1,bg="#ECF9FF",
                        font=('Microsoft YaHei UI Light ',11),textvariable=txtvar_of_lectemail)
lec_email_entry.grid(row=1,column=1,padx=5,pady=3)

department_label = Label(course_data_frame, text="Department related to course",
                         font=('Microsoft YaHei UI Light ',10,'bold'))
department_label.grid(row=2,column=0,padx=5,pady=3)
department_entry = Entry(course_data_frame,state='disabled',width=25,fg='#181823',border=1,bg="#ECF9FF",
                         font=('Microsoft YaHei UI Light ',11),textvariable=txtvar_of_department)
department_entry.grid(row=2,column=1,padx=5,pady=3)


def update():
    try:
        query = 'select * from lecturer where email=%s '
        mycursor.execute(query, (txtvar_of_lectemail.get()))
        row_email = mycursor.fetchone()

        query = 'select * from course where course_name=%s '
        mycursor.execute(query, (txtvar_of_coursename.get()))
        row_course_name = mycursor.fetchone()

        if txtvar_of_lectemail.get() == '' or txtvar_of_coursename.get() == '' or txtvar_of_coursename.get()=='':
            messagebox.showerror('Eror', 'Email and Course name is needed')
        elif row_email is None:
            messagebox.showerror('Error', 'This Email did not create yet')
        elif row_course_name is None:
            messagebox.showerror('Error', 'This Course Does not Exist')
        else:
            lec_email = txtvar_of_lectemail.get()
            course_name = txtvar_of_coursename.get()
            if messagebox.askyesno("Confirm","Are you sure want to update this course"):
                update_email_query = 'update course set lecturer_email =%s where course_name =%s'
                mycursor.execute(update_email_query,(lec_email,course_name))
                con_db.commit()
                reset()
                messagebox.showinfo('Done', 'Updated Successfully')
            else:
                return True
    except Exception as err:
        messagebox.showwarning('Error','DB exception: %s' % err)

update_btn = Button(course_data_frame,width=80,text="Update",cursor='hand2',fg='white',background="#57a1f8",bd=0,activebackground="#ECF9FF",
                   font=('Microsoft YaHei UI Light ',11,'bold'),command=update)
update_btn.place(x=310,y=150)


modify_window.mainloop()