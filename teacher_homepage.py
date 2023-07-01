import tkinter as tk
import mysql.connector
from tkinter import ttk
from functools import partial

class Teacher():
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
        # create a button to show the standard table
        # Define the buttons
        show_class_button = tk.Button(self.root, text="View my classes", command=partial(self.show_class, abc), width=54, height=2, bg='CadetBlue3', fg='white',
                                    activebackground='turquoise', activeforeground='white', borderwidth=0, relief='flat')
        show_class_button.grid(row=1, column=0, padx=8, pady=5)

        min_grades_button = tk.Button(self.root, text="See minimum grade", command=self.min_grade, width=54, height=2, bg='CadetBlue3', fg='white',
                                    activebackground='turquoise', activeforeground='white', borderwidth=0, relief='flat')
        min_grades_button.grid(row=2, column=0, padx=8, pady=5)

        above_grade_button = tk.Button(self.root, text="No. of students above grade", command=self.show_above_grade_window, width=54, height=2, bg='CadetBlue3', fg='white',
                                    activebackground='turquoise', activeforeground='white', borderwidth=0, relief='flat')
        above_grade_button.grid(row=3, column=0, padx=8, pady=5)



    def min_grade(self):

        min_grade_window = tk.Toplevel(self.root)
        min_grade_window.title("See minimum grade")
        min_grade_window.geometry("300x350")

        subject_label = ttk.Label(min_grade_window, text="Enter Subject Name:")
        subject_label.pack()
        subject_entry = ttk.Entry(min_grade_window)
        subject_entry.pack()

        std_label = ttk.Label(min_grade_window, text="Enter Standard:")
        std_label.pack()
        std_entry = ttk.Entry(min_grade_window)
        std_entry.pack()

        min_grade_button = ttk.Button(min_grade_window, text="Get Min Grade", command=lambda: self.get_min_grade(subject_entry.get(), std_entry.get()))
        min_grade_button.pack()

    def get_min_grade(self, subject_name, std):
        query = f"SELECT Grade AS Min_Grade FROM grade_table WHERE percentage = (SELECT MIN(Total) FROM (SELECT (CEIL((Pre_Mid + Mid_Term + Post_Mid + Final_Term)/2)) AS Total FROM assessment WHERE Subject_Name = '{subject_name}' AND Std = {std}) Class_Total)"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result is None:
            tk.messagebox.showinfo("Error", "No grade found for given inputs")
        else:
            min_grade = result[0]
            tk.messagebox.showinfo("Min Grade", "The minimum grade for given inputs is {}".format(min_grade))

    def show_class(self, id):

        show_classes_window = tk.Toplevel(self.root)
        show_classes_window.title("Show all classes")
        show_classes_window.geometry("600x350")

        class_tree = ttk.Treeview(show_classes_window, columns=("Class", "Subject"), show="headings")
        class_tree.heading("Class", text="Class")
        class_tree.heading("Subject", text="Subject")
        class_tree.pack()

        query = "SELECT Std, Subject_Name FROM class WHERE Teacher_ID = (SELECT Teacher_ID FROM teacher WHERE Person_ID = '{}')".format(id)
        self.cursor.execute(query)
        classes = self.cursor.fetchall()
        # insert the classes into the tree view
        for row in classes:
            class_tree.insert("", "end", values=(row[0], row[1]))

        # bind the tree view to a function that retrieves the assessment data for a selected class
        class_tree.bind("<Double-1>", lambda event: self.show_assessment(class_tree.item(class_tree.selection())['values']))

    def show_assessment(self, class_data):
        std = class_data[0]
        subject_name = class_data[1]
        # retrieve the assessment data for the selected class
        query = "SELECT Student_ID, Pre_Mid, Mid_Term, Post_Mid, Final_Term FROM assessment WHERE Std = %s AND Subject_Name = %s"
        self.cursor.execute(query, (class_data[0], class_data[1]))
        assessment_data = self.cursor.fetchall()

        # create a new window to display the assessment data
        assessment_window = tk.Toplevel(self.root)

        # create a tree view to display the assessment data
        assessment_tree = ttk.Treeview(assessment_window, columns=("Student ID", "Pre-Mid", "Mid-Term", "Post-Mid", "Final-Term"), show="headings")
        assessment_tree.heading("Student ID", text="Student ID")
        assessment_tree.heading("Pre-Mid", text="Pre-Mid")
        assessment_tree.heading("Mid-Term", text="Mid-Term")
        assessment_tree.heading("Post-Mid", text="Post-Mid")
        assessment_tree.heading("Final-Term", text="Final-Term")
        assessment_tree.pack()

        # insert the assessment data into the tree view
        for row in assessment_data:
            assessment_tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))

        assessment_tree.bind("<Double-1>", lambda event: self.edit_assessment(assessment_tree.item(assessment_tree.selection())['values'], std, subject_name))
    
    def edit_assessment(self, values, std, subject_name):
        student_id = values[0]

        # create a new window for editing the assessment
        edit_window = tk.Toplevel()
        edit_window.title("Edit Assessment")

        # fetch current values from the database
        self.cursor.execute("SELECT * FROM assessment WHERE Student_ID=%s AND Std=%s AND Subject_Name=%s", (student_id, std, subject_name))
        assessment = self.cursor.fetchone()

        pre_mid = tk.StringVar(value=assessment[3])
        mid_term = tk.StringVar(value=assessment[4])
        post_mid = tk.StringVar(value=assessment[5])
        final_term = tk.StringVar(value=assessment[6])

        # create labels and entry widgets for editing the assessment
        pre_mid_label = ttk.Label(edit_window, text="Pre-Mid:")
        pre_mid_entry = ttk.Entry(edit_window, textvariable=pre_mid)

        mid_term_label = ttk.Label(edit_window, text="Mid-Term:")
        mid_term_entry = ttk.Entry(edit_window, textvariable=mid_term)

        post_mid_label = ttk.Label(edit_window, text="Post-Mid:")
        post_mid_entry = ttk.Entry(edit_window, textvariable=post_mid)

        final_term_label = ttk.Label(edit_window, text="Final-Term:")
        final_term_entry = ttk.Entry(edit_window, textvariable=final_term)

        # create a save button to update the assessment
        def save_changes():
            new_values = (
                pre_mid_entry.get(),
                mid_term_entry.get(),
                post_mid_entry.get(),
                final_term_entry.get(),
                student_id,
                std,
                subject_name
            )
            self.cursor.execute("UPDATE assessment SET Pre_Mid=%s, Mid_Term=%s, Post_Mid=%s, Final_Term=%s WHERE Student_ID=%s AND Std=%s AND Subject_Name=%s", new_values)
            self.mydb.commit()
            edit_window.destroy()

        save_button = ttk.Button(edit_window, text="Save Changes", command=save_changes)

        # pack the labels, entry widgets, and save button
        pre_mid_label.pack()
        pre_mid_entry.pack()
        mid_term_label.pack()
        mid_term_entry.pack()
        post_mid_label.pack()
        post_mid_entry.pack()
        final_term_label.pack()
        final_term_entry.pack()
        save_button.pack()

    def show_above_grade_window(self):
        window = tk.Toplevel(self.root)
        window.title("Enter Grade Details")
        window.geometry("300x300")

        tk.Label(window, text="Standard").grid(row=0, column=0, padx=10, pady=5)
        standard_entry = tk.Entry(window)
        standard_entry.grid(row=0, column=1)

        tk.Label(window, text="Subject Name").grid(row=1, column=0, padx=10, pady=5)
        subject_entry = tk.Entry(window)
        subject_entry.grid(row=1, column=1)

        tk.Label(window, text="Minimum Grade").grid(row=2, column=0, padx=10, pady=5)
        grade_entry = tk.Entry(window)
        grade_entry.grid(row=2, column=1)

        submit_button = ttk.Button(window, text="Submit", command=lambda: self.show_above_grade_result(standard_entry.get(), subject_entry.get(), grade_entry.get()))
        submit_button.grid(row=3, column=1, padx=10, pady=10)


    def show_above_grade_result(self, standard, subject, grade):
        query = f"SELECT COUNT(Total) FROM (SELECT (CEIL((Pre_Mid + Mid_Term + Post_Mid + Final_Term)/2)) AS Total FROM assessment WHERE Subject_Name = '{subject}' AND Std = {standard}) final, (SELECT MAX(Percentage) as lowest FROM grade_table WHERE Grade = '{grade}') tll WHERE Total > lowest;"
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]

        if result is None:
            tk.messagebox.showinfo("Error", "No student or class found for given inputs")
        else:
            tk.messagebox.showinfo("Number of students", f"The number of such students above {grade} from standard {standard} in {subject} is {result}")