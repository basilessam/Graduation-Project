import tkinter
from tkinter import *
import cv2
import face_recognition as fr
import pymysql
from tkinter import messagebox

Newstudent_window=Tk()
Newstudent_window.title('Take New Student')
Newstudent_window.geometry("925x500+300+200")
Newstudent_window.config(bg="#ECF9FF")
Newstudent_window.resizable(False,False)
img_logo = tkinter.PhotoImage(file='logo.png',master=Newstudent_window)
Newstudent_window.iconphoto(False, img_logo)

con_db = pymysql.connect(host='localhost', user='root', password='123456789')
mycursor = con_db.cursor()
query = 'use facerecognation_attendance_System'
mycursor.execute(query)


#back forward button
def backfw_btn():
    Newstudent_window.withdraw()
    import attendence_dashboard
    attendence_dashboard.attendance_window.deiconify()


bfw_btn = tkinter.PhotoImage(file='backfw.png',master=Newstudent_window)
back_forward_btn = Button(Newstudent_window,cursor='hand2',image=bfw_btn,bd=0,bg="#ECF9FF",activebackground="#ECF9FF",height=80,width=80,command=backfw_btn)
back_forward_btn.place(x=10,y=5)

frame = Frame(Newstudent_window,width=350,height=370,bg="#ECF9FF")
frame.place(x=300,y=90)

def on_enter(e):
    stu_id_entry.delete(0,'end')
def on_leave(e):
    id =stu_id_entry.get()
    if id=='':
        stu_id_entry.insert(0, 'Enter Student ID or last 4 digit')


stu_id_entry = Entry(frame,width=35,fg='#181823',border=0,bg="#ECF9FF",font=('Microsoft YaHei UI Light ',15))
stu_id_entry.place(x=30,y=100)
stu_id_entry.insert(0,'Enter Student ID or last 4 digit')
stu_id_entry.bind('<FocusIn>',on_enter)
stu_id_entry.bind('<FocusOut>',on_leave)
Frame(frame,width=295,height=2,bg="black").place(x=25,y=125)

def take_attendance_manually():
    if stu_id_entry.get()=='Enter Student ID or last 4 digit':
        messagebox.showerror("Error","Pleas enter Student ID")
    else:
        query = "select fullname from student where student_id like '%"+stu_id_entry.get()+"'"
        mycursor.execute(query)
        row = mycursor.fetchone()
        if row is None:
            messagebox.showerror("Error","This student is not in the system yet")
            return False
        dataset_path = "set_images"
        cap = cv2.VideoCapture(0)
        face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        new_member_name = "".join(row)
        while True:
            ret, frame = cap.read()
            face_locations = fr.face_locations(frame)
            face_encodings = fr.face_encodings(frame, face_locations)
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                cv2.rectangle(frame, (left + 1, top + 1), (right + 1, bottom + 1), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 15), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, new_member_name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

            cv2.imshow('frame', frame)
            cv2.imwrite(f"{dataset_path}/{new_member_name}.jpg", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Done",f"New member {new_member_name} added to dataset.")


enter_btn = Button(frame,cursor='hand2',width=39,pady=7,text="Enter",
                   bg="#57a1f8",fg='white',border=0,command=take_attendance_manually)
enter_btn.place(x=35,y=250)

Newstudent_window.mainloop()