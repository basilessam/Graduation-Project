import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox , filedialog
import pymysql
import csv
import os
import datetime

current_date = datetime.datetime.today()
current_time = datetime.datetime.strftime(current_date,'%I:%M:%p')

con_db = pymysql.connect(host='localhost', user='root', password='123456789')
mycursor = con_db.cursor()
query = 'use facerecognation_attendance_System'
mycursor.execute(query)

doc_attend_sheet_window = Tk()
doc_attend_sheet_window.title("Attendance Sheet")
doc_attend_sheet_window.geometry("1450x720+40+40")
doc_attend_sheet_window.config(bg="#ECF9FF")
doc_attend_sheet_window.resizable(False,False)
img_logo =tkinter.PhotoImage(file='logo.png',master=doc_attend_sheet_window)
doc_attend_sheet_window.iconphoto(False,img_logo)


atten_list_frame = LabelFrame(doc_attend_sheet_window,text="Attendance List")
add_frame = LabelFrame(doc_attend_sheet_window,text="Add Student")

atten_list_frame.pack(fill="both",expand="yes",padx=20,pady=10)
add_frame.pack(fill="both",expand="yes",padx=20,pady=10)


def backfw_btn():
    doc_attend_sheet_window.withdraw()
    import attendence_dashboard
    attendence_dashboard.attendance_window.deiconify()

bfw_btn = tkinter.PhotoImage(file='backfw.png',master=doc_attend_sheet_window)
back_forward_btn = Button(atten_list_frame,cursor='hand2',image=bfw_btn,bd=0,
                          bg="#ECF9FF",activebackground="#ECF9FF",height=60,width=60,command=backfw_btn)
back_forward_btn.place(x=10,y=5)

mydata = []
def showdata(row):
    global mydata
    mydata = list(row)
    trv.delete(*trv.get_children())
    for i in row:
        trv.insert('','end',values=i)

trv = ttk.Treeview(atten_list_frame, columns=(1,2,3,4,5,6,7),show="headings",height="10")
trv.place(x=5,y=80)
yscrollbar = ttk.Scrollbar(atten_list_frame,orient="vertical",command=trv.yview)
yscrollbar.pack(side=RIGHT,fill='y')
#styling the head of table
s = ttk.Style(trv)
s.theme_use('clam')
s.configure('Treeview.Heading', background="green3")

trv.column(1, anchor=CENTER)
trv.heading(1, text="student name")
trv.column(2, anchor=CENTER)
trv.heading(2, text="time")
trv.column(3, anchor=CENTER)
trv.heading(3, text="attend_course_name")
trv.column(4, anchor=CENTER)
trv.heading(4, text="attendance date")
trv.column(5, anchor=CENTER)
trv.heading(5, text="student_id")
trv.column(6, anchor=CENTER)
trv.heading(6, text="acadymic_year")
trv.column(7, anchor=CENTER)
trv.heading(7, text="semester")

txtvar_of_stud_id= StringVar(master=doc_attend_sheet_window)
txtvar_of_date = StringVar(master=doc_attend_sheet_window)
txtvar_of_attend_course_name = StringVar(master=doc_attend_sheet_window)

#show the table of attendance
def reset_ac_course():
    try:
        sheet_query = " select distinct stu.fullname,shee.date_time,shee.attend_course_name,DATE(shee.arrivaldate),stu.student_id , stu.acadymic_year, stu.semester from attendance_sheet shee  join student stu on  stu.fullname like concat('%%',left(shee.stud_name,20),'%%') and attend_course_name =%s and date(shee.arrivaldate) =%s or shee.stud_id = stu.student_id and date(shee.arrivaldate) =%s and attend_course_name =%s order by semester asc"
        mycursor.execute(sheet_query,(txtvar_of_attend_course_name.get(),current_date.date(),current_date.date(),txtvar_of_attend_course_name.get()))
        row = mycursor.fetchall()
        showdata(row)
        no_attnd_labl.config(text="")
    except Exception as err:
        messagebox.showwarning('Error', 'DB exception: %s' % err)
#export and import section

def exportfile():
    crnttime = datetime.datetime.strftime(current_date,'%I-%M-%p')
    if len(mydata) < 1:
        messagebox.showerror('Error', 'There is now data to export')
        return False
    else:
        file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV",initialfile=txtvar_of_attend_course_name.get()+"-"+str(current_date.date())+"-"+str(crnttime)+'.csv',
                                            filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")))
        with open(file, mode='w', encoding="utf-8") as myfile:
            file_writer = csv.writer(myfile, delimiter=",")
            for i in mydata:
                file_writer.writerow(i)
        messagebox.showinfo('Data Exported','Your data has been exported ' + os.path.basename(file) + ' succesfully.')


#add student data section

#get data
def getrow(event):
    row_data = trv.identify_row(event.y)
    data = trv.item(trv.focus())
    txtvar_of_stud_id.set(data['values'][4])
    txtvar_of_attend_course_name.set(data['values'][2])
    txtvar_of_date.set(data['values'][3])


trv.bind("<Double-1>", getrow)

student_id_label = Label(add_frame, text="Student ID",font=('Microsoft YaHei UI Light ',15,'bold'))
student_id_label.grid(row=0,column=0,padx=5,pady=3)

student_id_entry = Entry(add_frame,width=70,fg='red',border=1,bg="#ECF9FF",
                        font=('Microsoft YaHei UI Light ',15),textvariable=txtvar_of_stud_id)
student_id_entry.grid(row=0,column=1,padx=5,pady=3)


coursename_combobox = ttk.Combobox(add_frame, width=15,textvariable=txtvar_of_attend_course_name)

