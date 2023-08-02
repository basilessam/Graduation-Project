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
show_attendance_sheet_query=" select distinct stu.fullname,shee.date_time,shee.attend_course_name,DATE(shee.arrivaldate),stu.student_id , stu.acadymic_year, stu.semester from attendance_sheet shee  join student stu on  stu.fullname like concat('%%',left(shee.stud_name,20),'%%')  or shee.stud_id = stu.student_id order by semester asc"

attendance_sheet_window = Tk()
attendance_sheet_window.title("Attendance Sheet")
attendance_sheet_window.geometry("1450x720+40+40")
attendance_sheet_window.config(bg="#ECF9FF")
attendance_sheet_window.resizable(False,False)
img_logo =tkinter.PhotoImage(file='logo.png',master=attendance_sheet_window)
attendance_sheet_window.iconphoto(False,img_logo)


atten_list_frame = LabelFrame(attendance_sheet_window,text="Attendance List")
#search_frame = LabelFrame(attendance_sheet_window,text="Search")
atten_data_frame = LabelFrame(attendance_sheet_window,text="Data")

atten_list_frame.pack(fill="both",expand="yes",padx=20,pady=10)
#search_frame.pack(fill="both",expand="yes",padx=20,pady=10)
atten_data_frame.pack(fill="both",expand="yes" ,padx=20,pady=10)


def backfw_btn():
    attendance_sheet_window.withdraw()
    import dashboard_admin
    dashboard_admin.admin_dashboard_window.deiconify()

bfw_btn = tkinter.PhotoImage(file='backfw.png',master=attendance_sheet_window)
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

#attendance sheet list section

def exportfile():
    crnttime = datetime.datetime.strftime(current_date, '%I-%M-%p')
    if len(mydata) < 1:
        messagebox.showerror('Error', 'There is now data to export')
        return False
    else:
        file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV",
                                            initialfile=txtvar_of_attend_course_name.get() + "-" + str(
                                                current_date.date()) + "-" + str(crnttime) + '.csv',
                                            filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")))
        with open(file, mode='w', encoding="utf-8") as myfile:
            file_writer = csv.writer(myfile, delimiter=",")
            for i in mydata:
                file_writer.writerow(i)
        messagebox.showinfo('Data Exported', 'Your data has been exported ' + os.path.basename(file) + ' succesfully.')

def importfile():
    mydata.clear()
    file = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV",
                                        filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")))
    with open(file) as myfile:
        csvread = csv.reader(myfile,delimiter=",")
        for i in csvread:
            mydata.append(i)
        if mydata == []:
            messagebox.showerror("Error", "Can not import an empty file")
    showdata(mydata)

#show the table of the lecturer
try:
    mycursor.execute(show_attendance_sheet_query)
    mainrowa = mycursor.fetchall()
    showdata(mainrowa)
except Exception as err:
    messagebox.showwarning('Error', 'DB exception: %s' % err)

