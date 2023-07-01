import mysql.connector
from tkinter import *
from admin_homepage import *
from teacher_homepage import *
from student_homepage import *

# Connect to the MySQL database
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Shardul4245",
  database="dbsproject"
)

# Create a cursor to interact with the database
cursor = db.cursor()

# Create the Tkinter login window
root = Tk()
root.title("Login")
root.geometry("400x400")

# Create the username and password entry fields
username_label = Label(root, text="Username:", font=("Arial", 14), fg="CadetBlue3")
username_label.pack(pady=10)

# Define the username entry
username_entry = Entry(root, font=("Arial", 14), bg="lightgray", bd=0)
username_entry.pack(ipady=5)

# Define the password label
password_label = Label(root, text="Password:", font=("Arial", 14), fg="CadetBlue3")
password_label.pack(pady=10)

# Define the password entry
password_entry = Entry(root, show="*", font=("Arial", 14), bg="lightgray", bd=0)
password_entry.pack(ipady=5)

# Create the login function
def login():
    
    # Get the username and password values from the entry fields
    username = username_entry.get()
    password = password_entry.get()

    # Search the database for the username and password combination
    sql = "SELECT role FROM person WHERE Person_ID = %s AND Password = %s"
    values = (username, password)
    cursor.execute(sql, values)
    result = cursor.fetchone()

    # If the combination is found, display a message and clear the entry fields
    if result:
        message_label.config(text="Login successful!")
        cursor.execute(f'SELECT Role from person where Person_ID="{username}"')
        role=cursor.fetchall()[0][0]
        root.destroy()
        root1 = Tk()
        root1.geometry("400x400")
        if role=="Administrator":
          root1.title("Admin")
          Admin(root1)
        elif role=="Student":
          root1.title("Student")
          Student(root1, username)
        else :
          root1.title("Teacher")
          Teacher(root1, username)
        root.mainloop()
    # If the combination is not found, display an error message
    else:
        message_label.config(text="Invalid username or password.")

# Create the login button
login_button = Button(root, text="Login", font=("Arial", 14), bg="CadetBlue3", fg="white", activebackground="lightblue", activeforeground="white", bd=0, padx=20, pady=10, command=login)
login_button.pack()



# Create a label to display messages
message_label = Label(root)
message_label.pack()

# Run the Tkinter event loop
root.mainloop()

# Close the database connection
db.close()