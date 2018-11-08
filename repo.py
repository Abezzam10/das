'''Author: Anirudh Das Bezzam'''


from prettytable import PrettyTable         # importing prettytable
from pp import file_reader                  # from my file reader importing my file reader
import os
import unittest
from collections import defaultdict

os.chdir('/Users/Anirudh/Desktop/PYFILES')

class Student:

    pt_labels = ["CWID", "NAME", "MAJOR", "COMPLETED COURSES", "REMAINING COURSES", "REMAINING ELECTIVES"]            # specifying the labels 

    def __init__(self, cwid, name, major, in_major):
        self._cwid = cwid
        self._name = name
        self._major = major
        self._inmajor = in_major
        self._courses = dict()          # specify  key = course and value is grade. dictionary
        

    def add_course(self, course, grade):
        grade_type = ['A', 'A-', 'B+', 'B-', 'C+', 'C-']
        if grade in grade_type:
            self._courses[course] = grade       # adding the course as a key and the grade as a value

    def pt_row(self):
        completed_courses, rem_required, rem_electives = self._inmajor.grade_check(self._courses)
        return[self._cwid, self._name, self._major, completed_courses, rem_required, rem_electives]  # using sort to sort the courses and their respective keys

class Instructor:

    pt_labels = ["CWID", "NAME", "DEPT", "COURSE", "STUDENTS"]

    def __init__(self, cwid, name, dept):
        self._cwid = cwid
        self._name = name 
        self._dept = dept
        self._courses = defaultdict(int)            #key is course and the value is the no of students.
    
    def add_course(self, course):
        self._courses[course] += 1

    def pt_row(self):
        for course, students in self._courses.items():
            yield[self._cwid, self._name, self._dept, course, students]    # using a generator to pause the 

    
class University:

    def __init__(self, wdir, ptables=True):
        self._wdir = wdir
        self._students = dict()
        self._instructors = dict()
        
        self._majors = dict()               #storing the major value as a dictionary
        
        
        self.read_instructors(os.path.join(wdir, 'instructors.txt'))
        self.read_majors(os.path.join(wdir, 'majors.txt'))
        self.read_students(os.path.join(wdir, 'students.txt'))          # joining the wdir with the files to read
        self.read_grades(os.path.join(wdir, 'grades.txt'))
        

        if ptables:
            print("\n Student Summary")
            self.student_prettytable()              # checking conditions for prettytables (if it is present)

            print("\n Instructor Summary")
            self.instructor_prettytable()
            
            print("\n Majors Summary")               # prettytable creation for Majors
            self.major_prettytable()
            
    
    def read_majors(self,path):
        try:
            for major, flag, course in file_reader(path, 3, sep = "\t", header = False):
                if major in self._majors:
                    self._majors[major].add_course(flag, course)    
                else:
                    self._majors[major] = Major(major)
                    #self._majors[major].add_course(flag, course)       
        except ValueError as err:
            print(err)



    def read_students(self, path):
        try:
            for cwid, name, major in file_reader(path, 3, sep = "\t", header = False):
                if cwid in self._students:
                    print(f"ALready exists {cwid}")                         # condition if the cwid already exists
                else:
                    self._students[cwid] = Student(cwid, name, major, self._majors[major])          # else add students cwid, name and major
        
        except ValueError as err:
            print(err)

    def read_instructors(self, path):
        try:
            for cwid, name, dept in file_reader(path, 3, sep = "\t", header = False):
                if cwid in self._instructors:
                    print(f"ALready exists {cwid}")
                else:
                    self._instructors[cwid] = Instructor(cwid, name, dept)
        except ValueError as err:
            print(err)


    def read_grades(self, path):
        try:
            for student_cwid, course, grade, instructor_cwid in file_reader(path, 4, sep ='\t', header = False):
                if student_cwid in self._students:
                    self._students[student_cwid].add_course(course, grade)      # using the student cwid as key
                else:
                    print(f"Warning: Student cwid {student_cwid} is not in the students file")

                if instructor_cwid in self._instructors:
                    self._instructors[instructor_cwid].add_course(course) # using the instructor cwid as key
                else:
                    print(f"Warning: instructor cwid {instructor_cwid} is not in the instructor file")
            
        except ValueError as erf:
            print(erf)

    def student_prettytable(self):
        pt = PrettyTable(field_names=Student.pt_labels)
        for student in self._students.values():         # printing pretty table for students 
            pt.add_row(student.pt_row())        
        print(pt)
    
    def instructor_prettytable(self):
        pt = PrettyTable(field_names=Instructor.pt_labels)
        for instructor in self._instructors.values():           # printing pretty table for instructors: multiple courses!!!!!!
            for row in instructor.pt_row():
                pt.add_row(row)
        print(pt)
    
    def major_prettytable(self):
        pt = PrettyTable(field_names=Major.pt_labels)
        for major in self._majors.values():             # printing pretty table for major
            pt.add_row(major.pt_row())        
        print(pt)

class Major:

    pt_labels = ["MAJOR", "REQUIRED COURSES", "ELECTIVES"]

    def __init__(self, name, passing=None):
        self._name = name
        self._required = set()
        self._electives = set()
        if passing is None:
            self._passing_grades = {'A', 'A-', 'B+', 'B-', 'C+', 'C-'}
        else:
            self._passing_grades = passing

    def add_course(self, flag, course):
        if flag == 'E':
            self._electives.add(course)
        elif flag == 'R':
            self._required.add(course)
        else:
            raise ValueError("No such {} course occurs".format(flag))

    def grade_check(self, courses):
        completed_courses = {course for course, grade in courses.items() if grade in self._passing_grades}
        if completed_courses == "{}":
            return[completed_courses, self._required, self._electives]
        else:
            rem_required = self._required-completed_courses
            if self._electives.intersection(completed_courses):
                rem_electives = None
            else:
                rem_electives = self._electives

            return[completed_courses, rem_required, rem_electives]

    def pt_row(self):
        return[self._name, self._required, self._electives]

def main():

    University("/Users/Anirudh/Desktop/PYFILES")        # create a main function to store the directory

        
if __name__ == "__main__":
    main()                      # call the main function
