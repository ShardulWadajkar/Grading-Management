import tkinter as tk
import tkinter.messagebox
import mysql.connector
from tkinter import ttk

class Admin():
    def __init__(self,root):
        self.root=root
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Shardul4245",
            database="dbsproject"
        )
        self.cursor=self.mydb.cursor()
        self.create_widgets()
    
    def create_widgets(self):
        # Define the add user and add teacher buttons
        add_user_button = tk.Button(self.root, text="Add Student", command=self.add_user, width=54, height=2, bg='CadetBlue3', fg='white',
                                    activebackground='turquoise', activeforeground='white', borderwidth=0, relief='flat')
        add_user_button.grid(row=0, column=0, padx=8, pady=5)

        add_user2_button = tk.Button(self.root, text="Add Teacher", command=self.add_user2, width=54, height=2, bg='CadetBlue3', fg='white',
                                    activebackground='turquoise', activeforeground='white', borderwidth=0, relief='flat')
        add_user2_button.grid(row=1, column=0, padx=8, pady=5)

        # Define the view profile, update profile, and delete profile buttons
        view_profile_button = tk.Button(self.root, text="View Profile", command=self.view_profile, width=54, height=2, bg='CadetBlue3', fg='white',
                                        activebackground='turquoise', activeforeground='white', borderwidth=0, relief='flat')
        view_profile_button.grid(row=2, column=0, padx=8, pady=5)

        update_profile_button = tk.Button(self.root, text="Update Profile", command=self.update_profile, width=54, height=2, bg='CadetBlue3', fg='white',
                                        activebackground='turquoise', activeforeground='white', borderwidth=0, relief='flat')
        update_profile_button.grid(row=3, column=0, padx=8, pady=5)

        delete_profile_button = tk.Button(self.root, text="Delete Profile", command=self.delete_profile, width=54, height=2, bg='CadetBlue3', fg='white',
                                        activebackground='turquoise', activeforeground='white', borderwidth=0, relief='flat')
        delete_profile_button.grid(row=4, column=0, padx=8, pady=5)

        # Define the view grades button
        view_grades_button = tk.Button(self.root, text="View All Grades", command=self.show_table, width=54, height=2, bg='CadetBlue3', fg='white',
                                    activebackground='turquoise', activeforeground='white', borderwidth=0, relief='flat')
        view_grades_button.grid(row=6, column=0, padx=8, pady=5, columnspan=2)


    def add_user(self):
        # Define the add user window
        add_user_window = tk.Toplevel(self.root)
        add_user_window.title("Add Student")
        add_user_window.geometry("300x350")

        tk.Label(add_user_window, text="Person ID").grid(row=0, column=0)
        person_id_entry = tk.Entry(add_user_window)
        person_id_entry.grid(row=0, column=1)

        tk.Label(add_user_window, text="First Name").grid(row=2, column=0)
        first_name_entry = tk.Entry(add_user_window)
        first_name_entry.grid(row=2, column=1)

        tk.Label(add_user_window, text="Last Name").grid(row=3, column=0)
        last_name_entry = tk.Entry(add_user_window)
        last_name_entry.grid(row=3, column=1)

        tk.Label(add_user_window, text="Gender(M/F)").grid(row=4, column=0)
        gender_entry = tk.Entry(add_user_window)
        gender_entry.grid(row=4, column=1)

        tk.Label(add_user_window, text="Standard").grid(row=5, column=0)
        std_entry = tk.Entry(add_user_window)
        std_entry.grid(row=5, column=1)
        
        tk.Label(add_user_window, text="DOB (YYYY/MM/DD)").grid(row=6, column=0)
        dob_entry = tk.Entry(add_user_window)
        dob_entry.grid(row=6, column=1)

        tk.Label(add_user_window, text="Ten Digit Contact No.").grid(row=7, column=0)
        contact_number_entry = tk.Entry(add_user_window)
        contact_number_entry.grid(row=7, column=1)

        tk.Label(add_user_window, text="Email").grid(row=8, column=0)
        email_entry = tk.Entry(add_user_window)
        email_entry.grid(row=8, column=1)

        tk.Label(add_user_window, text="Street").grid(row=9, column=0)
        street_entry = tk.Entry(add_user_window)
        street_entry.grid(row=9, column=1)

        tk.Label(add_user_window, text="PIN Code").grid(row=10, column=0)
        pincode_entry = tk.Entry(add_user_window)
        pincode_entry.grid(row=10, column=1)

        tk.Label(add_user_window, text="City").grid(row=11, column=0)
        city_entry = tk.Entry(add_user_window)
        city_entry.grid(row=11, column=1)

        tk.Label(add_user_window, text="State").grid(row=12, column=0)
        state_entry = tk.Entry(add_user_window)
        state_entry.grid(row=12, column=1)

        tk.Label(add_user_window, text="Password").grid(row=13, column=0)
        password_entry = tk.Entry(add_user_window, show="*")
        password_entry.grid(row=13, column=1)
        
        # Define the add button function
        def add():
            try:
                person_id = person_id_entry.get()
                first_name = first_name_entry.get()
                last_name = last_name_entry.get()
                gender = gender_entry.get()
                dob = dob_entry.get()
                contact_number = contact_number_entry.get()
                email = email_entry.get()
                street = street_entry.get()
                pincode = pincode_entry.get()
                city = city_entry.get()
                state = state_entry.get()
                password = password_entry.get()
                std = std_entry.get()
                self.add_user_to_database(std, person_id, first_name, last_name, gender, dob, contact_number, email, street, pincode, city, state, password)
                tk.messagebox.showinfo("Add Student", "Student added successfully")
                add_user_window.destroy()
            except :
                tk.messagebox.showinfo("Error occured", "Check your fields, some error occured")

        # Define the add button
        add_button = tk.Button(add_user_window, text="Add", command=add)
        add_button.grid(row=14, column=1, columnspan=2)

    def add_user_to_database(self, std, person_id, first_name, last_name, gender, dob, contact_number, email, street, pincode, city, state, password):
        self.cursor.execute("INSERT INTO person VALUES (%s,'Student' ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (person_id, first_name, last_name, gender, password, dob, contact_number, email, street, pincode, city, state))
        self.cursor.execute("INSERT INTO student VALUES (NULL, %s, %s)",(person_id, std))
        self.mydb.commit()

    def add_user2(self):
        # Define the add user window
        add_user2_window = tk.Toplevel(self.root)
        add_user2_window.title("Add Teacher")
        add_user2_window.geometry("300x350")

        tk.Label(add_user2_window, text="Person ID").grid(row=0, column=0)
        person_id_entry = tk.Entry(add_user2_window)
        person_id_entry.grid(row=0, column=1)

        tk.Label(add_user2_window, text="First Name").grid(row=1, column=0)
        first_name_entry = tk.Entry(add_user2_window)
        first_name_entry.grid(row=1, column=1)

        tk.Label(add_user2_window, text="Last Name").grid(row=2, column=0)
        last_name_entry = tk.Entry(add_user2_window)
        last_name_entry.grid(row=2, column=1)

        tk.Label(add_user2_window, text="Gender(M/F)").grid(row=3, column=0)
        gender_entry = tk.Entry(add_user2_window)
        gender_entry.grid(row=3, column=1)

        tk.Label(add_user2_window, text="DOB (YYYY/MM/DD)").grid(row=4, column=0)
        dob_entry = tk.Entry(add_user2_window)
        dob_entry.grid(row=4, column=1)

        tk.Label(add_user2_window, text="Ten Digit Contact No.").grid(row=5, column=0)
        contact_number_entry = tk.Entry(add_user2_window)
        contact_number_entry.grid(row=5, column=1)

        tk.Label(add_user2_window, text="Email").grid(row=6, column=0)
        email_entry = tk.Entry(add_user2_window)
        email_entry.grid(row=6, column=1)

        tk.Label(add_user2_window, text="Street").grid(row=7, column=0)
        street_entry = tk.Entry(add_user2_window)
        street_entry.grid(row=7, column=1)

        tk.Label(add_user2_window, text="PIN Code").grid(row=8, column=0)
        pincode_entry = tk.Entry(add_user2_window)
        pincode_entry.grid(row=8, column=1)

        tk.Label(add_user2_window, text="City").grid(row=9, column=0)
        city_entry = tk.Entry(add_user2_window)
        city_entry.grid(row=9, column=1)

        tk.Label(add_user2_window, text="State").grid(row=10, column=0)
        state_entry = tk.Entry(add_user2_window)
        state_entry.grid(row=10, column=1)

        tk.Label(add_user2_window, text="Password").grid(row=11, column=0)
        password_entry = tk.Entry(add_user2_window, show="*")
        password_entry.grid(row=11, column=1)
        
        # Define the add button function
        def add():
            try:
                person_id = person_id_entry.get()
                first_name = first_name_entry.get()
                last_name = last_name_entry.get()
                gender = gender_entry.get()
                dob = dob_entry.get()
                contact_number = contact_number_entry.get()
                email = email_entry.get()
                street = street_entry.get()
                pincode = pincode_entry.get()
                city = city_entry.get()
                state = state_entry.get()
                password = password_entry.get()
                self.add_users_to_database(person_id, first_name, last_name, gender, dob, contact_number, email, street, pincode, city, state, password)
                tk.messagebox.showinfo("Add Teacher", "Teacher added successfully")
                add_user2_window.destroy()
            except :
                tk.messagebox.showinfo("Error occured", "Check your fields, some error occured")

        # Define the add button
        add_button = tk.Button(add_user2_window, text="Add", command=add)
        add_button.grid(row=14, column=1, columnspan=2)

    def add_users_to_database(self, person_id, first_name, last_name, gender, dob, contact_number, email, street, pincode, city, state, password):
        self.cursor.execute("INSERT INTO person VALUES (%s,'Teacher' ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (person_id, first_name, last_name, gender, password, dob, contact_number, email, street, pincode, city, state))    
        self.cursor.execute(f"INSERT INTO teacher VALUES (NULL, '{person_id}')")
        self.mydb.commit()

    def view_profile(self):
        # Define the view profile window
        view_profile_window = tk.Toplevel(self.root)
        view_profile_window.title("View Profile")
        view_profile_window.geometry("300x300")

        # Define the username label and entry field
        tk.Label(view_profile_window, text="Person ID").grid(sticky="W", row=0, column=0)
        username_entry = tk.Entry(view_profile_window)
        username_entry.grid(sticky="W", row=0, column=1)

        def view():
            try:
                username = username_entry.get()
                result = self.get_user_from_database(username)
                tk.Label(view_profile_window, text=f"Person ID: {(result[0])}").grid(sticky="W", row=3, column=0)

                tk.Label(view_profile_window, text=f"Role: {(result[1])}").grid(sticky="W", row=4, column=0)

                tk.Label(view_profile_window, text=f"Name: {(result[2])} {(result[3])}").grid(sticky="W", row=5, column=0)

                tk.Label(view_profile_window, text=f"Gender: {(result[4])}").grid(sticky="W", row=6, column=0)
                
                tk.Label(view_profile_window, text=f"DOB: {(result[6])}").grid(sticky="W", row=7, column=0)

                tk.Label(view_profile_window, text=f"Contact No.:{(result[7])}").grid(sticky="W", row=8, column=0)

                tk.Label(view_profile_window, text=f"Email: {(result[8])}").grid(sticky="W", row=9, column=0)

                tk.Label(view_profile_window, text=f"Adress: {(result[9])}, {(result[11])}, {(result[12])}, {(result[10])}.").grid(sticky="W", row=10, column=0)

            except: 
                tk.messagebox.showinfo("Error occured", "Check your fields, some error occured")
                username_entry.delete(0, END)

        view_button = tk.Button(view_profile_window, text="View Profile", command=view)
        view_button.grid(sticky="W", row=0, column=2, columnspan=2)
    
    def get_user_from_database(self,pid):
        self.cursor.execute(f"SELECT * FROM person WHERE Person_ID='{pid}'")
        return self.cursor.fetchall()[0]

    def update_profile(self):
        # Define the update profile window
        update_profile_window = tk.Toplevel(self.root)
        update_profile_window.title("Update Profile")
        update_profile_window.geometry("400x400")

         # Define the username label and entry field
        tk.Label(update_profile_window, text="Person ID").place(x=20, y=20)
        person_id_entry = tk.Entry(update_profile_window)
        person_id_entry.place(x=100, y=20)

        tk.Label(update_profile_window, text="Select Field").place(x=20, y=50)
        # Define the drop down box
        columns = ['First_Name', 'Last_Name', 'Gender', 'Password', 'DOB', 'Contact_Number', 'Email', 'Street', 'Pincode', 'City', 'State']
        selected_column = tk.StringVar()
        drop_down_box = ttk.Combobox(update_profile_window, textvariable=selected_column, values=columns)
        drop_down_box.place(x=100,y=50)

        tk.Label(update_profile_window, text="New Value").place(x=20, y=80)
        value_entry = tk.Entry(update_profile_window)
        value_entry.place(x=100, y=80)

        def update():
            try:
                person_id = person_id_entry.get()
                attribute = selected_column.get()
                value = value_entry.get()
                self.update_in_database(person_id, value, attribute)
                tk.messagebox.showinfo("Update User", "User updated successfully")
                update_profile_window.destroy()

            except:
                tk.messagebox.showinfo("Error occured", "Check your fields, some error occured")

        add_button = tk.Button(update_profile_window, text="Update", command=update)
        add_button.place(x=100, y= 110)
    
    def update_in_database(self, person_id, value, attribute):
        self.cursor.execute(f"UPDATE person SET {attribute} = '{value}' WHERE Person_ID = '{person_id}'")
        self.mydb.commit()

    def delete_profile(self):
        # Define the update profile window
        delete_profile_window = tk.Toplevel(self.root)
        delete_profile_window.title("Delete Profile")
        delete_profile_window.geometry("400x400")

         # Define the username label and entry field
        tk.Label(delete_profile_window, text="Person ID").place(x=20, y=20)
        person_id_entry = tk.Entry(delete_profile_window)
        person_id_entry.place(x=100, y=20)

        def delete():
            try:
                person_id = person_id_entry.get()
                self.delete_from_database(person_id)
                delete_profile_window.destroy()
                tk.messagebox.showinfo("Delete User", "User deleted successfully")
                delete_profile_window.destroy()

            except:
                tk.messagebox.showinfo("Error occured", "Check your fields, some error occured")

        add_button = tk.Button(delete_profile_window, text="Delete", command=delete)
        add_button.place(x=100, y= 50)

    def delete_from_database(self, person_id):
        self.cursor.execute(f"DELETE FROM person WHERE Person_ID = '{person_id}'")
        self.mydb.commit()

    def show_table(self):
        # retrieve data from standard table
        self.cursor.execute("SELECT * FROM standard")
        data = self.cursor.fetchall()

        # create a new window to show the table
        table_window = tk.Toplevel(self.root)
        table_window.title("Standard Table")

        # create a treeview to display the data
        columns = ("Std",)
        tree = ttk.Treeview(table_window, columns=columns, show="headings")
        tree.heading("Std", text="Standard")
        tree.pack()

        # insert data into the treeview
        for row in data:
            tree.insert("", "end", values=row, tags=row)

        # bind a function to the treeview to show students for a standard when a row is clicked
        tree.bind("<ButtonRelease-1>", lambda event: self.show_students(tree.item(tree.focus())['values'][0]))

    def show_students(self, std):
        # retrieve data from students table for the selected standard
        self.cursor.execute(f"SELECT * FROM student WHERE Std={std}")
        data = self.cursor.fetchall()

        # create a new window to show the students for the standard
        student_window = tk.Toplevel(self.root)
        student_window.title(f"Students in Standard {std}")

        # create a treeview to display the data
        columns = ("Student ID", "Person ID", "Standard")
        tree = ttk.Treeview(student_window, columns=columns, show="headings")
        tree.heading("Student ID", text="Student ID")
        tree.heading("Person ID", text="Person ID")
        tree.heading("Standard", text="Standard")
        tree.pack()

        # insert data into the treeview
        for row in data:
            tree.insert("", "end", values=row, tags=row)

        # bind a function to the treeview to show assessment data for a student when a row is clicked
        tree.bind("<ButtonRelease-1>", lambda event: self.show_assessment(tree.item(tree.focus())['values'][0]))

    def show_assessment(self, student):
        # retrieve data from assessment and grade_table tables for the selected student
        self.cursor.execute(f"SELECT Subject_Name, Pre_Mid, Mid_Term, Post_Mid, Final_Term, Grade FROM assessment NATURAL JOIN grade_table WHERE Student_ID = {student};")
        data = self.cursor.fetchall()

        # create a new window to show the assessment data for the student
        assessment_window = tk.Toplevel(self.root)
        assessment_window.title(f"Assessment for Student {student}")

        # create a treeview to display the data
        columns = ("Subject Name", "Pre Mid Term", "Mid Term", "Post Mid Term", "Final Term", "Grade")
        tree = ttk.Treeview(assessment_window, columns=columns, show="headings")
        tree.heading("Subject Name", text="Subject Name")
        tree.heading("Pre Mid Term", text="Pre Mid Term")
        tree.heading("Mid Term", text="Mid Term")
        tree.heading("Post Mid Term", text="Post Mid Term")
        tree.heading("Final Term", text="Final Term")
        tree.heading("Grade", text="Grade")
        tree.pack()

        for row in data:
            tree.insert("", "end", values=row, tags=row)
