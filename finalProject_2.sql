create database facerecognation_attendance_System;
use facerecognation_attendance_System;

create table lecturer(
	lecturer_id int not null auto_increment,
    full_name varchar(30) not null,
    email varchar(50),
    pass varchar(40) not null,
    dep_name varchar(30),
    department_id int ,
    constraint lecturer_pk primary key (lecturer_id),
    constraint lect_dept_fk foreign key (department_id) references department(department_id)
);

#select * from lecturer;
#insert into lecturer(full_name,email,pass,dep_name) values('poula mansour','poula@gmail.com',1234,'علوم حاسب'),
															#('pepo maher','pepo@gmail.com',12345,'علوم حاسب'),
															#('basil essam','basil@gmail.com',123456,'نظم ومعلومات');
#alter table lecturer add column department_name varchar(30) not null references department (dep_name) ;
#alter table lecturer add constraint lect_dept_fk foreign key (department_name) references department(dep_name);
#select * from lecturer;

create table currentlogin(
	curent varchar(30),
	lect_id int,
    constraint currentlogin_lect_fk foreign key(lect_id) references lecturer(lecturer_id)
);
#insert into currentlogin(curent) values('poula@gmail.com');

#select * from currentlogin;
#select  full_name from lecturer join currentlogin on curent = email;
#select course_name from course join currentlogin on curent = lecturer_email;

create table admin(
	 admin_id int not null auto_increment,
	 full_name varchar(30) not null,
	 pass varchar(40) not null,
     constraint admin_pk primary key (admin_id)
);
#insert into admin(full_name,pass)values('poula mansour','123'),
										#('abanoub maher','1234'),
										#('basil essam','12345');

#select * from course;

create table student
(
student_id int not null,
fullname varchar(30) not null,
acadymic_year varchar(25),
semester varchar(25),
department_name varchar(30) not null,
course_name varchar(30),
constraint student_pk primary key (student_id)
);


#insert into student(student_id,fullname,acadymic_year,semester,department_name) values(320200029,'poula mansour gabr','22/23','first','علوم حاسب'),
																	   #(320200157,'abanoub maher moaoud','22/23','first','علوم حاسب'),
                                                                       #(320200123,'basil essam','22/23','first','نظم ومعلومات'),
                                                                       #(320200124,'pop','18/19','first','نظم ومعلومات');




#select * from student 
#order by acadymic_year desc;

#drop table student;
#select student_fullname , student_id from student st join department dep on st.department_name = dep.dep_name;
#select * from lecturer;


create table course
(
course_id int not null auto_increment,
course_name varchar(30) not null,
dept_name varchar(30) not null,
lecturer_email varchar(50),
acadymic_year varchar(25) not null,
semester varchar(25) not null,
constraint course_pk primary key (course_id)
#student_id int,
#dep_id int ,
#lecturer_id int ,
#constraint course_student_fk foreign key (student_id) references student(student_id),
#constraint course_lecturer_fk foreign key (lecturer_id) references lecturer(lecturer_id),
#constraint course_depart_fk foreign key(dep_id) references department (department_id)
);
#insert into course(course_name,dept_name,lecturer_email,acadymic_year,semester) values('database','علوم حاسب','poula@gmail.com','22/23','first'),
																						#('operating system','علوم حاسب','pepo@gmail.com','22/23','first'),
																						#('structure programming','علوم حاسب','basil@gmail.com','22/23','second');
																			



#drop table course;
#alter table course add column student_id int;
#alter table course add constraint course_student_fk foreign key (student_id) references student(student_id);
#alter table course add column acadymic_year varchar(25) not null;
#alter table course add column smaster varchar(25) not null;
#alter table course add constraint course_lecturer_fk foreign key (lecturer_id) references lecturer(lecturer_id);

create table department
(
dep_name varchar(30) not null,
department_id int not null auto_increment,
constraint department_pk primary key (department_id)
);
#select * from department;