def savefile():
        print(mydata)
        print(mainrowa)
        if(len(mydata)  < 1):
            messagebox.showerror("Error","There is now data to save")
        elif len(mydata) >= 1:
            for i in mydata:
                stud_name = i[0]
                cor_name = i[2]
                q = "select * from attendance_sheet where stud_name=%s and attend_course_name=%s and DATE(arrivaldate)=%s "
                mycursor.execute(q, (stud_name,cor_name, current_date.date()))
                row = mycursor.fetchone()
                print(stud_name , cor_name)
                print("row: "+str(row))
                if row is not None:
                    print("a")
                    messagebox.showerror("Error", "There is duplicate data please reimport with the correct data")
                    return False
                elif messagebox.askyesno("Confirmation", "Are you sure you wnat to save to database"):
                    for i in mydata:
                        stud_name = i[0]
                        date_time = i[1]
                        attend_course_name = i[2]
                        query = "insert into attendance_sheet(stud_name,date_time,attend_course_name,arrivaldate) values(%s,%s,%s,now())"
                        mycursor.execute(query, (stud_name, date_time, attend_course_name))
                    mydata.clear()
                    messagebox.showinfo("Data Saved", "Data has been saved to database")
                    con_db.commit()
                    txtvar_of_attend_course_name.set(attend_course_name)
                    reset()

        elif len(mainrowa) < 1:
            messagebox.showerror("Error", "There is now data to save")
        else:
            for i in mainrowa:
                stud_name = i[0]
                id = i[4]
                print(id)
                q = "select * from attendance_sheet where stud_id =%s or stud_name=%s"
                mycursor.execute(q, (id, stud_name))
                row = mycursor.fetchone()
                if row is not None:
                    print("b")
                    messagebox.showerror("Error", "There is duplicate data please reimport with the correct data")
                    return False
            if messagebox.askyesno("Confirmation", "Are you sure you wnat to save to database"):
                for i in mydata:
                    stud_name = i[0]
                    date_time = i[1]
                    attend_course_name = i[2]
                    query = "insert into attendance_sheet(stud_name,date_time,attend_course_name,arrivaldate) values(%s,%s,%s,now())"
                    mycursor.execute(query, (stud_name, date_time, attend_course_name))
                messagebox.showinfo("Data Saved", "Data has been saved to database")
                con_db.commit()
                reset()
            else:
                return False


no_attnd = Label(atten_list_frame, text="", fg="red", width=25, bg="#ECF9FF",
                 font=('Microsoft YaHei UI Light ', 30))
no_attnd.place(x=100, y=10)



def reset():
    try:
        if txtvar_of_attend_course_name.get() == '':
            messagebox.showerror("Error", "Please select course name")
            return False
        show_attendance_sheet_query = " select distinct stu.fullname,shee.date_time,shee.attend_course_name,DATE(shee.arrivaldate),stu.student_id , stu.acadymic_year, stu.semester from attendance_sheet shee  join student stu on  stu.fullname like concat('%%',left(shee.stud_name,20),'%%') and attend_course_name =%s   or shee.stud_id = stu.student_id and attend_course_name =%s order by semester asc"
        mycursor.execute(show_attendance_sheet_query,(txtvar_of_attend_course_name.get(),txtvar_of_attend_course_name.get()))
        row = mycursor.fetchall()
        showdata(row)
        no_attnd.config(text="")
    except Exception as err:
        messagebox.showwarning('Error', 'DB exception: %s' % err)

def reset_ac_course():
    try:
        sheet_query = " select distinct stu.fullname,shee.date_time,shee.attend_course_name,DATE(shee.arrivaldate),stu.student_id , stu.acadymic_year, stu.semester from attendance_sheet shee  join student stu on  stu.fullname like concat('%%',left(shee.stud_name,20),'%%') and attend_course_name =%s and date(shee.arrivaldate) =%s or shee.stud_id = stu.student_id and date(shee.arrivaldate) =%s and attend_course_name =%s order by semester asc"
        mycursor.execute(sheet_query,(txtvar_of_attend_course_name.get(),current_date.date(),current_date.date(),txtvar_of_attend_course_name.get()))
        row = mycursor.fetchall()
        showdata(row)
    except Exception as err:
        messagebox.showwarning('Error', 'DB exception: %s' % err)

#search section

#get data
txtvar_of_stud_name = StringVar(master=attendance_sheet_window)
txtvar_of_date_time = StringVar(master=attendance_sheet_window)
txtvar_of_attend_course_name = StringVar(master=attendance_sheet_window)
txtvar_of_student_id= StringVar(master=attendance_sheet_window)
txtvar_of_acadymic_year= StringVar(master=attendance_sheet_window)
txtvar_of_semester= StringVar(master=attendance_sheet_window)
#search for record
#txtvar_of_search = StringVar()


#student data section to update

def getrow(event):
    row_data = trv.identify_row(event.y)
    data = trv.item(trv.focus())
    txtvar_of_attend_course_name.set(data['values'][2])


trv.bind("<Double-1>", getrow)


