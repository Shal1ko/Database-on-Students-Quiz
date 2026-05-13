import sqlite3
import tkinter as tk

db = sqlite3.connect("students.db")
cur = db.cursor()

table = "Students"
table2 = "Grades"

cur.execute(f"CREATE TABLE IF NOT EXISTS {table} (ID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Age INTEGER)")
cur.execute(f"CREATE TABLE IF NOT EXISTS {table2} (ID INTEGER PRIMARY KEY AUTOINCREMENT, Student_ID INTEGER, Grade REAL, Subject TEXT)")

root = tk.Tk()
root.title("Student Database")
root.geometry("400x400")


def addStudentFunc():
    addSt = tk.Tk()
    addSt.title("Add Student")
    addSt.geometry("300x300")

    nameLabel = tk.Label(addSt, text="Name: ")
    nameEntry = tk.Entry(addSt)
    nameLabel.grid(row=0, column=0)
    nameEntry.grid(row=0, column=1)

    ageLabel = tk.Label(addSt, text="Age: ")
    ageEntry = tk.Entry(addSt)
    ageLabel.grid(row=1, column=0)
    ageEntry.grid(row=1, column=1)

    warningLabel = tk.Label(addSt)
    warningLabel.grid(row=3, column=1)

    def addStudentToDB():
        name = nameEntry.get()
        age = ageEntry.get()
        try:
            age = int(age)
            cur.execute(f"INSERT INTO {table} (Name, Age) VALUES (?,?)",(name, age))
            db.commit()
            nameEntry.delete(0, "end")
            ageEntry.delete(0, "end")
            warningLabel.configure(text="Student added successfully")
        except Exception:
            warningLabel.configure(text="Please input proper age")

    add = tk.Button(addSt, text="Add", command=addStudentToDB)
    add.grid(row=2, column=1)

    addSt.mainloop()

addStudent = tk.Button(root, text="Add Student", command=addStudentFunc)
addStudent.pack()


def viewStudents():
    viewSt = tk.Tk()
    viewSt.geometry("500x500")
    viewSt.title(f"{table} table")

    def removeStudent():
        remover = tk.Tk()
        remover.title("remover")
        remover.geometry("200x200")

        labelR = tk.Label(remover, text="ID")
        EntryR = tk.Entry(remover)
        labelR.grid(row=0,column=0)
        EntryR.grid(row=0,column=1)

        WarningLabel = tk.Label(remover)
        WarningLabel.grid(row=3, column=1)

        def remove():
            try:
                delete = int(EntryR.get())
                cur.execute(f"DELETE FROM {table} WHERE ID=?",(delete,))
                db.commit()
                WarningLabel.configure(text="Deletion success")
                update()
                remover.after(1200,remover.destroy)
            except Exception:
                WarningLabel.configure(text="Enter Valid ID")

        deLET = tk.Button(remover, text="Remove", command=remove)
        deLET.grid(row=2, column=1)

        remover.mainloop()

    removeButton = tk.Button(viewSt, text="DeLET a student", command=removeStudent)
    removeButton.pack()



    label = tk.Label(viewSt, text="ID       Name                    Age")
    textBox = tk.Text(viewSt, width=399, height= 399)
    label.pack()
    textBox.pack()

    def update():
        textBox.configure(state="normal")
        textBox.delete(1.0, "end")
        cur.execute(f"SELECT * FROM {table}")
        info = cur.fetchall()

        for row in info:
            line = " ".join(map(str,row)) + f"\n"
            textBox.insert("end", line)
        
        textBox.configure(state="disabled")

    update()

    viewSt.mainloop()


viewStudTable = tk.Button(root, text="View Students", command=viewStudents)
viewStudTable.pack()


def viewGrades():
    viewGr = tk.Tk()
    viewGr.title("Grades")
    viewGr.geometry("700x500")

    addGradeButton = tk.Button(viewGr, text="Add Grade")
    addGradeButton.pack()


    label = tk.Label(viewGr, text="ID       Name            Grade       Subject")
    textBox = tk.Text(viewGr, width=399, height=399)
    label.pack()
    textBox.pack()

    def update():
        textBox.configure(state="normal")
        textBox.delete(1.0, "end")
        cur.execute(f"SELECT {table}.ID, {table}.Name, {table2}.Grade, {table2}.Subject FROM {table} INNER JOIN {table2} ON {table}.ID = {table2}.Student_ID")
        info = cur.fetchall()

        for row in info:
            line = " ".join(map(str,row)) + "\n"
            textBox.insert("end", line)
        textBox.configure(state="disabled")
    
    update()

    def addGrade():
        addGr = tk.Tk()
        addGr.title("Add Grade")
        addGr.geometry("300x300")

        nameLabel = tk.Label(addGr, text="Student ID: ")
        nameEntry = tk.Entry(addGr)
        nameLabel.grid(row=0, column=0)
        nameEntry.grid(row=0, column=1)

        gradeLabel = tk.Label(addGr, text="Grade: ")
        gradeEntry = tk.Entry(addGr)
        gradeLabel.grid(row=1, column=0)
        gradeEntry.grid(row=1, column=1)

        subjectLabel = tk.Label(addGr, text="Subject: ")
        subjectEntry = tk.Entry(addGr)
        subjectLabel.grid(row=2, column=0)
        subjectEntry.grid(row=2, column=1)

        warningLabel = tk.Label(addGr)
        warningLabel.grid(row=4, column=1)

        def addGradeToDB():
            studentID = nameEntry.get()
            grade = gradeEntry.get()
            subject = subjectEntry.get()
            try:
                studentID = int(studentID)
                grade = float(grade)
                cur.execute(f"INSERT INTO {table2} (Student_ID, Grade, Subject) VALUES (?,?,?)",(studentID, grade, subject))
                db.commit()
                nameEntry.delete(0, "end")
                gradeEntry.delete(0, "end")
                subjectEntry.delete(0, "end")
                warningLabel.configure(text="Grade added successfully")
                update()
            except Exception:
                warningLabel.configure(text="Please input proper values")

        add = tk.Button(addGr, text="Add", command=addGradeToDB)
        add.grid(row=3, column=1)

        addGr.mainloop()

    addGradeButton.configure(command=addGrade)
    
    

    viewGr.mainloop()

viewGradesButton = tk.Button(root, text="View Grades", command=viewGrades)
viewGradesButton.pack()

    


root.mainloop()