#insert into department(dep_name) values('علوم حاسب'),
							#('نظم ومعلومات'),
                            #('اداره اعمال');
                            
						                    
                                                       
#create table alldata
#(
#acadymic_year varchar(25) not null,
#lec_email varchar(50),
#stu_id int references student (student_id),
#course_id int references course (course_id),
#constraint alldata_pk primary key (stu_id),
#constraint alldata_lect_fk foreign key(lec_email) references lecturer(email)
#);
#drop table alldata;
#alter table alldata add column lec_email varchar(50);
#alter table alldata add constraint alldata_lect_fk foreign key(lec_email) references lecturer(email);
#insert into alldata (acadymic_year,lec_email,stu_id,course_id)values ('18/10/2000','poula@gmail.com',320200029,11);
#update alldata set acadymic_year = '18/10/2000' where lec_email = 'poula@gmail.com';



create table attendance_sheet
(
stud_name varchar(30) not null,
date_time varchar(30) not null,
attend_course_name varchar(30) not null,
stud_id int,
constraint attendance_stud_fk foreign key (stud_id) references student(student_id)
);
insert into attendance_sheet(stud_name,date_time,attend_course_name) values('poula mansour','5 pm','database');

#select * from attendance_sheet;
#select * from lecturer;
#drop table attendance_sheet;

#select distinct shee.stud_name,shee.date_time,shee.attend_course_name,stu.fullname,stu.fullname,stu.student_id , stu.acadymic_year, stu.semester 
#from attendance_sheet shee  
#join student stu on left(shee.stud_name,5) = left(stu.fullname,5)  order by semester asc;

#select * from  student stu
#join attendance_sheet shee on left(stu.fullname,5) = left(shee.stud_name,5)  order by semester asc;

create table face_record
(
 face_id varchar(50),
 constraint facerecord_pk primary key (face_id),
 atten_num int references attendance_sheet(attendance_num)
);


create table capture_photo
(
stu_id int references student(student_id) ,
face_id varchar(50) references face_record (face_id),
constraint capturephoto_pk primary key (stu_id)
);

#select * from course;
#query to show table course and department
#select co.course_name ,dep.dep_name from course co right outer join department dep on dep.department_id = co.dep_id
#union
#select co.course_name ,dep.dep_name from course co left outer join department dep on dep.department_id = co.dep_id; 

#insert into course (course_name ,course_id ,dept_name,acadymic_year,smaster) values( 'bussiness ' ,16,'اداره اعمال','22/23','first');

#select * from course;
#query to show table lecturer that didn't have a course 
#select  co.course_id , co.course_name, co.lecturer_email ,co.dept_name , lec.full_name , lec.email , lec.dep_name
#from course co right outer join lecturer lec on lec.email = co.lecturer_email;

#select  co.course_id , co.course_name, co.lecturer_email ,co.dept_name , lec.full_name , lec.email
#from course co right outer join lecturer lec on lec.email = co.lecturer_email 
#union
#select  co.course_id , co.course_name, co.lecturer_email ,co.dept_name , lec.full_name , lec.email
#from course co left outer join lecturer lec on lec.email = co.lecturer_email ;

#select  co.course_id , co.course_name, co.lecturer_email ,co.dept_name , lec.full_name , lec.email
#from course co  join lecturer lec on lec.email = co.lecturer_email ;


#select * from course;
#query to show table course and student
#select  co.course_id ,co.course_name , co.student_id ,co.dept_name , co.acadymic_year , co.semester, stu.student_fullname,stu.student_id
#from course co  join student stu on co.student_id = stu.student_id;

#select * from lecturer;
#update course set lecturer_email = 'asmaa@gmail.com' where course_name ='bussiness ';

#select  co.course_id , co.course_name, co.lecturer_email ,co.dept_name , lec.full_name , lec.email
#from course co left outer join lecturer lec on lec.email = co.lecturer_email ;

#select * from student;

#update course set full_name ='basil essam' , email = 'basil@gmail.com' , pass ='1234' , department_name ='علوم حاسب'  where lecturer_id =3