coursename_combobox = ttk.Combobox(atten_data_frame, width=15,textvariable=txtvar_of_attend_course_name)

coursename_label = Label(atten_data_frame, text="Course Name",
                         font=('Microsoft YaHei UI Light ',15,'bold'))
coursename_label.grid(row=0,column=0,padx=5,pady=3)
# Adding combobox drop down list
list_courses = []
query = "select course_name from course"
mycursor.execute(query)
row_course = mycursor.fetchall()
for i in row_course:
    list_courses.append(i[0])
coursename_combobox['values'] =list_courses
coursename_combobox.grid(row=0,column=1,padx=5,pady=3)


def clear():
    txtvar_of_attend_course_name.set('')

def get_no_of_attend():
    global current_date
    try:
        query = "select count(*) from attendance_sheet where date(arrivaldate) =%s and attend_course_name=%s"
        mycursor.execute(query, (current_date.date(), txtvar_of_attend_course_name.get()))
        row_no_ofatt = mycursor.fetchone()[0]
        no_of_attnd = "number of attendees: "
        no_attnd.config(text=no_of_attnd + str(row_no_ofatt))#configure the label
        reset_ac_course()
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
            show_attendance_sheet_query = " select distinct stu.fullname,shee.date_time,shee.attend_course_name,DATE(shee.arrivaldate),stu.student_id , stu.acadymic_year, stu.semester from attendance_sheet shee  join student stu on left(shee.stud_name,5) = left(stu.fullname,5) or shee.stud_id = stu.student_id and DATE(shee.arrivaldate) = %s and attend_course_name= %s order by semester asc"
            mycursor.execute(show_attendance_sheet_query, (current_date.date(), txtvar_of_attend_course_name.get()))
            row = mycursor.fetchall()
            showdata(row)
            get_no_of_attend()
    except Exception as err:
        messagebox.showwarning('Error', 'DB exception: %s' % err)

# make export and import and save buttons
exp_btn = Button(atten_data_frame,width=20,text="Export File CSV",cursor='hand2',fg='white',background="#57a1f8",bd=0,activebackground="#ECF9FF",
                   font=('Microsoft YaHei UI Light ',11,'bold'),pady=5,command=exportfile)
exp_btn.place(x=180, y=170)

imp_btn = Button(atten_data_frame,width=20,text="Import File CSV",cursor='hand2',fg='white',background="#57a1f8",bd=0,activebackground="#ECF9FF",
                   font=('Microsoft YaHei UI Light ',11,'bold'),pady=5,command=importfile)
imp_btn.place(x=180, y=250)

save_btn = Button(atten_data_frame,width=20,text="Save Data ",cursor='hand2',fg='white',background="#57a1f8",bd=0,activebackground="#ECF9FF",
                   font=('Microsoft YaHei UI Light ',11,'bold'),pady=5,command=savefile)
save_btn.place(x=600, y= 170)

#reset btn
reset_btn = Button(atten_data_frame,text="View all sheets ",activebackground="#ECF9FF",bd=0,cursor="hand2",
                   width=20,background="#57a1f8",fg="white",
                   font=('Microsoft YaHei UI Light ',11,'bold'),pady=5,command=reset)
reset_btn.place(x= 600, y=250)
#show the sheet btn
viewsheet_btn = Button(atten_data_frame,width=20,text="View the sheet of \n "+str(current_date.date()),cursor='hand2',fg='white',background="#57a1f8",bd=0,activebackground="#ECF9FF",
                   font=('Microsoft YaHei UI Light ',12,'bold'),pady=5,command=show_sheet)
viewsheet_btn.place(x=1010,y=170)

#clear al fields btn
clear_btn = Button(atten_data_frame,width=20,text="Clear Fields",cursor='hand2',fg='white',background="#57a1f8",bd=0,activebackground="#ECF9FF",
                   font=('Microsoft YaHei UI Light ',12,'bold'),pady=5,command=clear)
clear_btn.place(x= 1010, y=250)
attendance_sheet_window.mainloop()
