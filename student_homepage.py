import tkinter as tk
import mysql.connector
from tkinter import ttk
from functools import partial

class Student():
    def __init__(self,root,abc):
        self.root=root
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Shardul4245",
            database="dbsproject"
        )
        self.cursor=self.mydb.cursor()
        self.create_widgets(abc)

    def create_widgets(self, abc):
        show_classes_button = tk.Button(self.root, text="View my classes", command=partial(self.show_classes, abc), width=54, height=2, bg='CadetBlue3', fg='white',
                                    activebackground='turquoise', activeforeground='white', bd=0)
        show_classes_button.grid(row=1, column=0, padx=8, pady=5)

        all_grades_button = tk.Button(self.root, text="Grade Sheet", command=partial(self.all_grades, abc), width=54, height=2, bg='CadetBlue3', fg='white',
                                            activebackground='turquoise', activeforeground='white', bd=0)
        all_grades_button.grid(row=2, column=0, padx=8, pady=5)

        all_subject_button = tk.Button(self.root, text="Select Subjects", command=partial(self.all_subjects, abc), width=54, height=2, bg='CadetBlue3', fg='white',
                                            activebackground='turquoise', activeforeground='white', bd=0)
        all_subject_button.grid(row=3, column=0, padx=8, pady=5)

    def show_classes(self, student_id):
        # create new window
        class_window = tk.Toplevel(self.root)
        class_window.title("My Classes")
        
        # run query
        query = f"SELECT Student_ID, Subject_Name FROM assessment WHERE Student_ID = (SELECT Student_ID from student WHERE Person_ID = '{student_id}')"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        
        # create treeview to display results
        columns = ('Student ID', 'Subject Name')
        tree = ttk.Treeview(class_window, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
        tree.pack()
        
        # insert data into treeview
        for row in result:
            tree.insert("", "end", values=row)

    def all_grades(self, abc):
        query = f"SELECT Subject_Name, Percentage, Grade FROM assessment NATURAL JOIN grade_table WHERE Student_ID = '{abc}';"

        self.cursor.execute(query)
        result = self.cursor.fetchall()

        # Create a new window to display the result
        new_window = tk.Toplevel(self.root)
        new_window.title("Grade Sheet")

        # Create a table to display the result
        table = ttk.Treeview(new_window, columns=("Subject Name", "Total", "Grade"), show="headings")
        table.heading("Subject Name", text="Subject Name")
        table.heading("Total", text="Total")
        table.heading("Grade", text="Grade")

        for row in result:
            table.insert("", tk.END, values=row)

        table.pack()

    def all_subjects(self, student_id):
        # create new window
        subject_window = tk.Toplevel(self.root)
        subject_window.title("Add Subjects")
        subject_window.geometry("300x300")

        tk.Label(subject_window, text="Subject Name").grid(row=0, column=0, padx=50, pady=5)
        subject_entry = tk.Entry(subject_window)
        subject_entry.grid(row=0, column=0)

        # run query
        query = f"SELECT Std FROM student WHERE Student_ID = (SELECT Student_ID from student WHERE Person_ID = '{student_id}')"
        self.cursor.execute(query)
        std = self.cursor.fetchall()[0][0]

        # Define the add button
        add_button = tk.Button(subject_window, text="Add", command=lambda: self.add_sub(student_id, std, subject_entry.get()))
        add_button.grid(row=1, column=0, columnspan=2)
    
    def add_sub(self, person_id, std, subject):
        # run query
        query = f"SELECT Teacher_ID FROM class WHERE Std = {std} AND Subject_Name = '{subject}'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()[0][0]
        print(result)

        q = f"SELECT Student_ID FROM student WHERE Person_ID = '{person_id}'"
        self.cursor.execute(q)
        student_id = self.cursor.fetchall()[0][0]
        
        if(result):
            k = f"SELECT * FROM assessment WHERE Std = {std} AND Student_ID = '{student_id}' AND Subject_Name = '{subject}'"
            self.cursor.execute(k)
            x = self.cursor.fetchall()[0][0]

            if x:
                tk.messagebox.showinfo("Error", "You are already enrolled in this subject.")    

            else:
                qu = f"INSERT INTO assessment VALUES ('{student_id}', {std}, '{subject}', DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT)"
                self.cursor.execute(qu)
                tk.messagebox.showinfo(f"Success!", "{subject} is added as your subject.")

        else:
            tk.messagebox.showinfo("Error", "No such subject is available for you.")