"""
Caleb Brown


This is the file where we will
+ Create the database need 
+ fill the database with tables

"""
import sqlite3


#this will be the database we will use for our school. Since this is a new database, 
#doing this line will create the database 'school' then connect to it, in the future it will only connect and not have to create it
conn = sqlite3.connect('school.db')

#An issue I have run into before is if you do not properly close the database or do something else incorrectly when making the tables, theres a chance the database might lock up
#So we will use a Try block to make sure that it does close after trying to make the table for our database

#This database will include tables for the school class schedule, the grades for the class, and all the homework
#once the table is made you dont actually have to keep the code, you can create the table if it doesnt already exist then actually delete the code for it, 
#Ill leave it so everyone can see each tables code


try:
    c = conn.cursor()
  

#First we create our classes table
    c.execute("""CREATE TABLE IF NOT EXISTS classes (
          class_id INTEGER PRIMARY KEY AUTOINCREMENT,
          class_name TEXT NOT NULL,
          class_day REAL,
          class_time REAL
          )""")
    conn.commit()
#Next we create our students table
    c.execute("""CREATE TABLE IF NOT EXISTS students (
          student_id INTEGER PRIMARY KEY AUTOINCREMENT,
          student_name TEXT NOT NULL,
          student_password TEXT NOT NULL
          )""")
          
    conn.commit()

#Last we create our enrollment table
    c.execute("""CREATE TABLE IF NOT EXISTS enrollment (
          student_id INTEGER,
          class_id INTEGER,
          grade TEXT NOT NULL,
          difficulty INTEGER,
          PRIMARY KEY(student_id,class_id),
          FOREIGN KEY (student_id)
            REFERENCES students (student_id),

          FOREIGN KEY (class_id)
            REFERENCES classes (class_id)
          )""")
          
    conn.commit()
finally:
    conn.close()

#--- IMPORTANT ---
#We will not be using two databases to do this, we will have just one database and we will host three tables on it, one for student id, one for class id, and then one to link the individual students to their classes
#I looked at previous code made and realized that if we use two databases we wont be able to properly link our student table in a student database to a classes table in a school database. 



