import os
import sqlite3                                       # importing the sqlite package
from prettytable import PrettyTable

os.chdir('/Users/Anirudh/Desktop/PYFILES')          # This is for the code to work on my system, please remove this while running on your computer.


def instructor_pt(path):

    pt_labels = ['CWID', 'Name', 'Department', 'Courses', 'Students']

    query = 'select a.Instructor_CWID, b.Name, b.Dept, a.Course, count(*) as Student_Count from HW11_grades a join HW11_instructors b on \
    a.Instructor_CWID = b.CWID group by a.Course order by a.Instructor_CWID ASC'        # writing the query for the relational database

    connect = sqlite3.connect(path)                    # use .connect to connect path with the database
    pt = PrettyTable(field_names=pt_labels)
    
    for row in connect.execute(query):                 # use .execute to execute the database and add row to the database.
        pt.add_row(row)

    print(pt)

instructor_pt('D:/Dass.db')                         # the name of my database i created on datagrip.