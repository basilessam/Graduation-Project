import tkinter
from tkinter import *
import pymysql
import csv
import os
from datetime import datetime

attendance_window=Tk()
attendance_window.title("Attendance System")
attendance_window.geometry("925x500+300+200")
attendance_window.config(bg="#ECF9FF")
attendance_window.resizable(False,False)

#back forward button
def backfw_btn():
    attendance_window.withdraw()
    import dashboard_doc
    dashboard_doc.doctor_window.deiconify()


bfw_btn = tkinter.PhotoImage(file='backfw.png',master=attendance_window)
back_forward_btn = Button(attendance_window,cursor='hand2',image=bfw_btn,bd=0,bg="#ECF9FF",activebackground="#ECF9FF",height=80,width=80,command=backfw_btn)
back_forward_btn.place(x=10,y=5)



img_logo = tkinter.PhotoImage(file='logo.png',master=attendance_window)
attendance_window.iconphoto(False,img_logo)

Label(attendance_window,image=img_logo, bg="white",background="#ECF9FF").place(x=50,y=120)
frame = Frame(attendance_window,width=420,height=400,bg="#ECF9FF")
frame.place(x=450,y=60)


def take_attendance():
    import cv2
    import face_recognition
    import numpy as np
    video_capture = cv2.VideoCapture(0)
    path = 'set_images'
    images = []
    known_faces_names = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        known_faces_names.append(os.path.splitext(cl)[0])
    print(known_faces_names)
    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]

            encodeList.append(encode)
        return encodeList
    print('Encoding Complete')
    known_face_encoding = findEncodings(images)
    students = known_faces_names.copy()
    face_locations = []
    face_encodings = []
    face_names = []
    s = True
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")

    f = open("e:\\" + current_date + '.csv', 'w+', newline='')
    lnwriter = csv.writer(f)
    while True:
        _, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        if s:
            face_locations = face_recognition.face_locations(frame,number_of_times_to_upsample=0,model="cnn")
            face_encodings = face_recognition.face_encodings(frame,face_locations)
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
                name = ""
                face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
                best_match_index = np.argmin(face_distance)
                if matches[best_match_index]:
                    name = known_faces_names[best_match_index]

                face_names.append(name)
                if name in known_faces_names:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    bottomLeftCornerOfText = (10, 100)
                    fontScale = 1.5
                    fontColor = (255, 0, 0)
                    thickness = 3
                    lineType = 2

                    cv2.putText(frame, name + ' Present',
                                bottomLeftCornerOfText,
                                font,
                                fontScale,
                                fontColor,
                                thickness,
                                lineType)

                    if name in students:
                        students.remove(name)
                        print(students)
                        current_time = now.strftime("%I:%M:%p")
                        lnwriter.writerow([name, current_time])
                        f.flush()


        cv2.imshow("attendence system", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    f.close()


def take_new_face():
    attendance_window.withdraw()
    import addstudent
    addstudent.Newstudent_window.deiconify()


def take_attendance_manually():
    attendance_window.withdraw()
    import attendsheet
    con_db = pymysql.connect(host='localhost', user='root', password='123456789')
    mycursor = con_db.cursor()
    query = 'use facerecognation_attendance_System'
    mycursor.execute(query)
    list_courses = []
    query = "select course_name from course where lecturer_email = (select email from lecturer join currentlogin on email = curent)"
    mycursor.execute(query)
    row_course = mycursor.fetchall()
    for i in row_course:
        list_courses.append(i[0])
    attendsheet.coursename_combobox['values'] = list_courses
    attendsheet.doc_attend_sheet_window.deiconify()


# create three buttons for taking attendance, adding new students, and viewing sheets
attendance_button = Button(frame,width=15,border=0 ,bg="#0081C9",fg='white',text="Take \n Attendance",
                           command=take_attendance, pady=8,font=("Arial", 14))
attendance_button.place(x=30,y=100)


add_button = Button(frame, width=15,border=0,bg="#0081C9",fg='white',text="Take New \n  Face ID",
                    command=take_new_face, pady=8,font=("Arial", 14))
add_button.place(x=220,y=100)



manualatten_button = Button(frame,width=32,border=0 ,anchor="center",bg="#0081C9",fg='white',text="Take Attendance \n Manually",
                       command=take_attendance_manually, pady=8,font=("Arial", 14))
manualatten_button.place(x=30,y=220)


attendance_window.mainloop()