coursename_label = Label(add_frame, text="Course Name",
                         font=('Microsoft YaHei UI Light ',15,'bold'))
coursename_label.grid(row=0,column=2,padx=5,pady=3)
# Adding combobox drop down list


coursename_combobox.grid(row=0,column=3,padx=5,pady=3)


def clear():
    txtvar_of_stud_id.set('')
    txtvar_of_attend_course_name.set('')
    no_attnd_labl.config(text='')

no_attnd_labl = Label(atten_list_frame, text="", fg="red", width=25, bg="#ECF9FF",
                         font=('Microsoft YaHei UI Light ', 30))
no_attnd_labl.place(x=100, y=10)
def get_no_of_attend():
    global current_date
    try:
        query = "select count(*) from attendance_sheet where date(arrivaldate) =%s and attend_course_name=%s"
        mycursor.execute(query, (current_date.date(), txtvar_of_attend_course_name.get()))
        row_no_ofatt = mycursor.fetchone()[0]
        no_of_attnd = "number of attendees: "
        no_attnd_labl.config(text=no_of_attnd+str(row_no_ofatt))
        #reset_ac_course()
    except Exception as err:
        messagebox.showerror("Error","%s"%err)


def show_sheet():
    try:
        query = "select * from course where course_name=%s"
        mycursor.execute(query, (txtvar_of_attend_course_name.get()))
        row = mycursor.fetchall()
        if txtvar_of_attend_course_name.get() == '':
            messagebox.showerror("Error", "Please select course name")
        elif row is None:
            messagebox.showerror("Error", "This course does not exist")
        else:
            show_attendance_sheet_query = " select distinct stu.fullname,shee.date_time,shee.attend_course_name,DATE(shee.arrivaldate),stu.student_id , stu.acadymic_year, stu.semester from attendance_sheet shee  join student stu on  stu.fullname like concat('%%',left(shee.stud_name,20),'%%') and attend_course_name =%s and date(shee.arrivaldate) =%s or shee.stud_id = stu.student_id and date(shee.arrivaldate) =%s and attend_course_name =%s order by semester asc"
            mycursor.execute(show_attendance_sheet_query, (txtvar_of_attend_course_name.get(),current_date.date(),current_date.date(), txtvar_of_attend_course_name.get()))
            row = mycursor.fetchall()
            showdata(row)
            #no_attnd_labl.config(text="")
            get_no_of_attend()
    except Exception as err:
        messagebox.showwarning('Error', 'DB exception: %s' % err)

def add_student_manually():
    query = "select * from course where course_name=%s"
    mycursor.execute(query, (txtvar_of_attend_course_name.get()))
    row_course = mycursor.fetchone()
    q = txtvar_of_stud_id.get()
    qdate = str(current_date.date())

    query = "select * from attendance_sheet where stud_name like concat('%%',(select fullname from student where student_id =%s),'%%')and DATE(arrivaldate) =%s and attend_course_name =%s or stud_id = (select student_id from student where student_id = %s) and DATE(arrivaldate) =%s and attend_course_name =%s "
    mycursor.execute(query,(txtvar_of_stud_id.get(),qdate,txtvar_of_attend_course_name.get(),txtvar_of_stud_id.get(),qdate,txtvar_of_attend_course_name.get()))
    row_stdid = mycursor.fetchone()

    query = "select * from student where student_id = %s"
    mycursor.execute(query,(txtvar_of_stud_id.get()))
    row_stud_table = mycursor.fetchone()
    if txtvar_of_attend_course_name.get() == '' or txtvar_of_stud_id.get() == '':
        messagebox.showerror("Error", "All fields are required")
    elif len(txtvar_of_stud_id.get())< 9 or len(txtvar_of_stud_id.get()) > 9:
        messagebox.showerror('Invalid ID', "Invalid Student ID")
    elif row_course is None:
        messagebox.showerror("Error", "This course does not exist")
    elif row_stud_table is None:
        messagebox.showerror("Error", "This student does not in the system yet!! or entered id is incorrect")
    elif row_stdid is not None:
        messagebox.showerror("Error", "This attendee has already taken")
    else:
        query = "insert into attendance_sheet(stud_id,date_time,attend_course_name,arrivaldate)values(%s,%s,%s,now())"
        mycursor.execute(query, (
            txtvar_of_stud_id.get(), current_time, txtvar_of_attend_course_name.get()))
        messagebox.showinfo("Done", "Student added successfully")
        reset_ac_course()
        get_no_of_attend()
        con_db.commit()


add_btn = Button(add_frame,width=45,text="Add",cursor='hand2',fg='white',background="#57a1f8",bd=0,activebackground="#ECF9FF",
                   font=('Microsoft YaHei UI Light ',12,'bold'),command=add_student_manually)
add_btn.place(x=220,y=150)

add_btn = Button(add_frame,width=45,text="View the sheet",cursor='hand2',fg='white',background="#57a1f8",bd=0,activebackground="#ECF9FF",
                   font=('Microsoft YaHei UI Light ',12,'bold'),command=show_sheet)
add_btn.place(x=720,y=150)

exp_btn = Button(add_frame,width=45,text="Export File CSV",cursor='hand2',fg='white',background="#57a1f8",bd=0,activebackground="#ECF9FF",
                   font=('Microsoft YaHei UI Light ',12,'bold'),command=exportfile)
exp_btn.place(x= 220, y=220)

exp_btn = Button(add_frame,width=45,text="Clear Fields",cursor='hand2',fg='white',background="#57a1f8",bd=0,activebackground="#ECF9FF",
                   font=('Microsoft YaHei UI Light ',12,'bold'),command=clear)
exp_btn.place(x= 720, y=220)


doc_attend_sheet_window.mainloop()
